"""
Support for getting the live mid-rates from FXMarketAPI.

configuration.yaml

sensor:
  - platform: fxmarketapi
    api_key: !secret fxmarketapi_key
    scan_interval: 00:60:00
    foreign_exchange:
      - name: USD to ZAR
        from: USD
        to: ZAR
      - name: ZAR to USD
        from: ZAR
        to: USD
"""
import logging
from datetime import timedelta
from datetime import datetime
import requests

import voluptuous as vol

from homeassistant.util import Throttle
from homeassistant.components import persistent_notification
from homeassistant.components.sensor import PLATFORM_SCHEMA

import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_API_KEY, CONF_NAME
from homeassistant.helpers.entity import Entity

from .const import NAME, DEFAULT_NAME, DOMAIN, ICON, SENSOR, API_URL, ICONS, STARTUP_MESSAGE

_LOGGER = logging.getLogger(__name__)

DEFAULT_SCAN_INTERVAL = timedelta(minutes=60)

CONF_FOREIGN_EXCHANGE = "foreign_exchange"
CONF_FROM = "from"
CONF_TO = "to"
CONF_SCAN_INTERVAL = "scan_interval"

CURRENCY_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_FROM): cv.string,
        vol.Required(CONF_TO): cv.string,
        vol.Optional(CONF_NAME): cv.string
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period,
    vol.Required(CONF_FOREIGN_EXCHANGE): vol.All(cv.ensure_list, [CURRENCY_SCHEMA])
})


def create_notification(hass, message, title):
    """Create a persistent notification from this sync platform setup."""
    hass.loop.call_soon_threadsafe(
        persistent_notification.async_create,
        hass,
        message,
        title,
    )


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the FXMarketAPI sensors."""

    api_key = config[CONF_API_KEY]
    scan_interval = config.get(CONF_SCAN_INTERVAL)
    conversions = config.get(CONF_FOREIGN_EXCHANGE, [])
    min_scan_interval = timedelta(minutes=1)

    if not conversions:
        msg = "No currencies configured."
        create_notification(hass, msg, f"Sensor {NAME}")
        _LOGGER.warning(msg)
        return

    if scan_interval < min_scan_interval:
        msg = f"Scan interval must be at least 1 minute (i.e. 00:00:01) - Configured Value: {scan_interval}. Configuration will use the default scan interval and continue."
        create_notification(hass, msg, f"Sensor {NAME}")
        _LOGGER.warning(msg)
        scan_interval = DEFAULT_SCAN_INTERVAL

    api_currencies = []
    for conversion in conversions:
        api_currencies.append([conversion[CONF_FROM], conversion[CONF_TO]])


    _LOGGER.info(f"{DEFAULT_NAME}: Scan Interval: {scan_interval}, API Currencies: {api_currencies}")

    updater = FXMarketAPIUpdater(api_key, scan_interval, api_currencies)
    updater.update()
    if updater.data is None:
        if updater.error_msg is None:
            updater.error_msg = "Unhandled Error"
        create_notification(hass, f"{updater.error_msg}. Please investigate logs.", f"Sensor {NAME}")
        raise Exception(f"{DEFAULT_NAME}: Invalid configuration for {NAME} platform. Error Message: {updater.error_msg}")
    else:
        _LOGGER.debug(f"{DEFAULT_NAME}: Returned Data: {updater.data}")
        if "error" in updater.data:
            error_info = updater.data["error"].get("info", updater.data["error"])
            create_notification(hass, f"FXMarketAPI error: {error_info}. Please investigate logs.", f"Sensor {NAME}")
            raise Exception(f"{DEFAULT_NAME}: FXMarketAPI returned an error for {NAME} platform. Data: {updater.data}")
        if updater.data.get("timestamp") is None:
            create_notification(hass, f"No timestamp data returned from API. Please investigate logs.", f"Sensor {NAME}")
            raise Exception(f"{DEFAULT_NAME}: No timestamp data returned from API for {NAME} platform. Data: {updater.data}")
        if updater.data.get("price") is None:
            create_notification(hass, f"No price data returned from API. Please investigate logs.", f"Sensor {NAME}")
            raise Exception(f"{DEFAULT_NAME}: No price data returned from API for {NAME} platform. Data: {updater.data}")
        if updater.data["price"] is not None:
            if "error" in updater.data["price"]:
                create_notification(hass, f"Invalid Currencies Specified. Please investigate logs.", f"Sensor {NAME}")
                raise Exception(f"{DEFAULT_NAME}: Invalid Currencies Specified for {NAME} platform. Data: updater.data['price']")

    dev = []
    for conversion in conversions:
        dev.append(FXMarketAPISensor(conversion, updater))

    add_entities(dev, True)

    _LOGGER.info(STARTUP_MESSAGE)


class FXMarketAPISensor(Entity):
    """Representation of a FXMarketAPI sensor."""
    def __init__(self, conversion, updater):
        """Initialize the sensor."""
        self._conversion = conversion
        self._from_currency = conversion[CONF_FROM]
        self._to_currency = conversion[CONF_TO]
        if CONF_NAME in conversion:
            self._name = f"{conversion.get(CONF_NAME)}"
        else:
            self._name = f"fxmarketapi_{self._to_currency}_{self._from_currency}"

        self._unique_id = f"fxmarketapi_{self._to_currency}_{self._from_currency}"
        self._api_name = f"{self._from_currency}{self._to_currency}"
        self._unit_of_measurement = self._to_currency
        self._timestamp = datetime(1900, 1, 1)
        self._icon = ICONS.get(self._from_currency, "USD")
        self._updater = updater
        self._data = None
        self._state = None

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def from_currency(self):
        """Return the from currency of this entity, if any."""
        return self._from_currency

    @property
    def to_currency(self):
        """Return the to currency of this entity, if any."""
        return self._to_currency

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._updater.data is not None:
            self._timestamp = datetime.fromtimestamp(self._updater.data["timestamp"])
            self._state = self._updater.data["price"][self._api_name]

        return self._state


    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return self._icon

    @property
    def device_state_attributes(self):
        """Return the state attributes of this device."""
        return {
            "timestamp": self._timestamp,
        }

    def update(self):
        self._updater.update()


class FXMarketAPIUpdater:
    def __init__(self, api_key, scan_interval, api_currencies):
        self.api_key = api_key
        self._api_currencies = api_currencies
        self.update = Throttle(scan_interval)(self._update)
        self.data = None
        self.error_msg = None

    def _update(self):
        self.error_msg = None
        data = {"timestamp": None, "price": {}}

        for from_currency, to_currency in self._api_currencies:
            params = {
                "api_key": self.api_key,
                "from": from_currency,
                "to": to_currency,
                "amount": 1,
            }
            logging_params = dict(params, api_key="XXXXX")
            _LOGGER.debug(f"{DEFAULT_NAME}: URL: {API_URL}, Params: {logging_params}")
            response = requests.get(API_URL, params=params)
            if response.status_code != 200 or response.content.__len__() == 0:
                msg = f"Error retrieving data. Status Code: {response.status_code}"
                self.error_msg = msg
                self.data = None
                return

            conversion_data = response.json()
            if "error" in conversion_data:
                self.data = conversion_data
                return

            api_name = f"{from_currency}{to_currency}"
            data["price"][api_name] = conversion_data.get("price")
            data["timestamp"] = conversion_data.get("timestamp", data["timestamp"])

        self.data = data

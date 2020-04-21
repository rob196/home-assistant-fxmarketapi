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
import json

import voluptuous as vol

from homeassistant.util import Throttle
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


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup the FXMarketAPI sensors."""

    api_key = config[CONF_API_KEY]
    scan_interval = config.get(CONF_SCAN_INTERVAL)
    conversions = config.get(CONF_FOREIGN_EXCHANGE, [])
    min_scan_interval = timedelta(minutes=1)
    
    if not conversions:
        msg = "No currencies configured."
        hass.components.persistent_notification.create(msg, f"Sensor {NAME}")
        _LOGGER.warning(msg)
        return

    if scan_interval < min_scan_interval:
        msg = f"Scan interval must be at least 1 minute (i.e. 00:00:01) - Configured Value: {scan_interval}. Configuration will use the default scan interval and continue."
        hass.components.persistent_notification.create(msg, f"Sensor {NAME}")
        _LOGGER.warning(msg)
        scan_interval = DEFAULT_SCAN_INTERVAL
    
    apiCurrencies = ""
    for conversion in conversions:
        apiCurrencies += conversion[CONF_FROM] + conversion[CONF_TO] + ","
    apiCurrencies = apiCurrencies[:-1]

    _LOGGER.debug(f"{DEFAULT_NAME}: Scan Interval: {scan_interval}, API Currencies: {apiCurrencies}")

    updater = FXMarketAPIUpdater(api_key, scan_interval, apiCurrencies)
    updater.update()
    if updater.data is None:
        if updater.error_msg is None:
            updater.error_msg = "Unhandled Error"
        hass.components.persistent_notification.create(f"{updater.error_msg}. Please investigate logs.", f"Sensor {NAME}")
        raise Exception(f"{DEFAULT_NAME}: Invalid configuration for {NAME} platform. Error Message: {updater.error_msg}")
    else:
        _LOGGER.debug(f"{DEFAULT_NAME}: Returned Data: {updater.data}")
        if updater.data["timestamp"] is None:
            hass.components.persistent_notification.create(f"No timestamp data returned from API. Please investigate logs.", f"Sensor {NAME}")
            raise Exception(f"{DEFAULT_NAME}: No timestamp data returned from API for {NAME} platform. Data: {updater.data}")
        if updater.data["price"] is None:
            hass.components.persistent_notification.create(f"No price data returned from API. Please investigate logs.", f"Sensor {NAME}")
            raise Exception(f"{DEFAULT_NAME}: No price data returned from API for {NAME} platform. Data: {updater.data}")
        if updater.data["price"] is not None:
            if "error" in updater.data["price"]:
                hass.components.persistent_notification.create(f"Invalid Currencies Specified. Please investigate logs.", f"Sensor {NAME}")
                raise Exception(f"{DEFAULT_NAME}: Invalid Currencies Specified for {NAME} platform. Data: updater.data['price']")
        
    dev = []
    for conversion in conversions:
        dev.append(FXMarketAPISensor(conversion, updater))

    async_add_entities(dev, True)

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
        address = f"{API_URL}?api_key={self.api_key}&currency={self._api_currencies}"
        loggingURL = f"{API_URL}?api_key=XXXXX&currency={self._api_currencies}"
        _LOGGER.debug(f"{DEFAULT_NAME}: URL: {loggingURL}")
        response = requests.get(address)
        if response.status_code == 200 and response.content.__len__() > 0:
            self.data =  response.json()
        else:
            msg = f"Error retrieving data. Status Code: {response.status_code}"
            self.error_msg = msg
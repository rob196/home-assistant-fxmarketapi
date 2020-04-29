[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)  [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/robalexanderza/)

# FXMarketAPI Sensor Component
This is a Custom Component for [Home-Assistant](https://home-assistant.io), it fetches live mid-rates using [FXMarketAPI](https://fxmarketapi.com/).

**NOTE:** You will need an FXMarketAPI account, you can sign up for free [here](https://fxmarketapi.com/signup).

**NOTE:** Not all currencies are available, to check the available currencies see this page [here](https://fxmarketapi.com/currencies).

## Installation

### HACS - Recommended
- Have [HACS](https://hacs.xyz) installed, this will allow you to easily manage and track updates.
- Open HACS and click 'Integrations' tab
- Search for 'FXMarketAPI Integration'.
- Click 'FXMarketAPI Integration'.
- Click Install below the found integration.
- Configure using the configuration instructions below.
- Restart Home-Assistant.

### Manual
- Download the latest [Release](https://github.com/rob196/home-assistant-fxmarketapi/releases)
- Open the dowloaded zip (or tar.gz)
- Copy directory `custom_components/fxmarketapi` from, the zip file to your `<config dir>/custom_components` directory.
- Configure with config like below.
- Restart Home-Assistant.


## Usage
To use this component in your installation, add the following to your `configuration.yaml` file:

  **NOTE:** For more info on using secrets look [here](https://www.home-assistant.io/docs/configuration/secrets/).

```yaml
# Example configuration.yaml entry
# The below will call the FXMarketAPI every hour and add sensors for USD to ZAR and ZAR to USD

sensor:
  - platform: fxmarketapi
    api_key: !secret fxmarketapi_key
    scan_interval: 01:00:00
    foreign_exchange:
      - name: USD to ZAR
        from: USD
        to: ZAR
      - name: ZAR to USD
        from: ZAR
        to: USD
```

## Configuration Options:

### Base Options
| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `api_key` | `string` | `True` | - | API key for your FXMarketAPI account|
| `scan_interval` | `time period` | `False` | `00:60:00` | Interval between sensor updates (API calls) |
| `foreign_exchange` | `list` | `True` | `[]` | Currencies to get live rates for (see below) |

### Foreign Exchange Options
| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | `string` | `False` | | Friendly name for the sensor |
| `from` | `string` | `True` | | The 3 digit currency code to get the exchange rate from (i.e. USD) |
| `to` | `string` | `True` | | The 3 digit currency code to get the exchange rate to (i.e. ZAR)|

## Screenshots

![Screenshot FXMarketAPI Results](https://github.com/rob196/home-assistant-fxmarketapi/blob/master/screenshots/FXMarketAPIResults.png?raw=true "Screenshot FXMarketAPI Results")

## Enable Debug Logging (for reporting bug's/issues)

Please refer to the [Home-Assistant Logger](https://www.home-assistant.io/integrations/logger/) page for detailed info.

### Example
```yaml
# Example configuration.yaml entry
logger:
  default: error
  logs:
    custom_components.fxmarketapi: debug

```

## Disclaimer
This integration is provided as-is without warranties of any kind.

## Donation
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/robalexanderza/)
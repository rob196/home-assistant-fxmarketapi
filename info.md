{% if installed %}
Version Installed: {{version_installed}}
Version: {{version_available}}
{% if version_available.replace("v", "").replace(".","") | int > version_installed.replace("v", "").replace(".","") | int %}

## Changes as compared to your installed version:

### Breaking Changes

### Changes
- Updated documentation
### Features

### Bugfixes

---

{% else %}

**You are running the latest version!**

---

{% endif %}

{% endif %}

# FXMarketAPI Sensor Component
This is a Custom Component for [Home-Assistant](https://home-assistant.io), it fetches live mid-rates using [FXMarketAPI](https://fxmarketapi.com/).

**NOTE:** You will need an FXMarketAPI account, you can sign up for free [here](https://fxmarketapi.com/signup).

**NOTE:** Not all currencies are available, to check the available currencies see this page [here](https://fxmarketapi.com/currencies).

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

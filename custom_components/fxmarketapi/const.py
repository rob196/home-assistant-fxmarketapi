"""Constants for FXMarketAPI."""
NAME = "FXMarketAPI"
DOMAIN = "fxmarketapi"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "1.0.1"

ISSUE_URL = "https://github.com/rob196/home-assistant-fxmarketapi/issues"

# Icons
ICON = "mdi:currency-usd"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options
CONF_ENABLED = "enabled"

# Defaults
DEFAULT_NAME = DOMAIN

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration to {NAME}!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

API_URL = 'https://fxmarketapi.com/apilive'

ICONS = {
    "AED": "mdi:currency-usd",	# "United Arab Emirates Dirham"
    "ARS": "mdi:currency-usd",	# "Argentine Peso"
    "AUD": "mdi:currency-usd",	# "Australian Dollar"
    "BRL": "mdi:currency-brl",	# "Brazilian Real"
    "BTC": "mdi:currency-btc",	# "Bitcoin"
    "CAD": "mdi:currency-cny",	# "Canadian Dollar"
    "CHF": "mdi:currency-usd",	# "Swiss Franc"
    "CLP": "mdi:currency-usd",	# "Chilean Peso"
    "CNY": "mdi:currency-cny",	# "Chinese Yuan"
    "COP": "mdi:currency-usd",	# "Colombian Peso"
    "CZK": "mdi:currency-usd",	# "Czech Koruna"
    "DKK": "mdi:currency-usd",	# "Danish Krone"
    "EUR": "mdi:currency-eur",	# "Euro"
    "GBP": "mdi:currency-gbp",	# "British Pound Sterling"
    "HKD": "mdi:currency-usd",	# "Hong Kong Dollar"
    "HRK": "mdi:currency-usd",	# "Croatian Kuna"
    "HUF": "mdi:currency-usd",	# "Hungarian Forint"
    "IDR": "mdi:currency-usd",	# "Indonesian Rupiah"
    "ILS": "mdi:currency-ils",	# "Israeli Sheqel"
    "INR": "mdi:currency-inr",	# "Indian Rupee"
    "ISK": "mdi:currency-usd",	# "Icelandic Krona"
    "JPY": "mdi:currency-jpy",	# "Japanese Yen"
    "KRW": "mdi:currency-krw",	# "South Korean Won"
    "KWD": "mdi:currency-usd",	# "Kuwaiti Dinar"
    "MAD": "mdi:currency-usd",	# "Moroccan Dirham"
    "MXN": "mdi:currency-usd",	# "Mexican Peso"
    "MYR": "mdi:currency-usd",	# "Malaysian Ringgit"
    "NOK": "mdi:currency-usd",	# "Norwegian Krone"
    "NZD": "mdi:currency-usd",	# "New Zealand Dollar"
    "PEN": "mdi:currency-usd",	# "Peruvian Nuevo Sol"
    "PHP": "mdi:currency-php",	# "Philippine Peso"
    "PLN": "mdi:currency-usd",	# "Polish Zloty"
    "RON": "mdi:currency-usd",	# "Romanian Leu"
    "RUB": "mdi:currency-rub",	# "Russian Ruble"
    "SEK": "mdi:currency-usd",	# "Swedish Krona"
    "SGD": "mdi:currency-usd",	# "Singapore Dollar"
    "THB": "mdi:currency-usd",	# "Thai Baht"
    "TRY": "mdi:currency-try",	# "Turkish Lira"
    "TWD": "mdi:currency-twd",	# "Taiwanese Dollar"
    "USD": "mdi:currency-usd",  # "United States Dollar"
    "XAG": "mdi:alpha-s",    	# "Silver (ounce)"
    "XAU": "mdi:gold",       	# "Gold (ounce)"
    "ZAR": "mdi:alpha-r"    	# "South African Rand"
}
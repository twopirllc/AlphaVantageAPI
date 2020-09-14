# AlphaVantageAPI
*An Opinionated AlphaVantage API Wrapper in Python 3.7*

Access to the AlphaVantage requires a free API key, that can be found at http://www.alphavantage.co/support/#api-key.


## Description
This API was designed to simplify the process of aquiring *free* financial data for retail traders and investors from the financial markets.  While it does require Pandas, Pandas' methods help simplify saving data requests into a variety of file formats such as: csv (default), json, pkl, html, and txt.  If the openpyxl module is also installed, it can be saved as an Excel file: xlsx.

### Main Features
* Extended the Pandas DataFrame with extension 'av'.  See the _*Extension Example*_ below.
* The extension has some aliases to simplify the download process.
* Can modify most properties of the AV class with the 'av' extension.
* Like terse commands?  The 'av' extension also includes their alias.  For example: df.av.daily_adjusted('aapl') = df.av.DA('aapl').  See help('aliases') for more shorter length commands.
* Returns a Pandas DataFrame for a simplified ETL pipeline.
* Simplifies column names i.e. "1. open" -> "open" when
"```clean=True```"
* Available export formats: csv (default), json, pkl, html, txt, xlsz (optional).
* A help method to reduce looking up 'required' and 'optional' parameters for each function.
* A call_history method to return all successful API calls.


## What's New?
* AlphaVantage has depreciated ```batch```, ```digital_intraday```, and ```sectors```.  
* Looking for Realtime Intraday data, AlphaVantage has partnered with [Polygon.io](https://polygon.io/) with partner code: ```ALPHAV```.
* **New Features:** AlphaVantage has added a new API endpoint: [Company Overview](https://www.alphavantage.co/documentation/#company-overview).

# Installation
## Required
```shell
pip install pandas
```

## Typical installation:
```shell
pip install alphaVantage-api
```

## With Excel file support:
```shell
pip install alphaVantage-api openpyxl
```

## For the most up to date version
<!-- Source installation: -->
```shell
git clone https://github.com/twopirllc/AlphaVantageAPI.git
pip install -e alphaVantage-api
```

# API Details
## Constructor Parameter Defaults
    api_key: str     = None
    premium: bool    = False
    output_size: str = 'compact'
    datatype: str    = 'json'
    export: bool     = False
    export_path: str = '~/av_data'
    output: str      = 'csv'
    clean: bool      = False
    proxy: dict      = {}


## Constructor Parameter Descriptions

### api_key : *str*
* Default: None.  If None, then do not forget to set your environment variable AV_API_KEY to API key. Otherwise set it in the class constructor.  If you have a Premium API key, do not forget to set the premium property to True as well.
### premium : *bool*
* Default: False.  Got premium?  Excellent!  You do not need to wait  15.02 seconds between each API call.
### output_size : *str*
* Default: 'compact'. The other option is 'full'.  See AlphaVantage API documentation for more details.
### datatype : *str*
* Default: 'json'. This is the preferred request type.  See AlphaVantage API documentation for more details.
### export : *bool*
* Default: False.  Set it to True if you want to save the file locally according to the export_path property.
### export_path : *bool*
* Default: *'~/av_data'*.  Or set it to a path you can write to.
### output : *str*
* Default: 'csv'.  Other options are 'json', 'pkl', 'html', and 'txt'.  If openpyxl is installed, then you can use 'xlsz'.
### clean : *bool*
* Default: False. Simplifies the column header names for instance: "1. open" -> "open".
### proxy : *dict*
* Default: {}.  See requests API documentation for more details.


# **Example**: Classic Behavior

## Initialization
```python
from alphaVantageAPI.alphavantage import AlphaVantage

# Initialize the AlphaVantage Class with default values
AV = AlphaVantage(
        api_key=None,
        premium=False,
        output_size="compact",
        datatype='json',
        export=False,
        export_path="~/av_data",
        output="csv",
        clean=False,
        proxy={}
    )
```

## Free API Key
```python
# Your FREE API calls are throttled by 15.01 seconds. 
AV = AlphaVantage(premium=False)
```

## Premium API Key
```python
# No API call throttling.
AV = AlphaVantage(premium=True)
```  

## Save locally
```python
# Cleans and save requests to the default export_path in 'csv' format
AV = AlphaVantage(export=True, output="csv", clean=True)
```

## Display Current settings
```python
print(AV)
```

## Help!
```python
# Help: lists all the functions and indicators AlphaVantage API supports
AV.help()

# Print 'function' aliases
AV.help("aliases")

# Help with a specific API function
AV.help("TIME_SERIES_DAILY")

# Help with an indicator
AV.help("BBANDS")
```


## Symbol Search
```python
found_symbol = AV.search("AA")
```


## Data Acquisition Methods
```python
# Parameters
ticker = "MSFT"
crypto = "BTC"
base_fx, to_fx = "USD", "CAD"

# Global Quote
quote_df = AV.global_quote(ticker)

## Company Information
ibm_overview_df = AV.overview(ticker)

# FX / Currency
fx_rate_df = AV.fxrate(from_currency=base_fx, to_currency=to_fx) # Rate
fx_I5_df = AV.fx(from_currency=base_fx, to_currency=to_fx, function="FXI", interval=5) # Intraday as int
fx_I60_df = AV.fx(from_currency=base_fx, to_currency=to_fx, function="FXI", interval="60min") # Intraday as str
fx_D_df = AV.fx(from_currency=base_fx, to_currency=to_fx, function="FXD") # Daily
fx_W_df = AV.fx(from_currency=base_fx, to_currency=to_fx, function="FXW") # Weekly
fx_M_df = AV.fx(from_currency=base_fx, to_currency=to_fx, function="FXM") # Monthly

## Crypto Rating
btc_rating_df = AV.crypto_rating(symbol=crypto)

## Digital/Crypto
btc_usd_I5_df = AV.digital(symbol=crypto, market=base_fx, function="CI", interval=5) # Intraday as int
btc_usd_I60_df = AV.digital(symbol=crypto, market=base_fx, function="CI", interval="60min") # Intraday as str
btc_usd_D_df = AV.digital(symbol=crypto, market=base_fx, function="CD") # Daily
btc_usd_W_df = AV.digital(symbol=crypto, market=base_fx, function="CW") # Weekly
btc_usd_M_df = AV.digital(symbol=crypto, market=base_fx, function="CM") # Monthly

## Generic Equity/ETF calls
ticker_I5_df = AV.intraday(symbol=ticker, interval=5) # Intraday as int
ticker_I60_df = AV.intraday(symbol=ticker, interval="60min") # Intraday as str
ticker_D_df = AV.data(symbol=ticker, function="D") # Daily
ticker_DA_df = AV.data(symbol=ticker, function="DA") # Daily Adjusted
ticker_W_df = AV.data(symbol=ticker, function="W") # Weekly
ticker_WA_df = AV.data(symbol=ticker, function="WA") # Weekly Adjusted
ticker_M_df = AV.data(symbol=ticker, function="M") # Monthly
ticker_MA_df = AV.data(symbol=ticker, function="MA") # Monthly Adjusted


# List of symbols Daily
symbols = ["AAPL", "MSFT", "XLK"]
tech_list = AV.data("D", symbols)  # returns list of DataFrames


## Indicators
# SMA(close, 20)
ticker_SMA_20_df = AV.data(symbol=ticker, function="SMA", series_type="close", time_period=20)

# STOCH(close)
ticker_STOCH_df = AV.data("STOCH", symbols[2], interval="daily", series_type="close")
```

## Call History
```python
# Returns all successfull calls to the API
history_list = AV.call_history()

# Pretty display of Call History
history_df = pd.DataFrame(history_list)[["symbol", "function", "interval", "time_period"]]
print(history_df)
```


# **Example**: DataFrame Extension 'av' Behavior

## Initialization
*For simplicity and protection of your AV API key, the extension uses the environment variable AV_API_KEY upon import of the module.*
```python
import pandas as pd
import alphaVantageAPI
```

## Empty DataFrame: No current data, no problem!
Since 'av' is an extension of a Pandas DataFrame, we need a DataFrame to work from.  Simply create an empty DataFrame, it's contents will be replaced anyhow.
```python
df = pd.DataFrame()
```


## Help!
```python
# Help: lists all the functions and indicators AlphaVantage API supports
df.av.help()

# Print 'function' aliases
df.av.help("aliases")

# Help with a specific API function
df.av.help("TIME_SERIES_DAILY")

# Help with an indicator
df.av.help("BBANDS")
```


## Symbol Search
```python
found_symbol = df.av.search("AA")
```


## Data Acquisition Methods
```python
# Parameters
ticker = "MSFT"
crypto = "BTC"
base_fx, to_fx = "USD", "EUR"

# Global Quote
quote_df = df.av.global_quote(ticker)
quote_df.av.name # returns "MSFT"

## Company Information
ticker_overview = df.av.overview(ticker)

# FX / Currency
fx_rate_df = df.av.fx(base_fx, to_currency=to_fx)
fx_rate_df.av.name # returns "USD.EUR"
fx_I5_df = df.av.fx_intraday(base_fx, to_currency=to_fx, interval=5) # Intraday as int
fx_I60_df = df.av.fx_intraday(base_fx, to_currency=to_fx, interval="60min") # Intraday as str
fx_D_df = df.av.fx_daily(base_fx, to_currency=to_fx) # Daily
fx_W_df = df.av.fx_weekly(base_fx, to_currency=to_fx) # Weekly
fx_M_df = df.av.fx_monthly(base_fx, to_currency=to_fx) # Monthly

# Crypto Rating
btc_rating_df = df.av.crypto_rating(crypto)
btc_rating_df.av.name # returns "BTC"

## Digital/Crypto
btc_usd_D_df = df.av.digital_daily(crypto, market=base_fx) # Daily
btc_usd_D_df.av.name # returns "BTC.USD"
btc_usd_W_df = df.av.digital_weekly(crypto, market=base_fx) # Weekly
btc_usd_M_df = df.av.digital_monthly(crypto, market=base_fx) # Monthly

## Equities/ ETFs
ticker_I5_df = df.av.intraday(ticker, interval=5) # Intraday as int
ticker_I5_df.av.name # returns "MSFT"
ticker_I60_df = df.av.intraday(ticker, interval="60min") # Intraday as str
ticker_D_df = df.av.daily(ticker) # Daily
ticker_DA_df = df.av.daily_adjusted(ticker) # Daily Adjusted
ticker_W_df = df.av.weekly(ticker) # Weekly
ticker_WA_df = df.av.weekly_adjusted(ticker) # Weekly Adjusted
ticker_M_df = df.av.monthly(ticker) # Monthly
ticker_MA_df = df.av.monthly_adjusted(ticker) # Monthly Adjusted
```



# Contributing
Contributions are welcome and I am open to new ideas or implementations.

# Inspiration
If this module does not suit your style or workflow, consider some of the following *AlphaVantage API Python Wrapper* implementations by:

Romel Torres: https://github.com/RomelTorres/alpha_vantage

portfoliome: https://github.com/portfoliome/alphavantage
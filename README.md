# AlphaVantageAPI
*An Opinionated AlphaVantage API Wrapper in Python 3.7*

Access to the AlphaVantage requires a free API key, that can be found at http://www.alphavantage.co/support/#api-key.


## Description
This API was designed to simplify the process of aquiring *free* financial data for retail traders and investors from the financial markets.  While it does require Pandas, Pandas' methods help simplify saving data requests into a variety of file formats such as: csv (default), json, pkl, html, and txt.  If the openpyxl module is also installed, it can be saved as an Excel file: xlsx.

* Main Features
    * **New Feature:** Extended the Pandas DataFrame with extension 'av'.  See the _*Extension Example*_ below.
    * **New Feature:** The extension has some aliases to simplify the download process. **However indicators have _not_ been implemented yet.**
    * **New Feature:** Can modify most properties of the AV class with the 'av' extension.
    * **New Feature:** Added new access points: GLOBAL_QUOTE and SYMBOL_SEARCH added to the AlphaVantageAPI and it's 'av' extension.
    * **New Feature:** Like terse commands?  The 'av' extension also includes their alias.  For example: df.av.daily_adjusted('aapl') = df.av.DA('aapl').  See help('aliases') for more shorter length commands.
    * Returns a Pandas DataFrame.
    * Simplifies column names i.e. "1. open" -> "open".
    * Available export formats: csv (default), json, pkl, html, txt, xlsz (optional).
    * A help method to reduce looking up 'required' and 'optional' parameters for each function.
    * A call_history method to return all successful API calls.  



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

#### api_key : *str*
* Default: None.  If None, then do not forget to set your environment variable AV_API_KEY to API key. Otherwise set it in the class constructor.  If you have a Premium API key, do not forget to set the premium property to True as well.
#### premium : *bool*
* Default: False.  Got premium?  Excellent!  You do not need to wait  15.02 seconds between each API call.
#### output_size : *str*
* Default: 'compact'. The other option is 'full'.  See AlphaVantage API documentation for more details.
#### datatype : *str*
* Default: 'json'. This is the preferred request type.  See AlphaVantage API documentation for more details.
#### export : *bool*
* Default: False.  Set it to True if you want to save the file locally according to the export_path property.
#### export_path : *bool*
* Default: *'~/av_data'*.  Or set it to a path you can write to.
#### output : *str*
* Default: 'csv'.  Other options are 'json', 'pkl', 'html', and 'txt'.  If openpyxl is installed, then you can use 'xlsz'.
#### clean : *bool*
* Default: False. Simplifies the column header names for instance: "1. open" -> "open".
#### proxy : *dict*
* Default: {}.  See requests API documentation for more details.


# Original Example

## Initialization
```python
from alphaVantageAPI.alphavantage import AlphaVantage

# Initialize the AlphaVantage Class with default values
AV = AlphaVantage(
        api_key=None,
        premium=False,
        output_size='compact',
        datatype='json',
        export=False,
        export_path='~/av_data',
        output='csv',
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
AV = AlphaVantage(export=True, output='csv', clean=True)
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
AV.help('aliases')

# Help with a specific API function
AV.help('TIME_SERIES_DAILY')

# Help with an indicator
AV.help('BBANDS')
```


## Symbol Search
```python
found_symbol = AV.search('AA')
```


## Data Acquisition Methods
```python
# Global Quote
quote_df = AV.global_quote('MSFT')

# Sectors
sectors_df = AV.sectors()

# FX / Currency
usd_cad_rate_df = AV.fxrate(from_currency='USD', to_currency='CAD') # Rate
usd_cad_I5_df = AV.fx(from_currency='USD', to_currency='CAD', function='FXI', interval=5) # Intraday as int
usd_cad_I60_df = AV.fx(from_currency='USD', to_currency='CAD', function='FXI', interval='60min') # Intraday as str
usd_cad_D_df = AV.fx(from_currency='USD', to_currency='CAD', function='FXD') # Daily
usd_cad_W_df = AV.fx(from_currency='USD', to_currency='CAD', function='FXW') # Weekly
usd_cad_M_df = AV.fx(from_currency='USD', to_currency='CAD', function='FXM') # Monthly

## Digital/Crypto
btc_usd_I5_df = AV.digital(symbol='BTC', market='USD', function='CI', interval=5) # Intraday as int
btc_usd_I60_df = AV.digital(symbol='BTC', market='USD', function='CI', interval='60min') # Intraday as str
btc_usd_D_df = AV.digital(symbol='BTC', market='USD', function='CD') # Daily
btc_usd_W_df = AV.digital(symbol='BTC', market='USD', function='CW') # Weekly
btc_usd_M_df = AV.digital(symbol='BTC', market='USD', function='CM') # Monthly

## Generic Equity/ETF calls
msft_I5_df = AV.intraday(symbol='MSFT', interval=5) # Intraday as int
msft_I60_df = AV.intraday(symbol='MSFT', interval='60min') # Intraday as str
msft_D_df = AV.data(symbol='MSFT', function='D') # Daily
msft_DA_df = AV.data(symbol='MSFT', function='DA') # Daily Adjusted
msft_W_df = AV.data(symbol='MSFT', function='W') # Weekly
msft_WA_df = AV.data(symbol='MSFT', function='WA') # Weekly Adjusted
msft_M_df = AV.data(symbol='MSFT', function='M') # Monthly
msft_MA_df = AV.data(symbol='MSFT', function='MA') # Monthly Adjusted


# List of symbols Daily
symbols = ['AAPL', 'MSFT', 'XLK']
tech_list = AV.data('D', symbols)  # returns list of DataFrames


## Indicators
# SMA(close, 20)
msft_SMA_20_df = AV.data(symbol='MSFT', function='SMA', series_type='close', time_period=20)

# STOCH(close)
msft_STOCH_df = AV.data('STOCH', symbols[1], interval='daily', series_type='close')
```

## Call History
```python
# Returns all successfull calls to the API
history_list = AV.call_history()

# Pretty display of Call History
history_df = pd.DataFrame(history_list)[['symbol', 'function', 'interval', 'time_period']]
print(history_df)
```


# Example: DataFrame Extension 'av'

## Initialization
*For simplicity and protection of your AV API key, the extension uses the environment variable AV_API_KEY upon import of the module.*
```python
import pandas as pd
import alphaVantageAPI
```

## Empty DataFrame: No current data, no problem!
Since 'av' is an extension of a Pandas DataFrame, we need a DataFrame to work from.  Simply create an empty DataFrame, it's contents will be replaced anyhow.
```python
e = pd.DataFrame()
```


## Help!
```python
# Help: lists all the functions and indicators AlphaVantage API supports
e.av.help()

# Print 'function' aliases
e.av.help('aliases')

# Help with a specific API function
e.av.help('TIME_SERIES_DAILY')

# Help with an indicator
e.av.help('BBANDS')
```


## Symbol Search
```python
found_symbol = e.av.search('AA')
```


## Data Acquisition Methods
```python
# Global Quote
quote_df = e.av.global_quote('MSFT')

# Sectors
sectors_df = e.av.sectors()

# FX / Currency
usd_cad_rate_df = e.av.fx('USD', to_currency='EUR')
usd_cad_I5_df = e.av.fx_intraday('USD', to_currency='EUR', interval=5) # Intraday as int
usd_cad_I60_df = e.av.fx_intraday('USD', to_currency='EUR', interval='60min') # Intraday as str
usd_cad_D_df = e.av.fx_daily('USD', to_currency='EUR') # Daily
usd_cad_W_df = e.av.fx_weekly('USD', to_currency='EUR') # Weekly
usd_cad_M_df = e.av.fx_monthly('USD', to_currency='EUR') # Monthly

## Digital/Crypto
btc_usd_I5_df = e.av.digital_intraday('BTC', market='USD', interval=5) # Intraday as int
btc_usd_I60_df = e.av.digital_intraday('BTC', market='USD', interval='60min') # Intraday as str
btc_usd_D_df = e.av.digital_daily('BTC', market='USD') # Daily
btc_usd_W_df = e.av.digital_weekly('BTC', market='USD') # Weekly
btc_usd_M_df = e.av.digital_monthly('BTC', market='USD') # Monthly

## Equities/ ETFs
msft_I5_df = e.av.intraday('MSFT', interval=5) # Intraday as int
msft_I60_df = e.av.intraday('MSFT', interval='60min') # Intraday as str
msft_D_df = e.av.daily('MSFT') # Daily
msft_DA_df = e.av.daily_adjusted('MSFT') # Daily Adjusted
msft_W_df = e.av.weekly('MSFT') # Weekly
msft_WA_df = e.av.weekly_adjusted('MSFT') # Weekly Adjusted
msft_M_df = e.av.monthly('MSFT') # Monthly
msft_MA_df = e.av.monthly_adjusted('MSFT') # Monthly Adjusted
```



# Contributing
Contributions are welcome and I am open to new ideas or implementations.

# Inspiration
If this module does not suit your style or workflow, consider some of the following *AlphaVantage API Python Wrapper* implementations by:

Romel Torres: https://github.com/RomelTorres/alpha_vantage

portfoliome: https://github.com/portfoliome/alphavantage
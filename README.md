# AlphaVantageAPI
*An Opinionated AlphaVantage API Wrapper in Python 3.7*

Access to the AlphaVantage requires a free API key, that can be found at http://www.alphavantage.co/support/#api-key.

By default, this wrapper downloads data as 'json' and converts the results into a Pandas DataFrame.

## Design Considerations
This wrapper was designed to simplify the process of aquiring *free* financial data for retail traders and investors from the financial markets.  While it does require Pandas, Pandas' methods help simplify saving data requests into a variety of file formats such as: csv (default), json, pkl, html, and txt.  If the openpyxl module is also installed, it can be saved as an Excel file: xlsx.

* Considerations
    * Returns a Pandas DataFrame.
    * Able to simplify column names i.e. "1. open" -> "open".
    * Available export formats: csv (default), json, pkl, html, txt, xlsz (optional).
    * A help method to reduce looking up 'required' and 'optional' parameters for each function.
    * A call_history method to return all successful API calls

## Python Modules:
    Required: pandas
    Optional: openpyxl
     *Future: sqlite3

## Installing
Currently only available on github and soon to be added to PyPi.
Ensure you are using Python 3.6.5+ and preferably in a virtual environment.

```shell
git clone https://github.com/twopirllc/alphaVantage.git
pip install pandas
```

Install 'openpyxl' if you want the option to save the results to an Excel file.
```shell
pip install openpyxl
```


### AlphaVantage Class Parameter Defaults
    api_key: str     = None
    output_size: str = 'compact'
    datatype: str    = 'json'
    export: bool     = False
    export_path: str = '~/av_data'
    output: str      = 'csv'
    clean: bool      = False
    proxy: dict      = {}



## Examples
### Initialization
```python
from alphaVantage import AlphaVantage

# Initialize the AlphaVantage Class with default values
av = AlphaVantage(
        api_key=None,
        output_size='compact',
        datatype='json',
        export=False,
        export_path='~/av_data',
        output='csv',
        clean=False,
        proxy={}
    )
```

### Display Current settings
```python
print(av)
```

### Help
```python
# Help: lists all the functions AlphaVantage API supports
print(av.help())

# Print 'function' aliases
print(av.help('aliases'))

# Help with a specific API function
print(av.help('TIME_SERIES_DAILY'))

# Help with an indicator
print(av.help('BBANDS'))
```


### Data Acquisition Methods
```python
# FX / Currency
# fx(from_currency:str, to_currency:str = 'USD')
fx_usd_cad_df = av.fx(from_currency='USD', to_currency='CAD')


# Sectors
sectors_df = av.sectors()


## Digital/Crypto
# digital(symbol:str, market:str = 'USD', function:str = 'CD')
digital_btc_usd_df = av.digital(symbol='BTC', market='USD', function='CD')


## Intraday
# Intervals as integers or strings
# intraday(symbol:str, interval=5)
msft_I5_df = av.intraday(symbol='MSFT', interval=5)
msft_I60_df = av.intraday(symbol='MSFT', interval='60min')


## Generic Equity/ETF calls
# data(function:str, symbol:str = None, **kwargs)
# Daily
msft_D_df = av.data(symbol='MSFT', function='D')

# Daily Adjusted
msft_DA_df = av.data(symbol='MSFT', function='DA')

# List of symbols Daily
symbols = ['AAPL', 'MSFT', 'XLK']
tech_list = av.data('D', symbols)  # returns list of DataFrames


## Indicators
# SMA close 20 Indicator
msft_SMA_20_df = av.data(symbol='MSFT', function='SMA', series_type='close', time_period=20)

# Daily Stochastic Indicator
msft_STOCH_df = av.data('STOCH', symbols[1], interval='daily', series_type='close')
```

### Call History
```python
# Returns all successfull calls to the API
history_list = av.call_history()
```

## Contributing
Contributions are welcome and I am open to new ideas or implementations.

## Inspiration
Check out additional *AlphaVantage API* Python Wrappers by:

Romel Torres: https://github.com/RomelTorres/alpha_vantage

portfoliome: https://github.com/portfoliome/alphavantage
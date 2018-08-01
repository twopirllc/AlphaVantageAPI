#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import re
import math
import requests
import pprint

from pathlib import Path, PurePath
from functools import wraps
from pandas import DataFrame
from .utils import is_home
from .validate_parameters import *

# import openpyxl if installed to support Excel DataFrame exports
try:
    import openpyxl
    _EXCEL_ = True
except ImportError:
    _EXCEL_ = False

# Missing API Key Message
MISSING_API_KEY = '''
[X] The AlphaVantage API key must be provided.

Get a free key from the alphavantage website:
https://www.alphavantage.co/support/#api-key
Use: api_key to set your AV API key
OR
Set your environment variable AV_API_KEY to your AV API key
'''


class AlphaVantage (object):
    """AlphaVantage Class

    A Class to handle Python 3.6 calls to the AlphaVantage API.  It requires Pandas
    module to simplify some operations.  All requests are 'json' requests to
    AlphaVantage's REST API and converted into Pandas DataFrames.

    Parameters
    ----------
    api_key: str = None
    output_size: str = 'compact'
    datatype: str = 'json'
    export: bool = False
    export_path: str = '~/av_data'
    output: str = 'csv'
    clean: bool = False
    proxy: dict = dict()
    
    Examples
    --------
    >>> import AlphaVantage
    >>> av = AlphaVantage(api_key='your API key')"""

    API_NAME = 'AlphaVantage'
    END_POINT = 'https://www.alphavantage.co/query'
    DEBUG = False

    def __init__(self,
            api_key: str = None,
            output_size: str = 'compact',
            datatype: str = 'json',
            export: bool = False,
            export_path: str = '~/av_data',
            output: str = 'csv',
            clean: bool = False,
            proxy: dict = {}
        ): # -> None

        # *future* May incorporate time to successful responses: self._response_history
        # Determining best format
        # self._local_time = time.localtime()
        # self._local_stime = time.strftime("%a, %d %b %Y %H:%M:%S +0000", self._local_time)
        # print(self._local_stime)

        # Load API json file        
        api_file = Path(PurePath(__file__).parent / 'data/api.json')
        self._load_api(api_file)
        
        # Initialize Class properties
        self.api_key     = api_key
        self.export      = export
        self.export_path = export_path

        self.output      = output
        self.datatype    = datatype
        self.output_size = output_size
        self.proxy       = proxy
        self.clean       = clean

        self._requests_session = requests.session()
        self._response_history = []


    # Private Methods
    def _init_export_path(self): # -> str
        """Create the export_path directory if it does not exist."""

        if self.export:
            try:
                if not self.export_path.exists():
                    self.export_path.mkdir(parents=True)
            except OSError as ex:
                raise
            except PermissionError as ex:
                raise


    def _load_api(self, api_file:Path): # -> None
        """Load API from a JSON file."""

        if api_file.exists():
            with api_file.open('r') as content:
                api = json.load(content)
            content.close()

            self.__api = api
            self._api_lists()
        else:
            raise ValueError(f'{api_file} does not exist.')


    def _api_lists(self): # -> None
        """Initialize lists based on API."""

        self.series = [x for x in self.__api['series']]
        self.__api_series = [x['function'] for x in self.series]
        self.__api_function = {x['alias']: x['function'] for x in self.__api['series']}
        self.__api_function_inv = {v: k for k, v in self.__api_function.items()}
        self.__api_datatype = self.__api['datatype']
        self.__api_outputsize = self.__api['outputsize']
        self.__api_series_interval = self.__api['series_interval']

        self.indicators = [x for x in self.__api['indicator']]
        self.__api_indicator = [x['function'] for x in self.indicators]
        self.__api_indicator_matype = self.__api['matype']


    def _function_alias(self, function:str): # -> str
        """Returns the function alias for the given 'function'."""

        return self.__api_function_inv[function] if function in self.__api_function_inv else function


    def _parameters(self, function:str, kind:str): # -> list
        """Returns 'required' or 'optional' parameters for a 'function'."""

        result = []
        if kind in ['required', 'optional']:
            try:
                all_functions = self.series + self.indicators
                result = [x[kind] for x in all_functions if kind in x and function == x['function']].pop()
            except IndexError as ex:
                pass
        return result


    def _av_api_call(self, parameters:dict, timeout:int = 60, **kwargs): # -> pandas DataFrame, json, None
        """Main method to handle AlphaVantage API call request and response."""

        proxies = kwargs['proxies'] if 'proxies' in kwargs else self.proxy

        # Everything is ok so far, add the AV API Key
        parameters['apikey'] = self.api_key

        # Ready to Go. Format and get request response
        try:
            # response =  self._requests_session.get(
            response =  requests.get(  # Use till self._requests_session can be mocked in unittests
                AlphaVantage.END_POINT,
                params = parameters,
                timeout = timeout,
                proxies = proxies
            )
        # except requests.RequestException as ex:
        except requests.exceptions.RequestException as ex:
            print(f"[X] response.get() exception: {ex}\n    parameters: {parameters}")
            pass
        finally:
            response.close()

        if response.status_code != 200:
            print(f"[X] Request Failed: {response.status_code}.\nText:\n{response.text}\n{parameters['function']}")

        # If 'json' datatype, return as 'json'. Otherwise return text response for 'csv'
        if self.datatype == 'json':
            response = response.json()
        else:
            response = response.text

        self._response_history.append(parameters)
        # **Underdevelopment
        # self._response_history.append({'last': time.localtime(), 'parameters': parameters})
        if self.datatype == 'json':
            response = self._to_dataframe(parameters['function'], response)
        return response


    def _save_df(self, function:str, df:DataFrame): # -> None
        """Save Pandas DataFrame to a file type given a 'function'."""

        # Get the alias for the 'function' so filenames are short
        short_function = self._function_alias(function)

        # Get the 'parameters' from the last AV api call since it was successful
        parameters = self.last()

        # Determine Path
        if function == 'CURRENCY_EXCHANGE_RATE': # ok
            path = f"{self.export_path}/{parameters['from_currency']}{parameters['to_currency']}"
        elif function == 'SECTOR': # ok
            path = f"{self.export_path}/sectors"
        elif function == 'BATCH_STOCK_QUOTES': #
            path = f"{self.export_path}/batch"
        elif function == 'TIME_SERIES_INTRADAY': #
            path = f"{self.export_path}/{parameters['symbol']}_{parameters['interval']}"
        elif short_function.startswith('C') and len(short_function) == 2:
            path = f"{self.export_path}/{parameters['symbol']}{parameters['market']}"
        elif function in self.__api_indicator:
            path = f"{self.export_path}/{parameters['symbol']}_{parameters['interval'][0].upper()}_{short_function}"
            if 'series_type' in parameters:
                path += f"_{parameters['series_type'][0].upper()}"
            if 'time_period' in parameters:
                path += f"_{parameters['time_period']}"
        else:
            path = f"{self.export_path}/{parameters['symbol']}_{short_function}"
        path += f".{self.output}"

        # Export desired format
        if self.output == 'csv':
            df.to_csv(path)
        elif self.output == 'json':
            df.to_json(path)
        elif self.output == 'pkl':
            df.to_pickle(path)
        elif self.output == 'html':
            df.to_html(path)
        elif self.output == 'txt':
            Path(path).write_text(df.to_string())
        elif _EXCEL_ and self.output == 'xlsx':
            df.to_excel(path, sheet_name = parameters['function'])


    def _to_dataframe(self, function:str, response:dict): # -> df
        """Converts json response into a Pandas DataFrame given a 'function'"""

        json_keys = response.keys()
        key = [x for x in json_keys if not x.startswith('Meta Data')].pop() or None

        if function == 'CURRENCY_EXCHANGE_RATE':
            df = DataFrame.from_dict(response, orient='index')
            df.set_index('6. Last Refreshed', inplace=True)
        elif function == 'SECTOR':
            df = DataFrame.from_dict(response)
            # Remove 'Information' and 'Last Refreshed' Rows
            df.dropna(axis='index', how='any', thresh=3, inplace=True)
            # Remove 'Meta Data' Column
            df.dropna(axis='columns', how='any', thresh=3, inplace=True)
            # Replace 'NaN' with '0%'
            df.fillna('0%', inplace=True)
        elif function == 'BATCH_STOCK_QUOTES':
            df = DataFrame(response[key], dtype=float)
        else:
            # Else it is a time-series
            df = DataFrame.from_dict(response[key], dtype=float).T
            df.index.rename('date', inplace=True)

        if function == 'SECTOR':
            # Convert sector values to floats
            df = df.applymap(lambda x: float(x.strip('%')) / 100)
        else:
            # Reverse the timeseries dfs
            df = df.iloc[::-1]

        if self.clean:
            df = self._simplify_dataframe_columns(function, df)
        
        if self.export:
            self._save_df(function, df)

        return df


    def _simplify_dataframe_columns(self, function:str, df:DataFrame): # -> df, None
        """Simplifies DataFrame Column Names given a 'function'."""

        if function == 'CURRENCY_EXCHANGE_RATE':
            column_names = ['from', 'from_name', 'to', 'to_name', 'rate', 'tz']
            df.index.rename('datetime', inplace = True)
        elif function == 'SECTOR':
            column_names = ['RT', '1D', '5D', '1M', '3M', 'YTD', '1Y', '3Y', '5Y', '10Y']
        elif function == 'BATCH_STOCK_QUOTES':
            column_names = [re.sub(r'\d+(|\w). ', '', name) for name in df.columns]
            # Greedy but only 4 columns
            column_names = [re.sub(r'timestamp', 'datetime', name) for name in column_names]
            column_names = [re.sub(r'price', 'last', name) for name in column_names]
        else:
            column_names = [re.sub(r'\d+(|\w). ', '', name) for name in df.columns]
            column_names = [re.sub(r' amount', '', name) for name in column_names]
            column_names = [re.sub(r'adjusted', 'adj', name) for name in column_names]
            column_names = [re.sub(r' ', '_', name) for name in column_names]

        df.columns = column_names
        return df


    def _saved_symbols(self, kind:str = None): # -> None
        """Returns a list of saved symbols beginning with: 'ticker_interval'"""

        if kind and isinstance(kind, str):
            files = Path(self.export_path).glob(f"*.{kind}")
        else:
            files = Path(self.export_path).glob(f"*.{self.output}")
        saved_files = sorted(files)

        symbols = set()
        for file in saved_files:
            file_stem_desc = file.stem.split('_')
            if len(file_stem_desc) == 2:
                # ticker = file_stem_desc[0]
                # interval = file_stem_desc[1]
                symbols.add(f"{file_stem_desc[0]}_{file_stem_desc[1]}")
        return list(symbols)


    # Public Methods
    def fx(self, from_currency:str, to_currency:str = 'USD', **kwargs): # -> df, None
        """Simple wrapper to _av_api_call method for currency requests."""

        parameters = {
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': from_currency.upper(),
            'to_currency': to_currency.upper()
        }

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def sectors(self, **kwargs): # -> df, None
        """Simple wrapper to _av_api_call method to request sector performances."""

        parameters = {'function':'SECTOR'}

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def digital(self, symbol:str, market:str = 'USD', function:str = 'CD', **kwargs): # -> df, None
        """Simple wrapper to _av_api_call method for digital currency requests."""

        parameters = {
            'function': self.__api_function[function.upper()],
            'symbol': symbol.upper(),
            'market': market.upper()
        }

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def batch(self, symbols:list, **kwargs): # -> df, None
        """Simple wrapper to _av_api_call method for a batch of symbols"""
    
        if not isinstance(symbols, list):
            symbols = [symbols]
        
        parameters = {
            'function': 'BATCH_STOCK_QUOTES',
            'symbols': ','.join([x.upper() for x in symbols][:100])
        }

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def intraday(self, symbol:str, interval=5, **kwargs): # -> df, None
        """Simple wrapper to _av_api_call method for intraday requests."""

        parameters = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol.upper(),
            'datatype': self.datatype,
            'outputsize': self.output_size
        }
        
        if isinstance(interval, str) and interval in self.__api_series_interval:
            parameters['interval'] = interval
        elif isinstance(interval, int) and interval in [int(re.sub(r'min', '', x)) for x in self.__api_series_interval]:
            parameters['interval'] = '{}min'.format(interval)
        else:
            return None

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def data(self, function:str, symbol:str = None, **kwargs): # -> df, list of df, None
        """Simple wrapper to _av_api_call method for an equity or indicator."""

        # Process a symbol list and return a list of DataFrames
        if isinstance(symbol, list) and len(symbol) > 1:
            # Create list: symbols, with all elements Uppercase from the list: symbol
            symbols = list(map(str.upper, symbol))
            # Call self.data for each ticker in the list: symbols
            return [self.data(function, ticker, **kwargs) for ticker in symbols]

        # Simple Bandaid for an odd occuring Exception
        try:
            symbol = symbol.upper()
        except AttributeError:
            pass
        function = function.upper()

        try:
            function = self.__api_function[function] if function not in self.__api_indicator else function
        except KeyError:
            print(f'[X] Perhaps \'function\' and \'symbol\' are interchanged!? function={function} and symbol={symbol}')
            function, symbol = symbol, function
            self.data(function, symbol, **kwargs)
            # return None

        parameters = {'function': function, 'symbol': symbol}

        if function not in self.__api_indicator:
            parameters['datatype'] = self.datatype
            parameters['outputsize'] = self.output_size

        required_parameters = self._parameters(parameters['function'], 'required')
        for required in required_parameters:
            if required in kwargs:
                parameters[required] = kwargs[required]

        optional_parameters = self._parameters(parameters['function'], 'optional')
        for option in optional_parameters:
            if option in kwargs:
                validate_parameters(self.__api_indicator_matype, option, parameters, **kwargs)

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def help(self, keyword:str = None): # -> None
        """Simple help system to print 'required' or 'optional' parameters based on a keyword."""

        def _functions(): print(f"   Functions:\n    {', '.join(self.__api_series)}")
        def _indicators(): print(f"  Indicators:\n    {', '.join(self.__api_indicator)}")
        def _aliases(): pprint.pprint(self.__api_function, indent=4)

        if keyword is None:
            print(f"{AlphaVantage.__name__} Help: Input a function name for more infomation on 'required'\nAvailable Functions:\n")
            _functions()
            _indicators()
        elif keyword == 'aliases':
            print(f"Aliases:")
            _aliases()
        elif keyword == 'functions':
            _functions()
        elif keyword == 'indicators':
            _indicators()
        else:
            keyword = keyword.upper()
            required = self._parameters(keyword, 'required')
            optional = self._parameters(keyword, 'optional')
            description = [x for x in self.series + self.indicators if x['function'] == keyword][0]['description']

            print(f'\n   Function: {keyword}')
            print(f'Description: {description}')
            print(f"   Required: {', '.join(required)}")
            print(f"   Optional: {', '.join(optional)}") if optional else None


    def call_history(self): # -> list
        """Returns a history of successful response calls."""

        return self._response_history


    def last(self, n:int = 1): # -> str
        """Returns the last \'n\' calls as a list."""

        return (self.call_history())[-n] if n > 0 else []



    # Class Properties
    @property
    def api_key(self): # -> str
        return self.__apikey

    @api_key.setter
    def api_key(self, value:str): # -> None
        if value is None:
            self.__apikey = os.getenv('AV_API_KEY')
        elif isinstance(value, str) and value:
            self.__apikey = value
        else:
            self.__apikey = None
            print(MISSING_API_KEY)
            sys.exit(1)


    @property
    def export(self): # -> bool
        return self.__export

    @export.setter
    def export(self, value:bool): # -> None
        if value is not None and isinstance(value, bool):
            self.__export = value
        else:
            self.__export = False


    @property
    def export_path(self): # -> str
        return self.__export_path

    @export_path.setter
    def export_path(self, value:str): # -> None
        # If using <Path home> /User, then set absolute path to the __export_path variable
        # Then set __export_path = value
        if value is not None and isinstance(value, str):
            path = Path(value)
            if is_home(path):
                # ~/ab/cd -> /ab/cd
                user_subdir = '/'.join(path.parts[1:])
                self.__export_path = Path.home().joinpath(user_subdir)
            else:
                self.__export_path = path
            
            # Initialize the export_path 
            self._init_export_path()


    @property
    def output_size(self): # -> str
        return self.__output_size

    @output_size.setter
    def output_size(self, value:str): # -> None
        if value is not None and value.lower() in self.__api_outputsize:
            self.__output_size = value.lower()
        else:
            self.__output_size = self.__api_outputsize[0]


    @property
    def output(self): # -> str
        return self.__output

    @output.setter
    def output(self, value:str): # -> None
        output_type = ['csv', 'json', 'pkl', 'html', 'txt']
        output_type.append('xlsx') if _EXCEL_ else None

        if value is not None and value.lower() in output_type:
            self.__output = value.lower()
        else:
            self.__output = output_type[0]


    @property
    def datatype(self): # -> str
        return self.__datatype

    @datatype.setter
    def datatype(self, value:str): # -> None
        if value is not None and value.lower() in self.__api_datatype:
            self.__datatype = value.lower()
        else:
            self.__datatype = self.__api_datatype[0]


    @property
    def proxy(self): # -> dict
        return self.__proxy

    @proxy.setter
    def proxy(self, value:dict):# = {}): # -> None
        if value is not None and isinstance(value, dict):
            self.__proxy = value
        else:
            self.__proxy = dict()


    @property
    def clean(self): # -> bool
        return self.__clean

    @clean.setter
    def clean(self, value:bool): # -> None
        if value is not None and isinstance(value, bool):
            self.__clean = value
        else:
            self.__clean = False



    def __repr__(self): # -> str
        s = '{}(end_point={}, api_key={}, export={}, export_path={}, output_size={}, output={}, datatype={}, clean={}, proxy={})'.format(
                AlphaVantage.API_NAME,
                AlphaVantage.END_POINT,
                self.api_key,
                self.export,
                self.export_path,
                self.output_size,
                self.output,
                self.datatype,
                self.clean,
                self.proxy
            )
        return s

    def __str__(self): # -> str
        s = '{}(\n  end_point:str = {},\n  api_key:str = {},\n  export:bool = {},\n  export_path:str = {},\n  output_size:str = {},\n  output:str = {},\n  datatype:str = {},\n  clean:bool = {},\n  proxy:dict = {}\n)'.format(
                AlphaVantage.API_NAME,
                AlphaVantage.END_POINT,
                self.api_key,
                self.export,
                self.export_path,
                self.output_size,
                self.output,
                self.datatype,
                self.clean,
                self.proxy
            )
        return s
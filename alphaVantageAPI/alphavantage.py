# -*- coding: utf-8 -*-
import json
import os
import requests

from datetime import datetime
from importlib.util import find_spec
from pathlib import Path, PurePath
from pprint import pprint
from re import sub as re_sub
from sys import exit as sys_exit
from time import sleep as tsleep

from pandas import DataFrame, DatetimeIndex

from .utils import is_home
from .validate import _validate


Ymd_format = "%Y-%m-%d"
excel = find_spec("openpyxl") is not None
if excel is not None:
    try: import openpyxl
    except ImportError: pass


# Missing API Key Message
MISSING_API_KEY = """
[X] The AlphaVantage API key must be provided.

Get a free key from the alphavantage website:
https://www.alphavantage.co/support/#api-key
Use: api_key to set your AV API key
OR
Set your environment variable AV_API_KEY to your AV API key
"""

class AlphaVantage(object):
    """AlphaVantage Class

    A Class to handle Python 3.6 calls to the AlphaVantage API.  It requires Pandas
    module to simplify some operations.  All requests are 'json' requests to
    AlphaVantage's REST API and converted into Pandas DataFrames.

    Parameters
    ----------
    api_key: str = None
    premium: bool = False
    output_size: str = "compact"
    datatype: str = "json"
    export: bool = False
    export_path: str = "~/av_data"
    output: str = "csv"
    clean: bool = False
    proxy: dict = dict()
    
    Examples
    --------
    >>> from alphaVantageAPI.alphavantage import AlphaVantage
    >>> av = AlphaVantage(api_key="your API key")"""

    API_NAME = "AlphaVantage"
    END_POINT = "https://www.alphavantage.co/query"
    DEBUG = False

    def __init__(self,
            api_key:str = None,
            premium:bool = False,
            export:bool = False,
            export_path:str = "~/av_data",
            output:str = "csv",
            datatype:str = "json",
            output_size:str = "compact",
            clean:bool = False,
            proxy:dict = {}
        ) -> None:

        # Load API json file        
        api_file = Path(PurePath(__file__).parent / "data/api.json")
        self._load_api(api_file)
        
        # Initialize Class properties
        self.api_key     = api_key
        self.premium     = premium
        self.export      = export
        self.export_path = export_path

        self.output      = output
        self.datatype    = datatype
        self.output_size = output_size
        self.proxy       = proxy
        self.clean       = clean

        self._requests_session = requests.session()
        self._response_history = []
        self._api_call_count = 0


    # Private Methods
    def _init_export_path(self) -> str:
        """Create the export_path directory if it does not exist."""
        if self.export:
            try:
                if not self.export_path.exists():
                    self.export_path.mkdir(parents=True)
            except OSError as ex:
                raise


    def _load_api(self, api_file:Path) -> None:
        """Load API from a JSON file."""
        if api_file.exists():
            with api_file.open("r") as content:
                api = json.load(content)
            content.close()

            self.__api = api
            self._api_lists()
        else:
            raise ValueError(f"{api_file} does not exist.")


    def _api_lists(self) -> None:
        """Initialize lists based on API."""
        self.series = [x for x in self.__api["series"]]
        self.__api_series = [x["function"] for x in self.series]
        self.__api_function = {x["alias"]: x["function"] for x in self.__api["series"]}
        self.__api_function_inv = {v: k for k, v in self.__api_function.items()}
        self.__api_datatype = self.__api["datatype"]
        self.__api_horizon = self.__api["horizon"]
        self.__api_listing_state = self.__api["listing_state"]
        self.__api_outputsize = self.__api["outputsize"]
        self.__api_series_interval = self.__api["series_interval"]
        self.__api_slice = self.__api["slice"]

        self.indicators = [x for x in self.__api["indicator"]]
        self.__api_indicator = [x["function"] for x in self.indicators]
        self.__api_indicator_matype = self.__api["matype"]


    def _function_alias(self, function:str) -> str:
        """Returns the function alias for the given "function."""
        return self.__api_function_inv[function] if function in self.__api_function_inv else function


    def _parameters(self, function:str, kind:str) -> list:
        """Returns 'required' or 'optional' parameters for a 'function'."""
        result = []
        if kind in ["required", "optional"]:
            try:
                all_functions = self.series + self.indicators
                result = [x[kind] for x in all_functions if kind in x and function == x["function"]].pop()
            except IndexError:
                pass
        return result


    def _av_api_call(self, parameters:dict, timeout:int = 60, **kwargs) -> DataFrame or json or None:
        """Main method to handle AlphaVantage API call request and response."""
        proxies = kwargs["proxies"] if "proxies" in kwargs else self.proxy

        # Everything is ok so far, add the AV API Key
        parameters["apikey"] = self.api_key

        if not self.premium and self._api_call_count > 0:
            tsleep(15.0001)

        # Ready to Go. Format and get request response
        try:
            # response =  self._requests_session.get(
            response =  requests.get(  # Use till self._requests_session can be mocked in unittests
                AlphaVantage.END_POINT,
                params = parameters,
                timeout = timeout,
                proxies = proxies
            )
        except requests.exceptions.RequestException as ex:
            print(f"[X] response.get() exception: {ex}\n    parameters: {parameters}")
            pass
        finally:
            response.close()

        if response.status_code != 200:
            print(f"[X] Request Failed: {response.status_code}.\nText:\n{response.text}\n{parameters['function']}")

        # If 'json' datatype, return as 'json'. Otherwise return text response for 'csv'
        if self.datatype == "json":
            response = response.json()
        else:
            response = response.text

        self._response_history.append(parameters)
        # **Underdevelopment**
        # self._response_history.append({"last": time.localtime(), "parameters": parameters})
        if self.datatype == "json":
            response = self._to_dataframe(parameters["function"], response)
        else:
            _TSIE = "TIME_SERIES_INTRADAY_EXTENDED"
            _csv_functions = ["EARNINGS_CALENDAR", "IPO_CALENDAR", "LISTING_STATUS", _TSIE]
            if parameters["function"] in _csv_functions:
                response = response.replace("\r", "")
                response = DataFrame(
                    [x.split(",") for x in response.split("\n")[1:]],
                    columns=[x for x in response.split("\n")[0].split(",")]
                )
                response = response.mask(response.eq("None")).dropna()
            
            if parameters["function"] == _TSIE:
                response = response.iloc[::-1]
                response.set_index(DatetimeIndex(response["time"]), inplace=True)
                response.drop(["time"], axis=1, inplace=True)
                response.index.name = "datetime"

        if self._api_call_count < 1:
            self._api_call_count += 1

        return response


    def _to_dataframe(self, function:str, response:dict) -> DataFrame:
        """Converts json response into a Pandas DataFrame given a 'function'"""
        try:
            json_keys = response.keys()
            key = [x for x in json_keys if not x.startswith("Meta Data")].pop()
        except IndexError:
            print(f" [X] Download failed.  Check the AV documentation for correct parameters: https://www.alphavantage.co/documentation/")
            sys_exit(1)

        reports = None
        if function == "CRYPTO_RATING":
            df = DataFrame.from_dict(response, orient="index")
        elif function == "GLOBAL_QUOTE":
            df = DataFrame.from_dict(response, orient="index")
        elif function == "CURRENCY_EXCHANGE_RATE":
            df = DataFrame.from_dict(response, orient="index")
        elif function == "SYMBOL_SEARCH":
            if len(response[key]) < 1: return None
            df = DataFrame(response[key])
        elif function == "OVERVIEW": #
            df = DataFrame.from_dict(response, orient="index")
        elif function == "INCOME_STATEMENT": #
            quarterlydf = DataFrame.from_dict(response["quarterlyReports"])
            quarterlydf.set_index("fiscalDateEnding", inplace=True)

            annuallydf = DataFrame.from_dict(response["annualReports"])
            annuallydf.set_index("fiscalDateEnding", inplace=True)

            reports = [quarterlydf, annuallydf]
        elif function == "BALANCE_SHEET": #
            quarterlydf = DataFrame.from_dict(response["quarterlyReports"])
            quarterlydf.set_index("fiscalDateEnding", inplace=True)

            annuallydf = DataFrame.from_dict(response["annualReports"])
            annuallydf.set_index("fiscalDateEnding", inplace=True)

            reports = [quarterlydf, annuallydf]
        elif function == "CASH_FLOW": #
            quarterlydf = DataFrame.from_dict(response["quarterlyReports"])
            quarterlydf.set_index("fiscalDateEnding", inplace=True)

            annuallydf = DataFrame.from_dict(response["annualReports"])
            annuallydf.set_index("fiscalDateEnding", inplace=True)

            reports = [quarterlydf, annuallydf]
        else:
            # Otherwise it is a time-series, also calls df = df.iloc[::-1] below
            df = DataFrame.from_dict(response[key], dtype=float).T
            df.index.rename("date", inplace=True)

        # Handle Reports / Search / GC /
        if reports is not None and len(reports) > 0:
            if self.export:
                self._save_df(function, reports[0], report_freq="Quarterly")
                self._save_df(function, reports[1], report_freq="Annually")
            return reports
        else:
            if function != "SYMBOL_SEARCH":
                df = df.iloc[::-1]
                df.reset_index(inplace=True)

            if self.clean:
                df = self._simplify_dataframe_columns(function, df)

                if function in ["SYMBOL_SEARCH"]: pass
                elif function == "CURRENCY_EXCHANGE_RATE":
                    df.set_index("refreshed", inplace=True)
                elif function == "CRYPTO_RATING":
                    df.drop(["index"], axis=1, inplace=True)
                    df.set_index("symbol", inplace=True)
                elif function == "GLOBAL_QUOTE":
                    df.drop(["index"], axis=1, inplace=True)
                    df.set_index("symbol", inplace=True)
                elif function != "OVERVIEW":
                    df.set_index(DatetimeIndex(df["date"]), inplace=True)
                    df.drop(["date"], axis=1, inplace=True)
                else:
                    df.set_index("item", inplace=True)

            if self.export:
                self._save_df(function, df)

        return df


    def _simplify_dataframe_columns(self, function:str, df:DataFrame) -> DataFrame or None:
        """Simplifies DataFrame Column Names given a 'function'."""
        if function == "CURRENCY_EXCHANGE_RATE":
            column_names = ["index", "from", "from_name", "to", "to_name", "rate", "refreshed", "tz", "bid", "ask"]
        elif function == "OVERVIEW":
            column_names = ["item", "value"]
        elif function in ["CRYPTO_RATING", "GLOBAL_QUOTE"]:
            column_names = [re_sub(r'\d+(|\w). ', "", name) for name in df.columns]
        elif function == "SYMBOL_SEARCH":
            column_names = ["symbol", "name", "type", "region", "market_open", "market_close", "tz", "currency", "match"]
        else:
            column_names = [re_sub(r'\d+(|\w). ', "", name) for name in df.columns]
            column_names = [re_sub(r' amount', "", name) for name in column_names]
            column_names = [re_sub(r'adjusted', "adj", name) for name in column_names]
            column_names = [re_sub(r' ', "_", name) for name in column_names]

        df.columns = column_names
        return df


    def _save_df(self, function:str, df:DataFrame, **kwargs) -> None:
        """Save Pandas DataFrame to a file type given a 'function'."""
        # Get the alias for the 'function' so filenames are short
        short_function = self._function_alias(function)

        # Get the 'parameters' from the last AV api call since it was successful
        parameters = self.last()

        dt_now = datetime.now().strftime(Ymd_format)

        report_freq = kwargs.pop("report_freq", None)
        # Determine Path
        if function == "CURRENCY_EXCHANGE_RATE": # ok
            path = f"{self.export_path}/{parameters['from_currency']}{parameters['to_currency']}"
        elif function in ["FXD", "FXM", "FXW", "FX_DAILY", "FX_MONTHLY", "FX_WEEKLY"]:
            path = f"{self.export_path}/{parameters['from_symbol']}{parameters['to_symbol']}_{short_function.replace('FX', '')}"
        elif function in ["FXI", "FX_INTRADAY"]:
            path = f"{self.export_path}/{parameters['from_symbol']}{parameters['to_symbol']}_{parameters['interval']}"
        elif function in ["CD", "CW", "CM", "DIGITAL_CURRENCY_DAILY", "DIGITAL_CURRENCY_WEEKLY", "DIGITAL_CURRENCY_MONTHLY"]:
            path = f"{self.export_path}/{parameters['symbol']}{parameters['market']}_{short_function.replace('C', '')}"
        elif function == "TIME_SERIES_INTRADAY_EXTENDED":
            ie_slice = re_sub(r'month', "M",  re_sub(r'year', "Y", parameters['slice']))
            ie_adjusted = "_ADJ" if parameters['adjusted'] == "true" else ""
            path = f"{self.export_path}/{parameters['symbol']}_{short_function}_{parameters['interval']}_{ie_slice}{ie_adjusted}"
        elif function == "OVERVIEW": #
            path = f"{self.export_path}/{parameters['symbol']}"
        elif function == "SYMBOL_SEARCH": #
            path = f"{self.export_path}/SEARCH_{parameters['keywords']}"
        elif function == "INCOME_STATEMENT": #
            if isinstance(report_freq, str):
                path = f"{self.export_path}/{parameters['symbol']}_IS_{report_freq}"
        elif function == "BALANCE_SHEET": #
            if isinstance(report_freq, str):
                path = f"{self.export_path}/{parameters['symbol']}_BS_{report_freq}"
        elif function == "CASH_FLOW": #
            if isinstance(report_freq, str):
                path = f"{self.export_path}/{parameters['symbol']}_CF_{report_freq}"
        elif function == "CRYPTO_RATING": #
            path = f"{self.export_path}/{parameters['symbol']}_RATING"
        elif function == "TIME_SERIES_INTRADAY": #
            i_adjusted = "_ADJ" if parameters['adjusted'] == "true" else ""
            path = f"{self.export_path}/{parameters['symbol']}_{parameters['interval']}{i_adjusted}"
        elif short_function.startswith("C") and len(short_function) == 2:
            path = f"{self.export_path}/{parameters['symbol']}{parameters['market']}"
        elif function in self.__api_indicator:
            path = f"{self.export_path}/{parameters['symbol']}_{parameters['interval'][0].upper()}_{short_function}"
            if "series_type" in parameters:
                path += f"_{parameters['series_type'][0].upper()}"
            if "time_period" in parameters:
                path += f"_{parameters['time_period']}"
        elif function == "EARNINGS_CALENDAR":
            if "symbol" in parameters:
                path = f"{self.export_path}/EARNINGS_{parameters['symbol']}_{parameters['horizon'].upper()}_{dt_now}"
            else:
                path = f"{self.export_path}/EARNINGS_{parameters['horizon'].upper()}_{dt_now}"
        elif function == "IPO_CALENDAR":
            path = f"{self.export_path}/IPOS_{dt_now}"
        elif function == "LISTING_STATUS":
            _state = "" if parameters["state"] == "active" else "DE"
            path = f"{self.export_path}/{_state}LISTED_{dt_now}"
            if "date" in parameters and parameters["date"] is not None:
                path += f"_FOR_{parameters['date']}"
        else:
            path = f"{self.export_path}/{parameters['symbol']}_{short_function}"
        path += f".{self.output}"

        # Export desired format
        if self.output == "csv":
            df.to_csv(path)
        elif self.output == "json":
            df.to_json(path)
        elif self.output == "pkl":
            df.to_pickle(path)
        elif self.output == "html":
            df.to_html(path)
        elif self.output == "txt":
            Path(path).write_text(df.to_string())
        elif excel and self.output == "xlsx":
            df.to_excel(path, sheet_name = parameters["function"])


    # Public Methods
    def fx(self, from_symbol:str = "EUR", to_symbol:str = "USD", function:str = "FXD", **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for FX requests."""
        if function.upper() not in ["FXD", "FXI", "FXM", "FXW", "FX_DAILY", "FX_INTRADAY", "FX_MONTHLY", "FX_WEEKLY"]:
            return None
        else:
            function = self.__api_function[function]

        parameters = {
            "function": function.upper(),
            "from_symbol": from_symbol.upper(),
            "to_symbol": to_symbol.upper()
        }

        interval = kwargs.pop("interval", None)
        if interval is not None:
            if isinstance(interval, str) and interval in self.__api_series_interval:
                parameters["interval"] = interval
            elif isinstance(interval, int) and interval in [int(re_sub(r'min', "", x)) for x in self.__api_series_interval]:
                parameters["interval"] = f"{interval}min"
            else:
                return None

        if function not in self.__api_indicator:
            parameters["datatype"] = self.datatype
            parameters["outputsize"] = self.output_size

        required_parameters = self._parameters(parameters["function"], "required")
        for required in required_parameters:
            if required in kwargs:
                parameters[required] = kwargs[required]

        optional_parameters = self._parameters(parameters["function"], "optional")
        for option in optional_parameters:
            if option in kwargs:
                _validate(self.__api_indicator_matype, option, parameters, **kwargs)

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def fxrate(self, from_symbol:str, to_symbol:str = "USD", **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for Digital Currency Rate requests."""
        parameters = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": from_symbol.upper(),
            "to_currency": to_symbol.upper()
        }

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def quote(self, symbol:str, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for Global Quote requests."""
        parameters = {"function": "GLOBAL_QUOTE", "symbol": symbol.upper()}

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def search(self, keywords:str, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for Search requests."""
        parameters = {"function": "SYMBOL_SEARCH", "keywords": keywords}

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def digital(self, symbol:str, market:str = "USD", function:str = "CD", **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for Digital Currency requests."""
        parameters = {
            "function": self.__api_function[function.upper()],
            "symbol": symbol.upper(),
            "market": market.upper()
        }

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def crypto_rating(self, symbol:str, function:str = "CR", **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for Digital Currency Rating requests."""
        parameters = {
            "function": self.__api_function[function.upper()],
            "symbol": symbol.upper(),
        }

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def intraday(self, symbol:str, interval=5, adjusted=True, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for Intraday requests."""
        parameters = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol.upper(),
            "datatype": self.datatype,
            "outputsize": self.output_size,
            "adjusted": "true" if adjusted else "false"
        }
        
        if isinstance(interval, str) and interval in self.__api_series_interval:
            parameters["interval"] = interval
        elif isinstance(interval, int) and interval in [int(re_sub(r'min', "", x)) for x in self.__api_series_interval]:
            parameters["interval"] = f"{interval}min"
        else:
            return None

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def intraday_extended(self, symbol:str, interval=5, slice="year1month1", adjusted=True, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for Intraday Extended requests."""
        parameters = {
            "function": "TIME_SERIES_INTRADAY_EXTENDED",
            "symbol": symbol.upper(),
            "adjusted": "true" if adjusted else "false"
        }

        if isinstance(interval, str) and interval in self.__api_series_interval:
            parameters["interval"] = interval
        elif isinstance(interval, int) and interval in [int(re_sub(r'min', "", x)) for x in self.__api_series_interval]:
            parameters["interval"] = f"{interval}min"
        else:
            return None

        if isinstance(slice, str) and slice.lower() in self.__api_slice:
            parameters["slice"] = slice.lower()

        self.datatype = "csv" # Returns csv by default
        download = self._av_api_call(parameters, **kwargs)

        if self.export:
            self._save_df(parameters["function"], download)
        return download if download is not None else None


    def earnings(self, symbol:str = None, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for Earnings Calendar requests."""
        parameters = {"function": "EARNINGS_CALENDAR"}
        ascending = kwargs.pop("asc", True)
        horizon = kwargs.pop("horizon", "3month")
        index = kwargs.pop("index", "symbol")

        if symbol is not None and isinstance(symbol, str) and len(symbol) > 0:
            parameters["symbol"] = symbol.upper()

        if isinstance(horizon, str) and horizon in self.__api_horizon:
            parameters["horizon"] = horizon

        self.datatype = "csv" # Returns csv by default
        download = self._av_api_call(parameters, **kwargs)
        download.set_index(index, inplace=True)
        download.sort_index(axis=0, ascending=ascending, inplace=True)

        if self.export:
            self._save_df(parameters["function"], download)
        return download if download is not None else None


    def ipos(self, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for IPO Calendar requests."""
        parameters = {"function": "IPO_CALENDAR"}
        ascending = kwargs.pop("asc", True)
        index = kwargs.pop("index", "symbol")

        self.datatype = "csv"
        download = self._av_api_call(parameters, **kwargs) # returns DataFrame
        download.set_index(index, inplace=True)
        download.sort_index(axis=0, ascending=ascending, inplace=True)

        if self.export:
            self._save_df(parameters["function"], download)
        return download if download is not None else None


    def listed(self, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for Listing Status requests."""
        parameters = {"function": "LISTING_STATUS"}
        ascending = kwargs.pop("asc", True)
        date = kwargs.pop("date", None)
        index = kwargs.pop("index", "symbol")
        state = kwargs.pop("state", "active")

        if date is not None and isinstance(date, str) and len(date) > 0:
            parameters["date"] = f"{date}"

        if isinstance(state, str) and state in self.__api_listing_state:
            parameters["state"] = state.lower()

        self.datatype = "csv" # Returns csv by default
        download = self._av_api_call(parameters, **kwargs)
        download.set_index(index, inplace=True)
        download.sort_index(axis=0, ascending=ascending, inplace=True)

        if self.export:
            self._save_df(parameters["function"], download)
        return download if download is not None else None

    # Company Information
    def overview(self, symbol:str, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for Company Overview requests."""
        parameters = {"function": "OVERVIEW", "symbol": symbol.upper()}
        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def balance(self, symbol:str, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for Balance Sheet requests."""
        parameters = {"function": "BALANCE_SHEET", "symbol": symbol.upper()}
        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def cashflow(self, symbol:str, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for Cash Flow requests."""
        parameters = {"function": "CASH_FLOW", "symbol": symbol.upper()}
        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def income(self, symbol:str, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for Income Statement requests."""
        parameters = {"function": "INCOME_STATEMENT", "symbol": symbol.upper()}
        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None


    def data(self, symbol:str, function:str = "D", **kwargs) -> DataFrame or list or None:
        """Simple wrapper to _av_api_call method for an Equity or Indicator."""
        if isinstance(symbol, str):
            symbol = symbol.upper()

        # TODO: Refactor for multithreading
        # Process a symbol list and return a list of DataFrames
        if isinstance(symbol, list) and len(symbol) > 1:
            # Create list: symbols, with all elements Uppercase from the list: symbol
            symbols = list(map(str.upper, symbol))
            # Call self.data for each ticker in the list: symbols
            return {ticker: self.data(ticker, function, **kwargs) for ticker in symbols}

        try:
            function = self.__api_function[function] if function not in self.__api_indicator else function
        except KeyError:
            print(f"[X] Perhaps \'function\' and \'symbol\' are interchanged!? function={function} and symbol={symbol}")
            function, symbol = symbol.upper(), function.upper()
            self.data(symbol, function, **kwargs)

        parameters = {"function": function, "symbol": symbol}

        if function not in self.__api_indicator:
            parameters["datatype"] = self.datatype
            parameters["outputsize"] = self.output_size

        required_parameters = self._parameters(parameters["function"], "required")
        for required in required_parameters:
            if required in kwargs:
                parameters[required] = kwargs[required]

        optional_parameters = self._parameters(parameters["function"], "optional")
        for option in optional_parameters:
            if option in kwargs:
                _validate(self.__api_indicator_matype, option, parameters, **kwargs)

        download = self._av_api_call(parameters, **kwargs)
        return download if download is not None else None



    def help(self, keyword:str = None) -> None:
        """Simple help system to print 'required' or 'optional' parameters based on a keyword."""
        def _functions(): print(f"   Functions:\n    {', '.join(self.__api_series)}")
        def _indicators(): print(f"  Indicators:\n    {', '.join(self.__api_indicator)}")
        def _aliases(): pprint(self.__api_function, indent=4)

        if keyword is None:
            print(f"{AlphaVantage.__name__} Help: Input a function name for more infomation on 'required'\nAvailable Functions:\n")
            _functions()
            _indicators()
        elif keyword == "aliases":
            print(f"Aliases:")
            _aliases()
        elif keyword == "functions": _functions()
        elif keyword == "indicators": _indicators()
        else:
            keyword = keyword.upper()
            required = self._parameters(keyword, "required")
            optional = self._parameters(keyword, "optional")
            description = [x for x in self.series + self.indicators if x["function"] == keyword][0]["description"]

            print(f"\n   Function: {keyword}")
            print(f"Description: {description}")
            print(f"   Required: {', '.join(required)}")
            print(f"   Optional: {', '.join(optional)}") if optional else None


    def call_history(self) -> list:
        """Returns a history of successful response calls."""
        return self._response_history


    def last(self, n:int = 1) -> str:
        """Returns the last \'n\' calls as a list."""
        return (self.call_history())[-n] if n > 0 else []


    # Class Properties
    @property
    def api_key(self) -> str:
        return self.__apikey

    @api_key.setter
    def api_key(self, value:str) -> None:
        if value is None:
            self.__apikey = os.getenv("AV_API_KEY")
        elif isinstance(value, str) and value:
            self.__apikey = value
        else:
            self.__apikey = None
            print(MISSING_API_KEY)
            sys_exit(1)


    @property
    def export(self) -> bool:
        return self.__export

    @export.setter
    def export(self, value:bool) -> None:
        if value is not None and isinstance(value, bool):
            self.__export = value
        else:
            self.__export = False


    @property
    def export_path(self) -> str:
        return self.__export_path

    @export_path.setter
    def export_path(self, value:str) -> None:
        # If using <Path home> /User, then set absolute path to the __export_path variable
        # Then set __export_path = value
        if value is not None and isinstance(value, str):
            path = Path(value)
            if is_home(path):
                # ~/ab/cd -> /ab/cd
                user_subdir = "/".join(path.parts[1:])
                self.__export_path = Path.home().joinpath(user_subdir)
            else:
                self.__export_path = path

            # Initialize the export_path
            self._init_export_path()


    @property
    def output_size(self) -> str:
        return self.__output_size

    @output_size.setter
    def output_size(self, value:str) -> None:
        if value is not None and value.lower() in self.__api_outputsize:
            self.__output_size = value.lower()
        else:
            self.__output_size = self.__api_outputsize[0]


    @property
    def output(self) -> str:
        return self.__output

    @output.setter
    def output(self, value:str) -> None:
        output_type = ["csv", "json", "pkl", "html", "txt"]
        if excel: output_type.append("xlsx")

        if value is not None and value.lower() in output_type:
            self.__output = value.lower()
        else:
            self.__output = output_type[0]


    @property
    def datatype(self) -> str:
        return self.__datatype

    @datatype.setter
    def datatype(self, value:str) -> None:
        if value is not None and value.lower() in self.__api_datatype:
            self.__datatype = value.lower()
        else:
            self.__datatype = self.__api_datatype[0]


    @property
    def proxy(self) -> dict:
        return self.__proxy

    @proxy.setter
    def proxy(self, value:dict) -> None:
        if value is not None and isinstance(value, dict):
            self.__proxy = value
        else:
            self.__proxy = dict()


    @property
    def clean(self) -> bool:
        return self.__clean

    @clean.setter
    def clean(self, value:bool) -> None:
        if value is not None and isinstance(value, bool):
            self.__clean = value
        else:
            self.__clean = False


    @property
    def premium(self) -> bool:
        return self.__premium

    @premium.setter
    def premium(self, value:bool) -> None:
        if value is not None and isinstance(value, bool):
            self.__premium = value
        else:
            self.__premium = False


    def __repr__(self) -> str:
        s  = f"{AlphaVantage.API_NAME}(\n  end_point:str = {AlphaVantage.END_POINT},\n"
        s += f"  api_key:str = {self.api_key},\n  export:bool = {self.export},\n"
        s += f"  export_path:str = {self.export_path},\n  output_size:str = {self.output_size},\n"
        s += f"  output:str = {self.output},\n  datatype:str = {self.datatype},\n"
        s += f"  clean:bool = {self.clean},\n  proxy:dict = {self.proxy}\n)"
        return s


    def __str__(self) -> str:
        s  = f"{AlphaVantage.API_NAME}(\n  end_point:str = {AlphaVantage.END_POINT},\n"
        s += f"  api_key:str = {self.api_key},\n  export:bool = {self.export},\n"
        s += f"  export_path:str = {self.export_path},\n  output_size:str = {self.output_size},\n"
        s += f"  output:str = {self.output},\n  datatype:str = {self.datatype},\n"
        s += f"  clean:bool = {self.clean},\n  proxy:dict = {self.proxy}\n)"
        return s

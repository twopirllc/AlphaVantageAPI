# -*- coding: utf-8 -*-
import time
import math
import re
import numpy as np
import pandas as pd

from os import getenv as os_getenv
from ._base_pandas_object import *
from alphaVantageAPI.alphavantage import AlphaVantage



# Load an instance of AV with user's environment variable 'AV_API_KEY'
# Force Clean
_AV_ = AlphaVantage(api_key=None, clean=True)


@pd.api.extensions.register_dataframe_accessor('av')
class AlphaVantageDownloader(BasePandasObject):
    # def __call__(self, kind=None, output_size='compact', alias=None, timed=False, *args, **kwargs):
    def __call__(self, q=None, output_size='compact', timed=False, *args, **kwargs):
        try:
            if isinstance(q, str):
                q = q.lower()
                fn = getattr(self, q)

                if timed:
                    stime = time.time()

                # Run the query
                query = fn(**kwargs)

                if timed:
                    time_diff = time.time() - stime
                    ms = time_diff * 1000
                    query.timed = f"{ms:2.3f} ms ({time_diff:2.3f} s)"

                # Add an alias if passed
                # if alias:
                #     query.alias = f"{alias}"
                
                return query
            else:
                self.help(keyword=kwargs.pop('help', None), *args, **kwargs)

        except:
            self.help(keyword=kwargs.pop('help', None), *args, **kwargs)


    def help(self, keyword=None, **kwargs):
        """Simple Help Screen"""
        _AV_.help(keyword)



    def daily(self, symbol:str, **kwargs): # -> df
        self._df = _AV_.data(function='D', symbol=symbol, **kwargs)
        print(f"[d]  df[{type(self._df)}]\n{self._df.index}\n{self._df}")
        return self._df


    def daily_adjusted(self, symbol:str, **kwargs): # -> df
        self._df = _AV_.data(function='DA', symbol=symbol, **kwargs)
        print(f"[da] df[{type(self._df)}]\n{self._df.index}\n{self._df}")
        return self._df


    def digital(self, symbol:str, market:str = 'USD', function:str = 'CD', **kwargs): # -> df
        self._df = _AV_.digital(symbol, market=market, function=function, **kwargs)
        print(f"[c]  df[{type(self._df)}]\n{self._df.index}\n{self._df}")
        return self._df


    def intraday(self, symbol:str, interval=5, **kwargs): # -> df
        self._df = _AV_.intraday(symbol, interval=interval, **kwargs)
        print(f"[i]  df[{type(self._df)}]\n{self._df.index}\n{self._df}")
        return self._df


    def fx(self, from_currency:str, to_currency:str = 'USD', **kwargs): # -> df
        self._df = _AV_.fx(from_currency=from_currency, to_currency=to_currency, **kwargs)
        print(f"[f]  df[{type(self._df)}]:\n{self._df}")
        return self._df


    def monthly(self, symbol:str, **kwargs): # -> df
        self._df = _AV_.data(function='M', symbol=symbol, **kwargs)
        print(f"[m]  df[{type(self._df)}]\n{self._df.index}\n{self._df}")
        return self._df


    def monthly_adjusted(self, symbol:str, **kwargs): # -> df
        self._df = _AV_.data(function='MA', symbol=symbol, **kwargs)
        print(f"[ma] df[{type(self._df)}]\n{self._df.index}\n{self._df}")
        return self._df


    def sectors(self, **kwargs): # -> df
        self._df = _AV_.sectors(**kwargs)
        print(f"[s]  df[{type(self._df)}]:\n{self._df}")
        return self._df


    def weekly(self, symbol:str, **kwargs): # -> df
        self._df = _AV_.data(function='W', symbol=symbol, **kwargs)
        print(f"[w]  df[{type(self._df)}]\n{self._df.index}\n{self._df}")
        return self._df


    def weekly_adjusted(self, symbol:str, **kwargs): # -> df
        self._df = _AV_.data(function='WA', symbol=symbol, **kwargs)
        print(f"[wa] df[{type(self._df)}]\n{self._df.index}\n{self._df}")
        return self._df



    @property
    def clean(self): # -> bool
        return _AV_.clean

    @clean.setter
    def clean(self, value:str): # -> None
        _AV_.clean = value


    @property
    def export(self): # -> bool
        return _AV_.export

    @clean.setter
    def export(self, value:str): # -> None
        _AV_.export = value


    @property
    def output(self): # -> str
        return _AV_.output

    @output.setter
    def output(self, value:str): # -> None
        _AV_.output = value


    @property
    def output_size(self): # -> str
        return _AV_.output_size

    @output_size.setter
    def output_size(self, value:str): # -> None
        _AV_.output_size = value


    @property
    def premium(self): # -> bool
        return _AV_.premium

    @premium.setter
    def premium(self, value:str): # -> None
        _AV_.premium = value


    @property
    def proxy(self): # -> dict
        return _AV_.proxy

    @proxy.setter
    def proxy(self, value:str): # -> None
        _AV_.proxy = value
# -*- coding: utf-8 -*-
import time
import math
import re
import numpy as np
import pandas as pd

from time import perf_counter

from os import getenv as os_getenv
from ._base_pandas_object import *
from .utils import final_time
from alphaVantageAPI.alphavantage import AlphaVantage


# Load an instance of AV with user's environment variable "AV_API_KEY"
# Force Clean
_AV_ = AlphaVantage(api_key=None, clean=True)


@pd.api.extensions.register_dataframe_accessor("av")
class AlphaVantageDownloader(BasePandasObject):
    _df = pd.DataFrame()

    def __call__(self, q=None, output_size="compact", timed=False, *args, **kwargs):
        try:
            if isinstance(q, str):
                q = q.lower()
                fn = getattr(self, q)

                if timed: stime = perf_counter()
                query = fn(**kwargs)
                if timed: query.timed = final_time(stime)
                return query
            else:
                self.help(keyword=kwargs.pop("help", None), *args, **kwargs)

        except:
            self.help(keyword=kwargs.pop("help", None), *args, **kwargs)
        finally:
            self._df = None


    def help(self, keyword=None, **kwargs):
        """Simple Help Screen"""
        _AV_.help(keyword)



    # Global Quote
    def global_quote(self, symbol:str, **kwargs) -> pd.DataFrame:
        self._df = _AV_.global_quote(symbol, **kwargs)
        self._df.name = symbol.upper()
        return self._df


    # Search
    def search(self, keywords:str, **kwargs) -> pd.DataFrame:
        self._df = _AV_.search(keywords, **kwargs)
        self._df.name = keywords.upper()
        return self._df


    # Company Information
    def overview(self, symbol:str, **kwargs) -> pd.DataFrame:
        self._df = _AV_.overview(symbol, **kwargs)
        self._df.name = symbol.upper()
        return self._df


    # Securities
    def daily(self, symbol:str, **kwargs) -> pd.DataFrame:
        self._df = _AV_.data(function="D", symbol=symbol, **kwargs)
        self._df.name = symbol.upper()
        return self._df


    def daily_adjusted(self, symbol:str, **kwargs) -> pd.DataFrame:
        self._df = _AV_.data(function="DA", symbol=symbol, **kwargs)
        self._df.name = symbol.upper()
        return self._df


    def intraday(self, symbol:str, interval=5, **kwargs) -> pd.DataFrame:
        self._df = _AV_.intraday(symbol, interval=interval, **kwargs)
        self._df.name = symbol.upper()
        return self._df


    def monthly(self, symbol:str, **kwargs) -> pd.DataFrame:
        self._df = _AV_.data(function="M", symbol=symbol, **kwargs)
        self._df.name = symbol.upper()
        return self._df


    def monthly_adjusted(self, symbol:str, **kwargs) -> pd.DataFrame:
        self._df = _AV_.data(function="MA", symbol=symbol, **kwargs)
        self._df.name = symbol.upper()
        return self._df


    def weekly(self, symbol:str, **kwargs) -> pd.DataFrame:
        self._df = _AV_.data(function="W", symbol=symbol, **kwargs)
        self._df.name = symbol.upper()
        return self._df


    def weekly_adjusted(self, symbol:str, **kwargs) -> pd.DataFrame:
        self._df = _AV_.data(function="WA", symbol=symbol, **kwargs)
        self._df.name = symbol.upper()
        return self._df


    # Crypto/Digital
    def crypto_rating(self, symbol:str, **kwargs) -> pd.DataFrame:
        self._df = _AV_.crypto_rating(symbol, function="CR", **kwargs)
        self._df.name = symbol.upper()
        return self._df

    def digital_daily(self, symbol:str, market:str = "USD", **kwargs) -> pd.DataFrame:
        self._df = _AV_.digital(symbol, market=market, function="CD", **kwargs)
        self._df.name = f"{symbol.upper()}.{market.upper()}"
        return self._df

    def digital_monthly(self, symbol:str, market:str = "USD", **kwargs) -> pd.DataFrame:
        self._df = _AV_.digital(symbol, market=market, function="CM", **kwargs)
        self._df.name = f"{symbol.upper()}.{market.upper()}"
        return self._df


    def digital_weekly(self, symbol:str, market:str = "USD", **kwargs) -> pd.DataFrame:
        self._df = _AV_.digital(symbol, market=market, function="CW", **kwargs)
        self._df.name = f"{symbol.upper()}.{market.upper()}"
        return self._df


    # FX
    def fxrate(self, from_currency:str, to_currency:str = "USD", **kwargs) -> pd.DataFrame:
        self._df = _AV_.fxrate(from_currency=from_currency, to_currency=to_currency, **kwargs)
        self._df.name = f"{from_currency.upper()}.{to_currency.upper()}"
        return self._df

    def fx_daily(self, from_symbol:str, to_symbol:str = "USD", **kwargs) -> pd.DataFrame:
        self._df = _AV_.fx("FXD", from_symbol=from_symbol, to_symbol=to_symbol, **kwargs)
        self._df.name = f"{from_symbol.upper()}.{to_symbol.upper()}"
        return self._df


    def fx_intraday(self, from_symbol:str, to_symbol:str = "USD", interval=5, **kwargs) -> pd.DataFrame:
        self._df = _AV_.fx("FXI", from_symbol=from_symbol, to_symbol=to_symbol, interval=interval, **kwargs)
        self._df.name = f"{from_symbol.upper()}.{to_symbol.upper()}"
        return self._df


    def fx_monthly(self, from_symbol:str, to_symbol:str = "USD", **kwargs) -> pd.DataFrame:
        self._df = _AV_.fx("FXM", from_symbol=from_symbol, to_symbol=to_symbol, **kwargs)
        self._df.name = f"{from_symbol.upper()}.{to_symbol.upper()}"
        return self._df


    def fx_weekly(self, from_symbol:str, to_symbol:str = "USD", **kwargs) -> pd.DataFrame:
        self._df = _AV_.fx("FXW", from_symbol=from_symbol, to_symbol=to_symbol, **kwargs)
        self._df.name = f"{from_symbol.upper()}.{to_symbol.upper()}"
        return self._df

    # Aliases
    CR = crypto_rating
    GQ = global_quote

    OV = overview

    D = daily
    DA = daily_adjusted
    I = intraday
    M = monthly
    MA = monthly_adjusted
    W = weekly
    WA = weekly_adjusted

    CD = digital_daily
    CM = digital_monthly
    CW = digital_weekly

    FX = fxrate
    FXD = fx_daily
    FXI = fx_intraday
    FXM = fx_monthly
    FXW = fx_weekly


    @property
    def clean(self) -> bool:
        return _AV_.clean

    @clean.setter
    def clean(self, value:str) -> None:
        _AV_.clean = value


    @property
    def export(self) -> bool:
        return _AV_.export

    @export.setter
    def export(self, value:str) -> None:
        _AV_.export = value


    @property
    def output(self) -> str:
        return _AV_.output

    @output.setter
    def output(self, value:str) -> None:
        _AV_.output = value


    @property
    def output_size(self) -> str:
        return _AV_.output_size

    @output_size.setter
    def output_size(self, value:str) -> None:
        _AV_.output_size = value


    @property
    def premium(self) -> bool:
        return _AV_.premium

    @premium.setter
    def premium(self, value:str) -> None:
        _AV_.premium = value


    @property
    def proxy(self) -> dict:
        return _AV_.proxy

    @proxy.setter
    def proxy(self, value:str) -> None:
        _AV_.proxy = value


    # Get only properties
    @property
    def name(self) -> bool:
        return self._df.name
# -*- coding: utf-8 -*-
import pandas as pd
from pandas.core.base import PandasObject


class BasePandasObject(PandasObject):
    """Simple PandasObject Extension

    Ensures the DataFrame is not empty and has columns.

    Args:
        df (pd.DataFrame): Extends Pandas DataFrame
    """
    def __init__(self, df, **kwargs):
        if df.empty: return
        self._df = df

    def __call__(self, kind, *args, **kwargs):
        raise NotImplementedError()
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

        # May implement if needed
        # total_columns = len(df.columns)
        # if total_columns > 0:
        #     # df._total_columns = total_columns
        #     self._df = df
        # else:
        #     raise AttributeError(f"[X] No columns!")

    def __call__(self, kind, *args, **kwargs):
        raise NotImplementedError()
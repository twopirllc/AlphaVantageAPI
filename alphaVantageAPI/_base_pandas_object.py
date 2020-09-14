# -*- coding: utf-8 -*-
from pandas.core.base import PandasObject
from pandas import DataFrame

class BasePandasObject(PandasObject):
    """Simple PandasObject Extension

    Ensures the DataFrame is not empty.

    Args:
        df (pd.DataFrame): Extends Pandas DataFrame
    """
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            if isinstance(args[0], DataFrame):
                df = args[0]
            if df.empty: return
            self._df = df
        return

    def __call__(self, kind, *args, **kwargs):
        raise NotImplementedError()
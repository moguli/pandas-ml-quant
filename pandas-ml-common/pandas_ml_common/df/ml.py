import pandas as pd
import numpy as np

from pandas_ml_common.df.index_utils import multi_index_shape
from pandas_ml_common.df.value_utils import unpack_nested_arrays, get_pandas_object


class ML(object):

    def __init__(self, df: pd.DataFrame):
        self.df = df

    @property
    def values(self):
        # get raw values
        values = unpack_nested_arrays(self.df)

        # return in multi level shape if multi index is used
        if hasattr(self.df, 'columns') and isinstance(self.df.columns, pd.MultiIndex):
            index_shape = multi_index_shape(self.df.columns)
            values = values.reshape((values.shape[0],) + index_shape + values.shape[len(index_shape):])

        return values

    def __getitem__(self, item):
        return get_pandas_object(self.df, item)

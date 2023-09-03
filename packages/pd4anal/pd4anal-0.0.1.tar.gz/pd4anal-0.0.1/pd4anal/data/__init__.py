from .frame import DataFrame
from .series import Series
from .schema import *
import pandas

def to_pa_dataframe_series(func):
    def warpper(*args, **kwargs):
        res = func(*args, **kwargs)
        if isinstance(res, pandas.core.frame.DataFrame):
            return DataFrame(res)
        elif isinstance(res, pandas.core.series.Series):
            return Series(res)
        return res
    return warpper

# 以下代码目的是使得某些操作后的dataframe是pd4anal.data.frame.DataFrame，可使用新增功能
pandas.read_excel = to_pa_dataframe_series(pandas.read_excel)
pandas.read_pickle = to_pa_dataframe_series(pandas.read_pickle)
pandas.read_csv = to_pa_dataframe_series(pandas.read_csv)

pandas.Series = Series
pandas.DataFrame = DataFrame
pandas.core.generic.NDFrame.copy = to_pa_dataframe_series(pandas.core.generic.NDFrame.copy)  # copy
pandas.concat = to_pa_dataframe_series(pandas.concat)  # concat
pandas.merge = to_pa_dataframe_series(pandas.merge)  # merge
pandas.core.frame.DataFrame.fillna = to_pa_dataframe_series(pandas.core.frame.DataFrame.fillna)  # fillna
pandas.core.indexing._LocationIndexer.__getitem__ = to_pa_dataframe_series(pandas.core.indexing._LocationIndexer.__getitem__)  # 切片
pandas.core.frame.DataFrame.drop = to_pa_dataframe_series(pandas.core.frame.DataFrame.drop)  # drop
pandas.core.frame.DataFrame.sample = to_pa_dataframe_series(pandas.core.frame.DataFrame.sample)  # drop

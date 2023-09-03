'''
投顾产品的使用
'''
from .base import DataLoader
import warnings
from ..data import DataFrame, schemacenter
import yaml
import os
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime


class UserInvestProductDataLoader(DataLoader):
    '''投顾产品的使用情况
    '''
    def __init__(self, source_um, pri_key='userid') -> None:
        super().__init__(source_um, pri_key, sheet_name='invest_product')
    
    def gen_sql(self, dt, target_sql, pri_key_list, feature_list):
        '''获取SQL，投顾服务一个客户一天最多使用一次，因此这里统计的是最近一段时间的使用情况
        原表中是明细数据，因此这里是取出来之后再依据excel中维护的字段选取部分列
        '''
        self.filter_featurs(feature_list)

        # 如果是单独的dt，则默认统计过去一个月
        if isinstance(dt, (str, int)):
            dt_start = datetime.strptime(str(dt), '%Y%m%d')-relativedelta(months=1)
            dt_start = int(datetime.strftime(dt_start, '%Y%m%d'))
            dt = [dt_start, dt]
            warnings.warn(f'Args `dt` is str/int formart, and reset to {dt}, you can input dt=[dt_start, dt_end] instead')

        dt_str = self.get_dt_str(dt)

        if pri_key_list:
            SQL_part = f" and {self.pri_key} in ({', '.join(pri_key_list)})"
        else:
            SQL_part = ''

        SQL = f'''select user_id as userid, productname, count(1) as productcount
                                    from {self.table_name} where {dt_str} {SQL_part}
                                    group by user_id, productname
                    '''
        return SQL

    def post_process(self, data):
        '''由于原表是明细数据，因此这里是取出来之后再截断
        '''
        # 先按照产品名称pivot下
        data = data.pivot(self.pri_key, 'productname')['productcount']
        data.reset_index(inplace=True)
        cols = [i for i in data.columns if i != self.pri_key]
        keep_columns = data[cols].sum(axis=0).sort_values(ascending=False).keys()
        data = data[[self.pri_key] + list(keep_columns)]

        return data
        
        # 暂时未根据excel中进行截断，因为会把target_sql中的误删
        sel_feats = [fea.name for fea in self.features.values() if fea.name in data.columns]
        return data[sel_feats]


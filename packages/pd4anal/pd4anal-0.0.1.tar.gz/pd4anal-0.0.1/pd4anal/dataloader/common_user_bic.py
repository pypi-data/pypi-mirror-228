'''
指标体系用户主题，从fact.UI_INDEX_MODULE_COLLECT2中取数
'''
from .base import DataLoader
import warnings
from ..data import DataFrame, schemacenter
import yaml
import os
import pandas as pd


class UserBicLoader(DataLoader):
    '''加载用户bic特征
    '''
    def __init__(self, source_um, pri_key='userid') -> None:
        super().__init__(source_um, pri_key, sheet_name='user_bic')
    
    def gen_sql(self, dt, target_sql, pri_key_list, feature_list):
        '''获取SQL
        主要修改是增加了去除异常用户的逻辑
        '''
        SQL = super().gen_sql(dt, target_sql, pri_key_list, feature_list)
        # 去除大小非non_trade | 仅保留个人客户mis_user_type | 去除客户状态异常cust_status(销户和不合格) | 客户账户类型cust_type
        SQL += ''' and (non_trade is null or non_trade <> '1') and (mis_user_type = '0')
                   and cust_status not in (8,9) and (cust_type between -1 and 4)'''
        return SQL

UserDataLoader = UserBicLoader

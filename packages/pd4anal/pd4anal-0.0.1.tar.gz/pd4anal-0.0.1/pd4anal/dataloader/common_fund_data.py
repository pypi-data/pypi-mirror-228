'''
bic指标系统理财产品主题, 从fact.UI_INDEX_MODULE_COLLECT_KYP_FUND取数
'''
from .base import DataLoader
import warnings
from ..data import DataFrame, schemacenter
import yaml
import os


class FundDataLoader(DataLoader):
    '''加载基金特征
    '''
    def __init__(self, source_um, pri_key='fund_code') -> None:
        super().__init__(source_um, pri_key, sheet_name='fund_data')

'''
用户注册大底表，从view.VIEW_USER_REG_INFO取数
'''
from .base import DataLoader
import warnings
from ..data import DataFrame, schemacenter
import yaml
import os
import pandas as pd


class UserRegInfoLoader(DataLoader):
    '''加载用户注册特征
    '''
    def __init__(self, source_um, pri_key='userid') -> None:
        super().__init__(source_um, pri_key, sheet_name='user_reg_info')

from .base import DataLoader
import warnings
from ..data.frame import DataFrame
import yaml
import os
from .common_user_bic import UserDataLoader
from .common_fund_data import FundDataLoader

class UserFundDataLoader(DataLoader):
    '''加载(用户, 基金)特征
    '''
    def __init__(self, source_um) -> None:
        self.user = UserDataLoader(source_um)
        self.fund = FundDataLoader(source_um)
        self.features = dict(self.user.features, **self.fund.features)  # 合并两者

    def load(self, **params):
        '''
        dt: 获取数据的日期，examples: 20221114, '20221114', [20221113, 20221114]
        target_sql: 取用y的sql, 至少包含两列[user_name, 'dt']
        user_name:
        user_list: user的unoin_id，否则取所有数据耗时太大
        feature_list: 只取其中的部分特征
        fund_code:
        fund_list: user的unoin_id，否则取所有数据耗时太大
        '''
        user_data = self.user.load(params)
        fund_data = self.fund.load(params)
        data = pd.concat([user_data, fund_data], ignore_index=True)
        return DataFrame(data)


if __name__ == '__main__':
    user = UserFundDataLoader()
    user.load(20221011, target_sql='select * from wia_robot.lb_fund_y where dt=20221011')

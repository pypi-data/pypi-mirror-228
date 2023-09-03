from ..models.model_center import modelcenter
from .scene_center import scenecenter


class Scene(object):
    def __init__(self, scene_name):
        '''场景初始化
        '''
        self.scene_name = scene_name
        self.sheets = dict()
        self.current_strategy = 'default'

    def register(self, sheet_name, sheet, strategy_name='default', replace=False, verbose=1, **kwargs):
        '''注册场景同时注册策略，名单是挂在策略上的
        sheet_name: 名单名称，可以是"第几批"等等
        sheet: 注册的名单, pandas的DataFrame格式
        strategy_name：策略名
        '''
        # 记录名单
        if strategy_name not in self.sheets:
            self.sheets[strategy_name] = dict()
        if (not replace) and (sheet_name in self.sheets[strategy_name]):
            raise ValueError(f'[Sheet] `{sheet_name}` is already in {strategy_name} and you can set `replace`=True to force regist')
        self.sheets[strategy_name][sheet_name] = sheet
        self.current_strategy = strategy_name

        # 存档到场景中心
        scenecenter.register(self.scene_name, self, replace, verbose, **kwargs)

    @staticmethod
    def infer(X, model_name=None, scene_name=None, probas=True, **params):
        '''模型预测, 这里注册为静态方法，是为了不用实例化scene也可以调用
        X: 待预测数据集
        model_name: 调用的模型名称
        scene_name：若模型是注册在场景下的，则需要提供场景名
        probas: 是否计算模型的概率
        '''
        # 数据处理流程
        X = modelcenter.fetch(model_name, scene_name, register_model=False).predict(X)
        # 模型获取
        model = modelcenter.fetch(model_name, scene_name)
        # 模型预测
        return model.predict(X, probas=probas, **params)
        
    def sheet_fetch(self, sheet_name=None, strategy_name=None):
        '''名单获取
        '''
        strategy = strategy_name or self.current_strategy
        assert strategy is not None, '`strategy` can not be None'
        if strategy not in self.sheets:
            raise ValueError(f'{strategy} is not in sheets')

        if sheet_name and sheet_name not in self.sheets[strategy]:
            raise ValueError(f'{sheet_name} is not in stragegy {strategy}')
        
        return self.sheets[strategy][sheet_name] if sheet_name else self.sheets[strategy]

    def sheet_drop_duplicate(self, df):
        '''名单去重
        '''
        pass

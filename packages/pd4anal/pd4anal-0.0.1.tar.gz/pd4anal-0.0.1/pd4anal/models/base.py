# from abc import abstractmethod, ABCMeta

# class Model(metaclass=ABCMeta):
#     '''通过接口Interface来实现
#     '''
#     @abstractmethod
#     def fit(self):
#         # 模型训练
#         pass

#     @abstractmethod
#     def predict(self):
#         # 模型预测
#         pass

from .model_center import modelcenter
from ..scene import scenecenter

class Model(object):
    '''模型基类
    主要需要实现fit和predict方法
    '''
    def fit(self):
        # 模型训练
        pass

    def predict(self):
        # 模型预测
        pass

    def register(self, model_name, scene_name=None, replace=False, verbose=1):
        # 模型注册
        modelcenter.register(model_name, self, scene_name, replace, verbose)

    def get_model2scene(self, model_anme):
        # 获取model到scene的映射关系
        return modelcenter.get_model2scene(model_name)

    def set_model2scene(self, model_anme, scene_name):
        # 设置model2scene的对应关系
        return modelcenter.set_model2scene(model_name, scene_name)
    

from ...models.model_center import modelcenter
from ...pipline import Pipeline


class FeatureTransformFlow():
    '''特征处理流，用于记录训练阶段的数据处理过程
    '''
    def __init__(self):
        self.initialize()

    def append(self, val):
        self.pipeline.append(val)

    def initialize(self, name='pa_feature_transform_pipline'):
        '''初始化特征处理流，需要保存训练数据的处理流程时候使用
        '''
        self.pipeline = Pipeline(steps=[], name='pa_feature_transform_pipline')

    def register(self, model_name, scene_name=None, replace=False, verbose=1):
        '''保存特征处理流

        :param model_name: 需要保存的模型对象
        :param scene_name: 场景名称，需要和场景一一绑定时候使用
        :param replace: 默认为False，如果已经存在会报错，则需设置为True才可以保存，防止误操作
        :param verbose: 是否打印
        '''
        modelcenter.register(model_name, self.pipeline, scene_name, replace=replace, register_model=False, verbose=verbose)

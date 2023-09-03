import warnings
import os
import joblib

root_model = './root_model'

class ModelCenter(object):
    def __init__(self) -> None:
        self.model_center = dict()
        self.transform_center = dict()
        self.model2scene = dict()  # 模型支持哪些场景 {model_name: [scene_name1, scene_name2]}
    
    def initialize(self):
        '''模型加载
        '''
        self.model2scene = joblib.load(os.path.join(root_model, 'model2scene.pkl'))

        for root, dirs, files in os.walk(root_model, topdown=False):
            keys = [i for i in root.replace(root_model, '').split('\\') if i]
            for name in files:
                if name == 'model2scene.pkl':
                    continue
                if name == 'model.pkl':
                    center = self.model_center
                elif name == 'transform.pkl':
                    center = self.transform_center
                else:
                    continue
                model = joblib.load(os.path.join(root, name))
                if len(keys) == 1:
                    center[keys[0]] = model
                elif len(keys) == 2:
                    center[keys[0]] = {keys[1]: model}
        print(f'[ModelCenter] Initialize {len(self.model_center)} models successfully')
    
    def dump(self, model_path, model, save_name):
        '''保存模型
        '''
        model_path = os.path.join(root_model, model_path)
        os.makedirs(model_path, exist_ok=True)
        joblib.dump(model, os.path.join(model_path, save_name))

    def get_model2scene(self, model_name=None):
        '''获取model_name适用于哪些scene
        '''
        if model_name is None:
            return self.model2scene
        else:
            return self.model2scene.get(model_name, None)
    
    def set_model2scene(self, model_name, scene_name):
        '''设置model_name适配的scene_name
        '''
        if isinstance(scene_name, str):
            scene_name = [scene_name]
        self.model2scene = scene_name + self.model2scene.get(model_name, [])

    def register(self, model_name, model, scene_name=None, replace=False, verbose=0, register_model=True):
        '''模型注册, 以model_name注册，或者以scene_name/model_name注册
        model_name: 注册的模型名
        model: 注册的模型
        scene_name：是否把模型注册到场景之下
        replace: 强制覆盖注册
        verbose：是否打印
        register_model：注册model还是transform，默认注册model
        '''
        if register_model:
            # 注册模型
            center = self.model_center
            prefix = '[Model]'
            save_name = 'model.pkl'
        else:
            # 注册数据处理
            center = self.transform_center
            prefix = '[Transform]'
            save_name = 'transform.pkl'

        if scene_name is None:
            # 注册通用模型
            if (not replace) and (model_name in center):
                raise ValueError(f'{prefix} `{model_name}` is already in model center and you can set `replace`=True to force regist')
            center[model_name] = model  # 维护模型
            self.dump(model_name, model, save_name)
        else:
            # 注册场景下模型
            if (not replace) and (scene_name in center):
                raise ValueError(f'[Scene] `{scene_name}` is already in model center and you can set `replace`=True to force regist')
            if (not replace) and (model_name in center.get(scene_name, {})):
                raise ValueError(f'[Scene]/{prefix} `{scene_name}/{model_name}` is already in model center and you can set `replace`=True to force regist')
            center[scene_name] = dict()
            center[scene_name][model_name] = model  # 维护模型
            self.dump(f'{scene_name}/{model_name}', model, save_name)
            self.model2scene[model_name] = [scene_name] + self.model2scene.get(model_name, [])  # 维护model2scene
            self.dump('', self.model2scene, 'model2scene.pkl')

        if verbose != 0:
            scene_str = '' if scene_name is None else f'{scene_name}/'
            print(f'{prefix} `{scene_str}{model_name}` registed success')

        return model
    
    def fetch(self, model_name, scene_name=None, register_model=True):
        '''获取模型
        '''
        center = self.model_center if register_model else self.transform_center
        if scene_name is None:
            if model_name not in center:
                raise ValueError(f'{model_name} is not in model center')
            return center[model_name]
        else:
            if scene_name not in center:
                raise ValueError(f'{scene_name} is not in model center')
            if model_name not in center[scene_name]:
                raise ValueError(f'{model_name} is not in model center scene {scene_name}')
            return center[scene_name][model_name]
    
    def drop(self, model_name):
        '''删除模型
        '''
        if model_name not in self.model_center:
            raise ValueError(f'{model_name} is not in model center')
        self.model_center.drop(model_name)

modelcenter = ModelCenter()

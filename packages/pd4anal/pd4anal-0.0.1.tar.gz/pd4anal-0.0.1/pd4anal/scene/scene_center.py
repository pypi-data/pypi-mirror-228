import os
import pandas as pd

root_scene = './root_scene'


def get_kw(f, kwargs):
    from inspect import signature
    sig = signature(f)
    sns_args = {}
    for k, v in kwargs.items():
        if k in sig.parameters.keys():
            sns_args[k] = v
    return sns_args

class SceneCenter(object):
    def __init__(self):
        self.scene_center = dict()
   
    def initialize(self):
        '''场景中心加载
        '''
        for root, dirs, files in os.walk(root_scene, topdown=False):
            keys = [i for i in root.replace(root_scene, '').split('\\') if i]
            if len(keys) != 2:
                continue
            for name in files:
                sheet_path = os.path.join(root, name)
                if sheet_path.endswith('.xlsx') or sheet_path.endswith('.xls'):
                    sheet = pd.read_excel(sheet_path)
                elif sheet_path.endswith('.csv') or sheet_path.endswith('.txt'):
                    sheet = pd.read_csv(sheet_path)
                else:
                    raise ValueError('Sheet saved file only suppprt (`xlsx`, `xls`, `csv`, `txt`) format')

                self.scene_center[keys[0]] = {keys[1]: sheet}
        print(f'[SceneCenter] Initialize {len(self.scene_center)} scenes successfully')
    
    def dump(self, scene_path, scene, **kwargs):
        '''保存某个场景
        '''
        scene_path = os.path.join(root_scene, scene_path)
        os.makedirs(scene_path, exist_ok=True)

        # 保存各个名单
        for strategy, sheets in scene.sheets.items():
            strategy_path = os.path.join(scene_path, strategy)
            os.makedirs(strategy_path, exist_ok=True)
            for sheet_name, sheet in sheets.items():
                sheet_path = os.path.join(strategy_path, sheet_name)
                if sheet_path.endswith('.xlsx') or sheet_path.endswith('.xls'):
                    sheet.to_excel(sheet_path, encoding='utf-8', index=False)
                elif sheet_path.endswith('.csv') or sheet_path.endswith('.txt'):
                    sheet.to_csv(sheet_path, encoding='utf-8', index=False)
                else:
                    sheet.to_csv(sheet_path+'.csv', encoding='utf-8', index=False)

    def get_scene2model(self, scene_name=None):
        '''获取scene适用于哪些model
        '''
        scene2model = dict()
        from ..models.model_center import modelcenter
        model2scene = modelcenter.get_model2scene()
        for model_name, scene_names in model2scene.items():
            for scene_name in scene_names:
                scene2model[scene_name] = scene2model.get(scene_name, []) + [model_name]

        if scene_name is None:
            return scene2model
        else:
            return scene2model.get(scene_name, None)

    def register(self, scene_name, scene, replace=False, verbose=0, **kwargs):
        '''场景注册，结构是保存下来，但是无存储操作
        '''
        if (not replace) and (scene_name in self.scene_center):
            raise ValueError(f'[Scene] `{scene_name}` is already in scene center and you can set `replace`=True to force regist')
        self.scene_center[scene_name] = scene
        
        # 存档
        self.dump(scene_name, scene, **kwargs)

        if verbose != 0:
            print(f'[Scene] `{scene_name}` registed success')
        return scene

    def fetch(self, scene_name):
        '''获取场景
        '''
        if scene_name not in self.scene_center:
            raise ValueError(f'[Scene] `{scene_name}`` is not in scene center')
        return self.scene_center[scene_name]
    
    def drop(self, scene_name):
        '''删除场景
        '''
        if scene_name not in self.scene_center:
            raise ValueError(f'[Scene] `{scene_name}`` is not in scene center')
        self.scene_center.drop(scene_name)

scenecenter = SceneCenter()


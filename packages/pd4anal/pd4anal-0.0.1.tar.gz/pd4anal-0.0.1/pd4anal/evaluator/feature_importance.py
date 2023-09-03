import warnings
import numpy as np
from collections import OrderedDict
import pandas as pd
import json
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
import copy


def get_importance(fea_cols, importances, use_abs=True):
    '''得到排序后的特征重要性字典
    '''
    if use_abs:
        fea_importance = [(i, abs(v)) for i, v in zip(fea_cols, importances)]
    fea_importance = [(i, np.float64(v)) for i, v in fea_importance]
    fea_importance = OrderedDict(sorted(fea_importance, key=lambda x: x[1], reverse=True))
    return fea_importance

def get_importances(fea_importances, cal_index, save_path='', title='Feature Importance'):
    '''汇总多折的特征重要性，输出最终特征重要性，保存特征重要性的排序图
    '''
    # 最终指标根据每个fold的指标汇总得到
    fea_importances_average = dict()
    for fea_importance in fea_importances:
        for fea, value in fea_importance.items():
            fea_importances_average[fea] = fea_importances_average.get(fea, 0) + value

    fea_importances_average = [(k, np.float64(v)) for k, v in fea_importances_average.items()]
    fea_importances_average = OrderedDict(sorted(fea_importances_average, key=lambda x: x[1], reverse=True))

    # 保存图片
    if save_path:
        df = pd.Series(fea_importances_average).to_frame().reset_index()
        df.columns = ['feature', cal_index]
        df = df.sort_values(cal_index)
        
        plt.figure(figsize=(8,int(df.shape[0]/3)))
        plt.barh(np.arange(len(df[cal_index])), df[cal_index])
        plt.yticks(np.arange(len(df[cal_index])), df.feature.values)
        plt.title(title,size=16)
        plt.ylim((-1,len(df[cal_index])))
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
    

class TreeFeatureImportance(object):
    def __init__(self, name='tree_feature_importance', save_path='', model_index=0):
        self.name = name
        self.feature_importance = []
        self.save_path = save_path
        self.model_index = model_index

    def fit(self, df_X, df_y=None, **tracker):
        if 'model' not in tracker:
            raise ValueError("TreeFeatureImportance request model is not None")
        for model in tracker['model']:
            fea_imp = get_importance(df_X.columns, model.feature_importances_)
            self.feature_importance.append(fea_imp)
        
        if self.save_path:
            # 保存文件
            save_dir = '/'.join(self.save_path.split('/')[:-1])
            save_file = self.save_path.split('/')[-1].split('.')[0]
            os.makedirs(save_dir, exist_ok=True)
            with open(os.path.join(save_dir, save_file+'.json'), 'w', encoding='utf-8') as f:
                json.dump(self.feature_importance, f, indent=4)
            get_importances(self.feature_importance, cal_index='tree_feature_importance', save_path=self.save_path+'.jpg', title=self.name)
        return df_X, df_y, tracker


class LrFeatureImportance(object):
    def __init__(self, name='lr_feature_importance'):
        self.name = name
        self.feature_importance = []

    def fit(self, df_X, df_y, **tracker):
        if 'model' not in tracker:
            raise ValueError("lr_feature_importance request model is not None")
        for model in tracker['model']:
            fea_imp = get_importance(df_X.columns, model.coef_[0])
            self.feature_importance.append(fea_imp)
        return df_X, df_y, tracker


class ShuffleFeatureImportance(object):
    def __init__(self, task, monitor, monitor_args={}, name='shuffle_feature_importance', batch_size=1, shuffle_count=1, model_index=0):
        self.name = name
        self.feature_importance = []
        self.model_index = model_index
        self.shuffle_count = shuffle_count
        self.batch_size = batch_size
        assert task in {'binary_classification', 'multi_classification', 'binary_classification_byuser', 'regression'}
        self.task = task
        assert monitor in {'f1', 'auc', 'gauc', 'mae', 'mse', 'custom'}
        self.monitor = monitor
        self.monitor_args = monitor_args

    def fit(self, df_X, df_y, **tracker):
        import torch
        from torch.utils.data import DataLoader, TensorDataset
        from .performance import MONITOR_MAP

        if 'model' not in tracker:
            raise ValueError(f'Shap calculation need model args in tracker')

        if 'kfold' not in tracker:
            warnings.warn('Use all data to calculate feature importance')
            X_valid = df_X.values
            y_valid = df_y.values
        else:
            valid_index = tracker['kfold'][self.model_index][1] if isinstance(tracker['kfold'][self.model_index], (tuple, list)) else tracker['kfold'][1]
            X_valid = df_X.values[valid_index]
            y_valid = df_y.values[valid_index]

        model = tracker['model'][self.model_index] if isinstance(tracker['model'], (tuple, list)) else tracker['model']
        fea_cols = df_X.columns
        X_valid = torch.tensor(X_valid, dtype=torch.float, device=model.device)
        y_valid = torch.tensor(y_valid, dtype=torch.long, device=model.device)
        valid_dataloader = DataLoader(TensorDataset(X_valid, y_valid), batch_size=self.batch_size)

        model.eval()
        preds = {}
        with torch.no_grad():
            for batch in tqdm(valid_dataloader, desc='evaluate'):
                X_valid, y_valid = batch[0].to(model.device), batch[1]
                oof_preds = model(X_valid)
                
                for _ in range(self.shuffle_count):
                    preds['y'] = preds.get('y', []) + [y_valid.cpu().numpy()]
                    preds['BASELINE'] = preds.get('BASELINE', []) + self.get_pred(oof_preds)

                    if fea_cols is None:
                        fea_cols = [i for i in range(X_valid.shape[1])]

                    for k in range(len(fea_cols)):
                        # SHUFFLE FEATURE K
                        save_col = copy.deepcopy(X_valid[:,k])
                        np.random.shuffle(X_valid[:,k])

                        # COMPUTE OOF MAE WITH FEATURE K SHUFFLED
                        oof_preds = model(X_valid)
                        preds[fea_cols[k]] = preds.get(fea_cols[k],[]) + self.get_pred(oof_preds)
                        X_valid[:,k] = save_col  # 恢复该结果
        
        # 合并多次计算的结果
        df_preds = pd.DataFrame()
        for k, v in preds.items():
            df_preds[k] = np.concatenate(v)

        results = {}
        for col in df_preds.columns:
            if col == 'y':
                continue
            results[col] = MONITOR_MAP[self.monitor](df_preds['y'], df_preds[col], **self.monitor_args.get(self.monitor, {}))
            if self.monitor in {'f1', 'auc', 'gauc'}:
                results[col] = 1 - results[col]

        # DISPLAY FEATURE IMPORTANCE
        self.fea_importance = get_importance(results.keys(), results.values())
        return df_X, df_y, tracker

    # 指标方式
    def get_pred(self, oof_preds):
        if self.monitor == 'f1':
            return oof_preds.argmax(dim=-1).cpu().numpy()
        elif self.monitor in {'auc', 'gauc'}:
            if self.task == 'binary_classification':
                return 1/(1 + np.exp(-oof_preds.cpu().numpy()))
            else:
                return [oof_preds[:, 1].cpu().numpy()]
        elif self.monitor == 'mae':
            return oof_preds.cpu().numpy()


class TreeShapFeatureImportance(object):
    def __init__(self, task='binary_classification', save_path=None, 
                 name='tree_shap_feature_importance', model_index=0):
        '''树模型的shap重要性计算, 多个模型的仅计算其中model_index这一个
        '''
        self.name = name
        self.feature_importance = []
        if save_path is not None:
            save_dir = '/'.join(save_path.split('/')[:-1])
            os.makedirs(save_dir, exist_ok=True)
            save_file = save_path.split('/')[-1].split('.')[0]
            self.save_path = os.path.join(save_dir, save_file+'.pdf')
        else:
            self.save_path = save_path
        assert task in {'binary_classification', 'multi_classification', 'binary_classification_byuser', 'regression'}
        self.task = task
        self.model_index = model_index

    def fit(self, df_X, df_y, **tracker):
        '''tracker: {'model': ..., 'kfold': ...}
        '''
        import shap
        from matplotlib.backends.backend_pdf import PdfPages
        
        if 'model' not in tracker:
            raise ValueError(f'Shap calculation need model args in tracker')

        if 'kfold' not in tracker:
            warnings.warn('Use all data to calculate feature importance')
            X_valid = df_X.values
        else:
            valid_index = tracker['kfold'][self.model_index][1] if isinstance(tracker['kfold'][self.model_index], (tuple, list)) else tracker['kfold'][1]
            X_valid = df_X.values[valid_index]
        
        if self.save_path:
            pdf = PdfPages(self.save_path)
        model = tracker['model'][self.model_index] if isinstance(tracker['model'], (tuple, list)) else tracker['model']
        fea_cols = df_X.columns

        if self.task == 'multi_classification':
            shap_values = shap.Explainer(model).shap_values(X_valid)
            fig = plt.figure()
            if 'y_map' in tracker:
                shap.summary_plot(shap_values, feature_names= fea_cols, plot_type='bar', show=False, class_names=list(tracker['y_map'].keys()))
            else:
                shap.summary_plot(shap_values, feature_names= fea_cols, plot_type='bar', show=False)
            plt.title(f'shap fea_importance')
            plt.tight_layout()
            if self.save_path:
                pdf.savefig(fig)
            plt.close()

            # importance  尚未测试
            self.feature_importance.append(get_importance(df_X.columns, shap_values.abs.mean(0).values))
        elif self.task == 'binary_classification':
            explainer = shap.Explainer(model, feature_names=fea_cols)
            shap_values = explainer(X_valid)
            # bar图
            fig = plt.figure()
            shap.plots.bar(shap_values, show=False)
            plt.title(f'shap fea_importance')
            plt.tight_layout()
            if self.save_path:
                pdf.savefig(fig)
            plt.close()

            # importance
            self.feature_importance.append(get_importance(df_X.columns, shap_values.abs.mean(0).values))

            # beewarm图
            fig = plt.figure()
            shap.plots.beeswarm(shap_values, show=False)
            plt.title(f'beeswarm')
            plt.tight_layout()
            if self.save_path:
                pdf.savefig(fig)
            plt.close()

        # # 目前只有二分类才绘制，scatter图（仅保留top的几个特征, 仅取一个fold否则太多）
        # for j, (k, v) in enumerate(fea_importance.items()):
        #     shap.plots.scatter(shap_values[:, k], color=shap_values, show=False)
        #     plt.title(f'scatter fea={k} value={v:.2f}')
        #     plt.tight_layout()
        #     pdf.savefig()
        #     plt.close()
        #     if j >= 10:
        #         break
        if self.save_path:
            pdf.close()
        return df_X, df_y, tracker


class DeepShapFeatureImportance(object):
    def __init__(self, task, save_path, name='deep_shap_feature_importance', model_index=0):
        self.name = name
        self.feature_importance = []
        save_dir = '/'.join(save_path.split('/')[:-1])
        save_file = save_path.split('/')[-1].split('.')[0]
        self.save_path = os.path.join(save_dir, save_file+'.pdf')
        self.task = task
        self.model_index = model_index

    def fit(self, df_X, df_y, **tracker):
        '''绘制shap图
        '''
        import shap
        from shap._explanation import Explanation
        from matplotlib.backends.backend_pdf import PdfPages       
        
        if 'model' not in tracker:
            raise ValueError(f'Shap calculation need model args in tracker')

        if 'kfold' not in tracker:
            warnings.warn('Use all data to calculate feature importance')
            train_index = tracker['kfold'][self.model_index][0] if isinstance(tracker['kfold'][self.model_index], (tuple, list)) else tracker['kfold'][0]
            X_train = df_X.values[train_index]
            X_valid = df_X.values
        else:
            train_index = tracker['kfold'][self.model_index][0] if isinstance(tracker['kfold'][self.model_index], (tuple, list)) else tracker['kfold'][0]
            X_train = df_X.values[train_index]
            valid_index = tracker['kfold'][self.model_index][1] if isinstance(tracker['kfold'][self.model_index], (tuple, list)) else tracker['kfold'][1]
            X_valid = df_X.values[valid_index]
        
        pdf = PdfPages(self.save_path)
        model = tracker['model'][self.model_index] if isinstance(tracker['model'], (tuple, list)) else tracker['model']
        fea_cols = df_X.columns
        train_index = tracker['kfold'][self.model_index][0] if isinstance(tracker['kfold'][self.model_index], (tuple, list)) else tracker['kfold'][0]
        X_train = df_X.values[train_index]
        valid_index = tracker['kfold'][self.model_index][1] if isinstance(tracker['kfold'][self.model_index], (tuple, list)) else tracker['kfold'][1]
        X_valid = df_X.values[valid_index]

        # 从train中抽样用于计算期望值
        e = shap.DeepExplainer(model, X_train)
        
        # 从dev中抽样用于计算shap值            
        shap_values = e.shap_values(X_valid)
        if self.task == 'binary_classification':
            shap_values = shap_values[1]
        elif self.task == 'regression':
            pass

        shap_v = Explanation(values=shap_values, data=X_valid.numpy(), base_values=e.expected_value[-1], feature_names=fea_cols)
        
        # bar图
        fig = plt.figure()
        shap.plots.bar(shap_v, show=False)
        plt.title(f'shap fea_importance')
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()
        
        # beewarm图
        fig = plt.figure()
        shap.plots.beeswarm(shap_v, show=False)
        plt.title(f'shap beeswarm')
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()

        # # 目前只有二分类才绘制，scatter图（仅保留top的几个特征, 仅取一个fold否则太多）
        # for j, (k, v) in enumerate(fea_importance.items()):
        #     shap.plots.scatter(shap_values[:, k], color=shap_values, show=False)
        #     plt.title(f'scatter fea={k} value={v:.2f}')
        #     plt.tight_layout()
        #     pdf.savefig()
        #     plt.close()
        #     if j >= 10:
        #         break
        pdf.close()
        return df_X, df_y, tracker

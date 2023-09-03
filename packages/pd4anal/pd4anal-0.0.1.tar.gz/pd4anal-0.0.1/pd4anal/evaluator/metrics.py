from collections import defaultdict
from sklearn.metrics import f1_score, roc_auc_score, mean_squared_error, mean_absolute_error
import numpy as np
import os
import json


def safe_calculate(func, *args, default_value=0, **kwargs):
    '''安全计算指标值，防止报错
    '''
    def new_func(*args, **kwargs):
        try:
            index = func(*args, **kwargs)
        except Exception as e:
            print('[Error message]: ', e)
            index = default_value
        return index
    return new_func


@safe_calculate
def eval_cal_group_auc(labels, preds, user_id_list):
    """Calculate group auc"""
    if len(user_id_list) != len(labels):
        raise ValueError(
            "impression id num should equal to the sample num," \
            "impression id num is {0}".format(len(user_id_list)))
    group_score = defaultdict(lambda: [])
    group_truth = defaultdict(lambda: [])
    for idx, truth in enumerate(labels):
        user_id = user_id_list[idx]
        score = preds[idx]
        truth = labels[idx]
        group_score[user_id].append(score)
        group_truth[user_id].append(truth)

    group_flag = defaultdict(lambda: False)
    for user_id in set(user_id_list):
        truths = group_truth[user_id]
        flag = False
        for i in range(len(truths) - 1):
            if truths[i] != truths[i + 1]:
                flag = True
                break
        group_flag[user_id] = flag

    impression_total = 0
    total_auc, eps = 0, 1e-7
    
    for user_id in group_flag:
        if group_flag[user_id]:
            auc = roc_auc_score(np.asarray(group_truth[user_id]), np.asarray(group_score[user_id]))
            total_auc += auc * len(group_truth[user_id])
            impression_total += len(group_truth[user_id])
    group_auc = float(total_auc) / (impression_total + eps)
    group_auc = round(group_auc, 4)
    return group_auc


@safe_calculate
def eval_f1_score(y_true, y_prob, **kwargs):
    return f1_score(y_true, y_prob.argmax(), **kwargs)


@safe_calculate
def eval_roc_auc_score(y_true, y_prob, sel_col=1, **kwargs):
    '''计算auc
    如果y_prob是含多列，则仅取其中的sel_col列来计算
    '''
    if len(y_prob.shape) > 1:
        return roc_auc_score(y_true, y_prob[:, sel_col], **kwargs)
    else:
        return roc_auc_score(y_true, y_prob, **kwargs)


@safe_calculate
def eval_mean_squared_error(y_true, y_prob, **kwargs):
    return mean_squared_error(y_true, y_prob, **kwargs)


@safe_calculate
def eval_mean_absolute_error(y_true, y_prob, **kwargs):
    return mean_absolute_error(y_true, y_prob, **kwargs)

MONITOR_MAP = {
    'auc': eval_roc_auc_score,
    'gauc': eval_cal_group_auc,
    'f1': eval_f1_score,
    'mse': eval_mean_squared_error,
    'mae': eval_mean_absolute_error
}


class Performance(object):
    def __init__(self, monitor, name='performance', monitor_args={}, save_path=''):
        self.name = name
        assert isinstance(monitor, (str, list)), f'monitor args {monitor} not supported'
        self.monitor = [monitor] if isinstance(monitor, str) else monitor
        self.monitor_args = monitor_args
        self.performance = dict()
        self.save_path = save_path

    def fit(self, df_X, df_y, **tracker):
        if 'y_valid_prob' not in tracker:
            return df_X, df_y, tracker

        self.performance['performance'] = dict()
        for moni in self.monitor:
            for y_valid, y_prob in tracker['y_valid_prob']:
                perf = MONITOR_MAP[moni](y_valid, y_prob, **self.monitor_args.get(moni, {}))
                self.performance['performance'][moni] = self.performance.get(moni, []) + [perf]
            self.performance['performance'][moni+'_average'] = np.average(self.performance['performance'][moni])   

        if self.save_path:
            # 保存文件
            save_dir = '/'.join(self.save_path.split('/')[:-1])
            save_file = self.save_path.split('/')[-1].split('.')[0]
            os.makedirs(save_dir, exist_ok=True)
            with open(os.path.join(save_dir, save_file+'.json'), 'w', encoding='utf-8') as f:
                json.dump(self.performance['performance'], f, indent=4)

        tracker['performance'] = self.performance['performance']
        return df_X, df_y, tracker

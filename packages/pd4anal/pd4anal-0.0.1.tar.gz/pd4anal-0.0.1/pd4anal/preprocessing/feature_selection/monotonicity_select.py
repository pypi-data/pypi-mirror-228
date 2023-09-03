import pandas as pd
import numpy as np
from collections import OrderedDict
import warnings
import os
import json
import traceback
from tqdm import tqdm
from pd4anal.utils import is_dtype_numberic


class MonotonicityFeatureSelect(object):
    '''计算不同区间的人数占比，找出单调性较高的特征（潜在有业务价值的特征）
    :param sparse_list
    :param dense_list
    :param bin_count
    :param topk
    :param bins
    :param bin_cutmode
    :param dense_fill
    :param save_path: json文件保存地址
    :param patience
    :param up_down_threshold: 上涨和下跌的幅度
    '''
    def __init__(self, name='monotonicity_feature_select', sparse_list=[], dense_list=[], bin_count=10, up_down_threshold=0.2,
                 topk=1000, bins=None, bin_cutmode='qcut', dense_fill='default', save_path=None, patience=1, **kwargs):
        super().__init__()
        self.name = name
        self.bin_count = bin_count
        self.sparse_list = sparse_list
        self.dense_list = dense_list
        self.pipeline_return = False
        self.topk = topk
        self.bins = bins or {}
        self.bin_cutmode = bin_cutmode
        self.dense_fill = dense_fill
        self.save_path = save_path
        self.patience = patience
        self.up_down_threshold = up_down_threshold

    def fit(self, df_X, df_y, **tracker):
        df = df_X.copy()
        if df_y is not None:
            tgt_name = df_y.name
            df[tgt_name] = df_y
            df[tgt_name] = df[tgt_name].astype(float)
            assert df[tgt_name].nunique() >= 2, f'{tgt_name} class num not >=2'
        else:
            tgt_name = None

        if self.save_path is not None:
            # 创建文件夹
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            # 从本地文件恢复
            if os.path.exists(self.save_path):
                print(f'[INFO] resume monotonicity json data from local cached file: {self.save_path}')
                with open(self.save_path, 'r', encoding='utf-8') as f:
                    return json.load(f)

        self.sparse_list += [i for i in tracker.get('sparse_list', []) if i not in self.sparse_list]
        self.dense_list += [i for i in tracker.get('dense_list', []) if i not in self.dense_list]

        # 如果均为空，则默认使用df_X的字段类型来判断
        if len(self.sparse_list) + len(self.dense_list) == 0:
            self.dense_list = [col for col in df_X.columns if is_dtype_numberic(df_X[col])]
            self.sparse_list = [col for col in df_X.columns if col not in self.dense_list]

        # ================计算单调性================
        monotonicity_importance= []
        for fea in tqdm(self.dense_list, desc='Calculating'):
            try:
                __fea = '__' + fea
                # 自定义切分，适用于有业务含义时候，如aum以1万，5万，20万等作为分割点
                if (self.bins is not None) and (fea in self.bins):
                    # 如果有指定bins则使用cut, 此时格式为[-np.inf, 0, 10000, 10000, np.inf]
                    assert len(self.bins[fea]) > 1, f'Args `bins` {fea} only support >1 split points'
                    df[__fea] = pd.cut(df[fea], self.bins[fea], duplicates='drop', retbins=True, include_lowest=True)[0]
                # 等距切分
                elif self.bin_cutmode == 'cut':
                    # 这里默认的cut会导致边界没有含义，因此这里是自己切分
                    min_, max_ = df[fea].min(), df[fea].max()
                    start, bins = min_, [min_-self.eps]
                    while True:
                        start = start + (max_-min_)/self.bin_count
                        if start >= max_-self.eps:
                            break
                        bins.append(start)
                    bins.append(max_+self.eps)
                    df[__fea] = pd.cut(df[fea], bins, duplicates='drop', retbins=True, include_lowest=True)[0]
                # 等量切分
                elif self.bin_cutmode == 'qcut':
                    # df[__fea] = pd.qcut(df[fea], q=bin_count, duplicates='drop', labels=False)
                    df[__fea] = pd.qcut(df[fea], q=self.bin_count, duplicates='drop', retbins=True)[0]
                else:
                    raise ValueError('Args `bins` and `bin_cunmode` is illegal')

                # =========================评估切分后的单调情况=========================
                df_plt = df.groupby([__fea, tgt_name])[tgt_name].count().unstack()
                df_plt = (df_plt[df_plt.columns[1]] / (df_plt.sum(axis=1) + 1e-5))  # pos占比，可用于判断单调性
                diff = df_plt.diff()

                if len(df_plt) <= 2:  # 如果只有两个，则单调无意义
                    continue
                
                # 满足patience要求，即要么基本上单调增，要么基本上单调减
                if len(df_plt) <= 3:  # 只有三个分区，要求完全单调
                    patience = 0
                elif self.patience < 1:
                    patience = int(self.patience * len(diff))
                else:
                    patience = self.patience
                # 不服从单调的容忍程度，能容忍几个值不服从单调
                if min((diff >= 0).sum(), (diff <= 0).sum()) > patience:
                    continue
                # 如果上涨的比例和下降的比例太相近，即使其满足patience要求，也需要丢弃
                up_down_rate = (abs(diff.loc[diff<=0].sum()), diff.loc[diff>=0].sum())
                if min(up_down_rate) / (max(up_down_rate) + 1e-4) <= self.up_down_threshold:
                    monotonicity_importance.append((fea, diff.sum()))
            except:
                print(traceback.format_exc())

        monotonicity_importance = OrderedDict(sorted(monotonicity_importance, key=lambda x: abs(x[1]), reverse=True)[:self.topk])
        # 保存文件到本地
        if self.save_path is not None:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(monotonicity_importance, f, indent=4, ensure_ascii=False)
            print(f'[INFO] save monotonicity json data to local cached file: {self.save_path}')

        if self.pipeline_return:
            return df_X, df_y, tracker
        else:
            return monotonicity_importance

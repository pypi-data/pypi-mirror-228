from datetime import datetime

class Pipeline(object):
    def __init__(self, steps=[], name='pipeline', verbose=0):
        self.steps = steps
        self.name = name
    
    def __str__(self):
        str_ = 'Pipeline name=`' + self.name + '`\'s steps is \n'
        str_ += '\n'.join([f'{i}. {step.name}' for i, step in enumerate(self.steps, start=1)])
        return str_

    def __repr__(self):
        str_ = 'Pipeline name=`' + self.name + '`\'s steps is \n'
        str_ += '\n'.join([f'{i}. {step.name}' for i, step in enumerate(self.steps, start=1)])
        return str_
        
    def load(self, load_path):
        # 加载定义好的pipline
        pass
    
    def save(self, save_path):
        # 保存定义好的pipline
        pass

    def append(self, transformer):
        self.steps.append(transformer)

    def fit(self, X, y=None, **tracker):
        '''模型训练, 仅允许嵌套两层
        '''
        for transformer in self.steps:
            time_start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if (verbose != 0) and isinstance(transformer, Pipeline):
                print(f'{time_start} - ' + f'Processing pipeline {transformer.name}'.center(80, '-'))
            elif verbose != 0:
                print(f'{time_start} - Processing {transformer.name}')
            
            # 如果存在pipline_return，则置为True
            if hasattr(transformer, 'pipeline_return'):
                self.pipeline_return = True
            X, y, tracker = transformer.fit(X, y, **tracker)
            # self.steps[step_idx] = (name, fitted_transformer)
        return X, y, tracker

    def predict(self, X):
        '''模型预测
        '''
        for transformer in self.steps:
            X = transformer.predict(X)
        return X

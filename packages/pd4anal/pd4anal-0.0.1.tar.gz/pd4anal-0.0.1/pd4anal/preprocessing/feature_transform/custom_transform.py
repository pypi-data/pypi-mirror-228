import types
from functools import wraps

def custom_transform(params={}):
    class CustomTranform:
        def __init__(self, func):
            wraps(func)(self)
            self.name = params.get('name', 'custom_transform')
            self.params = params
            for k, v in params.items():
                exec(f'self.{k} = {v}')

        def __getitem__(self, param):
            if hasattr(self, param):
                return eval(f'self.{param}')
            raise ValueError(f'{param} not exists')

        def __call__(self, *args, **kwargs):
            return self.__wrapped__(*args, **kwargs)
    
        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                return types.MethodType(self, instance)

        def fit(self, *args, **kwargs):
            return [self.__call__(*args, **kwargs)]
        
        def predict(self, *args, **kwargs):
            return self.__call__(*args, **kwargs)
    return CustomTranform

# class CustomTranform:
#     def __init__(self, func, name='custom_transform', inplace=False, **params):
#         self.func = self.decorate(func)
#         self.name = name
#         self.inplace = inplace
#         self.params = params

#     def fit(self,X, y=None, **tracker):
#         df = X if self.inplace else X.copy()
#         return [self.func(df)]
    
#     def predict(self, X):
#         return self.func(X)
    
#     def decorate(self, wrapped):
#         def wrapper(*args, **kwargs):
#             params = self.params
#             res = wrapped(*args, **kwargs)
#             return res
#         return wrapper

class CustomTranform:
    def __init__(self, func, name='custom_transform', inplace=False, **params):
        self.func = func
        self.name = name
        self.inplace = inplace
        self.params = params

    def fit(self,X, y=None, **tracker):
        df = X if self.inplace else X.copy()
        return [self.func(df)]
    
    def predict(self, X):
        return self.func(X)
    
    # def decorate(self, wrapped):
    #     def wrapper(*args, **kwargs):
    #         params = self.params
    #         res = wrapped(*args, **kwargs)
    #         return res
    #     return wrapper

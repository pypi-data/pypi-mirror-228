class TransformCenter(object):
    def __init__(self) -> None:
        self.transform_center = {}

    def load(self, path):
        '''特征转化中心加载
        '''
        pass

    def register(self, transform_name, transform):
        '''特征转化注册
        '''
        if transform_name in self.transform_center:
            raise ValueError(f'{transform_name} is already in transform center')
        self.transform_center[transform_name] = transform
        return transform
    
    def fetch(self, transform_name):
        '''获取特征转化
        '''
        if transform_name not in self.transform_center:
            raise ValueError(f'{transform_name} is not in transform center')
        return self.transform_center[transform_name]
    
    def drop(self, transform_name):
        '''删除特征转化
        '''
        if transform_name not in self.transform_center:
            raise ValueError(f'{transform_name} is not in transform center')
        self.transform_center.drop(transform_name)

transform_center = TransformCenter()


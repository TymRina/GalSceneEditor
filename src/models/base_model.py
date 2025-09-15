"""模型基类

为所有模型提供基础功能
"""
from datetime import datetime


class BaseModel:
    """模型基类，提供所有模型共用的基础功能"""
    
    def __init__(self):
        """初始化基础模型"""
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
    
    @property
    def created_at(self):
        """获取创建时间"""
        return self._created_at
    
    @property
    def updated_at(self):
        """获取最后更新时间"""
        return self._updated_at
    
    def update(self):
        """更新模型，记录更新时间"""
        self._updated_at = datetime.now()
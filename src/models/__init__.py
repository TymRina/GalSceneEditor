"""模型包

包含所有数据模型
"""
from .base_model import BaseModel
from .scene.scene_model import SceneModel
from .resource.resource_model import ResourceModel

__all__ = ['BaseModel', 'SceneModel', 'ResourceModel']
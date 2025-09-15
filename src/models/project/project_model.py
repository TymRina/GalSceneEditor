"""
项目模型

负责管理应用程序的项目数据
"""
from pathlib import Path
from models.base_model import BaseModel
from utils.helpers.logger import log_error, log_info


class ProjectModel(BaseModel):
    """项目模型，负责管理应用程序的项目数据"""
    
    def __init__(self, config=None):
        """初始化项目模型
        
        Args:
            config: 应用程序配置
        """
        super().__init__()
        self.config = config or {}
        
        # 从配置中获取应用程序根目录
        self.app_root = self.config.get('app_root')
        
        # 初始化项目数据
        self.project_data = {}
        self.current_project = None
        
        log_info("项目模型初始化完成")
        
    def get_project_info(self):
        """获取项目信息
        
        Returns:
            dict: 项目信息字典
        """
        return self.project_data
        
    def set_project_info(self, project_info):
        """设置项目信息
        
        Args:
            project_info: 项目信息字典
        """
        self.project_data = project_info
        
    def get_current_project(self):
        """获取当前项目路径
        
        Returns:
            str: 当前项目文件路径
        """
        return self.current_project
        
    def set_current_project(self, project_path):
        """设置当前项目路径
        
        Args:
            project_path: 项目文件路径
        """
        self.current_project = project_path
        log_info(f"当前项目已设置: {project_path}")
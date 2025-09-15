"""场景模型

负责管理场景数据和业务逻辑
"""
import json
from datetime import datetime
from pathlib import Path
from models.base_model import BaseModel
from services.file.file_service import FileService
from utils.helpers.logger import log_error, log_info, log_warning


class SceneModel(BaseModel):
    """场景模型，负责管理场景数据"""
    
    def __init__(self, config=None):
        """初始化场景模型
        
        Args:
            config: 应用程序配置
        """
        super().__init__()
        self.config = config or {}
        self.scene_data = {
            "metadata": {
                "version": "1.0",
                "created": datetime.now().strftime("%Y-%m-%d"),
                "last_modified": datetime.now().strftime("%Y-%m-%d")
            },
            "scenes": []
        }
        self.current_file = None
        self.portrait_count = self.config.get("editor", {}).get("portrait_count", 4)
        self.file_service = FileService()
    
    def create_new_project(self, file_path):
        """创建新项目
        
        Args:
            file_path: 项目文件路径
            
        Returns:
            str: 项目文件路径
        """
        # 确保文件扩展名正确
        if not file_path.lower().endswith(('.json', '.xml')):
            file_path += '.json'  # 默认使用json格式
        
        self.scene_data = {
            "metadata": {
                "version": "1.0",
                "created": datetime.now().strftime("%Y-%m-%d"),
                "last_modified": datetime.now().strftime("%Y-%m-%d")
            },
            "scenes": []
        }
        
        self.current_file = file_path
        self.save_to_file()
        return file_path
    
    def load_project(self, file_path):
        """加载现有项目
        
        Args:
            file_path: 项目文件路径
            
        Returns:
            bool: 是否加载成功
        """
        try:
            # 根据文件扩展名选择加载方法
            if file_path.lower().endswith('.json'):
                self.scene_data = self.file_service.load_json(file_path)
            elif file_path.lower().endswith('.xml'):
                self.scene_data = self.file_service.load_xml(file_path)
            else:
                # 未知格式，尝试JSON格式
                self.scene_data = self.file_service.load_json(file_path)
                
            if self.scene_data:
                self.current_file = file_path
                log_info(f"项目加载成功: {file_path}")
                return True
            return False
        except Exception as e:
            log_error(f"加载文件失败: {str(e)}")
            return False
    
    def save_to_file(self):
        """将当前数据保存到文件
        
        Returns:
            bool: 是否保存成功
        """
        if not self.current_file:
            log_warning("没有当前文件可保存")
            return False
        
        try:
            # 更新模型
            self.update()
            # 更新最后修改时间
            current_time = datetime.now().strftime("%Y-%m-%d")
            self.scene_data["metadata"]["last_modified"] = current_time
            
            # 根据文件扩展名选择保存方法
            result = False
            if self.current_file.lower().endswith('.json'):
                result = self.file_service.save_json(self.current_file, self.scene_data)
            elif self.current_file.lower().endswith('.xml'):
                result = self.file_service.save_xml(self.current_file, self.scene_data)
            else:
                # 默认使用JSON格式
                result = self.file_service.save_json(self.current_file, self.scene_data)
            
            if result:
                log_info(f"项目保存成功: {self.current_file}")
            else:
                log_warning(f"项目保存返回非成功状态")
            return result
        except Exception as e:
            log_error(f"保存文件失败: {str(e)}")
            return False
    
    def save_current_scene(self, scene_info):
        """保存当前场景
        
        Args:
            scene_info: 场景信息
            
        Returns:
            bool: 是否保存成功
        """
        # 确保metadata键存在
        if "metadata" not in self.scene_data:
            current_time = datetime.now().strftime("%Y-%m-%d")
            self.scene_data["metadata"] = {
                "version": "1.0",
                "created": current_time,
                "last_modified": current_time
            }
        else:
            # 更新最后修改时间
            self.scene_data["metadata"]["last_modified"] = datetime.now().strftime("%Y-%m-%d")
        
        # 添加场景信息
        self.scene_data.setdefault("scenes", []).append(scene_info)
        
        # 保存到文件
        return self.save_to_file()
    
    def get_default_save_dir(self):
        """获取默认保存目录
        
        Returns:
            str: 默认保存目录路径
        """
        default_dir = self.config.get("paths", {}).get("output", "output")
        if not Path(default_dir).is_absolute():
            # 获取应用程序根目录（src的父目录）
            app_root = Path(__file__).parent.parent.parent.parent
            default_dir = str(app_root / default_dir)
        
        Path(default_dir).mkdir(parents=True, exist_ok=True)
        return default_dir
    
    def get_current_scene(self):
        """获取当前场景
        
        Returns:
            dict: 当前场景数据，如果没有场景则返回空字典
        """
        scenes = self.scene_data.get("scenes", [])
        if scenes:
            return scenes[-1]  # 返回最后一个场景作为当前场景
        return {}
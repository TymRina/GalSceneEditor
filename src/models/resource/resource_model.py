"""
资源模型

负责管理应用程序的资源文件
"""
from pathlib import Path
import shutil
from models.base_model import BaseModel
from utils.helpers.logger import log_error, log_debug


class ResourceModel(BaseModel):
    """资源模型，负责管理应用程序的资源文件"""
    
    def __init__(self, config=None):
        """初始化资源模型
        
        Args:
            config: 应用程序配置
        """
        super().__init__()
        self.config = config or {}
        
        # 获取资源路径配置
        resource_path_config = self.config.get("paths", {}).get("resources", "resources")
        
        # 优先使用从main.py传递的app_root路径
        if "app_root" in self.config:
            app_root = self.config["app_root"]
            self.resource_path = str(Path(app_root) / resource_path_config)
        else:
            # 如果是相对路径，则相对于应用程序根目录
            if not Path(resource_path_config).is_absolute():
                # 获取应用程序根目录（src的父目录）
                app_root = Path(__file__).parent.parent.parent.parent
                self.resource_path = str(app_root / resource_path_config)
            else:
                self.resource_path = resource_path_config
        
        # 确保资源目录存在
        resource_dir = Path(self.resource_path)
        if not resource_dir.exists():
            try:
                resource_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                log_error(f"无法创建资源目录: {str(e)}")
        
        self.error_callback = None
    
    def set_error_callback(self, callback):
        """设置错误回调函数
        
        Args:
            callback: 错误回调函数，接收一个错误信息字符串参数
        """
        self.error_callback = callback
    
    def scan_resource_folder(self, resource_type):
        """扫描资源文件夹
        
        Args:
            resource_type: 资源类型，如background, portrait, bgm等
            
        Returns:
            list: 资源列表，每个元素为(name, path)元组
        """
        resource_dir = Path(self.resource_path) / resource_type
        if not resource_dir.exists():
            return []
        
        resources = []
        for file_path in resource_dir.glob("*.*"):
            # 跳过隐藏文件和非文件
            if file_path.name.startswith(".") or not file_path.is_file():
                continue
            
            # 添加到资源列表
            resources.append((file_path.stem, str(file_path)))
        
        # 按名称排序
        resources.sort(key=lambda x: x[0])
        return resources
    
    def get_resource_path(self, resource_type, resource_name):
        """获取资源文件路径
        
        Args:
            resource_type: 资源类型，如background, portrait, bgm等
            resource_name: 资源名称
            
        Returns:
            str: 资源文件路径
        """
        resource_dir = Path(self.resource_path) / resource_type
        
        # 如果提供了扩展名，直接查找
        if "." in resource_name:
            resource_path = resource_dir / resource_name
            if resource_path.exists():
                return str(resource_path)
        
        # 否则，查找所有匹配的文件
        for file_path in resource_dir.glob(f"{resource_name}.*"):
            if file_path.is_file():
                return str(file_path)
        
        return None
    
    def import_resource_file(self, file_path, resource_type):
        """导入资源文件到指定目录
        
        Args:
            file_path: 源文件路径
            resource_type: 资源类型
            
        Returns:
            bool: 导入是否成功
        """
        try:
            # 获取文件信息
            source_path = Path(file_path)
            if not source_path.exists() or not source_path.is_file():
                error_msg = f"源文件不存在: {file_path}"
                log_debug(error_msg)
                # 返回错误信息给调用者
                if self.error_callback:
                    self.error_callback(error_msg)
                return False
            
            # 创建目标目录
            target_dir = Path(self.resource_path) / resource_type
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # 构建目标文件路径
            file_name = source_path.name
            target_path = target_dir / file_name
            
            # 检查文件名冲突
            counter = 1
            base_name = source_path.stem
            extension = source_path.suffix
            
            # 如果文件已存在，添加数字后缀避免覆盖
            while target_path.exists():
                new_file_name = f"{base_name}_{counter}{extension}"
                target_path = target_dir / new_file_name
                counter += 1
            
            # 复制文件
            shutil.copy2(source_path, target_path)
            return True
        except Exception as e:
            error_msg = f"导入资源文件失败: {str(e)}"
            log_error(error_msg)
            # 返回错误信息给调用者
            if self.error_callback:
                self.error_callback(error_msg)
            return False
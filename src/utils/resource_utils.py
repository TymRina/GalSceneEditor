"""
资源加载工具模块

提供通用的资源加载功能
"""
from typing import Optional, Dict, Any
from pathlib import Path
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaContent
from utils.helpers.logger import log_error, log_debug


class ResourceLoader:
    """资源加载器，提供通用的资源加载功能"""
    
    @staticmethod
    def load_image(image_path: str) -> Optional[QPixmap]:
        """加载图片资源
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            Optional[QPixmap]: 加载的图片，如果加载失败则返回None
        """
        try:
            if not image_path:
                return None
            
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                log_debug(f"加载图片失败: {image_path}")
                return None
            
            return pixmap
        except Exception as e:
            log_error(f"加载图片时发生错误: {e}")
            return None
    
    @staticmethod
    def load_font(font_path: str, font_size: Optional[int] = None) -> Optional[QFont]:
        """加载字体资源
        
        Args:
            font_path: 字体文件路径
            font_size: 字体大小
            
        Returns:
            Optional[QFont]: 加载的字体，如果加载失败则返回None
        """
        try:
            if not font_path:
                # 使用系统默认字体
                font = QFont()
                if font_size:
                    font.setPointSize(font_size)
                return font
            
            # 检查字体文件是否存在
            font_path_obj = Path(font_path)
            if not font_path_obj.exists():
                log_debug(f"字体文件不存在: {font_path}")
                return None
            
            # 使用QFontDatabase加载字体文件
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id == -1:
                log_debug(f"加载字体失败: {font_path}")
                return None
            
            # 获取字体族名
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if not font_families:
                log_debug(f"无法获取字体族: {font_path}")
                return None
            
            # 创建字体对象
            font = QFont(font_families[0])
            if font_size:
                font.setPointSize(font_size)
            
            return font
        except Exception as e:
            log_error(f"加载字体时发生错误: {e}")
            return None
    
    @staticmethod
    def create_media_content(file_path: str) -> Optional[QMediaContent]:
        """创建媒体内容
        
        Args:
            file_path: 媒体文件路径
            
        Returns:
            Optional[QMediaContent]: 创建的媒体内容，如果失败则返回None
        """
        try:
            if not file_path:
                return None
            
            # 检查文件是否存在
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                log_debug(f"媒体文件不存在: {file_path}")
                return None
            
            url = QUrl.fromLocalFile(file_path)
            return QMediaContent(url)
        except Exception as e:
            log_error(f"创建媒体内容时发生错误: {e}")
            return None
    
    @staticmethod
    def scale_pixmap(pixmap: QPixmap, scale: float) -> QPixmap:
        """缩放图片
        
        Args:
            pixmap: 要缩放的图片
            scale: 缩放比例
            
        Returns:
            QPixmap: 缩放后的图片
        """
        try:
            if pixmap.isNull():
                return pixmap
            
            width = int(pixmap.width() * scale)
            height = int(pixmap.height() * scale)
            
            # 使用Qt.KeepAspectRatio保持宽高比
            return pixmap.scaled(width, height, aspectRatioMode=Qt.KeepAspectRatio)
        except Exception as e:
            log_error(f"缩放图片时发生错误: {e}")
            return pixmap
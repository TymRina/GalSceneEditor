"""媒体服务

负责音频和图像处理
"""
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtMultimedia import QMediaContent
from utils.resource_utils import ResourceLoader
from utils.helpers.logger import log_info


class MediaService:
    """媒体服务，负责加载和管理各种媒体资源"""
    
    def __init__(self):
        """初始化媒体服务"""
        # 资源缓存
        self.image_cache = {}
        self.audio_cache = {}
        self.font_cache = {}
    
    def load_image(self, image_path):
        """加载图片资源，使用缓存优化性能
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            QPixmap: 图像对象，加载失败时返回None
        """
        # 空路径检查
        if not image_path:
            return None
            
        # 检查缓存
        if image_path in self.image_cache:
            return self.image_cache[image_path]
        
        # 使用 ResourceLoader 加载图片
        pixmap = ResourceLoader.load_image(image_path)
        
        # 存入缓存
        if pixmap:
            self.image_cache[image_path] = pixmap
        
        return pixmap
    
    def load_audio(self, audio_path):
        """加载音频资源，使用缓存优化性能
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            QMediaContent: 音频对象，加载失败时返回None
        """
        # 空路径检查
        if not audio_path:
            return None
            
        # 检查缓存
        if audio_path in self.audio_cache:
            return self.audio_cache[audio_path]
        
        # 使用 ResourceLoader 创建媒体内容
        media_content = ResourceLoader.create_media_content(audio_path)
        
        # 存入缓存
        if media_content:
            self.audio_cache[audio_path] = media_content
        
        return media_content
    
    def load_font(self, font_path, font_size=None):
        """加载字体资源，使用缓存优化性能
        
        Args:
            font_path: 字体文件路径
            font_size: 字体大小，默认为None，表示使用默认大小
            
        Returns:
            QFont: 字体对象，加载失败时返回默认字体
        """
        # 创建缓存键
        cache_key = (font_path, font_size)
        
        # 检查缓存
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        # 使用 ResourceLoader 加载字体
        font = ResourceLoader.load_font(font_path, font_size)
        
        # 如果加载失败，创建默认字体
        if not font:
            font = QFont()
            if font_size:
                font.setPointSize(font_size)
        
        # 存入缓存
        self.font_cache[cache_key] = font
        return font
        
    def scale_image(self, image_path, scale):
        """加载并缩放图片
        
        Args:
            image_path: 图像文件路径
            scale: 缩放比例
            
        Returns:
            QPixmap: 缩放后的图像对象，加载失败时返回None
        """
        # 先加载图片
        pixmap = self.load_image(image_path)
        if not pixmap or pixmap.isNull():
            return None
        
        # 使用 ResourceLoader 缩放图片
        return ResourceLoader.scale_pixmap(pixmap, scale)
        
    def clear_cache(self, cache_type=None):
        """清除缓存
        
        Args:
            cache_type: 缓存类型，可选值：'image', 'audio', 'font'，如果为None则清除所有缓存
        """
        if cache_type == 'image' or cache_type is None:
            self.image_cache.clear()
        if cache_type == 'audio' or cache_type is None:
            self.audio_cache.clear()
        if cache_type == 'font' or cache_type is None:
            self.font_cache.clear()
            
        log_info(f"缓存已清除: {cache_type if cache_type else '所有'}")
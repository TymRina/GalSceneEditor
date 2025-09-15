"""资源处理器

负责处理资源相关的操作
"""
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtMultimedia import QMediaContent
from utils.helpers.logger import log_error


class ResourceHandler:
    """资源处理器，负责处理资源相关的操作"""
    
    def __init__(self, resource_model, media_service, config=None):
        """初始化资源处理器
        
        Args:
            resource_model: 资源模型
            media_service: 媒体服务
            config: 应用程序配置
        """
        self.resource_model = resource_model
        self.media_service = media_service
        self.config = config or {}
        # 从配置中获取立绘数量，默认为4
        self.portrait_count = self.config.get("editor", {}).get("portrait_count", 4)
        self.current_portraits = [None] * self.portrait_count
        self.current_portrait_scales = [1.0] * self.portrait_count
    
    def change_background(self, image_label, path):
        """更改背景
        
        Args:
            image_label: 图像标签
            path: 背景图片路径
        """
        if not path:
            # 清除背景
            image_label.set_background(None)
            return
        
        pixmap = self.media_service.load_image(path)
        if pixmap:
            image_label.set_background(pixmap)
    
    def change_portrait(self, image_label, path, portrait_index, scale=1.0):
        """更改立绘
        
        Args:
            image_label: 图像标签
            path: 立绘图片路径
            portrait_index: 立绘索引
            scale: 缩放比例
        """
        if portrait_index < 0 or portrait_index >= self.portrait_count:
            log_error(f"立绘索引超出范围: {portrait_index}")
            return
        
        if not path:
            # 清除立绘
            self.current_portraits[portrait_index] = None
            image_label.set_portrait(None, portrait_index)
            return
        
        pixmap = self.media_service.load_image(path)
        if pixmap:
            self.current_portraits[portrait_index] = pixmap
            self.current_portrait_scales[portrait_index] = scale
            # 应用缩放
            scaled_pixmap = pixmap.scaled(
                int(pixmap.width() * scale),
                int(pixmap.height() * scale),
                aspectRatioMode=Qt.KeepAspectRatio
            )
            image_label.set_portrait(scaled_pixmap, portrait_index)
    
    def change_audio(self, media_player, path):
        """通用音频更改方法
        
        Args:
            media_player: 媒体播放器
            path: 音频文件路径
        """
        if not path:
            # 停止播放
            media_player.stop()
            return
        
        url = QUrl.fromLocalFile(path)
        content = QMediaContent(url)
        media_player.setMedia(content)
        media_player.play()
    
    def change_bgm(self, media_player, path):
        """更改背景音乐
        
        Args:
            media_player: 媒体播放器
            path: 音频文件路径
        """
        self.change_audio(media_player, path)
    
    def change_sound(self, media_player, path):
        """更改音效
        
        Args:
            media_player: 媒体播放器
            path: 音频文件路径
        """
        self.change_audio(media_player, path)
    
    def change_voice(self, media_player, path):
        """更改语音
        
        Args:
            media_player: 媒体播放器
            path: 音频文件路径
        """
        self.change_audio(media_player, path)
    
    def change_font(self, text_edit, path, font_size=None):
        """更改字体
        
        Args:
            text_edit: 文本编辑器
            path: 字体文件路径
            font_size: 字体大小，默认为None，表示使用当前大小
        """
        if not path:
            # 使用系统默认字体
            font = QFont()
            if font_size:
                font.setPointSize(font_size)
            text_edit.setFont(font)
            return
        
        font = self.media_service.load_font(path, font_size)
        if font:
            text_edit.setFont(font)
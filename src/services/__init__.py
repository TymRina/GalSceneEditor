"""服务包

包含所有服务
"""
from .file.file_service import FileService
from .media.media_service import MediaService

__all__ = ['FileService', 'MediaService']
"""配置包

包含应用程序配置
"""
from .settings import load_settings, save_settings, DEFAULT_CONFIG

__all__ = ['load_settings', 'save_settings', 'DEFAULT_CONFIG']
"""应用程序配置

负责管理应用程序的全局设置和配置
"""
import json
from pathlib import Path
from utils.helpers.logger import log_error

# 默认配置
DEFAULT_CONFIG = {
    "app": {
        "name": "Galgame场景编辑器",
        "version": "1.0.0",
        "theme": "default"
    },
    "editor": {
        "portrait_count": 4,  # 默认支持的立绘数量
        "default_font": "系统默认",
        "default_font_size": 16
    },
    "paths": {
        "resources": "resources",
        "output": "output",
        "logs": "logs"
    },
    "logging": {
        "level": "INFO",
        "file_size": 1048576,  # 1MB
        "backup_count": 3
    }
}


def load_settings(config_path=None):
    """加载应用程序配置
    
    Args:
        config_path: 配置文件路径，如果为None则使用默认配置
        
    Returns:
        dict: 配置字典
    """
    if config_path and Path(config_path).exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 合并默认配置，确保所有必要的配置项都存在
                merged_config = DEFAULT_CONFIG.copy()
                _deep_update(merged_config, config)
                return merged_config
        except Exception as e:
            log_error(f"加载配置文件失败: {str(e)}")
    
    # 返回默认配置
    return DEFAULT_CONFIG.copy()


def save_settings(config, config_path):
    """保存应用程序配置
    
    Args:
        config: 配置字典
        config_path: 配置文件保存路径
        
    Returns:
        bool: 是否保存成功
    """
    try:
        # 确保目录存在
        Path(config_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        log_error(f"保存配置文件失败: {str(e)}")
        return False


def _deep_update(d, u):
    """深度更新字典
    
    Args:
        d: 目标字典
        u: 源字典
    """
    for k, v in u.items():
        if isinstance(v, dict) and k in d and isinstance(d[k], dict):
            _deep_update(d[k], v)
        else:
            d[k] = v
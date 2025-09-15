"""日志工具

提供日志记录功能
"""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path


# 默认日志记录器
default_logger = None


def setup_logger(name, log_file=None, level=logging.INFO, config=None):
    """设置日志记录器
    
    Args:
        name: 日志记录器名称
        log_file: 日志文件路径，如果为None则输出到控制台
        level: 日志级别
        config: 日志配置字典，可覆盖默认设置
    
    Returns:
        logging.Logger: 日志记录器
    """
    # 应用配置
    log_config = config or {
        'file_size': 1048576,  # 1MB
        'backup_count': 3
    }
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 创建处理器
    if log_file:
        # 确保日志目录存在
        log_dir = str(Path(log_file).parent)
        if log_dir and not Path(log_dir).exists():
            os.makedirs(log_dir)
        
        # 文件处理器（带轮转功能）
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=log_config.get('file_size', 1048576),
            backupCount=log_config.get('backup_count', 3),
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# 初始化默认日志记录器
def ensure_default_logger():
    """确保默认日志记录器已初始化"""
    global default_logger
    if default_logger is None:
        # 获取应用程序根目录（src的父目录）
        app_root = Path(__file__).parent.parent.parent.parent
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = str(app_root / 'logs' / f'app_{date_str}.log')
        default_logger = setup_logger(
            'galgame_editor',
            log_file
        )
    return default_logger


# 立即初始化确保日志记录器可用
default_logger = ensure_default_logger()


def initialize_logger(config=None):
    """使用配置初始化日志器
    
    Args:
        config: 包含日志配置的应用程序配置
    """
    global default_logger
    
    if config:
        log_config = config.get('logging', {})
        log_level_str = log_config.get('level', 'INFO').upper()
        log_level = getattr(logging, log_level_str, logging.INFO)
        
        # 获取日志目录
        log_dir = config.get('paths', {}).get('logs', 'logs')
        
        # 如果是相对路径，则相对于应用程序根目录
        if not Path(log_dir).is_absolute():
            # 获取应用程序根目录（src的父目录）
            app_root = Path(__file__).parent.parent.parent.parent
            log_dir = str(app_root / log_dir)
        
        # 确保日志目录存在
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = str(Path(log_dir) / f'app_{date_str}.log')
        
        # 重新创建日志器
        for handler in default_logger.handlers[:]:
            handler.close()
            default_logger.removeHandler(handler)
        
        default_logger = setup_logger(
            'galgame_editor',
            log_file,
            log_level,
            log_config
        )
    
    return default_logger


def log_info(message):
    """记录信息日志
    
    Args:
        message: 日志消息
    """
    ensure_default_logger()
    default_logger.info(message)


def log_warning(message):
    """记录警告日志
    
    Args:
        message: 日志消息
    """
    ensure_default_logger()
    default_logger.warning(message)


def log_error(message, exc_info=False):
    """记录错误日志
    
    Args:
        message: 日志消息
        exc_info: 是否包含异常信息
    """
    ensure_default_logger()
    default_logger.error(message, exc_info=exc_info)


def log_debug(message):
    """记录调试日志
    
    Args:
        message: 日志消息
    """
    ensure_default_logger()
    default_logger.debug(message)


def log_critical(message, exc_info=False):
    """记录严重错误日志
    
    Args:
        message: 日志消息
        exc_info: 是否包含异常信息
    """
    ensure_default_logger()
    default_logger.critical(message, exc_info=exc_info)
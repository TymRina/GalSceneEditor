"""主程序入口

这是应用程序的入口点，负责启动细分后的MVC架构的Galgame场景编辑器
"""
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from controllers.app_controller import AppController
from config.settings import load_settings
from utils.helpers.logger import initialize_logger, log_info, log_error

# 解决PyInstaller打包后资源路径问题
def get_app_root():
    # 检查是否在PyInstaller打包环境中
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller打包后，临时目录为sys._MEIPASS
        return Path(sys._MEIPASS)
    else:
        # 开发环境下，返回src的父目录
        return Path(__file__).parent.parent

def main():
    try:
        # 获取应用程序根目录
        app_root = get_app_root()
        log_info(f"应用程序根目录: {app_root}")
        
        # 加载应用程序配置
        settings = load_settings()
        
        # 初始化日志系统
        initialize_logger(settings)
        log_info("应用程序启动")
        
        # 创建应用程序实例
        app = QApplication(sys.argv)
        # 设置应用程序图标
        icon_path = app_root / 'resources' / 'icon' / 'GalSceneEditor.ico'
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
            log_info(f"设置应用程序图标: {icon_path}")
        else:
            log_error(f"未找到图标文件: {icon_path}")
        log_info(f"创建应用程序实例: {app.applicationName()}")
        
        # 将app_root传递给settings，确保其他模块也能正确找到资源
        settings['app_root'] = app_root
        
        # 创建并运行控制器
        controller = AppController(settings)
        controller.run()
        
        # 执行应用程序
        exit_code = app.exec_()
        log_info(f"应用程序退出，退出代码: {exit_code}")
        sys.exit(exit_code)
    except Exception as e:
        log_error(f"应用程序运行出错: {str(e)}")
        raise


if __name__ == "__main__":
    main()
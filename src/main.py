"""主程序入口

这是应用程序的入口点，负责启动细分后的MVC架构的Galgame场景编辑器
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from controllers.app_controller import AppController
from config.settings import load_settings
from utils.helpers.logger import initialize_logger, log_info, log_error


def main():
    try:
        # 加载应用程序配置
        settings = load_settings()
        
        # 初始化日志系统
        initialize_logger(settings)
        log_info("应用程序启动")
        
        # 创建应用程序实例
        app = QApplication(sys.argv)
        # 设置应用程序图标
        # 获取应用程序根目录（src的父目录）
        app_root = Path(__file__).parent.parent
        icon_path = app_root / 'resources' / 'icon' / 'GalSceneEditor.ico'
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
            log_info(f"设置应用程序图标: {icon_path}")
        else:
            log_error(f"未找到图标文件: {icon_path}")
        log_info(f"创建应用程序实例: {app.applicationName()}")
        
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
"""应用控制器

负责协调模型和视图
"""
import json
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QAction
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap, QKeySequence
from utils.helpers.logger import log_error

from models.scene.scene_model import SceneModel
from models.resource.resource_model import ResourceModel
from models.project.project_model import ProjectModel
from views.screens.main_view import MainView
from services.media.media_service import MediaService
from controllers.handlers.resource_handler import ResourceHandler


class AppController:
    """应用程序控制器，负责管理应用程序的生命周期和核心功能"""
    
    def __init__(self, config=None):
        """初始化应用程序控制器
        
        Args:
            config: 应用程序配置
        """
        self.config = config or {}
        
        # 从配置中获取应用程序根目录
        self.app_root = self.config.get('app_root')
        
        # 初始化各个模型
        self.project_model = ProjectModel(config=self.config)
        
        # 初始化资源模型时传递包含app_root的配置
        self.resource_model = ResourceModel(config=self.config)
        
        self.scene_model = SceneModel(config=self.config)
        
        # 初始化视图
        self.view = MainView(self.config)
        self.view.set_controller(self)
        
        # 初始化服务
        self.media_service = MediaService()
        
        # 初始化处理器
        self.resource_handler = ResourceHandler(self.resource_model, self.media_service)
        
        # 初始化标志变量
        self.save_warning_shown = False
        self.initialized = False
        
        # 项目状态
        self.current_project = None
        
        # 设置资源模型的错误回调函数
        self.resource_model.set_error_callback(self._show_error_message)
        
        # 初始化资源
        self.init_resources()
    
    def _initialize_resources(self):
        """初始化应用程序资源"""
        try:
            # 初始化资源模型
            log_debug("正在初始化资源模型")
            log_info(f"资源模型初始化完成，资源路径: {self.resource_model.resource_path}")
            log_info(f"应用程序根目录: {self.app_root}")
        except Exception as e:
            log_error(f"初始化资源失败: {str(e)}")
    
    def _show_error_message(self, error_msg):
        """显示错误消息
        
        Args:
            error_msg: 错误信息
        """
        QMessageBox.warning(self.view, "操作失败", error_msg)
    
    def run(self):
        """运行应用程序"""
        self.view.show()
    
    def init_resources(self):
        """初始化资源"""
        # 加载背景资源
        backgrounds = self.resource_model.scan_resource_folder("background")
        self.view.combo_bg.clear()
        self.view.combo_bg.addItem("无背景", "")
        for name, path in backgrounds:
            self.view.combo_bg.addItem(name, path)
        
        # 加载立绘资源
        portraits = self.resource_model.scan_resource_folder("portrait")
        for combo in self.view.portrait_combos:
            combo.clear()
            combo.addItem("无立绘", "")
            for name, path in portraits:
                combo.addItem(name, path)
        
        # 加载BGM资源
        bgms = self.resource_model.scan_resource_folder("background_music")
        self.view.combo_bgm.clear()
        self.view.combo_bgm.addItem("无BGM", "")
        for name, path in bgms:
            self.view.combo_bgm.addItem(name, path)
        
        # 加载音效资源
        sounds = self.resource_model.scan_resource_folder("sound")
        self.view.combo_sound.clear()
        self.view.combo_sound.addItem("无音效", "")
        for name, path in sounds:
            self.view.combo_sound.addItem(name, path)
        
        # 加载语音资源
        voices = self.resource_model.scan_resource_folder("voice")
        self.view.combo_voice.clear()
        self.view.combo_voice.addItem("无语音", "")
        for name, path in voices:
            self.view.combo_voice.addItem(name, path)
        
        # 加载字体资源
        fonts = self.resource_model.scan_resource_folder("font")
        self.view.combo_font.clear()
        self.view.combo_font.addItem("系统默认", "")
        for name, path in fonts:
            self.view.combo_font.addItem(name, path)
        
        # 初始化完成
        self.initialized = True
    
    def on_new_project(self):
        """创建新项目"""
        file_path, _ = QFileDialog.getSaveFileName(
            self.view,
            "新建项目",
            self.scene_model.get_default_save_dir(),
            "游戏场景文件 (*.json *.xml);;JSON文件 (*.json);;XML文件 (*.xml)"
        )
        
        if file_path:
            self.scene_model.create_new_project(file_path)
            QMessageBox.information(self.view, "提示", f"项目已创建: {file_path}")
    
    def on_open_project(self):
        """打开项目"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "打开项目",
            self.scene_model.get_default_save_dir(),
            "游戏场景文件 (*.json *.xml);;JSON文件 (*.json);;XML文件 (*.xml)"
        )
        
        if file_path and self.scene_model.load_project(file_path):
            QMessageBox.information(self.view, "提示", f"项目已加载: {file_path}")
        elif file_path:
            QMessageBox.warning(self.view, "警告", "项目加载失败")
    
    def on_save_project(self):
        """保存项目"""
        if not self.scene_model.current_file:
            file_path, _ = QFileDialog.getSaveFileName(
                self.view,
                "保存项目",
                self.scene_model.get_default_save_dir(),
                "游戏场景文件 (*.json *.xml);;JSON文件 (*.json);;XML文件 (*.xml)"
            )
            
            if file_path:
                # 检查文件是否已存在
                file_exists = Path(file_path).exists()
                if file_exists:
                    # 文件已存在，询问用户是续写还是新建
                    reply = QMessageBox.question(
                        self.view,
                        "文件已存在",
                        "所选文件已存在，是否要续写该文件？\n\n选择'是'：将当前场景追加到现有文件\n选择'否'：创建新文件覆盖现有文件",
                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                    )
                    
                    if reply == QMessageBox.Yes:
                        # 续写模式：加载现有文件内容
                        if not self.scene_model.load_project(file_path):
                            QMessageBox.warning(self.view, "警告", "加载现有文件失败，将创建新文件")
                            self.scene_model.create_new_project(file_path)
                    elif reply == QMessageBox.No:
                        # 新建模式：覆盖现有文件
                        self.scene_model.create_new_project(file_path)
                    else:
                        # 用户取消操作
                        return
                else:
                    # 文件不存在，创建新项目
                    self.scene_model.create_new_project(file_path)
            else:
                return
        
        # 收集并保存当前场景信息
        self.save_current_scene_info()
        
        if self.scene_model.save_to_file():
            QMessageBox.information(self.view, "提示", "项目已保存")
        else:
            QMessageBox.warning(self.view, "警告", "项目保存失败")
    
    def save_current_scene_info(self):
        """保存当前场景信息"""
        try:
            # 先检查是否有打开的项目文件
            if not self.scene_model.current_file:
                # 没有打开项目文件时安静返回，不显示任何提示
                return
            
            # 获取配置值
            portrait_count = self.config.get("editor", {}).get("portrait_count", 4)
            
            # 收集当前场景信息
            character_name = self.view.name_input.text().strip()
            text_content = self.view.text_edit.toPlainText()
            
            # 判断是否为旁白
            is_narration = not character_name and text_content
            display_name = character_name if character_name else ("旁白" if text_content else "")
            
            scene_info = {
                "background": self.view.combo_bg.itemData(self.view.combo_bg.currentIndex()),
                "portraits": [],
                "audio": {
                    "bgm": self.view.combo_bgm.itemData(self.view.combo_bgm.currentIndex()),
                    "sound": self.view.combo_sound.itemData(self.view.combo_sound.currentIndex()),
                    "voice": self.view.combo_voice.itemData(self.view.combo_voice.currentIndex())
                },
                "character_name": display_name,
                "is_narration": is_narration,
                "text": text_content,
                "font": {
                    "path": self.view.combo_font.itemData(self.view.combo_font.currentIndex()),
                    "size": self.view.slider_font_size.value()
                },
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 收集立绘信息 - 只保存非空的立绘数据
            container_width = self.view.image_label.width()
            container_height = self.view.image_label.height()
            
            for i in range(portrait_count):
                path = self.view.portrait_combos[i].itemData(self.view.portrait_combos[i].currentIndex())
                if path:  # 只有当立绘路径不为空时才保存
                    # 计算相对位置（百分比）
                    x = self.view.image_label.portrait_positions[i].x()
                    y = self.view.image_label.portrait_positions[i].y()
                    
                    # 避免除零错误
                    rel_x = x / container_width if container_width > 0 else 0
                    rel_y = y / container_height if container_height > 0 else 0
                    
                    portrait_info = {
                        "path": path,
                        "scale": self.view.portrait_scale_sliders[i].value() / 100.0,
                        "position": {
                            "rel_x": rel_x,  # 相对于容器宽度的比例
                            "rel_y": rel_y,  # 相对于容器高度的比例
                            "x": x,          # 保留绝对坐标作为兼容旧版本
                            "y": y           # 保留绝对坐标作为兼容旧版本
                        },
                        "index": i
                    }
                    scene_info["portraits"].append(portrait_info)
            
            # 保存场景信息
            if not self.scene_model.save_current_scene(scene_info):
                log_error("保存场景信息失败")
                self._show_error_message("保存场景信息失败")
        except Exception as e:
            log_error(f"收集和保存场景信息时出错: {str(e)}")
            self._show_error_message(f"保存场景信息时发生错误: {str(e)}")
    
    def on_background_changed(self, index):
        """背景变更事件
        
        Args:
            index: 下拉框索引
        """
        new_path = self.view.combo_bg.itemData(index)
        # 获取旧的背景路径
        current_scene = self.scene_model.get_current_scene()
        old_path = current_scene.get("background", "")
        
        # 直接更改背景
        self.resource_handler.change_background(self.view.image_label, new_path)
        
        # 更新视图中的当前背景路径
        self.view.update_background(new_path)
        
        # 不再自动保存，只在用户点击保存按钮时保存
        # self.save_current_scene_info()
        
    def on_portrait_changed(self, index, portrait_index):
        """立绘变更事件
        
        Args:
            index: 下拉框索引
            portrait_index: 立绘索引
        """
        new_path = self.view.portrait_combos[portrait_index].itemData(index)
        new_scale = self.view.portrait_scale_sliders[portrait_index].value() / 100.0
        
        # 获取旧的立绘信息
        current_scene = self.scene_model.get_current_scene()
        old_path = ""
        old_scale = 1.0
        if "portraits" in current_scene:
            for portrait in current_scene["portraits"]:
                if portrait.get("index") == portrait_index:
                    old_path = portrait.get("path", "")
                    old_scale = portrait.get("scale", 1.0)
                    break
        
        # 直接更新立绘
        self.resource_handler.change_portrait(self.view.image_label, new_path, portrait_index, new_scale)
        # 不再自动保存，只在用户点击保存按钮时保存
        # self.save_current_scene_info()
        
    def on_portrait_scale_changed(self, value, portrait_index):
        """立绘缩放变更事件
        
        Args:
            value: 滑块值
            portrait_index: 立绘索引
        """
        new_scale = value / 100.0
        combo = self.view.portrait_combos[portrait_index]
        path = combo.itemData(combo.currentIndex())
        
        # 获取旧的缩放比例
        current_scene = self.scene_model.get_current_scene()
        old_scale = 1.0
        if "portraits" in current_scene:
            for portrait in current_scene["portraits"]:
                # 检查当前立绘是否是对应的索引（通过路径匹配）
                if portrait.get("path") == path:
                    old_scale = portrait.get("scale", 1.0)
                    break
        
        # 直接更新立绘缩放比例
        self.resource_handler.change_portrait(self.view.image_label, path, portrait_index, new_scale)
        # 不再自动保存，只在用户点击保存按钮时保存
        # self.save_current_scene_info()
    
    def on_bgm_changed(self, index):
        """BGM变更事件
        
        Args:
            index: 下拉框索引
        """
        new_path = self.view.combo_bgm.itemData(index)
        
        # 直接更改BGM
        self.resource_handler.change_bgm(self.view.bgm_player, new_path)
        # 不再自动保存，只在用户点击保存按钮时保存
        
        
    def on_sound_changed(self, index):
        """音效变更事件
        
        Args:
            index: 下拉框索引
        """
        new_path = self.view.combo_sound.itemData(index)
        
        # 直接更改为当前音效
        self.resource_handler.change_sound(self.view.sound_player, new_path)
    
    def on_voice_changed(self, index):
        """语音变更事件
        
        Args:
            index: 下拉框索引
        """
        new_path = self.view.combo_voice.itemData(index)
        
        # 直接更改为当前语音
        self.resource_handler.change_voice(self.view.voice_player, new_path)

    def on_font_changed(self, index):
        """字体变更事件
        
        Args:
            index: 下拉框索引
        """
        new_path = self.view.combo_font.itemData(index)
        new_size = self.view.slider_font_size.value()
        
        # 获取旧的字体信息
        current_scene = self.scene_model.get_current_scene()
        old_path = ""
        old_size = new_size  # 默认使用当前字号
        if "font" in current_scene:
            font_info = current_scene["font"]
            if "path" in font_info:
                old_path = font_info["path"]
            if "size" in font_info:
                old_size = font_info["size"]
        
        # 直接更改字体
        self.resource_handler.change_font(self.view.text_edit, new_path, new_size)
    
    def on_font_size_changed(self, value):
        """字体大小变更事件
        
        Args:
            value: 滑块值
        """
        # 更新字号显示标签
        self.view.label_font_size.setText(str(value))
        
        # 获取字体路径和旧的字体大小
        path = self.view.combo_font.itemData(self.view.combo_font.currentIndex())
        
        # 获取旧的字体大小
        current_scene = self.scene_model.get_current_scene()
        old_size = value  # 默认使用当前值
        if "font" in current_scene and "size" in current_scene["font"]:
            old_size = current_scene["font"]["size"]
        
        # 直接更改字体大小
        self.resource_handler.change_font(self.view.text_edit, path, value)
    
    def on_name_updated(self):
        """角色姓名更新事件"""
        # 获取输入的角色姓名
        new_name = self.view.name_input.text().strip()
        
        # 判断是否为旁白
        is_narration = new_name.lower() in ["旁白", "narration"]
        if is_narration:
            new_name = ""
        
        # 获取旧的角色姓名和旁白状态
        current_scene = self.scene_model.get_current_scene()
        old_name = ""
        old_is_narration = False
        if "character_name" in current_scene:
            old_name = current_scene["character_name"]
        if "is_narration" in current_scene:
            old_is_narration = current_scene["is_narration"]
        
        # 直接更新角色姓名和旁白状态
        if is_narration:
            self.view.name_input.setText("")
            self.view.name_display_label.setText("旁白")
        else:
            self.view.name_input.setText(new_name)
            self.view.name_display_label.setText(f"角色: {new_name}")
        

    
    def import_voice_file(self):
        """导入新的语音文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "导入语音文件",
            "",
            "音频文件 (*.mp3 *.wav *.ogg)"
        )
        
        if file_path:
            # 复制文件到语音资源目录
            success = self.resource_model.import_resource_file(file_path, "voice")
            if success:
                QMessageBox.information(self.view, "成功", "语音文件导入成功")
                # 重新加载语音资源
                voices = self.resource_model.scan_resource_folder("voice")
                self.view.combo_voice.clear()
                self.view.combo_voice.addItem("无语音", "")
                for name, path in voices:
                    self.view.combo_voice.addItem(name, path)
            else:
                QMessageBox.warning(self.view, "失败", "语音文件导入失败")
    
    def on_portrait_position_changed(self, index, old_x, old_y, new_x, new_y):
        """处理立绘位置变化信号，更新立绘位置信息
        
        Args:
            index: 立绘索引
            old_x: 拖动前的x坐标
            old_y: 拖动前的y坐标
            new_x: 拖动后的x坐标
            new_y: 拖动后的y坐标
        """
        # 固定使用1280×720计算相对坐标（确保分母不为零）
        CANVAS_WIDTH = 1280
        CANVAS_HEIGHT = 720
        
        rel_x = new_x / CANVAS_WIDTH if CANVAS_WIDTH > 0 else 0
        rel_y = new_y / CANVAS_HEIGHT if CANVAS_HEIGHT > 0 else 0
        
        # 直接更新立绘位置，同时保存相对坐标和绝对坐标
        current_scene = self.scene_model.get_current_scene()
        if "portraits" in current_scene:
            for portrait in current_scene["portraits"]:
                if portrait.get("index") == index:
                    portrait["position"] = {
                        "x": new_x,
                        "y": new_y,
                        "rel_x": rel_x,
                        "rel_y": rel_y
                    }
                    break
    

    
    def load_scene(self, scene_info):
        """加载场景信息
        
        Args:
            scene_info: 场景信息字典
        """

        # 加载背景
        if "background" in scene_info and scene_info["background"]:
            background_path = scene_info["background"]
            # 查找对应的索引
            index = self.view.combo_bg.findData(background_path)
            if index >= 0:
                self.view.combo_bg.setCurrentIndex(index)
                self.refresh_background(background_path)
        
        # 加载立绘
        if "portraits" in scene_info:
            # 清空当前所有立绘
            for i in range(self.config.get("editor", {}).get("portrait_count", 4)):
                self.resource_handler.change_portrait(self.view.image_label, None, i, 1.0)
                self.view.portrait_combos[i].setCurrentIndex(0)  # 选择默认项
            
            # 加载立绘信息
            for i, portrait_info in enumerate(scene_info["portraits"]):
                if "path" in portrait_info and portrait_info["path"]:
                    path = portrait_info["path"]
                    scale = portrait_info.get("scale", 1.0)
                    
                    # 查找对应的索引
                    index = self.view.portrait_combos[i].findData(path)
                    if index >= 0:
                        self.view.portrait_combos[i].setCurrentIndex(index)
                        self.view.portrait_scale_sliders[i].setValue(int(scale * 100))
                        self.resource_handler.change_portrait(self.view.image_label, path, i, scale)
                        
                        # 恢复位置
                        if "position" in portrait_info:
                            pos = portrait_info["position"]
                            
                            # 固定使用1280×720作为画布尺寸
                            CANVAS_WIDTH = 1280
                            CANVAS_HEIGHT = 720
                            
                            # 优先使用相对坐标（如果有）
                            if isinstance(pos, dict) and "rel_x" in pos and "rel_y" in pos:
                                # 根据相对坐标计算基于固定画布的绝对位置
                                x = int(pos["rel_x"] * CANVAS_WIDTH)
                                y = int(pos["rel_y"] * CANVAS_HEIGHT)
                            else:
                                # 否则使用绝对坐标（兼容旧版本）
                                if isinstance(pos, list) and len(pos) >= 2:
                                    x = pos[0]
                                    y = pos[1]
                                elif isinstance(pos, dict):
                                    x = pos.get("x", 0)
                                    y = pos.get("y", 0)
                                else:
                                    x = 0
                                    y = 0
                            
                            # 设置立绘位置
                            self.view.image_label.set_portrait_position(i, x, y)
        
        # 加载音频
        if "audio" in scene_info:
            audio_info = scene_info["audio"]
            
            # 加载BGM
            if "bgm" in audio_info and audio_info["bgm"]:
                bgm_path = audio_info["bgm"]
                index = self.view.combo_bgm.findData(bgm_path)
                if index >= 0:
                    self.view.combo_bgm.setCurrentIndex(index)
                    self.resource_handler.change_bgm(self.view.bgm_player, bgm_path)
            
            # 加载音效
            if "sound" in audio_info and audio_info["sound"]:
                sound_path = audio_info["sound"]
                index = self.view.combo_sound.findData(sound_path)
                if index >= 0:
                    self.view.combo_sound.setCurrentIndex(index)
                    self.resource_handler.change_sound(self.view.sound_player, sound_path)
            
            # 加载语音
            if "voice" in audio_info and audio_info["voice"]:
                voice_path = audio_info["voice"]
                index = self.view.combo_voice.findData(voice_path)
                if index >= 0:
                    self.view.combo_voice.setCurrentIndex(index)
                    self.resource_handler.change_voice(self.view.voice_player, voice_path)
        
        # 加载文本和字体
        if "text" in scene_info:
            self.view.text_edit.setPlainText(scene_info["text"])
        
        if "character_name" in scene_info:
            # 检查是否为旁白
            is_narration = scene_info.get("is_narration", False)
            if is_narration:
                # 旁白时，姓名输入框为空，但显示标签显示"旁白"
                self.view.name_input.setText("")
                self.view.name_display_label.setText("旁白")
            else:
                # 非旁白时，正常显示角色姓名
                self.view.name_input.setText(scene_info["character_name"])
                self.view.name_display_label.setText(f"角色: {scene_info['character_name']}")
        
        if "font" in scene_info:
            font_info = scene_info["font"]
            
            # 加载字体
            if "path" in font_info and font_info["path"]:
                font_path = font_info["path"]
                index = self.view.combo_font.findData(font_path)
                if index >= 0:
                    self.view.combo_font.setCurrentIndex(index)
                    font_size = font_info.get("size", self.view.slider_font_size.value())
                    self.resource_handler.change_font(self.view.text_edit, font_path, font_size)
            
            # 加载字体大小
            if "size" in font_info:
                font_size = font_info["size"]
                self.view.slider_font_size.setValue(font_size)
                self.view.label_font_size.setText(str(font_size))
    
    def refresh_background(self, background_path):
        """刷新背景图片
        
        Args:
            background_path: 背景图片路径
        """
        # 使用资源处理器来刷新背景
        self.resource_handler.change_background(self.view.image_label, background_path)
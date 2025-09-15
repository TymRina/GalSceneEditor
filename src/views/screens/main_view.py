"""主视图

负责整体UI布局
"""
from PyQt5.QtWidgets import (
    QGridLayout, QComboBox, QTextEdit,
    QPushButton, QHBoxLayout, QVBoxLayout, QLabel,
    QWidget, QMainWindow, QFrame, QGroupBox, QTabWidget,
    QSlider, QLineEdit, QCheckBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from views.components.draggable_image_label import DraggableImageLabel


class MainView(QMainWindow):
    """主视图，负责整体UI布局"""
    
    def __init__(self, config=None):
        """初始化主视图
        
        Args:
            config: 应用程序配置
        """
        super().__init__()
        self.config = config or {}
        self.controller = None
        self.portrait_count = self.config.get("editor", {}).get("portrait_count", 4)
        
        # 初始化UI
        self.init_ui()
        
        # 初始化媒体播放器
        self.init_media_players()
    
    def init_ui(self):
        """初始化UI"""
        # 设置窗口标题和初始大小
        self.setWindowTitle(self.config.get("app", {}).get("name", "Galgame场景编辑器"))
        self.resize(1280, 720)
        
        # 设置窗口为可调整大小
        self.setMinimumSize(800, 600)  # 设置最小尺寸
        self.is_fullscreen = False  # 全屏状态标志
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建顶部工具栏
        toolbar_layout = QHBoxLayout()
        main_layout.addLayout(toolbar_layout)
        
        # 创建新建项目按钮
        self.btn_new = QPushButton("新建项目")
        toolbar_layout.addWidget(self.btn_new)
        
        # 创建打开项目按钮
        self.btn_open = QPushButton("打开项目")
        toolbar_layout.addWidget(self.btn_open)
        
        # 创建保存项目按钮
        self.btn_save = QPushButton("保存项目")
        toolbar_layout.addWidget(self.btn_save)
        
        # 创建内容区域
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # 创建左侧面板
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        content_layout.addWidget(left_panel, 1)
        
        # 创建背景选择组
        bg_group = QGroupBox("背景")
        bg_layout = QVBoxLayout(bg_group)
        self.combo_bg = QComboBox()
        bg_layout.addWidget(self.combo_bg)
        left_layout.addWidget(bg_group)
        
        # 创建立绘选择组
        portrait_group = QGroupBox("立绘")
        portrait_layout = QVBoxLayout(portrait_group)
        self.portrait_combos = []
        self.portrait_scale_sliders = []
        
        for i in range(self.portrait_count):
            portrait_row = QHBoxLayout()
            combo = QComboBox()
            combo.setObjectName(f"combo_portrait_{i}")
            portrait_row.addWidget(combo, 3)
            
            scale_slider = QSlider(Qt.Horizontal)
            scale_slider.setObjectName(f"slider_portrait_{i}")
            scale_slider.setRange(50, 150)
            scale_slider.setValue(100)
            portrait_row.addWidget(scale_slider, 1)
            
            portrait_layout.addLayout(portrait_row)
            self.portrait_combos.append(combo)
            self.portrait_scale_sliders.append(scale_slider)
        
        left_layout.addWidget(portrait_group)
        
        # 创建音频选择组
        audio_group = QGroupBox("音频")
        audio_layout = QVBoxLayout(audio_group)
        
        # BGM选择
        bgm_layout = QHBoxLayout()
        bgm_layout.addWidget(QLabel("BGM:"))
        self.combo_bgm = QComboBox()
        bgm_layout.addWidget(self.combo_bgm)
        audio_layout.addLayout(bgm_layout)
        
        # 音效选择
        sound_layout = QHBoxLayout()
        sound_layout.addWidget(QLabel("音效:"))
        self.combo_sound = QComboBox()
        sound_layout.addWidget(self.combo_sound)
        audio_layout.addLayout(sound_layout)
        
        # 语音选择
        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("语音:"))
        self.combo_voice = QComboBox()
        voice_layout.addWidget(self.combo_voice)
        self.btn_import_voice = QPushButton("导入")
        voice_layout.addWidget(self.btn_import_voice)
        audio_layout.addLayout(voice_layout)
        
        left_layout.addWidget(audio_group)
        
        # 创建文本编辑组
        text_group = QGroupBox("文本")
        text_layout = QVBoxLayout(text_group)
        
        # 角色姓名输入
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("角色姓名:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("输入角色姓名")
        name_layout.addWidget(self.name_input, 3)
        self.btn_update_name = QPushButton("更新")
        name_layout.addWidget(self.btn_update_name)
        text_layout.addLayout(name_layout)
        
        # 字体选择
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("字体:"))
        self.combo_font = QComboBox()
        font_layout.addWidget(self.combo_font, 3)
        
        # 字体大小调整
        font_layout.addWidget(QLabel("字号:"))
        self.slider_font_size = QSlider(Qt.Horizontal)
        self.slider_font_size.setRange(8, 36)  # 字体大小范围8-36pt
        self.slider_font_size.setValue(12)     # 默认12pt
        font_layout.addWidget(self.slider_font_size, 1)
        
        # 显示当前字号
        self.label_font_size = QLabel("12")
        self.label_font_size.setFixedWidth(30)
        self.label_font_size.setAlignment(Qt.AlignCenter)
        font_layout.addWidget(self.label_font_size)
        
        text_layout.addLayout(font_layout)
        
        # 显示角色姓名的label
        self.name_display_label = QLabel("角色: ")
        self.name_display_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)
        self.name_display_label.setFont(font)
        text_layout.addWidget(self.name_display_label)

        # 文本编辑
        self.text_edit = QTextEdit()
        text_layout.addWidget(self.text_edit)
        
        left_layout.addWidget(text_group)
        
        # 创建右侧预览区域
        self.preview_group = QGroupBox("预览")
        self.preview_layout = QVBoxLayout(self.preview_group)
        # 设置预览布局的边距，确保四个方向间距一致（左边距、上边距、右边距、下边距）
        self.preview_layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建预览标签
        self.image_label = DraggableImageLabel(self.portrait_count)
        # 设置最小尺寸为16:9比例
        self.image_label.setMinimumSize(800, 450)  # 16:9比例的最小尺寸
        self.image_label.setFrameShape(QFrame.Box)
        # 确保预览标签保持16:9的宽高比
        self.image_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.preview_layout.addWidget(self.image_label)
        
        content_layout.addWidget(self.preview_group, 2)
        
        # 初始化定时器用于延迟刷新
        from PyQt5.QtCore import QTimer
        self.resize_timer = QTimer(self)
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.on_resize_finished)
        
        # 存储当前背景图片路径
        self.current_background = ""
        
        # 监听窗口大小变化事件
        self.resizeEvent = self.on_resize
    
    def on_resize(self, event):
        """处理窗口大小变化事件"""
        # 调用父类方法
        super().resizeEvent(event)
        
        # 固定使用1280×720作为内部画布尺寸
        CANVAS_WIDTH = 1280
        CANVAS_HEIGHT = 720
        
        # 获取可用空间大小（减去布局边距）
        margins = self.preview_layout.contentsMargins()
        left = margins.left()
        top = margins.top()
        right = margins.right()
        bottom = margins.bottom()
        
        # 确保可用空间至少为最小尺寸
        available_width = max(200, self.preview_group.width() - left - right)
        available_height = max(150, self.preview_group.height() - top - bottom)
        
        # 计算缩放比例，确保1280×720的画布能完整显示在可用空间内
        scale = min(available_width / CANVAS_WIDTH, available_height / CANVAS_HEIGHT)
        
        # 确保缩放比例不为零
        if scale <= 0:
            scale = 0.1
        
        # 计算实际显示尺寸
        display_width = int(CANVAS_WIDTH * scale)
        display_height = int(CANVAS_HEIGHT * scale)
        
        # 确保显示尺寸不为零
        display_width = max(100, display_width)
        display_height = max(100, display_height)
        
        # 设置预览标签的显示尺寸
        self.image_label.setFixedSize(display_width, display_height)
        
        # 设置画布尺寸为固定的1280×720（内部使用）
        if hasattr(self.image_label, 'set_canvas_size'):
            self.image_label.set_canvas_size(CANVAS_WIDTH, CANVAS_HEIGHT)
        
        # 启动定时器，当用户停止调整窗口大小200毫秒后执行刷新
        self.resize_timer.start(200)
    
    def on_resize_finished(self):
        """窗口调整大小完成后执行的方法"""
        # 刷新背景图片（如果有）
        if self.current_background and self.controller:
            self.controller.refresh_background(self.current_background)
    
    def update_background(self, image_path):
        """更新背景图片并保存路径"""
        # 保存当前背景图片路径
        self.current_background = image_path
        
    def toggle_fullscreen(self):
        """切换全屏模式"""
        if self.is_fullscreen:
            # 退出全屏
            self.showNormal()
            self.is_fullscreen = False
        else:
            # 进入全屏
            self.showFullScreen()
            self.is_fullscreen = True
        
        # 全屏切换后刷新背景图片
        if self.current_background and self.controller:
            self.controller.refresh_background(self.current_background)
    
    def init_media_players(self):
        """初始化媒体播放器"""
        # 创建BGM播放器
        self.bgm_player = QMediaPlayer()
        # 设置BGM自动循环播放
        self.bgm_player.mediaStatusChanged.connect(self.on_bgm_status_changed)
        
        # 创建音效播放器
        self.sound_player = QMediaPlayer()
        
        # 创建语音播放器
        self.voice_player = QMediaPlayer()
    
    def on_bgm_status_changed(self, status):
        """处理BGM播放状态变化，实现循环播放"""
        from PyQt5.QtMultimedia import QMediaPlayer
        # 当BGM播放结束时，重新播放
        if status == QMediaPlayer.EndOfMedia and self.bgm_player.mediaStatus() != QMediaPlayer.NoMedia:
            self.bgm_player.setPosition(0)
            self.bgm_player.play()
    
    def set_controller(self, controller):
        """设置控制器
        
        Args:
            controller: 控制器对象
        """
        self.controller = controller
        
        # 连接信号和槽
        self.connect_signals()
        
        # 为了防止文本框内容变化过于频繁导致命令历史过多，我们使用定时器延迟处理
        from PyQt5.QtCore import QTimer
        self.text_change_timer = QTimer(self)
        self.text_change_timer.setSingleShot(True)
        self.text_change_timer.setInterval(500)  # 500毫秒延迟
        self.text_change_timer.timeout.connect(self._on_text_change_timeout)
        
        # 存储文本框当前内容，用于比较是否真正发生变化
        self.last_text_content = self.text_edit.toPlainText()
    
    def connect_signals(self):
        """连接信号和槽"""
        # 连接按钮信号
        self.btn_new.clicked.connect(self.controller.on_new_project)
        self.btn_open.clicked.connect(self.controller.on_open_project)
        self.btn_save.clicked.connect(self.controller.on_save_project)
        
        # 仅添加全屏快捷键 (Alt+Enter)
        from PyQt5.QtWidgets import QShortcut
        from PyQt5.QtGui import QKeySequence
        self.fullscreen_shortcut = QShortcut(QKeySequence("Alt+Return"), self)
        self.fullscreen_shortcut.activated.connect(self.toggle_fullscreen)
        
        # 连接下拉框信号
        self.combo_bg.currentIndexChanged.connect(self.controller.on_background_changed)
        
        # 连接立绘下拉框和滑块信号
        for i, (combo, slider) in enumerate(zip(self.portrait_combos, self.portrait_scale_sliders)):
            combo.currentIndexChanged.connect(lambda idx, i=i: self.controller.on_portrait_changed(idx, i))
            slider.valueChanged.connect(lambda val, i=i: self.controller.on_portrait_scale_changed(val, i))
        
        # 连接立绘位置变化信号到控制器的保存方法
        self.image_label.portrait_position_changed.connect(self.controller.on_portrait_position_changed)
        
        # 连接音频下拉框信号
        self.combo_bgm.currentIndexChanged.connect(self.controller.on_bgm_changed)
        self.combo_sound.currentIndexChanged.connect(self.controller.on_sound_changed)
        self.combo_voice.currentIndexChanged.connect(self.controller.on_voice_changed)
        
        # 连接字体下拉框和字体大小滑块信号
        self.combo_font.currentIndexChanged.connect(self.controller.on_font_changed)
        self.slider_font_size.valueChanged.connect(self.controller.on_font_size_changed)
        
        # 连接角色姓名更新按钮信号
        self.btn_update_name.clicked.connect(self.controller.on_name_updated)
        
        # 连接导入语音按钮信号
        self.btn_import_voice.clicked.connect(self.controller.import_voice_file)
        
        # 连接文本框内容变化信号
        self.text_edit.textChanged.connect(self._on_text_changed)
    
    def _on_text_changed(self):
        """文本内容变化时的处理函数"""
        # 每次文本变化时，重新启动定时器
        self.text_change_timer.start()
    
    def _on_text_change_timeout(self):
        """定时器超时后的处理函数，检查文本是否真正变化并通知控制器"""
        current_text = self.text_edit.toPlainText()
        if current_text != self.last_text_content:
            # 文本确实发生了变化，通知控制器
            if hasattr(self.controller, 'on_text_changed'):
                self.controller.on_text_changed(self.last_text_content, current_text)
            self.last_text_content = current_text
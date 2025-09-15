"""可拖动图像标签组件

用于显示和拖动背景和立绘
"""
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter


class DraggableImageLabel(QLabel):
    """可拖动图像标签组件，用于显示和拖动背景和立绘"""
    
    # 添加信号：立绘位置变化信号
    portrait_position_changed = pyqtSignal(int, int, int, int, int)  # 索引, old_x, old_y, new_x, new_y
    
    def __init__(self, max_portraits=4):
        """初始化可拖动图像标签
        
        Args:
            max_portraits: 最大立绘数量
        """
        super().__init__()
        self.background = None
        self.portraits = [None] * max_portraits  # 立绘列表
        self.portrait_positions = [QPoint(0, 0)] * max_portraits
        self.scale_factors = [1.0] * max_portraits  # 默认缩放比例的列表
        self.current_drag_index = 0
        self.drag_start_pos = None
        self.setAcceptDrops(True)
        # 默认画布尺寸为1280×720
        self.canvas_width = 1280
        self.canvas_height = 720
        self.display_scale = 1.0
    
    def set_canvas_size(self, width, height):
        """设置内部画布尺寸
        
        Args:
            width: 画布宽度
            height: 画布高度
        """
        self.canvas_width = width
        self.canvas_height = height
        # 计算显示缩放比例
        if self.width() > 0 and self.height() > 0:
            self.display_scale = min(self.width() / width, self.height() / height)
        # 重新绘制显示
        self.update_display()

    def resizeEvent(self, event):
        """处理控件大小变化事件"""
        # 调用父类方法
        super().resizeEvent(event)
        
        # 计算显示缩放比例，并确保它不为零
        if self.canvas_width > 0 and self.canvas_height > 0:
            scale = min(self.width() / self.canvas_width, self.height() / self.canvas_height)
            # 确保缩放比例不为零
            self.display_scale = max(0.1, scale)
        else:
            self.display_scale = 1.0
        
        # 刷新显示
        self.update_display()
    
    def set_background(self, pixmap):
        """设置背景图片
        
        Args:
            pixmap: 背景图片
        """
        # 处理"无背景"：清空背景图片，恢复默认背景色
        if pixmap is None:
            self.background = None
            self.update_display()
            return

        # 背景缩放逻辑：基于固定的画布尺寸进行缩放
        scaled_pixmap = pixmap.scaled(
            self.canvas_width, self.canvas_height,  # 按画布尺寸缩放
            Qt.KeepAspectRatioByExpanding,  # 填满画布
            Qt.SmoothTransformation  # 平滑缩放，避免锯齿
        )

        # 创建与画布匹配的QPixmap
        self.background = QPixmap(self.canvas_width, self.canvas_height)
        self.background.fill(Qt.transparent)  # 透明底色，避免干扰

        # 居中绘制（超出部分自动裁剪，确保视觉居中）
        painter = QPainter(self.background)
        offset_x = (self.canvas_width - scaled_pixmap.width()) // 2
        offset_y = (self.canvas_height - scaled_pixmap.height()) // 2
        painter.drawPixmap(offset_x, offset_y, scaled_pixmap)
        painter.end()

        self.update_display()
    
    def set_portrait(self, pixmap, index=0, scale_factor=1.0):
        """设置立绘图片
        
        Args:
            pixmap: 立绘图片
            index: 立绘索引
            scale_factor: 缩放比例
        """
        if index >= len(self.portraits):
            return

        # 添加None值检查
        if pixmap is None:
            self.portraits[index] = None
            self.update_display()
            return

        if pixmap.isNull():
            self.portraits[index] = None
            self.update_display()
            return

        self.scale_factors[index] = scale_factor
        scaled_pixmap = pixmap.scaled(
            int(pixmap.width() * scale_factor),
            int(pixmap.height() * scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.portraits[index] = scaled_pixmap
        self.update_display()
    
    def update_display(self):
        """刷新显示"""
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿
        
        # 计算居中偏移，使画布在控件中居中显示
        offset_x = (self.width() - int(self.canvas_width * self.display_scale)) // 2
        offset_y = (self.height() - int(self.canvas_height * self.display_scale)) // 2
        
        # 绘制背景（如果有）
        if self.background:
            # 缩放背景到显示尺寸并居中绘制
            painter.save()
            painter.translate(offset_x, offset_y)
            painter.scale(self.display_scale, self.display_scale)
            painter.drawPixmap(0, 0, self.background)
            painter.restore()

        # 绘制所有立绘
        for i, portrait in enumerate(self.portraits):
            if portrait:
                # 缩放立绘到显示尺寸并在正确位置绘制
                painter.save()
                painter.translate(offset_x, offset_y)
                painter.scale(self.display_scale, self.display_scale)
                painter.drawPixmap(self.portrait_positions[i], portrait)
                painter.restore()

        painter.end()
        self.setPixmap(pixmap)
    
    def mousePressEvent(self, event):
        """鼠标按下事件
        
        Args:
            event: 鼠标事件
        """
        if event.button() == Qt.LeftButton:
            # 计算居中偏移
            offset_x = (self.width() - int(self.canvas_width * self.display_scale)) // 2
            offset_y = (self.height() - int(self.canvas_height * self.display_scale)) // 2
            
            # 转换为画布坐标
            canvas_x = (event.pos().x() - offset_x) / self.display_scale
            canvas_y = (event.pos().y() - offset_y) / self.display_scale
            
            # 检查点击位置是否在立绘上
            for i, portrait in enumerate(self.portraits):
                if portrait:
                    portrait_rect = portrait.rect().translated(self.portrait_positions[i])
                    if portrait_rect.contains(canvas_x, canvas_y):
                        self.current_drag_index = i
                        self.drag_start_pos = QPoint(canvas_x, canvas_y) - self.portrait_positions[i]
                        break
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件
        
        Args:
            event: 鼠标事件
        """
        if self.drag_start_pos is not None and self.portraits[self.current_drag_index]:
            # 计算居中偏移
            offset_x = (self.width() - int(self.canvas_width * self.display_scale)) // 2
            offset_y = (self.height() - int(self.canvas_height * self.display_scale)) // 2
            
            # 转换为画布坐标
            canvas_x = (event.pos().x() - offset_x) / self.display_scale
            canvas_y = (event.pos().y() - offset_y) / self.display_scale
            
            # 计算新位置
            new_pos = QPoint(canvas_x, canvas_y) - self.drag_start_pos
            
            # 获取当前立绘
            current_portrait = self.portraits[self.current_drag_index]
            
            # 添加边界限制：允许立绘适当超出边界
            # 限制x：允许立绘超出边界一半宽度
            min_x = - current_portrait.width() // 2
            max_x = self.canvas_width - current_portrait.width() // 2
            # 限制y：允许立绘超出边界一半高度
            min_y = - current_portrait.height() // 2
            max_y = self.canvas_height - current_portrait.height() // 2
            
            # 修正位置（确保在边界内）
            new_pos_x = max(min_x, min(new_pos.x(), max_x))
            new_pos_y = max(min_y, min(new_pos.y(), max_y))
            new_pos = QPoint(new_pos_x, new_pos_y)
            
            self.portrait_positions[self.current_drag_index] = new_pos
            self.update_display()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件
        
        Args:
            event: 鼠标事件
        """
        if event.button() == Qt.LeftButton:
            # 保存拖动后的位置
            pos = self.portrait_positions[self.current_drag_index]
            
            # 计算居中偏移
            offset_x = (self.width() - int(self.canvas_width * self.display_scale)) // 2
            offset_y = (self.height() - int(self.canvas_height * self.display_scale)) // 2
            
            # 转换为画布坐标
            canvas_x = (event.pos().x() - offset_x) / self.display_scale
            canvas_y = (event.pos().y() - offset_y) / self.display_scale
            
            # 发射立绘位置变化信号（传递拖动前和拖动后的位置）
            if 0 <= self.current_drag_index < len(self.portraits) and self.drag_start_pos is not None:
                # 计算拖动前的位置
                old_x = pos.x() - (canvas_x - (self.drag_start_pos.x() + self.portrait_positions[self.current_drag_index].x()))
                old_y = pos.y() - (canvas_y - (self.drag_start_pos.y() + self.portrait_positions[self.current_drag_index].y()))
                # 发射信号，包含旧位置和新位置
                self.portrait_position_changed.emit(self.current_drag_index, old_x, old_y, pos.x(), pos.y())
                
            self.drag_start_pos = None
            
    def set_portrait_position(self, index, x, y):
        """设置立绘位置
        
        Args:
            index: 立绘索引
            x: x坐标 - 基于画布坐标系统
            y: y坐标 - 基于画布坐标系统
        """
        if index >= len(self.portraits):
            return
            
        # 获取当前立绘（如果存在）
        current_portrait = self.portraits[index]
        if current_portrait:
            # 添加边界限制：允许立绘适当超出边界
            # 限制x：允许立绘超出边界一半宽度
            min_x = - current_portrait.width() // 2
            max_x = self.canvas_width - current_portrait.width() // 2
            # 限制y：允许立绘超出边界一半高度
            min_y = - current_portrait.height() // 2
            max_y = self.canvas_height - current_portrait.height() // 2
            
            # 修正位置（确保在边界内）
            x = max(min_x, min(x, max_x))
            y = max(min_y, min(y, max_y))
        
        # 设置位置
        self.portrait_positions[index] = QPoint(x, y)
        self.update_display()
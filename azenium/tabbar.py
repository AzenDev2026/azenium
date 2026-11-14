"""Azenium 自定义标签栏：双击空白处新建标签，中键点击关闭标签。"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QTabBar


class BrowserTabBar(QTabBar):
    """独立标签栏（与 QStackedWidget 配合，标签栏位于工具栏上方）。"""

    new_tab_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setExpanding(False)          # 标签宽度按内容自适应
        self.setMovable(True)             # 可拖动排序
        self.setTabsClosable(True)        # 每个标签带关闭按钮
        self.setUsesScrollButtons(True)   # 标签过多时可滚动
        self.setElideMode(Qt.TextElideMode.ElideRight)
        self.setDocumentMode(True)
        self.setDrawBase(False)

    # -- 双击空白处 → 新建标签 ------------------------------------------------
    def mouseDoubleClickEvent(self, event):
        pos = event.position().toPoint()
        if self.tabAt(pos) == -1:
            self.new_tab_requested.emit()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)

    # -- 中键点击标签 → 关闭 --------------------------------------------------
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            index = self.tabAt(event.position().toPoint())
            if index >= 0:
                self.tabCloseRequested.emit(index)
                event.accept()
                return
        super().mouseReleaseEvent(event)

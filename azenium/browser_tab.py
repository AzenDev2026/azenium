"""Azenium 标签页：封装 QWebEngineView（Chromium 内核）并提供状态信号。"""

from urllib.parse import quote

from PyQt6.QtCore import QUrl, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView


def resolve_url(text: str, fallback_url: str) -> QUrl:
    """把地址栏输入转成可导航的 URL。

    规则：
    - 空输入 → 打开新标签页地址（https://azen.dev/search）
    - 已带协议（http/https/file/about）→ 原样使用
    - localhost → http://localhost
    - 含点且无空格（像域名）→ 自动补 https://
    - 其余 → Google 搜索（与 azen.dev/search 网页的搜索行为一致）
    """
    t = text.strip()
    if not t:
        return QUrl(fallback_url)
    if t == "localhost" or t.startswith("localhost:"):
        return QUrl("http://" + t)
    if t.startswith(("http://", "https://", "file://", "about:", "data:")):
        return QUrl(t)
    if "." in t and " " not in t:
        return QUrl("https://" + t)
    return QUrl("https://www.google.com/search?q=" + quote(t))


class BrowserTab(QWidget):
    """一个标签页：内部是一个 Chromium 内核的网页视图。"""

    title_changed = pyqtSignal(object, str)     # (tab, 标题)
    icon_changed = pyqtSignal(object, object)   # (tab, QIcon)
    url_changed = pyqtSignal(object, object)    # (tab, QUrl)
    loading_changed = pyqtSignal(object, bool)  # (tab, 是否加载中)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = QWebEngineView(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.view)

        self.view.titleChanged.connect(lambda t: self.title_changed.emit(self, t))
        self.view.iconChanged.connect(lambda i: self.icon_changed.emit(self, i))
        self.view.urlChanged.connect(lambda u: self.url_changed.emit(self, u))
        self.view.loadStarted.connect(lambda: self.loading_changed.emit(self, True))
        self.view.loadFinished.connect(lambda _: self.loading_changed.emit(self, False))

    # ------------------------------------------------------------------
    def load(self, url):
        """加载 QUrl 或字符串地址。"""
        self.view.load(url if isinstance(url, QUrl) else QUrl(url))

    def zoom_factor(self) -> float:
        return self.view.zoomFactor()

    def set_zoom_factor(self, factor: float) -> None:
        self.view.setZoomFactor(factor)

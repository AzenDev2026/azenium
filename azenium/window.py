"""Azenium 主窗口：标签栏 + 工具栏（导航/地址栏）+ 网页区。"""

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QAction, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QStackedWidget,
    QStyle,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from . import APP_NAME, APP_VERSION, HOMEPAGE
from . import config, theme
from .browser_tab import BrowserTab, resolve_url
from .settings_dialog import SettingsDialog
from .tabbar import BrowserTabBar


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cfg = config.load()
        self._urlbar_editing = False  # 用户正在地址栏里输入时，不覆盖文本

        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")
        self.resize(1200, 780)

        # ---------- 中央布局：标签栏 / 工具栏 / 网页堆栈 -------------------
        central = QWidget(self)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.tab_bar = BrowserTabBar(central)
        self.stack = QStackedWidget(central)

        self.toolbar = self._build_toolbar(central)

        root.addWidget(self.tab_bar)
        root.addWidget(self.toolbar)
        root.addWidget(self.stack, 1)
        self.setCentralWidget(central)

        # ---------- 信号连接 ------------------------------------------------
        self.tab_bar.currentChanged.connect(self._on_current_changed)
        self.tab_bar.tabCloseRequested.connect(self._close_tab)
        self.tab_bar.tabMoved.connect(self._on_tab_moved)
        self.tab_bar.new_tab_requested.connect(self._new_tab)

        self.urlbar.returnPressed.connect(self._navigate)

        self._setup_shortcuts()
        self._apply_theme()

        # 启动时打开一个新标签页（默认 https://azen.dev/search）
        self._new_tab()

    # ==================================================================
    # 工具栏
    # ==================================================================
    def _build_toolbar(self, parent) -> QToolBar:
        toolbar = QToolBar(parent)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)

        style = self.style()

        def nav_button(sp, tip):
            btn = QToolButton(toolbar)
            btn.setIcon(style.standardIcon(sp))
            btn.setToolTip(tip)
            btn.setAutoRaise(True)
            toolbar.addWidget(btn)
            return btn

        self.back_btn = nav_button(QStyle.StandardPixmap.SP_ArrowBack, "后退 (Alt+←)")
        self.fwd_btn = nav_button(QStyle.StandardPixmap.SP_ArrowForward, "前进 (Alt+→)")
        self.reload_btn = nav_button(
            QStyle.StandardPixmap.SP_BrowserReload, "刷新 (F5 / Ctrl+R)"
        )
        self.stop_btn = nav_button(QStyle.StandardPixmap.SP_BrowserStop, "停止 (Esc)")
        self.stop_btn.hide()

        self.back_btn.clicked.connect(lambda: self._current_view().back())
        self.fwd_btn.clicked.connect(lambda: self._current_view().forward())
        self.reload_btn.clicked.connect(lambda: self._current_view().reload())
        self.stop_btn.clicked.connect(lambda: self._current_view().stop())

        # 地址栏
        self.urlbar = QLineEdit(toolbar)
        self.urlbar.setObjectName("urlbar")
        self.urlbar.setPlaceholderText("搜索或输入网址")
        self.urlbar.setClearButtonEnabled(True)
        self.urlbar.textEdited.connect(self._on_urlbar_edited)
        toolbar.addWidget(self.urlbar)

        # 右侧：新标签 / 设置
        self.new_tab_btn = QToolButton(toolbar)
        self.new_tab_btn.setText("＋")
        self.new_tab_btn.setToolTip("新建标签页 (Ctrl+T)")
        self.new_tab_btn.setAutoRaise(True)
        self.new_tab_btn.clicked.connect(self._new_tab)
        toolbar.addWidget(self.new_tab_btn)

        self.settings_btn = QToolButton(toolbar)
        self.settings_btn.setText("⚙")
        self.settings_btn.setToolTip("设置")
        self.settings_btn.setAutoRaise(True)
        self.settings_btn.clicked.connect(self._open_settings)
        toolbar.addWidget(self.settings_btn)

        return toolbar

    # ==================================================================
    # 标签页管理
    # ==================================================================
    def _new_tab(self, url: str | None = None):
        tab = BrowserTab(self.stack)
        self.stack.addWidget(tab)
        index = self.tab_bar.addTab("新标签页")
        self.tab_bar.setCurrentIndex(index)

        tab.title_changed.connect(self._on_tab_title)
        tab.icon_changed.connect(self._on_tab_icon)
        tab.url_changed.connect(self._on_tab_url)
        tab.loading_changed.connect(self._on_tab_loading)

        tab.load(url or self.cfg["new_tab_url"])

    def _close_tab(self, index: int):
        if index < 0 or index >= self.stack.count():
            return
        widget = self.stack.widget(index)
        self.tab_bar.removeTab(index)
        self.stack.removeWidget(widget)
        widget.deleteLater()
        if self.tab_bar.count() == 0:
            # 最后一个标签被关掉时，自动开一个新标签页而不是退出
            self._new_tab()

    def _on_tab_moved(self, frm: int, to: int):
        widget = self.stack.widget(frm)
        self.stack.removeWidget(widget)
        self.stack.insertWidget(to, widget)

    def _current_view(self):
        widget = self.stack.currentWidget()
        return widget.view if widget is not None else None

    def _current_tab(self):
        return self.stack.currentWidget()

    # ==================================================================
    # 标签状态 → 界面同步
    # ==================================================================
    def _on_tab_title(self, tab, title: str):
        index = self.stack.indexOf(tab)
        if index < 0:
            return
        text = title if title else "新标签页"
        self.tab_bar.setTabText(index, text)
        self.tab_bar.setTabToolTip(index, text)
        if index == self.tab_bar.currentIndex():
            self.setWindowTitle(f"{text} — {APP_NAME}")

    def _on_tab_icon(self, tab, icon):
        index = self.stack.indexOf(tab)
        if index >= 0:
            self.tab_bar.setTabIcon(index, icon)

    def _on_tab_url(self, tab, url: QUrl):
        if tab is not self._current_tab() or self._urlbar_editing:
            return
        text = url.toString()
        if text in ("about:blank", ""):
            text = ""
        self.urlbar.setText(text)

    def _on_tab_loading(self, tab, loading: bool):
        if tab is not self._current_tab():
            return
        self.reload_btn.setVisible(not loading)
        self.stop_btn.setVisible(loading)
        self._sync_nav_state(tab)

    def _on_current_changed(self, index: int):
        if index < 0:
            return
        tab = self.stack.widget(index)
        self.stack.setCurrentIndex(index)
        self._sync_nav_state(tab)
        if not self._urlbar_editing:
            text = tab.view.url().toString()
            self.urlbar.setText("" if text == "about:blank" else text)
        self.setWindowTitle(f"{tab.view.title() or '新标签页'} — {APP_NAME}")

    def _sync_nav_state(self, tab):
        view = tab.view
        history = view.history()
        self.back_btn.setEnabled(history.canGoBack())
        self.fwd_btn.setEnabled(history.canGoForward())
        self.reload_btn.setEnabled(not view.isLoading())

    # ==================================================================
    # 地址栏
    # ==================================================================
    def _on_urlbar_edited(self, _text: str):
        self._urlbar_editing = True

    def _navigate(self):
        view = self._current_view()
        if view is None:
            return
        url = resolve_url(self.urlbar.text(), self.cfg["new_tab_url"])
        view.load(url)
        self._urlbar_editing = False

    # ==================================================================
    # 快捷键
    # ==================================================================
    def _setup_shortcuts(self):
        def bind(seq, slot):
            sc = QShortcut(QKeySequence(seq), self)
            sc.activated.connect(slot)

        bind("Ctrl+T", self._new_tab)
        bind("Ctrl+W", lambda: self._close_tab(self.tab_bar.currentIndex()))
        bind("Ctrl+L", self._focus_urlbar)
        bind("Ctrl+Tab", self._next_tab)
        bind("Ctrl+PgDown", self._next_tab)
        bind("Ctrl+Shift+Tab", self._prev_tab)
        bind("Ctrl+PgUp", self._prev_tab)
        bind("F5", lambda: self._current_view().reload())
        bind("Ctrl+R", lambda: self._current_view().reload())
        bind("Esc", lambda: self._current_view().stop())
        bind("Alt+Left", lambda: self._current_view().back())
        bind("Alt+Right", lambda: self._current_view().forward())
        bind("Ctrl+=", lambda: self._zoom(0.25))
        bind("Ctrl+-", lambda: self._zoom(-0.25))
        bind("Ctrl+0", lambda: self._set_zoom(1.0))
        for i in range(1, 9):
            bind(f"Ctrl+{i}", lambda i=i: self.tab_bar.setCurrentIndex(i - 1))

        # 菜单项（Alt 显示菜单栏时也能用）
        menu = self.menuBar().addMenu("&标签页")
        act = QAction("新建标签页", self)
        act.setShortcut(QKeySequence("Ctrl+T"))
        act.triggered.connect(self._new_tab)
        menu.addAction(act)

    def _focus_urlbar(self):
        self.urlbar.setFocus()
        self.urlbar.selectAll()

    def _next_tab(self):
        count = self.tab_bar.count()
        if count:
            self.tab_bar.setCurrentIndex((self.tab_bar.currentIndex() + 1) % count)

    def _prev_tab(self):
        count = self.tab_bar.count()
        if count:
            self.tab_bar.setCurrentIndex((self.tab_bar.currentIndex() - 1) % count)

    def _zoom(self, delta: float):
        view = self._current_view()
        if view is not None:
            view.setZoomFactor(max(0.25, min(4.0, view.zoomFactor() + delta)))

    def _set_zoom(self, factor: float):
        view = self._current_view()
        if view is not None:
            view.setZoomFactor(factor)

    # ==================================================================
    # 设置与主题
    # ==================================================================
    def _open_settings(self):
        dialog = SettingsDialog(self.cfg, self)
        if dialog.exec() == SettingsDialog.DialogCode.Accepted:
            self.cfg = dialog.result_config()
            config.save(self.cfg)
            self._apply_theme()

    def _apply_theme(self):
        app = QApplication.instance()
        theme.apply_palette(app, self.cfg["theme"])
        qss = theme.build_qss(self.cfg["style"], self.cfg["theme"], self.cfg["font_size"])
        app.setStyleSheet(qss)

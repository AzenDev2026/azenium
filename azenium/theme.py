"""Azenium 主题系统：三种 UI 风格 × 深浅色，生成 Qt 样式表（QSS）与调色板。"""

from string import Template

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication

# ---------------------------------------------------------------------------
# 深 / 浅 基础调色板
# ---------------------------------------------------------------------------

_DARK = {
    # 以 #202020 为基调的中性灰深色
    "window_bg": "#202020",
    "toolbar_bg": "#262626",
    "surface": "#2d2d2d",
    "surface_hover": "#3a3a3a",
    "text": "#e6e6e6",
    "text_dim": "#9f9f9f",
    "border": "#383838",
    "urlbar_bg": "#282828",
    "tab_active": "#2d2d2d",
    "shadow": "rgba(0,0,0,0.45)",
}

_LIGHT = {
    "window_bg": "#f2f3f6",
    "toolbar_bg": "#fafbfd",
    "surface": "#e7eaef",
    "surface_hover": "#dce0e6",
    "text": "#1b1e23",
    "text_dim": "#60666e",
    "border": "#d3d7dd",
    "urlbar_bg": "#ffffff",
    "tab_active": "#ffffff",
    "shadow": "rgba(0,0,0,0.15)",
}

# ---------------------------------------------------------------------------
# 三种风格的形状与主色
# ---------------------------------------------------------------------------

_STYLES = {
    # 现代：直角利落、蓝色强调、选中标签顶部有一条色带
    "modern": {
        "accent_dark": "#4d8dff",
        "accent_light": "#2f6fe4",
        "accent_soft_dark": "rgba(77,141,255,0.16)",
        "accent_soft_light": "rgba(47,111,228,0.13)",
        "tab_radius": "6px",
        "btn_radius": "6px",
        "urlbar_radius": "8px",
        "tab_pad": "6px 14px",
        "tab_selected_extra": "border-top: 2px solid $accent;",
        "tab_base_extra": "border-top: 2px solid transparent;",
        "toolbar_bottom": "1px solid $border",
        "bold_selected": "font-weight: 500;",
    },
    # 圆润：大圆角胶囊标签、柔和紫色、选中标签带淡彩底
    "rounded": {
        "accent_dark": "#9d7bff",
        "accent_light": "#6d4fd8",
        "accent_soft_dark": "rgba(157,123,255,0.20)",
        "accent_soft_light": "rgba(109,79,216,0.14)",
        "tab_radius": "12px",
        "btn_radius": "10px",
        "urlbar_radius": "14px",
        "tab_pad": "6px 16px",
        "tab_selected_extra": "background: $accent_soft; color: $accent;",
        "tab_base_extra": "",
        "toolbar_bottom": "1px solid $border",
        "bold_selected": "font-weight: 600;",
    },
    # 简洁：极扁、几乎无边框、选中标签仅加粗 + 下划线
    "minimal": {
        "accent_dark": "#9aa4b0",
        "accent_light": "#56606c",
        "accent_soft_dark": "rgba(154,164,176,0.16)",
        "accent_soft_light": "rgba(86,96,108,0.12)",
        "tab_radius": "3px",
        "btn_radius": "4px",
        "urlbar_radius": "6px",
        "tab_pad": "6px 12px",
        "tab_selected_extra": "border-bottom: 2px solid $accent;",
        "tab_base_extra": "border-bottom: 2px solid transparent;",
        "toolbar_bottom": "1px solid transparent",
        "bold_selected": "font-weight: 600;",
    },
}

_QSS = Template(
    """
/* ---------- 全局 ---------- */
QWidget {
    font-size: ${font_size}px;
    color: $text;
}
QMainWindow, QDialog {
    background-color: $window_bg;
}
QLabel[class="hint"] {
    color: $text_dim;
}

/* ---------- 工具栏 ---------- */
QToolBar {
    background: $toolbar_bg;
    border: none;
    border-bottom: $toolbar_bottom;
    padding: 5px 8px;
    spacing: 4px;
}
QToolButton {
    background: transparent;
    border: none;
    border-radius: $btn_radius;
    padding: 6px;
    color: $text;
}
QToolButton:hover {
    background: $surface;
}
QToolButton:pressed {
    background: $surface_hover;
}
QToolButton:disabled {
    color: $text_dim;
    background: transparent;
}

/* ---------- 地址栏 ---------- */
QLineEdit#urlbar {
    background: $urlbar_bg;
    border: 1px solid $border;
    border-radius: $urlbar_radius;
    padding: 6px 14px;
    color: $text;
    selection-background-color: $accent;
    selection-color: $window_bg;
}
QLineEdit#urlbar:focus {
    border: 1px solid $accent;
}

/* ---------- 标签栏 ---------- */
QTabBar {
    background: $toolbar_bg;
    border: none;
}
QTabBar::tab {
    background: transparent;
    color: $text_dim;
    border: none;
    border-radius: $tab_radius;
    padding: $tab_pad;
    margin: 4px 2px;
    $tab_base_extra
}
QTabBar::tab:hover {
    background: $surface;
}
QTabBar::tab:selected {
    background: $tab_active;
    color: $text;
    $bold_selected
    $tab_selected_extra
}

/* ---------- 菜单 ---------- */
QMenuBar {
    background: $toolbar_bg;
    color: $text;
}
QMenuBar::item {
    padding: 4px 10px;
    border-radius: $btn_radius;
}
QMenuBar::item:selected {
    background: $surface;
}
QMenu {
    background: $surface;
    color: $text;
    border: 1px solid $border;
    border-radius: 8px;
    padding: 6px 0;
}
QMenu::item {
    padding: 6px 26px;
    border-radius: 5px;
    margin: 1px 6px;
}
QMenu::item:selected {
    background: $accent_soft;
    color: $accent;
}

/* ---------- 按钮 / 对话框控件 ---------- */
QPushButton {
    background: $surface;
    color: $text;
    border: 1px solid $border;
    border-radius: $btn_radius;
    padding: 7px 18px;
}
QPushButton:hover {
    background: $surface_hover;
}
QPushButton:pressed {
    background: $surface;
}
QPushButton:default {
    background: $accent;
    color: $window_bg;
    border: 1px solid transparent;
    font-weight: 600;
}
QPushButton:default:hover {
    background: $accent;
}
QPushButton:disabled {
    color: $text_dim;
    background: transparent;
}

QRadioButton {
    color: $text;
    spacing: 8px;
    padding: 4px 0;
}
QRadioButton::indicator {
    width: 17px;
    height: 17px;
    border-radius: 9px;
    border: 2px solid $border;
    background: $urlbar_bg;
}
QRadioButton::indicator:checked {
    border: 5px solid $accent;
}

QSpinBox, QComboBox {
    background: $urlbar_bg;
    color: $text;
    border: 1px solid $border;
    border-radius: $btn_radius;
    padding: 4px 8px;
    selection-background-color: $accent;
}
QSpinBox:focus, QComboBox:focus {
    border: 1px solid $accent;
}

/* ---------- 滚动条 ---------- */
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: $surface_hover;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
}

/* ---------- 工具提示 ---------- */
QToolTip {
    background: $surface;
    color: $text;
    border: 1px solid $border;
    padding: 5px 8px;
}
"""
)


def _resolve(template: str, values: dict, depth: int = 8) -> str:
    """递归替换：处理「值里再嵌套 $变量」的情况。

    例如 rounded 风格的 tab_selected_extra 值是
    "background: $accent_soft; color: $accent;"，一次性 substitute
    不会展开这些内层变量，会留下非法 CSS。迭代替换直到没有 $ 残留。
    """
    result = template
    for _ in range(depth):
        result = Template(result).substitute(values)
        if "$" not in result:
            break
    return result


def accent_color(style: str, theme: str) -> str:
    """当前风格/主题的主色（含 #，如 "#5170ff"）。"""
    s = _STYLES.get(style, _STYLES["modern"])
    return s["accent_dark"] if theme == "dark" else s["accent_light"]


def build_qss(style: str, theme: str, font_size: int = 13) -> str:
    """根据风格与主题生成完整样式表。"""
    base = _DARK if theme == "dark" else _LIGHT
    s = _STYLES.get(style, _STYLES["modern"])
    values = dict(base)
    values.update(s)
    values["accent"] = s["accent_dark"] if theme == "dark" else s["accent_light"]
    values["accent_soft"] = (
        s["accent_soft_dark"] if theme == "dark" else s["accent_soft_light"]
    )
    values["font_size"] = font_size
    return _resolve(_QSS.template, values)


def apply_palette(app: QApplication, theme: str) -> None:
    """同步设置 QPalette，让未被 QSS 覆盖的默认图标等也适配深浅色。"""
    dark = theme == "dark"
    p = QPalette()

    p.setColor(QPalette.ColorRole.Window, QColor("#202020" if dark else "#f2f3f6"))
    p.setColor(QPalette.ColorRole.WindowText, QColor("#e6e6e6" if dark else "#1b1e23"))
    p.setColor(QPalette.ColorRole.Base, QColor("#282828" if dark else "#ffffff"))
    p.setColor(QPalette.ColorRole.AlternateBase, QColor("#262626" if dark else "#fafbfd"))
    p.setColor(QPalette.ColorRole.Text, QColor("#e6e6e6" if dark else "#1b1e23"))
    p.setColor(QPalette.ColorRole.Button, QColor("#2d2d2d" if dark else "#e7eaef"))
    p.setColor(QPalette.ColorRole.ButtonText, QColor("#e6e6e6" if dark else "#1b1e23"))
    p.setColor(QPalette.ColorRole.Highlight, QColor("#4d8dff" if dark else "#2f6fe4"))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor("#202020" if dark else "#ffffff"))
    p.setColor(QPalette.ColorRole.ToolTipBase, QColor("#2d2d2d" if dark else "#fafbfd"))
    p.setColor(QPalette.ColorRole.ToolTipText, QColor("#e6e6e6" if dark else "#1b1e23"))
    p.setColor(QPalette.ColorRole.PlaceholderText, QColor("#9f9f9f" if dark else "#60666e"))
    p.setColor(QPalette.ColorRole.Link, QColor("#4d8dff" if dark else "#2f6fe4"))

    app.setPalette(p)

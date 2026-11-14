"""Azenium 设置对话框：UI 风格、深色/浅色模式、新标签页地址、字号。"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
)

STYLE_INFO = {
    "modern": "直角利落，蓝色强调，选中标签顶部带一条色带",
    "rounded": "大圆角胶囊标签，柔和紫色，整体更柔和可爱",
    "minimal": "极简扁平，几乎无边框，选中标签以下划线标示",
}

STYLE_NAMES = {
    "modern": "现代",
    "rounded": "圆润",
    "minimal": "简洁",
}


class SettingsDialog(QDialog):
    def __init__(self, cfg: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Azenium 设置")
        self.setModal(True)
        self._cfg = dict(cfg)

        root = QVBoxLayout(self)
        root.setSpacing(14)

        # ---- 外观风格 ----------------------------------------------------
        style_box = QGroupBox("UI 风格")
        style_layout = QVBoxLayout(style_box)
        self._style_group = QButtonGroup(self)
        for key in ("modern", "rounded", "minimal"):
            radio = QRadioButton(STYLE_NAMES[key], style_box)
            radio.setToolTip(STYLE_INFO[key])
            hint = QLabel(STYLE_INFO[key], style_box)
            hint.setProperty("class", "hint")
            hint.setContentsMargins(26, 0, 0, 2)
            self._style_group.addButton(radio)
            style_layout.addWidget(radio)
            style_layout.addWidget(hint)
            if self._cfg["style"] == key:
                radio.setChecked(True)
        root.addWidget(style_box)

        # ---- 主题 --------------------------------------------------------
        theme_box = QGroupBox("外观模式")
        theme_layout = QHBoxLayout(theme_box)
        self._theme_group = QButtonGroup(self)
        light_radio = QRadioButton("浅色", theme_box)
        dark_radio = QRadioButton("深色", theme_box)
        self._theme_group.addButton(light_radio)
        self._theme_group.addButton(dark_radio)
        (dark_radio if self._cfg["theme"] == "dark" else light_radio).setChecked(True)
        theme_layout.addWidget(light_radio)
        theme_layout.addWidget(dark_radio)
        theme_layout.addStretch(1)
        root.addWidget(theme_box)

        # ---- 新标签页地址 & 字号 ------------------------------------------
        form_box = QGroupBox("常规")
        form = QFormLayout(form_box)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self._url_edit = QLineEdit(self._cfg["new_tab_url"], form_box)
        self._url_edit.setPlaceholderText("https://azen.dev/search")
        form.addRow("新标签页地址", self._url_edit)

        self._font_spin = QSpinBox(form_box)
        self._font_spin.setRange(8, 20)
        self._font_spin.setValue(self._cfg["font_size"])
        self._font_spin.setSuffix(" px")
        form.addRow("界面字号", self._font_spin)
        root.addWidget(form_box)

        # ---- 按钮 --------------------------------------------------------
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel,
            parent=self,
        )
        buttons.button(QDialogButtonBox.StandardButton.Save).setText("保存")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("取消")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)

        self.resize(430, 480)

    # ------------------------------------------------------------------
    def result_config(self) -> dict:
        """按用户选择组装新配置（类型校验与 config 模块保持一致）。"""
        style = "modern"
        for key, radio in zip(("modern", "rounded", "minimal"), self._style_group.buttons()):
            if radio.isChecked():
                style = key
        theme = "light"
        if self._theme_group.buttons()[1].isChecked():
            theme = "dark"

        cfg = dict(self._cfg)
        cfg["style"] = style
        cfg["theme"] = theme
        cfg["font_size"] = self._font_spin.value()
        url = self._url_edit.text().strip()
        cfg["new_tab_url"] = url if url else "https://azen.dev/search"
        return cfg

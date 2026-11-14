"""Azenium settings dialog: UI style, dark/light mode, new tab page, font size."""

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
    "modern": "Sharp corners with a blue accent; selected tab has a top color bar",
    "rounded": "Large-radius capsule tabs, soft purple accent, overall rounder look",
    "minimal": "Ultra-flat, almost borderless; selected tab is underlined",
}

STYLE_NAMES = {
    "modern": "Modern",
    "rounded": "Rounded",
    "minimal": "Minimal",
}


class SettingsDialog(QDialog):
    def __init__(self, cfg: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Azenium Settings")
        self.setModal(True)
        self._cfg = dict(cfg)

        root = QVBoxLayout(self)
        root.setSpacing(14)

        # ---- UI style ----------------------------------------------------
        style_box = QGroupBox("UI Style")
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

        # ---- Color mode ----------------------------------------------------
        theme_box = QGroupBox("Appearance")
        theme_layout = QHBoxLayout(theme_box)
        self._theme_group = QButtonGroup(self)
        light_radio = QRadioButton("Light", theme_box)
        dark_radio = QRadioButton("Dark", theme_box)
        self._theme_group.addButton(light_radio)
        self._theme_group.addButton(dark_radio)
        (dark_radio if self._cfg["theme"] == "dark" else light_radio).setChecked(True)
        theme_layout.addWidget(light_radio)
        theme_layout.addWidget(dark_radio)
        theme_layout.addStretch(1)
        root.addWidget(theme_box)

        # ---- New tab page ---------------------------------------------------
        tab_box = QGroupBox("New Tab Page")
        tab_layout = QVBoxLayout(tab_box)
        self._newtab_group = QButtonGroup(self)
        self._builtin_radio = QRadioButton(
            "Built-in minimal page (logo + search + weather & clock)", tab_box
        )
        self._custom_radio = QRadioButton("Custom URL", tab_box)
        self._newtab_group.addButton(self._builtin_radio)
        self._newtab_group.addButton(self._custom_radio)
        (self._builtin_radio if self._cfg.get("new_tab") != "custom"
         else self._custom_radio).setChecked(True)
        tab_layout.addWidget(self._builtin_radio)
        tab_layout.addWidget(self._custom_radio)

        self._url_edit = QLineEdit(self._cfg["new_tab_url"], tab_box)
        self._url_edit.setPlaceholderText("https://azen.dev/search")
        self._url_edit.setEnabled(self._cfg.get("new_tab") == "custom")
        self._custom_radio.toggled.connect(self._url_edit.setEnabled)
        tab_layout.addWidget(self._url_edit)
        root.addWidget(tab_box)

        form_box = QGroupBox("General")
        form = QFormLayout(form_box)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self._font_spin = QSpinBox(form_box)
        self._font_spin.setRange(8, 20)
        self._font_spin.setValue(self._cfg["font_size"])
        self._font_spin.setSuffix(" px")
        form.addRow("UI font size", self._font_spin)
        root.addWidget(form_box)

        # ---- Buttons --------------------------------------------------------
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel,
            parent=self,
        )
        buttons.button(QDialogButtonBox.StandardButton.Save).setText("Save")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancel")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)

        self.resize(430, 480)

    # ------------------------------------------------------------------
    def result_config(self) -> dict:
        """Assemble the new config from the current selection."""
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
        cfg["new_tab"] = "custom" if self._custom_radio.isChecked() else "builtin"
        url = self._url_edit.text().strip()
        cfg["new_tab_url"] = url if url else "https://azen.dev/search"
        return cfg

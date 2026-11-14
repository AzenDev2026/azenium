"""Azenium 启动入口。"""

import sys
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

# 注意：必须在创建 QApplication 之前导入窗口模块，
# 这样 QtWebEngine（Chromium 内核）才能正确初始化。
from azenium import APP_NAME, APP_VERSION
from azenium.window import BrowserWindow

ASSETS_DIR = Path(__file__).resolve().parent / "assets"


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setDesktopFileName("azenium")  # KDE 任务栏/启动器图标关联

    icon_path = ASSETS_DIR / "azenium.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = BrowserWindow()
    window.setWindowIcon(app.windowIcon())
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

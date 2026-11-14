"""Azenium 启动入口。"""

import sys

from PyQt6.QtWidgets import QApplication

# 注意：必须在创建 QApplication 之前导入窗口模块，
# 这样 QtWebEngine（Chromium 内核）才能正确初始化。
from azenium import APP_NAME, APP_VERSION
from azenium.window import BrowserWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)

    window = BrowserWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

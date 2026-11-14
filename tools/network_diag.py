"""Azenium 网络诊断：用浏览器内核直接加载 Google，打印结果。

用法：.venv/bin/python tools/network_diag.py
如果 Google 能加载，说明浏览器本身没问题（之前的报错可能是瞬时断网）；
如果报错，把完整输出发给开发者排查。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtWidgets import QApplication

from azenium.window import BrowserWindow


def main() -> int:
    app = QApplication(sys.argv)
    win = BrowserWindow()
    win.show()
    view = win._current_view()

    def report():
        print("=" * 50)
        print("URL  :", view.url().toString())
        print("Title:", repr(view.title()))
        print("=" * 50)
        if "google" in view.title().lower():
            print("✅ Google 加载正常，浏览器网络没有问题")
        else:
            print("❌ Google 加载失败，请把以上输出复制给开发者")
        app.quit()

    def start():
        print("正在加载 https://www.google.com …（约 15 秒）")
        view.load(QUrl("https://www.google.com"))
        QTimer.singleShot(15000, report)

    # 等事件循环跑起来、视图就绪后再加载
    QTimer.singleShot(500, start)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

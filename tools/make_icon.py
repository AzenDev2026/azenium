"""Azenium 图标工具：从用户设计的 assets/azenium.png 生成多尺寸图标。

用法：.venv/bin/python tools/make_icon.py
说明：主图标由 AzenDev2026 设计（500×500 PNG），本脚本负责把它
缩放到窗口图标（256）与 hicolor 全套尺寸（16~512），供安装使用。
"""

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
HICOLOR = ASSETS / "icons" / "hicolor"
SOURCE = ASSETS / "azenium.png"

SIZES = (512, 256, 128, 64, 48, 32, 24, 16)


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"找不到 {SOURCE}，请先把设计好的图标放到该路径。")

    img = QImage(str(SOURCE))
    if img.isNull():
        raise SystemExit(f"{SOURCE} 不是有效的图片。")
    print(f"源图标: {img.width()}x{img.height()}")

    # 窗口图标：256
    window = img.scaled(
        256, 256, Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )
    window.save(str(SOURCE))
    print(f"✓ {SOURCE.relative_to(ROOT)} (256x256)")

    # hicolor 全套
    for size in SIZES:
        scaled = img.scaled(
            size, size, Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        out = HICOLOR / f"{size}x{size}" / "apps" / "azenium.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        scaled.save(str(out))
        print(f"✓ {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

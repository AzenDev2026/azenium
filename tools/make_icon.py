"""生成 Azenium 图标（多尺寸 PNG），用 Qt QPainter 离屏渲染。

运行：.venv/bin/python tools/make_icon.py
输出：assets/azenium.png（256px，窗口图标）
      assets/icons/hicolor/<size>/apps/azenium.png（安装用多尺寸）
"""

from pathlib import Path

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QBrush, QColor, QImage, QLinearGradient, QPainter, QPainterPath, QPen

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
HICOLOR = ASSETS / "icons" / "hicolor"

# 设计基准：512x512 坐标
SIZES = (512, 256, 128, 64, 48, 32, 24, 16)


def render(size: int) -> QImage:
    img = QImage(size, size, QImage.Format.Format_ARGB32)
    img.fill(Qt.GlobalColor.transparent)
    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    s = size / 512.0

    # ---- 渐变圆角底（Azen 蓝 → 紫） ----
    grad = QLinearGradient(0, 0, 512 * s, 512 * s)
    grad.setColorAt(0.0, QColor("#3d7bff"))
    grad.setColorAt(1.0, QColor("#8a5cf6"))
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(grad))
    p.drawRoundedRect(QRectF(4 * s, 4 * s, 504 * s, 504 * s), 118 * s, 118 * s)

    # ---- 倾斜轨道环（后段，模拟浏览器/网络） ----
    p.save()
    p.translate(256 * s, 256 * s)
    p.rotate(-26)
    p.setPen(QPen(QColor(255, 255, 255, 120), 15 * s))
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawEllipse(QRectF(-196 * s, -122 * s, 392 * s, 244 * s))
    p.restore()

    # ---- 地球 ----
    r = 140 * s
    earth = QRectF(256 * s - r, 256 * s - r, 2 * r, 2 * r)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(QColor("#f2f6ff")))
    p.drawEllipse(earth)

    # 经纬线（裁剪在地球内）
    p.save()
    clip = QPainterPath()
    clip.addEllipse(earth)
    p.setClipPath(clip)
    line_pen = QPen(QColor("#3d6fd6"), 7 * s)
    p.setPen(line_pen)
    p.setBrush(Qt.BrushStyle.NoBrush)
    cx, cy = 256 * s, 256 * s
    # 经线（竖椭圆）
    for k in (-0.55, 0.0, 0.55):
        p.drawEllipse(QRectF(cx + k * r - 0.55 * r, cy - r, 1.1 * r, 2 * r))
    # 纬线（赤道 + 上下两条，横椭圆）
    p.drawEllipse(QRectF(cx - r, cy - 0.12 * r, 2 * r, 0.24 * r))
    p.drawEllipse(QRectF(cx - r, cy - 0.62 * r, 2 * r, 0.24 * r))
    p.drawEllipse(QRectF(cx - r, cy + 0.38 * r, 2 * r, 0.24 * r))
    p.restore()

    # 地球描边
    p.setPen(QPen(QColor(255, 255, 255, 210), 6 * s))
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawEllipse(earth)

    # ---- 轨道环（前段，压在地球上方，更有层次） ----
    p.save()
    p.translate(256 * s, 256 * s)
    p.rotate(-26)
    p.setPen(QPen(QColor(255, 255, 255, 235), 15 * s))
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawArc(QRectF(-196 * s, -122 * s, 392 * s, 244 * s), 130 * 16, 210 * 16)
    p.restore()

    p.end()
    return img


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for size in SIZES:
        img = render(size)
        out_dir = HICOLOR / f"{size}x{size}" / "apps"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / "azenium.png"
        img.save(str(out))
        print(f"✓ {out.relative_to(ROOT)}")
    # 窗口图标用 256
    window_icon = ASSETS / "azenium.png"
    render(256).save(str(window_icon))
    print(f"✓ {window_icon.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

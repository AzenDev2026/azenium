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

    # ---- 灰色分段环（像 Chrome 一样被切成 3 段） ----
    # 环中心线半径 191，环宽 38；每段弧 100°，段间缺口 20°
    ring_r = 191 * s
    ring_w = 38 * s
    ring_rect = QRectF(256 * s - ring_r, 256 * s - ring_r, 2 * ring_r, 2 * ring_r)
    p.setPen(QPen(QColor("#e8e9eb"), ring_w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
    p.setBrush(Qt.BrushStyle.NoBrush)
    for start in (-90, 30, 150):
        p.drawArc(ring_rect, start * 16, 100 * 16)

    # ---- 中心淡蓝色圆 ----
    ball_r = 122 * s
    ball = QRectF(256 * s - ball_r, 256 * s - ball_r, 2 * ball_r, 2 * ball_r)
    p.setPen(QPen(QColor(255, 255, 255, 90), 5 * s))
    p.setBrush(QBrush(QColor("#b7d3ff")))
    p.drawEllipse(ball)

    # 淡蓝圆上的高光（左上柔光，让球更有质感）
    p.save()
    hl = QPainterPath()
    hl.addEllipse(QRectF(256 * s - ball_r * 0.62, 256 * s - ball_r * 0.62,
                         ball_r * 1.24, ball_r * 1.24))
    p.setClipPath(hl)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(QColor(255, 255, 255, 46)))
    p.drawEllipse(QRectF(256 * s - ball_r * 0.78, 256 * s - ball_r * 1.02,
                         ball_r * 1.56, ball_r * 1.2))
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

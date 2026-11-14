#!/usr/bin/env bash
# Azenium 启动脚本
cd "$(dirname "$0")"

# 若在 Wayland 会话下遇到渲染问题（花屏 / 网页区域黑屏 / 闪退），
# 取消下面这行的注释，强制走 XWayland 兼容模式再启动：
# export QT_QPA_PLATFORM=xcb

exec python3 main.py "$@"

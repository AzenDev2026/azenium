#!/usr/bin/env bash
# Azenium 启动脚本
cd "$(dirname "$0")"

# 使用项目自带的虚拟环境（Qt 全家桶版本自洽，避免与系统 Qt 混用崩溃）
if [ ! -x ".venv/bin/python3" ]; then
    echo "未找到 .venv，正在创建并安装依赖（首次约 1-2 分钟）..."
    python3 -m venv .venv
    .venv/bin/pip install -q "PyQt6==6.11.0" "PyQt6-WebEngine==6.11.0" || exit 1
    echo "依赖安装完成。"
fi

# 若在 Wayland 会话下遇到渲染问题（花屏 / 网页区域黑屏 / 闪退），
# 取消下面这行的注释，强制走 XWayland 兼容模式再启动：
# export QT_QPA_PLATFORM=xcb

# 网络稳定性：关闭 QUIC（UDP，部分路由器/运营商拦截会导致
# ERR_NETWORK_ACCESS_DENIED）并忽略系统代理，走传统 TCP 直连。
# 如果你确认网络没问题，可以删掉这行。
export QTWEBENGINE_CHROMIUM_FLAGS="--no-proxy-server --disable-quic"

exec .venv/bin/python3 main.py "$@"

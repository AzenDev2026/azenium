#!/usr/bin/env bash
# Azenium 安装脚本：把浏览器装到当前用户的应用菜单 + 图标主题
# （全部写入用户目录，不需要 sudo）
set -e

cd "$(dirname "$0")"
PROJECT_DIR="$(pwd)"

ICON_BASE="$HOME/.local/share/icons"
APP_BASE="$HOME/.local/share/applications"

echo "== Azenium 安装 =="
echo "项目目录: $PROJECT_DIR"

# 1. 图标 → ~/.local/share/icons/hicolor
echo "[1/3] 安装图标..."
mkdir -p "$ICON_BASE"
if [ -d "assets/icons/hicolor" ]; then
    cp -r assets/icons/hicolor/. "$ICON_BASE/hicolor/"
    echo "      ✓ 图标已安装到 $ICON_BASE/hicolor"
else
    echo "      ⚠ 未找到图标目录，先运行: .venv/bin/python tools/make_icon.py"
fi

# 2. .desktop 入口
echo "[2/3] 写入应用菜单入口..."
mkdir -p "$APP_BASE"
cat > "$APP_BASE/azenium.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Azenium
GenericName=Web Browser
Comment=Azenium - Chromium-based lightweight web browser
Exec=$PROJECT_DIR/run.sh
Icon=azenium
Terminal=false
Categories=Network;WebBrowser;
Keywords=browser;web;internet;azen;
StartupWMClass=Azenium
EOF
echo "      ✓ 已写入 $APP_BASE/azenium.desktop"

# 3. 刷新缓存
echo "[3/3] 刷新桌面数据库..."
update-desktop-database "$APP_BASE" 2>/dev/null || true
command -v kbuildsycoca6 >/dev/null 2>&1 && kbuildsycoca6 2>/dev/null || true

echo ""
echo "✅ Azenium 安装完成！"
echo "   现在可以在应用菜单（KDE 开始菜单 → Internet）里找到 Azenium，"
echo "   也可以右键桌面 → 创建链接到应用 → Azenium，把它放到桌面上。"

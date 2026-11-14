# Azenium 🐋

Azen 的第一款浏览器 —— 基于 **Chromium 内核**（QtWebEngine）的轻量多标签浏览器。

> 内核版本：Chromium 130+（随 Qt 6.11 WebEngine）｜ 开发语言：Python 3 + PyQt6

## ✨ 功能（v0.1.0）

- **多标签页浏览**
  - `Ctrl+T` 或双击标签栏空白处 → 新建标签
  - `Ctrl+W`、点击 ✕ 或中键点标签 → 关闭标签
  - 拖动标签可排序，`Ctrl+Tab` / `Ctrl+PgUp` 切换
- **智能地址栏**
  - 输入网址自动补全 `https://`
  - 输入普通文字 → 自动用 Google 搜索（与 azen.dev/search 网页行为一致）
- **新标签页** 默认打开 <https://azen.dev/search>（可在设置中修改）
- **外观设置**（⚙ 按钮打开）
  - UI 风格：**现代**（直角蓝色）/ **圆润**（胶囊紫色）/ **简洁**（极简扁平）
  - 外观模式：**深色** / **浅色**，保存后即时生效
  - 界面字号可调（8–20px）
- **配置持久化**：所有设置保存在 `~/.azenium/settings.json`

## 🚀 运行

```bash
cd ~/Desktop/azenium
./run.sh          # 首次运行会自动创建 .venv 并安装依赖
```

`run.sh` 使用项目自带的虚拟环境（`.venv`），里面是配套的
**PyQt6 6.11 + QtWebEngine 6.11（Chromium 内核）** 全家桶。

> ⚠️ 版本必须配套：系统 pacman 的 `python-pyqt6 6.12`（Qt 6.12）不能与 pip 的
> WebEngine 混用——pip 版 WebEngine 是独立 Qt 库，与系统 Qt 私有 API 不匹配，
> 会导致 Chromium 子进程崩溃（"Invalid file descriptor to ICU data received"）。
> 因此本项目固定使用 `.venv` 内的 Qt 6.11.2 全套，`requirements.txt` 锁定版本，**不要升级**。

若在 Wayland 会话下遇到渲染问题（花屏 / 黑屏），编辑 `run.sh`，取消注释
`export QT_QPA_PLATFORM=xcb` 即可走 XWayland 兼容模式。

## ⌨️ 快捷键

| 快捷键 | 功能 |
| --- | --- |
| `Ctrl+T` | 新建标签页 |
| `Ctrl+W` | 关闭当前标签 |
| `Ctrl+L` | 聚焦地址栏 |
| `Ctrl+Tab` / `Ctrl+PgDown` | 下一个标签 |
| `Ctrl+Shift+Tab` / `Ctrl+PgUp` | 上一个标签 |
| `Ctrl+1` … `Ctrl+8` | 跳转到第 N 个标签 |
| `F5` / `Ctrl+R` | 刷新 |
| `Esc` | 停止加载 |
| `Alt+←` / `Alt+→` | 后退 / 前进 |
| `Ctrl+=` / `Ctrl+-` / `Ctrl+0` | 放大 / 缩小 / 重置缩放 |

## 📁 项目结构

```
azenium/
├── main.py                 # 入口
├── run.sh                  # 启动脚本
├── requirements.txt
└── azenium/
    ├── __init__.py         # 应用名与版本
    ├── config.py           # 配置读写（~/.azenium/settings.json）
    ├── theme.py            # 主题：3 风格 × 深浅色 QSS + 调色板
    ├── tabbar.py           # 自定义标签栏（双击新建 / 中键关闭）
    ├── browser_tab.py      # 标签页封装（QWebEngineView + URL 解析）
    ├── settings_dialog.py  # 设置对话框
    └── window.py           # 主窗口
```

## 🗺️ 后续计划

- 书签与历史记录
- 下载管理器
- 扩展支持
- 深色模式跟随网页（prefers-color-scheme 注入）

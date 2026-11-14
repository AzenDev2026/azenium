# Azenium 🐋

Azen's first web browser — a lightweight multi-tab browser powered by the **Chromium engine** (QtWebEngine).

> Engine: Chromium 130+ (Qt 6.11 WebEngine) · Language: Python 3 + PyQt6

## ✨ Features (v0.3.0)

- **Multi-tab browsing**
  - `Ctrl+T` or double-click empty tab bar area → new tab
  - `Ctrl+W`, click ✕ or middle-click a tab → close tab
  - Drag tabs to reorder, `Ctrl+Tab` / `Ctrl+PgUp` to switch
- **Built-in minimal new tab page**
  - Centered search box (slightly below middle) with the Azenium logo & name above
  - Bottom-left **weather widget** (Open-Meteo, no API key; Sydney by default,
    follows location when permitted) and bottom-right **clock**
  - Follows the app theme (dark/light) and style accent color
  - Switchable to a custom URL in Settings
- **Smart address bar**
  - Type a domain → `https://` is added automatically
  - Type plain text → searches Google (same behavior as the new tab search box)
- **Appearance settings** (⚙ button)
  - UI styles: **Modern** (sharp, blue) / **Rounded** (capsule, purple) / **Minimal** (flat, subtle)
  - Color mode: **Dark** (#202020-based) / **Light**, applied instantly
  - UI font size adjustable (8–20px)
- **Persistent settings**: everything is stored in `~/.azenium/settings.json`
- **Desktop integration**: bundled icon, installable into the app menu

## 🚀 Running

```bash
cd ~/Desktop/azenium
./run.sh          # creates .venv and installs dependencies on first run
```

`run.sh` uses the project's own virtual environment (`.venv`) with a matching
**PyQt6 6.11 + QtWebEngine 6.11 (Chromium)** toolchain.

> ⚠️ Versions must match: the system `python-pyqt6 6.12` (Qt 6.12) cannot be mixed
> with pip's WebEngine — the pip wheel ships its own Qt libraries whose private
> APIs are incompatible with the system Qt, which crashes the Chromium child
> process ("Invalid file descriptor to ICU data received"). This project
> therefore pins the full Qt 6.11.2 toolchain inside `.venv` via
> `requirements.txt` — **do not upgrade**.

If you hit rendering issues on Wayland (flicker / black page), edit `run.sh`
and uncomment `export QT_QPA_PLATFORM=xcb` to use XWayland compatibility mode.

## 📦 Install to the app menu (use it like a normal app)

```bash
cd ~/Desktop/azenium
./install.sh      # no sudo needed, installs to your user directory only
```

You will find **Azenium** in your KDE app menu (Internet category). You can also
right-click the desktop → Create link to application → Azenium. To uninstall,
just delete `~/.local/share/applications/azenium.desktop`.

### Regenerating the icon

```bash
.venv/bin/python tools/make_icon.py   # then re-run ./install.sh
```

## ⌨️ Keyboard shortcuts

| Shortcut | Action |
| --- | --- |
| `Ctrl+T` | New tab |
| `Ctrl+W` | Close current tab |
| `Ctrl+L` | Focus address bar |
| `Ctrl+Tab` / `Ctrl+PgDown` | Next tab |
| `Ctrl+Shift+Tab` / `Ctrl+PgUp` | Previous tab |
| `Ctrl+1` … `Ctrl+8` | Jump to tab N |
| `F5` / `Ctrl+R` | Reload |
| `Esc` | Stop loading |
| `Alt+←` / `Alt+→` | Back / Forward |
| `Ctrl+=` / `Ctrl+-` / `Ctrl+0` | Zoom in / out / reset |

## 📁 Project structure

```
azenium/
├── main.py                 # Entry point (window icon / desktop integration)
├── run.sh                  # Launcher (manages .venv)
├── install.sh              # Installer for the app menu
├── requirements.txt
├── assets/
│   ├── azenium.png         # Window icon (designed by AzenDev2026)
│   ├── icons/hicolor/…     # Multi-size icons (for installation)
│   └── newtab/index.html   # Built-in minimal new tab page
├── tools/
│   └── make_icon.py        # Icon resizer (multi-size from assets/azenium.png)
└── azenium/
    ├── __init__.py         # App name & version
    ├── config.py           # Settings persistence (~/.azenium/settings.json)
    ├── theme.py            # Themes: 3 styles × dark/light QSS + palettes
    ├── tabbar.py           # Custom tab bar (double-click new / middle-click close)
    ├── browser_tab.py      # Tab wrapper (QWebEngineView + URL resolution)
    ├── settings_dialog.py  # Settings dialog
    └── window.py           # Main window
```

## 🗺️ Roadmap

- Bookmarks & history
- Download manager
- Extension support
- Dark mode for web content (prefers-color-scheme injection)

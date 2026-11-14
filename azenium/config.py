"""Azenium 配置读写（持久化到 ~/.azenium/settings.json）。"""

import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".azenium"
CONFIG_FILE = CONFIG_DIR / "settings.json"

# 默认配置；load() 时用默认值兜底并对类型做校验，
# 配置文件损坏或缺失都不会影响启动。
DEFAULT_CONFIG: dict = {
    "theme": "dark",        # dark | light
    "style": "rounded",     # modern | rounded | minimal
    "new_tab_url": "https://azen.dev/search",
    "font_size": 13,
}

VALID_THEMES = ("dark", "light")
VALID_STYLES = ("modern", "rounded", "minimal")


def load() -> dict:
    """读取配置，缺失的键和非法值一律回落默认值。"""
    cfg = dict(DEFAULT_CONFIG)
    try:
        if CONFIG_FILE.exists():
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            for key, default in DEFAULT_CONFIG.items():
                value = data.get(key)
                if value is not None and isinstance(value, type(default)):
                    cfg[key] = value
    except (OSError, json.JSONDecodeError):
        pass  # 配置损坏时静默使用默认值
    # 枚举值二次校验
    if cfg["theme"] not in VALID_THEMES:
        cfg["theme"] = DEFAULT_CONFIG["theme"]
    if cfg["style"] not in VALID_STYLES:
        cfg["style"] = DEFAULT_CONFIG["style"]
    if not (8 <= cfg["font_size"] <= 20):
        cfg["font_size"] = DEFAULT_CONFIG["font_size"]
    return cfg


def save(cfg: dict) -> None:
    """把配置写入磁盘（目录不存在时自动创建）。"""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(
            json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except OSError:
        pass  # 写入失败不影响浏览器继续运行

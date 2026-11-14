"""Модуль загрузки и валидации конфигурации из INI-файла."""

import configparser
import os


def load_config(filepath):
    """Считывает и проверяет параметры из INI-файла."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл конфигурации не найден: {filepath}")

    parser = configparser.ConfigParser()
    parser.read(filepath, encoding="utf-8")

    if "settings" not in parser:
        raise ValueError("В конфиге отсутствует секция [settings]")

    cfg = parser["settings"]
    return _extract_settings(cfg)


def _extract_settings(cfg):
    """Извлекает и валидирует обязательные поля настроек."""
    required = ["package_name", "repo_url", "test_mode", "version"]
    for key in required:
        if not cfg.get(key, "").strip():
            raise ValueError(f"Не задан обязательный параметр: {key}")

    test_str = cfg.get("test_mode").strip().lower()
    if test_str not in ("true", "false"):
        raise ValueError("Параметр test_mode должен быть true или false")

    return {
        "package_name": cfg.get("package_name").strip(),
        "repo_url": cfg.get("repo_url").strip(),
        "test_mode": test_str == "true",
        "version": cfg.get("version").strip(),
        "filter_substring": cfg.get("filter_substring", "").strip(),
        "mode": cfg.get("mode", "graph").strip(),
    }

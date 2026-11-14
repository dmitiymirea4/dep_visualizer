"""Модуль получения зависимостей пакетов для Ubuntu apt и тест-режима."""

import gzip
import re
import urllib.request


def fetch_repo_data(repo_url, test_mode):
    """Загружает сырые данные репозитория из файла или по URL."""
    if test_mode:
        with open(repo_url, "r", encoding="utf-8") as file:
            return file.read()

    req = urllib.request.urlopen(repo_url, timeout=15)
    raw = req.read()
    if repo_url.endswith(".gz"):
        return gzip.decompress(raw).decode("utf-8", errors="ignore")
    return raw.decode("utf-8", errors="ignore")


def parse_test_repo(raw_text):
    """Парсит тестовый репозиторий формата A: B C."""
    graph = {}
    for line in raw_text.splitlines():
        if ":" not in line:
            continue
        pkg, deps = line.split(":", 1)
        graph[pkg.strip()] = [d.strip() for d in deps.split() if d.strip()]
    return graph


def parse_apt_packages(raw_text):
    """Парсит индекс пакетов Ubuntu apt в словарь зависимостей."""
    graph = {}
    blocks = raw_text.strip().split("\n\n")
    for block in blocks:
        pkg, ver, deps = _parse_apt_block(block)
        if pkg:
            graph[(pkg, ver)] = deps
    return graph


def _parse_apt_block(block):
    """Извлекает имя, версию и список прямых зависимостей из блока apt."""
    pkg, ver, deps = "", "", []
    for line in block.splitlines():
        if line.startswith("Package: "):
            pkg = line[9:].strip()
        elif line.startswith("Version: "):
            ver = line[9:].strip()
        elif line.startswith("Depends: "):
            deps = _clean_depends(line[9:])
    return pkg, ver, deps


def _clean_depends(dep_str):
    """Очищает строку Depends от версий и альтернатив."""
    result = []
    for item in dep_str.split(","):
        first_alt = item.split("|")[0].strip()
        name = re.sub(r"\(.*?\)", "", first_alt).strip()
        if name:
            result.append(name)
    return result

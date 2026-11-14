"""Главный модуль CLI-приложения визуализации графа зависимостей."""

import sys
from config_loader import load_config
from fetcher import fetch_repo_data, parse_apt_packages, parse_test_repo
from graph_ops import build_dfs_graph, find_reverse_deps
from visualizer import generate_plantuml, show_graph_window


def main():
    """Запускает полный цикл анализа и визуализации зависимостей."""
    if len(sys.argv) < 2:
        print("Ошибка: укажите путь к INI-файлу конфигурации.")
        sys.exit(1)

    cfg = load_config(sys.argv[1])
    raw_data = fetch_repo_data(cfg["repo_url"], cfg["test_mode"])
    raw_graph = _prepare_graph(raw_data, cfg)
    _run_mode(raw_graph, cfg)


def _prepare_graph(raw_data, cfg):
    """Подготавливает словарь зависимостей в зависимости от режима."""
    if cfg["test_mode"]:
        return parse_test_repo(raw_data)

    apt_map = parse_apt_packages(raw_data)
    simple_graph = {}
    for (pkg, _), deps in apt_map.items():
        simple_graph[pkg] = deps
    return simple_graph


def _run_mode(raw_graph, cfg):
    """Выполняет построение графа или поиск обратных зависимостей."""
    pkg = cfg["package_name"]
    sub = cfg["filter_substring"]

    if cfg["mode"] == "reverse":
        rev = find_reverse_deps(pkg, raw_graph, sub)
        print(f"Обратные зависимости для {pkg}: {', '.join(rev)}")
        return

    edges = build_dfs_graph(pkg, raw_graph, sub)
    puml = generate_plantuml(edges)
    print(puml)
    show_graph_window(puml)


if __name__ == "__main__":
    main()

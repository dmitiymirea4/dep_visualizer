"""Модульные тесты для проверки всех этапов визуализатора зависимостей."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath("src"))

from config_loader import load_config
from fetcher import parse_apt_packages, parse_test_repo
from graph_ops import build_dfs_graph, find_reverse_deps
from visualizer import generate_plantuml


class TestDependencyVisualizer(unittest.TestCase):
    """Набор тестов для конфигурации, парсеров, графов и PlantUML."""

    def test_parse_test_repo(self):
        """Проверка разбора тестового графа с циклами."""
        data = "A: B C\nB: A\nC:"
        graph = parse_test_repo(data)
        self.assertEqual(graph["A"], ["B", "C"])

    def test_dfs_with_cycles_and_filter(self):
        """Проверка DFS без рекурсии, защиты от циклов и фильтрации."""
        graph = {"A": ["B", "C_dev"], "B": ["A"], "C_dev": []}
        edges = build_dfs_graph("A", graph, "dev")
        self.assertEqual(edges, [("A", "B"), ("B", "A")])

    def test_reverse_dependencies(self):
        """Проверка поиска обратных зависимостей."""
        graph = {"A": ["B"], "B": ["C"], "C": []}
        rev = find_reverse_deps("C", graph, "")
        self.assertEqual(rev, ["A", "B"])

    def test_apt_parser(self):
        """Проверка разбора формата пакетов Ubuntu apt."""
        apt_txt = "Package: curl\nVersion: 1.0\nDepends: libc6 (>= 2.1)\n"
        parsed = parse_apt_packages(apt_txt)
        self.assertEqual(parsed[("curl", "1.0")], ["libc6"])

    def test_plantuml_generation(self):
        """Проверка генерации синтаксиса PlantUML."""
        puml = generate_plantuml([("A", "B")])
        self.assertIn("@startuml", puml)
        self.assertIn("[A] --> [B]", puml)

    def test_invalid_config(self):
        """Проверка обработки ошибки отсутствующего файла конфига."""
        with self.assertRaises(FileNotFoundError):
            load_config("non_existent.ini")


if __name__ == "__main__":
    unittest.main()

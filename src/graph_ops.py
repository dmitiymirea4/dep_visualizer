"""Модуль построения графа зависимостей и поиска обратных связей."""


def build_dfs_graph(start_pkg, raw_graph, filter_sub):
    """Строит транзитивный граф зависимостей алгоритмом DFS без рекурсии."""
    visited = set()
    edges = []
    stack = [start_pkg]

    while stack:
        curr = stack.pop()
        if curr in visited:
            continue
        visited.add(curr)

        for dep in raw_graph.get(curr, []):
            if filter_sub and filter_sub in dep:
                continue
            edges.append((curr, dep))
            if dep not in visited:
                stack.append(dep)
    return edges


def find_reverse_deps(target_pkg, raw_graph, filter_sub):
    """Находит все пакеты, которые прямо или косвенно зависят от target_pkg."""
    rev_graph = _invert_graph(raw_graph)
    edges = build_dfs_graph(target_pkg, rev_graph, filter_sub)
    dependents = set()
    for _, parent in edges:
        dependents.add(parent)
    return sorted(dependents)


def _invert_graph(raw_graph):
    """Инвертирует направления ребер графа для поиска обратных зависимостей."""
    inverted = {}
    for pkg, deps in raw_graph.items():
        for dep in deps:
            inverted.setdefault(dep, []).append(pkg)
    return inverted

"""Breadth-First Search for an unweighted graph of cities."""

from collections import deque
from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class SearchResult:
    """BFS output: path and the order in which vertices were explored."""

    path: tuple[str, ...]
    explored_order: tuple[str, ...]

    @property
    def found(self) -> bool:
        return bool(self.path)

    @property
    def cost(self) -> int | None:
        """Each edge costs exactly 1; return None if unreachable."""
        return len(self.path) - 1 if self.found else None

    @property
    def explored_nodes(self) -> int:
        return len(self.explored_order)


def bfs_shortest_path(
    graph: Mapping[str, Sequence[str]], start: str, goal: str
) -> SearchResult:
    """Return a minimum-hop path from ``start`` to ``goal`` using BFS.

    Vertices are marked as discovered when enqueued. This prevents cycles and
    preserves shortest-path correctness on unweighted graphs. BFS terminates
    when the goal is taken from the queue.

    Time: O(V + E); auxiliary space: O(V).
    """
    if start not in graph:
        raise ValueError(f"Unknown start city: {start}")
    if goal not in graph:
        raise ValueError(f"Unknown destination city: {goal}")

    queue = deque([start])
    parents: dict[str, str | None] = {start: None}
    explored: list[str] = []

    while queue:
        current = queue.popleft()
        explored.append(current)

        if current == goal:
            reversed_path: list[str] = []
            node: str | None = goal
            while node is not None:
                reversed_path.append(node)
                node = parents[node]
            reversed_path.reverse()
            return SearchResult(tuple(reversed_path), tuple(explored))

        for neighbor in graph[current]:
            if neighbor not in graph:
                raise ValueError(f"Graph references undefined city: {neighbor}")
            if neighbor not in parents:
                parents[neighbor] = current
                queue.append(neighbor)

    return SearchResult((), tuple(explored))

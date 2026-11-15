"""Small, illustrative city network for an AI search-algorithm project.

This is an educational graph: the links and canvas positions are simplified,
not a validated road network or geographically scaled map.
"""

from typing import Final

# Coordinates are for the schematic Tkinter canvas (not GPS coordinates).
CITY_POSITIONS: Final[dict[str, tuple[int, int]]] = {
    "Alexandria": (106, 113),
    "Tanta": (268, 185),
    "Mansoura": (420, 138),
    "Port Said": (627, 103),
    "Zagazig": (433, 277),
    "Cairo": (282, 341),
    "Giza": (132, 354),
    "6th of October": (90, 472),
    "Ismailia": (607, 323),
    "Suez": (627, 470),
}

# Every link has a cost of one. Links are bidirectional.
EDGES: Final[tuple[tuple[str, str], ...]] = (
    ("Alexandria", "Tanta"),
    ("Tanta", "Mansoura"),
    ("Tanta", "Zagazig"),
    ("Tanta", "Cairo"),
    ("Mansoura", "Port Said"),
    ("Mansoura", "Zagazig"),
    ("Port Said", "Ismailia"),
    ("Zagazig", "Cairo"),
    ("Zagazig", "Ismailia"),
    ("Cairo", "Giza"),
    ("Cairo", "Ismailia"),
    ("Giza", "6th of October"),
    ("Ismailia", "Suez"),
)


def build_graph() -> dict[str, list[str]]:
    """Return the undirected graph with stable neighbor insertion order."""
    graph: dict[str, list[str]] = {city: [] for city in CITY_POSITIONS}
    for left, right in EDGES:
        if left not in graph or right not in graph:
            raise ValueError("An edge references a city missing from CITY_POSITIONS")
        graph[left].append(right)
        graph[right].append(left)
    return graph


GRAPH: Final[dict[str, list[str]]] = build_graph()

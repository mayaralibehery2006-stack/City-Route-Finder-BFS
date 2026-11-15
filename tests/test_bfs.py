"""Run with: python -m unittest discover -s tests -v"""

import unittest

from bfs import bfs_shortest_path
from graph_data import CITY_POSITIONS, EDGES, GRAPH


class TestBreadthFirstSearch(unittest.TestCase):
    def test_shortest_route(self):
        result = bfs_shortest_path(GRAPH, "Cairo", "Port Said")
        self.assertEqual(result.path, ("Cairo", "Ismailia", "Port Said"))
        self.assertEqual(result.cost, 2)

    def test_start_is_goal(self):
        result = bfs_shortest_path(GRAPH, "Giza", "Giza")
        self.assertEqual(result.path, ("Giza",))
        self.assertEqual(result.cost, 0)
        self.assertEqual(result.explored_nodes, 1)

    def test_unreachable_goal(self):
        disconnected = {"A": ["B"], "B": ["A"], "C": []}
        result = bfs_shortest_path(disconnected, "A", "C")
        self.assertFalse(result.found)
        self.assertEqual(result.path, ())
        self.assertIsNone(result.cost)
        self.assertEqual(result.explored_order, ("A", "B"))

    def test_unknown_start(self):
        with self.assertRaises(ValueError):
            bfs_shortest_path(GRAPH, "Unknown", "Cairo")

    def test_unknown_goal(self):
        with self.assertRaises(ValueError):
            bfs_shortest_path(GRAPH, "Cairo", "Unknown")

    def test_minimum_hops_not_dfs_path(self):
        graph = {"S": ["A", "T"], "A": ["B"], "B": ["T"], "T": []}
        result = bfs_shortest_path(graph, "S", "T")
        self.assertEqual(result.path, ("S", "T"))
        self.assertEqual(result.cost, 1)

    def test_graph_links_are_bidirectional(self):
        for u, v in EDGES:
            self.assertIn(v, GRAPH[u])
            self.assertIn(u, GRAPH[v])

    def test_every_city_can_reach_every_other_city(self):
        for start in CITY_POSITIONS:
            for goal in CITY_POSITIONS:
                with self.subTest(start=start, goal=goal):
                    self.assertTrue(bfs_shortest_path(GRAPH, start, goal).found)

    def test_route_edges_exist(self):
        result = bfs_shortest_path(GRAPH, "Alexandria", "Suez")
        self.assertTrue(result.found)
        for first, second in zip(result.path, result.path[1:]):
            self.assertIn(second, GRAPH[first])


if __name__ == "__main__":
    unittest.main()

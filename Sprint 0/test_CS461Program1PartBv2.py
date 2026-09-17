import unittest

from CS461Program1PartBv2 import (
    bfs,
    dfs,
    normalize_graph,
    generate_random_graph
)


class TestGraphSearch(unittest.TestCase):

    def test_bfs_finds_path(self):
        graph = {
            "A": ["B"],
            "B": ["A", "C"],
            "C": ["B", "D"],
            "D": ["C"]
        }

        path = bfs(graph, "A", "D")

        self.assertEqual(
            path,
            ["A", "B", "C", "D"]
        )

    def test_dfs_finds_path(self):
        graph = {
            "A": ["B"],
            "B": ["A", "C"],
            "C": ["B", "D"],
            "D": ["C"]
        }

        path = dfs(graph, "A", "D")

        self.assertEqual(
            path,
            ["A", "B", "C", "D"]
        )

    def test_bfs_no_path(self):
        graph = {
            "A": ["B"],
            "B": ["A"],
            "C": ["D"],
            "D": ["C"]
        }

        path = bfs(graph, "A", "D")

        self.assertIsNone(path)

    def test_normalize_graph(self):
        cities = {
            "A": (10, 20),
            "B": (30, 40),
            "C": (50, 60)
        }

        adjacencies = {
            "A": {"B", "D"},
            "B": {"A", "C"},
            "C": {"B"}
        }

        result = normalize_graph(
            cities,
            adjacencies
        )

        expected = {
            "A": ["B"],
            "B": ["A", "C"],
            "C": ["B"]
        }

        self.assertEqual(
            result,
            expected
        )

    def test_generate_random_graph(self):
        cities, graph = generate_random_graph(
            node_count=5
        )

        self.assertEqual(
            len(cities),
            5
        )

        self.assertEqual(
            len(graph),
            5
        )

        for city in cities:
            self.assertIn(city, graph)


if __name__ == "__main__":
    unittest.main()

import unittest
from ranking import merge_sort, rank_players
import pandas as pd


class TestRanking(unittest.TestCase):

    def setUp(self):
        self.players = [
            {"player": "Curry", "pts": 25, "reb": 5},
            {"player": "LeBron", "pts": 30, "reb": 8},
            {"player": "Durant", "pts": 25, "reb": 7},
            {"player": "Giannis", "pts": 32, "reb": 12}
        ]

    def test_descending(self):
        result = merge_sort(self.players, "pts", True)

        self.assertEqual(
            [p["player"] for p in result],
            ["Giannis", "LeBron", "Curry", "Durant"]
        )

    def test_ascending(self):
        result = merge_sort(self.players, "pts", False)

        self.assertEqual(
            [p["player"] for p in result],
            ["Curry", "Durant", "LeBron", "Giannis"]
        )

    def test_different_metric(self):
        result = merge_sort(self.players, "reb", True)

        self.assertEqual([p["reb"] for p in result], [12, 8, 7, 5])
        self.assertEqual(
            [p["player"] for p in result],
            ["Giannis", "LeBron", "Durant", "Curry"]
        )

    def test_empty_list(self):
        result = merge_sort([])
        self.assertEqual(result, [])

    def test_rank_players(self):
        df = pd.DataFrame([
            {"player": "Curry", "season": 2025, "pts": 30},
            {"player": "LeBron", "season": 2025, "pts": 25},
            {"player": "Durant", "season": 2024, "pts": 35},
            {"player": "Giannis", "season": 2025, "pts": 32}
        ])

        result = rank_players(df, 2025, "pts", True)

        self.assertEqual(
            [p["player"] for p in result],
            ["Giannis", "Curry", "LeBron"]
        )


if __name__ == '__main__':
    unittest.main()

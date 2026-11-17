import unittest
from player_index import PlayerIndex
import pandas as pd


class TestPlayerIndex(unittest.TestCase):
    def setUp(self):
        self.h = PlayerIndex()

        self.stats_2020 = {
            "team": "GSW",
            "pts": 30.0,
            "reb": 5.5,
            "ast": 6.0,
            "gp": 63
        }

        self.stats_2021 = {
            "team": "GSW",
            "pts": 32.0,
            "reb": 5.2,
            "ast": 6.3,
            "gp": 64
        }

        self.stats_2020_duplicate = {
            "team": "GSW",
            "pts": 31.0,
            "reb": 5.5,
            "ast": 6.0,
            "gp": 63
        }

    def test_add(self):
        # add to empty dict
        self.h.add("Stephen Curry", 2020, self.stats_2020)
        self.assertEqual(self.h.get_season(
            "stephen curry", 2020), self.stats_2020)
        # add to existing dict
        self.h.add("stephen curry", 2021, self.stats_2021)
        self.assertEqual(self.h.get_season(
            "stephen curry", 2020), self.stats_2020)
        self.assertEqual(self.h.get_season(
            "stephen curry", 2021), self.stats_2021)

    def test_get_season(self):
        self.h.add("Stephen Curry", 2020, self.stats_2020)

        # player doesn't exist
        self.assertIsNone(
            self.h.get_season("LeBron James", 2020)
        )

        # season does not exist
        self.assertIsNone(
            self.h.get_season("Stephen Curry", 2025)
        )

        # case sensitive
        self.assertEqual(
            self.h.get_season("stephen curry", 2020),
            self.stats_2020
        )

    def test_duplicate_season(self):
        self.h.add("Stephen Curry", 2020, self.stats_2020)
        with self.assertRaises(ValueError):
            self.h.add("Stephen Curry", 2020, self.stats_2020_duplicate)

        self.assertEqual(
            self.h.get_season("stephen curry", 2020), self.stats_2020
        )

    def test_from_dataframe(self):
        df = pd.DataFrame([
            {
                "player": "Stephen Curry",
                "team": "GSW",
                "season": 2020,
                "pts": 30.0,
                "reb": 5.5,
                "ast": 6.0,
                "gp": 63,
                "eff": 22.5
            },
            {
                "player": "Stephen Curry",
                "team": "GSW",
                "season": 2021,
                "pts": 32.0,
                "reb": 5.2,
                "ast": 6.3,
                "gp": 64,
                "eff": 24.0
            }
        ])

        index = PlayerIndex.from_dataframe(df)

        self.assertEqual(
            index.get_season("Stephen Curry", 2020)["pts"],
            30.0
        )

        self.assertEqual(
            index.get_season("stephen curry", 2021)["pts"],
            32.0
        )


if __name__ == '__main__':
    unittest.main()

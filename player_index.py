import pandas as pd


class PlayerIndex:

    def __init__(self):
        self._data = {}

    def _norm(self, s: str) -> str:
        return s.strip().lower()

    def add(self, player: str, season: int, stats: dict):
        key = self._norm(player)
        if key not in self._data:
            self._data[key] = {}

        if season in self._data[key]:
            raise ValueError(
                f"Duplicate season {season} for {player}"
            )

        self._data[key][season] = stats

    def get_season(self, player: str, season: int):
        key = self._norm(player)

        if key not in self._data:
            return None
        return self._data[key].get(season)

    @classmethod
    def from_dataframe(cls, df):
        index = cls()

        for _, row in df.iterrows():

            player = row["player"]
            season = int(row["season"])

            stats = {
                "team": str(row["team"]),
                "pts": float(row["pts"]),
                "reb": float(row["reb"]),
                "ast": float(row["ast"]),
                "gp": int(row["gp"]),
                "eff": float(row["eff"])
            }

            # TODO: 呼叫你之前寫好的 add()
            # 將 player、season、stats 加入 index
            index.add(player, season, stats)

        return index

# project.py
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from ranking import rank_players

DATA_PATH = "data/nba_2022-23_to_2026-27_players.csv"

# ---------------- Utility ----------------


def _norm(s: str) -> str:
    return s.strip().lower()


# ---------------- Core (pandas) ----------------


def load_data(csv_path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["season"] = df["season"].astype(int)
    df["gp"] = df["gp"].astype(int)
    for c in ["pts", "reb", "ast"]:
        df[c] = df[c].astype(float)

    # self-defined efficiency
    df["eff"] = df["pts"] * 0.65 + df["reb"] * 0.2 + df["ast"] * 0.3
    return df


def analyze_player(df: pd.DataFrame, player: str,
                   start: int | None = None,
                   end: int | None = None) -> dict:
    sub = df[df["player"].str.strip().str.lower() == _norm(player)].copy()
    if start is not None:
        sub = sub[sub["season"] >= start]
    if end is not None:
        sub = sub[sub["season"] <= end]
    if sub.empty:
        raise ValueError(f"No data for {player} in selected range.")

    w = sub["gp"]
    total_gp = int(w.sum())
    if total_gp == 0:
        raise ValueError(f"{player} has zero games in the selected range.")

    def wavg(col: str) -> float:
        return float((sub[col] * w).sum() / total_gp)

    overall = {
        "pts": wavg("pts"),
        "reb": wavg("reb"),
        "ast": wavg("ast"),
        "eff": wavg("eff"),
        "gp": total_gp,
    }

    per_season = (
        sub.sort_values("season")[["season", "pts", "reb", "ast", "eff", "gp"]]
        .to_dict(orient="records")
    )
    return {"player": player, "overall": overall, "per_season": per_season}


def compare_players(df: pd.DataFrame, p1: str, p2: str,
                    metric: str = "pts",
                    start: int | None = None,
                    end: int | None = None) -> dict:
    metric = metric.lower()
    if metric not in {"pts", "reb", "ast", "eff"}:
        raise ValueError(
            f"Invalid metric: {metric} (choose from pts, reb, ast, eff)")
    s1 = analyze_player(df, p1, start, end)["overall"][metric]
    s2 = analyze_player(df, p2, start, end)["overall"][metric]
    return {"metric": metric, p1: float(s1), p2: float(s2), "diff": float(s1 - s2)}


def plot_player_timeseries(df: pd.DataFrame, players: list[str],
                           metric: str = "pts", save: str | None = None):
    metric = metric.lower()
    if metric not in {"pts", "reb", "ast", "eff"}:
        raise ValueError("metric must be one of: pts, reb, ast, eff")

    df = df.copy()
    df["player_norm"] = df["player"].str.strip().str.lower()
    chosen = [_norm(p) for p in players]
    sub = df[df["player_norm"].isin(chosen)].sort_values(["player", "season"])

    if sub.empty:
        raise ValueError(f"No data for players: {players}")

    sns.set_theme(style="whitegrid")
    ax = sns.lineplot(data=sub, x="season", y=metric, hue="player", marker="o")
    ax.set_title(f"{metric.upper()} by Season")
    ax.set_xlabel("Season")
    ax.set_ylabel(metric.upper())
    plt.tight_layout()

    if save:
        plt.savefig(save)
        print(f"Plot saved to {save}")
    else:
        plt.show()

# ---------------- CLI ----------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="NBA Analytics (pandas + seaborn)")
    sub = p.add_subparsers(dest="cmd", required=True)

    # summary
    s = sub.add_parser("summary", help="Show a player's weighted averages")
    s.add_argument("player", help='e.g. "LeBron James"')
    s.add_argument("--start", type=int, help="start season (inclusive)")
    s.add_argument("--end", type=int, help="end season (inclusive)")

    # compare
    c = sub.add_parser("compare", help="Compare two players on a metric")
    c.add_argument("player1")
    c.add_argument("player2")
    c.add_argument(
        "--metric", choices=["pts", "reb", "ast", "eff"], default="pts")
    c.add_argument("--start", type=int, help="start season (inclusive)")
    c.add_argument("--end", type=int, help="end season (inclusive)")

    # plot (multi-player)
    g = sub.add_parser(
        "plot", help="Plot seasonal trend for one or more players")
    g.add_argument("players", nargs="+",
                   help='one or more names, e.g. "LeBron James" "Stephen Curry"')
    g.add_argument(
        "--metric", choices=["pts", "reb", "ast", "eff"], default="pts")
    g.add_argument(
        "--save", help="path to save the figure (PNG). If omitted, show window.")

    # rank
    r = sub.add_parser("rank", help="Rank players by metrics in a season")
    r.add_argument("--season", type=int, required=True,
                   help="choose a season(2022-2026)")
    r.add_argument(
        "--metric", choices=["pts", "reb", "ast", "eff"], default="pts")
    r.add_argument("--top", type=int, default=10)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    df = load_data(DATA_PATH)

    if args.cmd == "summary":
        res = analyze_player(df, args.player, args.start, args.end)
        overall = res["overall"]
        print(f"\nPlayer: {res['player']}")
        if args.start or args.end:
            lo = args.start if args.start is not None else "-∞"
            hi = args.end if args.end is not None else "+∞"
            print(f"Seasons: [{lo}, {hi}]")
        print(f"Games: {overall['gp']}")
        print(
            f"PTS: {overall['pts']:.1f}  REB: {overall['reb']:.1f}  AST: {overall['ast']:.1f}  EFF: {overall['eff']:.2f}")
        print("\nPer-season:")
        for row in res["per_season"]:
            print(
                f"  {row['season']}: {row['pts']:.1f} pts, {row['reb']:.1f} reb, {row['ast']:.1f} ast, EFF {row['eff']:.2f} (GP {row['gp']})")

    elif args.cmd == "compare":
        res = compare_players(df, args.player1, args.player2,
                              args.metric, args.start, args.end)
        p1, p2 = args.player1, args.player2
        if args.start or args.end:
            lo = args.start if args.start is not None else "-∞"
            hi = args.end if args.end is not None else "+∞"
            print(f"\nSeasons: [{lo}, {hi}]")
        print(f"Metric: {res['metric'].upper()}")
        print(f"{p1}: {res[p1]:.2f}")
        print(f"{p2}: {res[p2]:.2f}")
        print(f"Diff ( {p1} - {p2} ): {res['diff']:.2f}")

    elif args.cmd == "plot":
        plot_player_timeseries(df, args.players, args.metric, args.save)

    elif args.cmd == "rank":
        if args.top <= 0:
            parser.error("--top must be a positive integer")
        ranking = rank_players(df, args.season, args.metric)
        if not ranking:
            print(f"No data for season {args.season}.")
            return
        k = args.top
        rankingTopk = ranking[:k]
        print(
            f"{args.season}-{str(args.season + 1)[-2:]} NBA Ranking — {args.metric.upper()}")
        for rank, player in enumerate(rankingTopk, start=1):
            print(f"{rank}. {player['player']} — {player[args.metric]:.2f}")


if __name__ == "__main__":
    main()

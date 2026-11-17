import pytest
import importlib
import project
import os


# ------------------- load_data -------------------

def test_load_data_has_eff_column():
    df = project.load_data()
    assert "eff" in df.columns
    # eff 應該跟 pts/reb/ast 有數值關聯
    row = df.iloc[0]
    eff_calc = row["pts"]*0.65 + row["reb"]*0.2 + row["ast"]*0.3
    assert abs(row["eff"] - eff_calc) < 1e-6


# ------------------- analyze_player -------------------

def test_analyze_player_overall_contains_eff():
    df = project.load_data()
    res = project.analyze_player(df, "LeBron James")
    overall = res["overall"]
    for key in ["pts", "reb", "ast", "eff", "gp"]:
        assert key in overall
    assert overall["gp"] > 0


def test_analyze_player_with_year_filters_changes_gp():
    df = project.load_data()
    res_all = project.analyze_player(df, "Stephen Curry")
    res_2022 = project.analyze_player(
        df, "Stephen Curry", start=2022, end=2022)
    # 過濾年份後 gp 應該不同
    assert res_all["overall"]["gp"] != res_2022["overall"]["gp"]


# ------------------- compare_players -------------------

def test_compare_players_eff_diff_matches_manual():
    df = project.load_data()
    res = project.compare_players(
        df, "LeBron James", "Stephen Curry", metric="eff")
    # 手動算
    v1 = project.analyze_player(df, "LeBron James")["overall"]["eff"]
    v2 = project.analyze_player(df, "Stephen Curry")["overall"]["eff"]
    assert abs(res["diff"] - (v1 - v2)) < 1e-6


def test_compare_players_with_year_filters():
    df = project.load_data()
    res_range = project.compare_players(
        df, "LeBron James", "Stephen Curry", metric="pts", start=2023, end=2025)
    assert "LeBron James" in res_range and "Stephen Curry" in res_range


def test_compare_players_invalid_metric_raises():
    df = project.load_data()
    with pytest.raises(ValueError):
        project.compare_players(
            df, "LeBron James", "Stephen Curry", metric="blk")


# ------------------- CLI -------------------


def run_cli(monkeypatch, argv):
    monkeypatch.setattr("sys.argv", argv)
    importlib.reload(project)  # 重新載入模組確保使用最新程式碼
    project.main()             # 💥 真的執行 CLI 入口


def test_cli_summary(monkeypatch, capsys):
    run_cli(monkeypatch, ["project.py", "summary",
            "LeBron James", "--start", "2022", "--end", "2026"])
    out = capsys.readouterr().out.lower()
    assert "player: lebron james" in out
    assert "eff" in out


def test_cli_compare(monkeypatch, capsys):
    run_cli(monkeypatch, ["project.py", "compare",
            "LeBron James", "Stephen Curry", "--metric", "eff"])
    out = capsys.readouterr().out
    assert "Metric: EFF" in out
    assert "Diff" in out


def test_cli_plot_multiple_players(monkeypatch):
    out_file = "test_plot.png"
    if os.path.exists(out_file):
        os.remove(out_file)

    run_cli(
        monkeypatch,
        ["project.py", "plot", "LeBron James", "Stephen Curry",
            "--metric", "pts", "--save", out_file],
    )
    assert os.path.exists(out_file)
    os.remove(out_file)


def test_cli_rank(monkeypatch, capsys):
    # TODO 1: run_cli(...)
    run_cli(monkeypatch, [
        "project.py", "rank",
        "--season", "2024",
        "--metric", "reb",
        "--top", "5"
    ])

    # TODO 2: 擷取輸出
    out = capsys.readouterr().out.lower()
    # TODO 3: 檢查 NBA Ranking
    assert "nba ranking" in out
    # TODO 4: 檢查 Top 5
    lines = out.strip().splitlines()
    assert len(lines) == 6

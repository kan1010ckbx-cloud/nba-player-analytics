# NBA Player Analytics & Ranking System

A Python command-line application for exploring NBA player-season statistics, comparing players, visualizing trends, and ranking performances. This project began as a CS50P final project and was extended with data structures, a custom sorting algorithm, and automated tests while studying computer science at the University of Connecticut.

## Features

- **Player summaries:** Calculate games-played-weighted averages across available seasons, with optional season filters.
- **Player comparisons:** Compare two players using points, rebounds, assists, or a custom efficiency score.
- **Seasonal visualizations:** Plot statistical trends for one or more players and optionally save the figure.
- **Top-K rankings:** Rank players within a selected season by a chosen metric, in descending order.
- **Player hash index:** Use nested dictionaries keyed by normalized player name and season to retrieve statistics; reject duplicate player-season records.
- **Custom merge sort:** Apply a stable merge-sort implementation to lists of player records, supporting ascending and descending order.

## Technology

Python · Pandas · NumPy · Matplotlib · Seaborn · argparse · pytest · unittest · Git

## Getting Started

### 1. Set up an environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
python -m pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate` instead.

### 2. Prepare the data

The default data file is:

```text
data/nba_2022-23_to_2026-27_players.csv
```

The processed CSV is expected to contain the following columns:

| Column | Meaning |
| --- | --- |
| `season` | Starting year of the NBA season (e.g., `2025` for 2025–26) |
| `player` | Player name |
| `team` | Team abbreviation |
| `gp` | Games played |
| `pts` | Points per game |
| `reb` | Rebounds per game |
| `ast` | Assists per game |

The application computes the derived `eff` metric on load. Verify that the CSV is present before running commands. Season availability depends on the dataset; the 2026–27 season is in progress as of November 2026, so its statistics are not final.

> **Data provenance:** Add the original data-provider URL, retrieval date, any processing steps, and applicable redistribution terms here before publishing the dataset. The source and license have not been independently verified in this README. If redistribution is not allowed, omit the CSV from the public repository and provide instructions to obtain it.

## CLI Usage

Run the commands from the project root directory.

### Summarize a player's performance

```bash
python project.py summary "LeBron James"
python project.py summary "Stephen Curry" --start 2023 --end 2025
```

### Compare two players

```bash
python project.py compare "LeBron James" "Stephen Curry" --metric eff
python project.py compare "LeBron James" "Stephen Curry" --metric pts --start 2023 --end 2025
```

### Visualize seasonal trends

```bash
python project.py plot "Stephen Curry" "LeBron James" --metric pts
python project.py plot "Stephen Curry" --metric reb --save curry_rebounds.png
```

### Rank players within a season

```bash
python project.py rank --season 2025 --metric pts --top 10
python project.py rank --season 2024 --metric reb --top 5
```

Available metrics: `pts`, `reb`, `ast`, and `eff`. Use `python project.py --help` or `python project.py rank --help` for argument details.

## Efficiency Metric

The project uses a **custom illustrative scoring formula**, not the NBA's official player efficiency rating (PER):

```text
eff = 0.65 × pts + 0.20 × reb + 0.30 × ast
```

This metric is intended for practicing data processing and comparisons, not for drawing definitive conclusions about player quality.

## Data Structures and Algorithms

**PlayerIndex (`player_index.py`):** A nested mapping of the form `normalized_player_name -> season -> statistics`. Dictionary-based lookups are expected to be O(1) on average, subject to normal hash-table assumptions. A duplicate player-season entry raises `ValueError`.

**Ranking (`ranking.py`):** A custom stable merge sort orders player-season records by the requested metric. Merge sort has O(n log n) time complexity; this project uses auxiliary lists during merging.

## Testing

Run the complete test suite:

```bash
python -m pytest -v
```

The most recent local full run reported **19 passing tests** (November 17, 2026), covering data processing, player indexing, sorting, and CLI behavior. This is a recorded result, not a guarantee about every environment or future dataset revision.

## Project Structure

```text
project.py             # Data loading, analysis functions, CLI, and plotting
player_index.py        # Hash-based player/season index
ranking.py             # Stable merge sort and player rankings
test_project.py        # Analysis and CLI tests
test_player_index.py   # PlayerIndex tests
test_ranking.py        # Sorting and ranking tests
requirements.txt       # Python dependencies
data/                  # Player-season data (subject to redistribution rights)
```

## Limitations and Future Work

- The dataset may contain incomplete current-season data; season comparisons must account for this.
- The `eff` score is a custom weighted metric rather than an official NBA advanced statistic.
- Additional work could cover input-data validation, clearer handling of traded players, and a reproducible data acquisition pipeline.

## Author

**Ruei Shin Gan**  
University of Connecticut — Undergraduate student (ACES; intended Data Science and Engineering)  
[GitHub](https://github.com/kan1010ckbx-cloud) · [LinkedIn](https://www.linkedin.com/in/ruei-shin-gan-45a6a1403)

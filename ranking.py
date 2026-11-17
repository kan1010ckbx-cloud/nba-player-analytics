def merge_sort(records: list, metric: str = "pts",
               descending: bool = True) -> list:

    if len(records) <= 1:
        return records[:]

    mid = len(records) // 2

    A = records[:mid]
    B = records[mid:]
    merge_sort(A, metric, descending)
    merge_sort(B, metric, descending)

    merge(records, A, B, metric, descending)

    return records


def merge(L, A, B, metric, descending):
    i = j = 0
    while i < len(A) and j < len(B):
        # descending order
        if descending:
            if A[i][metric] < B[j][metric]:
                L[i+j] = B[j]
                j += 1
            else:
                L[i+j] = A[i]
                i += 1
        # ascending order
        else:
            if A[i][metric] <= B[j][metric]:
                L[i+j] = A[i]
                i += 1
            else:
                L[i+j] = B[j]
                j += 1

    L[i+j:] = A[i:] + B[j:]


def rank_players(df, season: int,
                 metric: str = "pts",
                 descending: bool = True) -> list:
    valid_metrics = {"pts", "reb", "ast", "eff"}

    if metric not in valid_metrics:
        return ValueError("Invalid metric!!")

    season_df = df[df["season"] == season]

    records = season_df.to_dict(orient="records")

    merge_sort(records, metric, descending)

    return records

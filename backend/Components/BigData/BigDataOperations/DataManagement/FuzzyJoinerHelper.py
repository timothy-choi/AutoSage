import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from typing import Optional


def fuzzy_join(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    left_on: str,
    right_on: str,
    threshold: int = 80,
    limit: Optional[int] = None,
) -> pd.DataFrame:
    try:
        matched_rows = []

        for idx, left_val in left_df[left_on].items():
            matches = process.extractBests(
                left_val,
                right_df[right_on].astype(str),
                scorer=fuzz.token_sort_ratio,
                score_cutoff=threshold,
                limit=limit or 1,
            )

            for match_val, score in matches:
                right_match = right_df[right_df[right_on] == match_val]
                for _, right_row in right_match.iterrows():
                    combined = pd.concat(
                        [left_df.loc[[idx]].reset_index(drop=True), right_row.to_frame().T.reset_index(drop=True)],
                        axis=1,
                    )
                    matched_rows.append(combined)

        if matched_rows:
            return pd.concat(matched_rows, ignore_index=True)
        else:
            return pd.DataFrame()

    except Exception as e:
        print(f"Error during fuzzy join: {e}")
        return pd.DataFrame()
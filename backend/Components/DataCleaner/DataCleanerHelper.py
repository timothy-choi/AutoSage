import re
from typing import List, Dict, Union


def remove_nulls(data: List[Dict[str, Union[str, int, float, None]]]) -> List[Dict]:
    return [{k: v for k, v in row.items() if v is not None} for row in data]


def strip_strings(data: List[Dict[str, Union[str, int, float, None]]]) -> List[Dict]:
    return [{k: v.strip() if isinstance(v, str) else v for k, v in row.items()} for row in data]


def lower_case_strings(data: List[Dict[str, Union[str, int, float, None]]]) -> List[Dict]:
    return [{k: v.lower() if isinstance(v, str) else v for k, v in row.items()} for row in data]


def remove_duplicates(data: List[Dict]) -> List[Dict]:
    seen = set()
    unique = []
    for row in data:
        row_tuple = tuple(sorted(row.items()))
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique.append(row)
    return unique


def standardize_column_names(data: List[Dict]) -> List[Dict]:
    return [{re.sub(r"\W+", "_", k).strip("_").lower(): v for k, v in row.items()} for row in data]


def fill_missing_with_default(data: List[Dict], default: Union[str, int, float]) -> List[Dict]:
    return [{k: (v if v is not None else default) for k, v in row.items()} for row in data]


def filter_rows_with_keywords(data: List[Dict[str, Union[str, int, float]]], column: str, keywords: List[str]) -> List[Dict]:
    return [row for row in data if any(kw.lower() in str(row.get(column, '')).lower() for kw in keywords)]


def normalize_whitespace(data: List[Dict]) -> List[Dict]:
    return [{k: re.sub(r'\s+', ' ', v).strip() if isinstance(v, str) else v for k, v in row.items()} for row in data]
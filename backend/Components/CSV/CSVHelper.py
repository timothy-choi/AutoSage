import csv
from typing import List, Dict, Optional
import os
from collections import defaultdict


def read_csv(filepath: str, delimiter: str = ",") -> List[Dict[str, str]]:
    with open(filepath, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return [row for row in reader]

def write_csv(filepath: str, data: List[Dict[str, str]], fieldnames: Optional[List[str]] = None, delimiter: str = ","):
    if not data:
        raise ValueError("Data list is empty.")

    if fieldnames is None:
        fieldnames = list(data[0].keys())

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)

def get_csv_headers(filepath: str, delimiter: str = ",") -> List[str]:
    with open(filepath, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        headers = next(reader)
    return headers

def preview_csv(filepath: str, num_rows: int = 5, delimiter: str = ",") -> List[Dict[str, str]]:
    with open(filepath, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return [row for _, row in zip(range(num_rows), reader)]

def filter_csv(filepath: str, column: str, value: str, delimiter: str = ",") -> List[Dict[str, str]]:
    data = read_csv(filepath, delimiter)
    return [row for row in data if row.get(column) == value]

def count_rows(filepath: str, delimiter: str = ",") -> int:
    with open(filepath, mode="r", newline="", encoding="utf-8") as f:
        return sum(1 for _ in csv.reader(f, delimiter=delimiter)) - 1

def append_csv(filepath: str, row: Dict[str, str], delimiter: str = ","):
    file_exists = os.path.isfile(filepath)
    with open(filepath, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys(), delimiter=delimiter)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def rename_column(data: List[Dict[str, str]], old_name: str, new_name: str) -> List[Dict[str, str]]:
    return [{(new_name if k == old_name else k): v for k, v in row.items()} for row in data]

def sort_csv(data: List[Dict[str, str]], column: str, reverse: bool = False) -> List[Dict[str, str]]:
    return sorted(data, key=lambda x: x.get(column, ""), reverse=reverse)

def deduplicate_csv(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    deduped = []
    for row in data:
        row_tuple = tuple(row.items())
        if row_tuple not in seen:
            seen.add(row_tuple)
            deduped.append(row)
    return deduped

def column_stats(data: List[Dict[str, str]], column: str) -> Dict[str, int]:
    stats = defaultdict(int)
    for row in data:
        value = row.get(column, "")
        stats[value] += 1
    return dict(stats)
from typing import List
import re

def full_text_search(data: List[dict], query: str, fields: List[str]) -> List[dict]:
    try:
        query_lower = query.lower()
        results = []
        for row in data:
            for field in fields:
                if field in row and query_lower in str(row[field]).lower():
                    results.append(row)
                    break
        return results
    except Exception as e:
        return [{"error": str(e)}]
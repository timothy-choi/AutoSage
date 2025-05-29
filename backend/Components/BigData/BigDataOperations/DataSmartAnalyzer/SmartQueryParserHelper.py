from typing import Optional
from sqlalchemy import text
import re

def smart_query_parser(natural_language: str) -> Optional[str]:
    try:
        nl = natural_language.lower()
        if "average" in nl or "mean" in nl:
            column = re.findall(r"\b(?:of|for) ([a-zA-Z_][a-zA-Z0-9_]*)", nl)
            if column:
                return f"SELECT AVG({column[0]}) FROM dataset;"
        elif "count" in nl:
            return "SELECT COUNT(*) FROM dataset;"
        elif "maximum" in nl or "highest" in nl:
            column = re.findall(r"\b(?:of|for) ([a-zA-Z_][a-zA-Z0-9_]*)", nl)
            if column:
                return f"SELECT MAX({column[0]}) FROM dataset;"
        elif "show all" in nl or "list all" in nl:
            return "SELECT * FROM dataset;"
        return None
    except Exception as e:
        return f"Error parsing natural language: {e}"
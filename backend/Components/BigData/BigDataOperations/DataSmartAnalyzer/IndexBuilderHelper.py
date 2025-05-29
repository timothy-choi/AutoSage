import os
import json
from typing import List, Dict
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

INDEX_DIR = "indexdir"

def create_schema() -> Schema:
    return Schema(id=ID(stored=True, unique=True), content=TEXT(stored=True))

def build_index(data: List[Dict[str, str]], key_field: str = "id", text_field: str = "content") -> str:
    try:
        if not os.path.exists(INDEX_DIR):
            os.mkdir(INDEX_DIR)
            ix = index.create_in(INDEX_DIR, create_schema())
        else:
            ix = index.open_dir(INDEX_DIR)

        writer = ix.writer()
        for record in data:
            writer.update_document(
                id=str(record[key_field]),
                content=record[text_field]
            )
        writer.commit()
        return "Index built successfully."
    except Exception as e:
        return f"Error building index: {str(e)}"

def search_index(query_str: str, limit: int = 10) -> List[Dict[str, str]]:
    try:
        ix = index.open_dir(INDEX_DIR)
        parser = QueryParser("content", schema=ix.schema)
        query = parser.parse(query_str)

        results = []
        with ix.searcher() as searcher:
            hits = searcher.search(query, limit=limit)
            for hit in hits:
                results.append({"id": hit["id"], "content": hit["content"]})
        return results
    except Exception as e:
        return [{"error": str(e)}]
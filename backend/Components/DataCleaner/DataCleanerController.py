from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Union
from DataCleanerHelper import *

app = FastAPI()

class DataInput(BaseModel):
    data: List[Dict[str, Union[str, int, float, None]]]

class DefaultFillInput(DataInput):
    default: Union[str, int, float]

class KeywordFilterInput(DataInput):
    column: str
    keywords: List[str]

@app.post("/clean/remove-nulls")
def api_remove_nulls(payload: DataInput):
    try:
        return {"result": remove_nulls(payload.data)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/clean/strip-strings")
def api_strip_strings(payload: DataInput):
    try:
        return {"result": strip_strings(payload.data)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/clean/lower-case")
def api_lower_case(payload: DataInput):
    try:
        return {"result": lower_case_strings(payload.data)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/clean/remove-duplicates")
def api_remove_duplicates(payload: DataInput):
    try:
        return {"result": remove_duplicates(payload.data)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/clean/standardize-columns")
def api_standardize_columns(payload: DataInput):
    try:
        return {"result": standardize_column_names(payload.data)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/clean/fill-missing")
def api_fill_missing(payload: DefaultFillInput):
    try:
        return {"result": fill_missing_with_default(payload.data, payload.default)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/clean/filter-keywords")
def api_filter_keywords(payload: KeywordFilterInput):
    try:
        return {"result": filter_rows_with_keywords(payload.data, payload.column, payload.keywords)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/clean/normalize-whitespace")
def api_normalize_whitespace(payload: DataInput):
    try:
        return {"result": normalize_whitespace(payload.data)}
    except Exception as e:
        return {"error": str(e)}
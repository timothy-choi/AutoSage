from fastapi import FastAPI, Query
from pydantic import BaseModel
from TextFormatterHelper import *

app = FastAPI()

class TextInput(BaseModel):
    text: str

class WrapInput(BaseModel):
    text: str
    width: int = 80

class CountCharInput(BaseModel):
    text: str
    include_spaces: bool = True

@app.post("/format/capitalize")
def api_capitalize(data: TextInput):
    try:
        return {"result": capitalize_text(data.text)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/format/title")
def api_title_case(data: TextInput):
    try:
        return {"result": title_case_text(data.text)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/format/upper")
def api_upper_case(data: TextInput):
    try:
        return {"result": upper_case_text(data.text)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/format/lower")
def api_lower_case(data: TextInput):
    try:
        return {"result": lower_case_text(data.text)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/format/reverse")
def api_reverse_text(data: TextInput):
    try:
        return {"result": reverse_text(data.text)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/format/trim")
def api_trim_whitespace(data: TextInput):
    try:
        return {"result": remove_whitespace(data.text)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/format/wrap")
def api_wrap_text(data: WrapInput):
    try:
        return {"result": wrap_text(data.text, data.width)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/format/strip-punctuation")
def api_strip_punctuation(data: TextInput):
    try:
        return {"result": strip_punctuation(data.text)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/format/count-words")
def api_count_words(data: TextInput):
    try:
        return {"count": count_words(data.text)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/format/count-characters")
def api_count_characters(data: CountCharInput):
    try:
        return {"count": count_characters(data.text, data.include_spaces)}
    except Exception as e:
        return {"error": str(e)}

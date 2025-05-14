from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import WebScraperHelper

app = FastAPI()

def validate_required_fields(data: dict, required_fields: list):
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")
    return True

class WebScraperRequest(BaseModel):
    url: str
    output_path: str
    element_selector: str = None
    attribute_name: str = None
    text_content: bool = False
    html_content: bool = False

class WebScraperResponse(BaseModel):
    status: str
    data: dict = None
    error: str = None

@app.post("/WebScraper/fetchPage")
async def fetch_page(request: WebScraperRequest):
    form = await request.form()
    url = form.get("url")
    output_path = form.get("output_path")
    element_selector = form.get("element_selector")
    attribute_name = form.get("attribute_name")
    text_content = form.get("text_content", "false").lower() == "true"
    html_content = form.get("html_content", "false").lower() == "true"

    validate_required_fields(form, ["url", "output_path"])

    try:
        data = WebScraperHelper.fetch_page(url, output_path, element_selector, attribute_name, text_content, html_content)
        return WebScraperResponse(status="success", data=data)
    except Exception as e:
        return WebScraperResponse(status="error", error=str(e))
    
@app.post("/WebScraper/extractLinks")
async def extract_links(request: WebScraperRequest):
    form = await request.form()
    url = form.get("url")
    output_path = form.get("output_path")

    validate_required_fields(form, ["url", "output_path"])

    try:
        links = WebScraperHelper.extract_links(url, output_path)
        return WebScraperResponse(status="success", data=links)
    except Exception as e:
        return WebScraperResponse(status="error", error=str(e))
    
@app.post("/WebScraper/extractTextBySelector")
async def extract_text_by_selector(request: WebScraperRequest):
    form = await request.form()
    url = form.get("url")
    output_path = form.get("output_path")
    element_selector = form.get("element_selector")

    validate_required_fields(form, ["url", "output_path", "element_selector"])

    try:
        text = WebScraperHelper.extract_text_by_selector(url, output_path, element_selector)
        return WebScraperResponse(status="success", data=text)
    except Exception as e:
        return WebScraperResponse(status="error", error=str(e))
    
@app.post("/WebScraper/extractTableData")
async def extract_table_data(request: WebScraperRequest):
    form = await request.form()
    url = form.get("url")
    output_path = form.get("output_path")

    validate_required_fields(form, ["url", "output_path"])

    try:
        table_data = WebScraperHelper.extract_table_data(url, output_path)
        return WebScraperResponse(status="success", data=table_data)
    except Exception as e:
        return WebScraperResponse(status="error", error=str(e))
    
@app.post("/WebScraper/extractImages")
async def extract_images(request: WebScraperRequest):
    form = await request.form()
    url = form.get("url")
    output_path = form.get("output_path")

    validate_required_fields(form, ["url", "output_path"])

    try:
        images = WebScraperHelper.extract_images(url, output_path)
        return WebScraperResponse(status="success", data=images)
    except Exception as e:
        return WebScraperResponse(status="error", error=str(e))
    
@app.post("/WebScraper/extractMetaData")
async def extract_meta_data(request: WebScraperRequest):
    form = await request.form()
    url = form.get("url")
    output_path = form.get("output_path")

    validate_required_fields(form, ["url", "output_path"])

    try:
        meta_data = WebScraperHelper.extract_meta_data(url, output_path)
        return WebScraperResponse(status="success", data=meta_data)
    except Exception as e:
        return WebScraperResponse(status="error", error=str(e))

@app.post("/WebScraper/extractHeadings")
async def extract_headings(request: WebScraperRequest):
    form = await request.form()
    url = form.get("url")
    output_path = form.get("output_path")

    validate_required_fields(form, ["url", "output_path"])

    try:
        headings = WebScraperHelper.extract_headings(url, output_path)
        return WebScraperResponse(status="success", data=headings)
    except Exception as e:
        return WebScraperResponse(status="error", error=str(e))
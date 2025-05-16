from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import BrowserScraperHelper

app = FastAPI()

@app.post("/BrowserScraper/fetch_content")
async def fetch_content(url: str, browser: str):
    driver = BrowserScraperHelper.create_driver(browser)
    try:
        content = BrowserScraperHelper.fetch_content(driver, url)
        return {"html": content}
    except:
        return HTTPException(status_code=500)
    finally:
        BrowserScraperHelper.close_driver(driver)

@app.post("/BrowserScraper/text")
async def get_text(url: str, selector: str, browser):
    driver = BrowserScraperHelper.create_driver(browser)
    try:
        texts = BrowserScraperHelper.extract_text_by_selector(driver, selector)
        return {"texts": texts}
    except:
        return HTTPException(status_code=500)
    finally:
        BrowserScraperHelper.close_driver(driver)

@app.post("/BrowserScraper/links")
async def get_links(url: str, browser: str):
    driver = BrowserScraperHelper.create_driver(browser)
    try:
        links = BrowserScraperHelper.extract_links(driver)
        return {"links": links}
    except:
        return HTTPException(status_code=500)
    finally:
        BrowserScraperHelper.close_driver(driver)

@app.post("/BrowserScraper/table")
async def get_table(url: str, browser: str):
    driver = BrowserScraperHelper.create_driver(browser)
    try:
        table = BrowserScraperHelper.extract_table_data(driver)
        return {"table": table}
    except:
        return HTTPException(status_code=500)
    finally:
        BrowserScraperHelper.close_driver(driver)

@app.post("/BrowserScraper/scroll_to_bottom")
async def scroll_to_bottom(pause_time: float, browser: str):
    driver = BrowserScraperHelper.create_driver(browser)
    try:
        BrowserScraperHelper.scroll_to_bottom(driver, pause_time)
        return {"scrolled": True}
    except:
        return HTTPException(status_code=500)
    finally:
        BrowserScraperHelper.close_driver(driver)

@app.post("/BrowserScraper/scroll_to_top")
async def scroll_to_top(pause_time: float, browser: str):
    driver = BrowserScraperHelper.create_driver(browser)
    try:
        BrowserScraperHelper.scroll_to_top(driver, pause_time)
        return {"scrolled": True}
    except:
        return HTTPException(status_code=500)
    finally:
        BrowserScraperHelper.close_driver(driver)

@app.post("/BrowserScraper/click")
async def click_element(selector: str, browser: str):
    driver = BrowserScraperHelper.create_driver(browser)
    try:
        BrowserScraperHelper.click_element_by_selector(driver, selector)
        return {"clicked": True}
    except:
        return HTTPException(status_code=500)
    finally:
        BrowserScraperHelper.close_driver(driver)

@app.post("/BrowserScraper/screenshot")
async def take_screenshot(path: str, browser: str):
    driver = BrowserScraperHelper.create_driver(browser)
    try:
        BrowserScraperHelper.take_screenshot(driver, path)
        return {"screenshot": True}
    except:
        return HTTPException(status_code=500)
    finally:
        BrowserScraperHelper.close_driver(driver)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from typing import List
import time

def create_driver(browser: str = "chrome", headless: bool = True):
    browser = browser.lower()

    if browser == "chrome":
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        return webdriver.Chrome(options=options)
    elif browser == "firefox":
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        return webdriver.Firefox(options=options)
    elif browser == "edge":
        from selenium.webdriver.edge.options import Options as EdgeOptions
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        return webdriver.Edge(options=options)
    elif browser == "safari":
        from selenium.webdriver.safari.options import Options as SafariOptions
        options = SafariOptions()
        if headless:
            options.add_argument("--headless")
        return webdriver.Safari(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")


def fetch_content(driver: webdriver, url: str) -> str:
    driver.get(url)
    time.sleep(2)
    return driver.page_source

def extract_links(driver: webdriver) -> List[str]:
    return [a.get_attribute("href") for a in driver.find_elements(By.TAG_NAME, "a")]

def extract_text_by_selector(driver: webdriver, selector: str) -> List[str]:
    return [el.text for el in driver.find_elements(By.CSS_SELECTOR, selector)]

def extract_table_data(driver: webdriver) -> List[List[str]]:
    table = driver.find_element(By.TAG_NAME, "table")
    rows = table.find_elements(By.TAG_NAME, "tr")
    return [[cell.text for cell in row.find_elements(By.TAG_NAME, "td") + row.find_elements(By.TAG_NAME, "th")] for row in rows]

def scroll_to_bottom(driver: webdriver, pause_time: float = 1.0):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scroll_to_top(driver: webdriver, pause_time: float = 1.0):
    current_height = driver.execute_script("return window.scrollY")
    while current_height > 0:
        driver.execute_script("window.scrollBy(0, -window.innerHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return window.scrollY")
        if new_height == current_height:
            break
        current_height = new_height

def click_element_by_selector(driver: webdriver, selector: str):
    el = driver.find_element(By.CSS_SELECTOR, selector)
    el.click()

def take_screenshot(driver: webdriver, path: str):
    driver.save_screenshot(path)

def close_driver(driver: webdriver):
    driver.quit()
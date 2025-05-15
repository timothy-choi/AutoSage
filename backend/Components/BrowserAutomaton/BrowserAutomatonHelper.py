from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.safari.options import Options as SafariOptions
from typing import Optional
import time

def create_driver(browser: str = "chrome", headless: bool = True):
    browser = browser.lower()

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        return webdriver.Firefox(options=options)

    elif browser == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        return webdriver.Edge(options=options)
    
    elif browser == "safari":
        options = SafariOptions()
        if headless:
            options.add_argument("--headless")
        return webdriver.Safari(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

def open_url(driver: webdriver.Remote, url: str):
    driver.get(url)
    time.sleep(1)

def click_element(driver: webdriver.Remote, selector: str):
    element = driver.find_element(By.CSS_SELECTOR, selector)
    element.click()
    time.sleep(0.5)

def type_into_field(driver: webdriver.Remote, selector: str, text: str, clear: bool = True):
    field = driver.find_element(By.CSS_SELECTOR, selector)
    if clear:
        field.clear()
    field.send_keys(text)
    time.sleep(0.5)

def press_key(driver: webdriver.Remote, selector: str, key: str):
    element = driver.find_element(By.CSS_SELECTOR, selector)
    key_map = {
        "enter": Keys.ENTER,
        "tab": Keys.TAB,
        "escape": Keys.ESCAPE
    }
    element.send_keys(key_map.get(key.lower(), key))
    time.sleep(0.5)

def wait_for_element(driver: webdriver.Remote, selector: str, timeout: float = 10.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            driver.find_element(By.CSS_SELECTOR, selector)
            return True
        except:
            time.sleep(0.5)
    return False

def take_screenshot(driver: webdriver.Remote, path: str):
    driver.save_screenshot(path)

def hover_over_element(driver: webdriver.Remote, selector: str):
    element = driver.find_element(By.CSS_SELECTOR, selector)
    ActionChains(driver).move_to_element(element).perform()
    time.sleep(0.5)

def drag_and_drop(driver: webdriver.Remote, source_selector: str, target_selector: str):
    source = driver.find_element(By.CSS_SELECTOR, source_selector)
    target = driver.find_element(By.CSS_SELECTOR, target_selector)
    ActionChains(driver).drag_and_drop(source, target).perform()
    time.sleep(0.5)

def scroll_to_element(driver: webdriver.Remote, selector: str):
    element = driver.find_element(By.CSS_SELECTOR, selector)
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(0.5)

def close_driver(driver: webdriver.Remote):
    driver.quit()

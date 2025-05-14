from bs4 import BeautifulSoup
from typing import List

def fetch_page(self, url: str) -> str:
    try:
        response = self.session.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise RuntimeError(f"Failed to fetch page content from {url}: {e}")

def extract_links(self, html: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    return [link for link in links if link]

def extract_text_by_selector(self, html: str, selector: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select(selector)
    return [el.get_text(strip=True) for el in elements]

def extract_table_data(self, html: str) -> List[List[str]]:
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    if not table:
        return []

    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all(['td', 'th'])
        data.append([col.get_text(strip=True) for col in cols])
    return data

def extract_images(self, html: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    images = [img.get('src') for img in soup.find_all('img', src=True)]
    return [img for img in images if img]

def extract_meta_tags(self, html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    meta_tags = soup.find_all('meta')
    meta_data = {}
    for tag in meta_tags:
        name = tag.get('name')
        content = tag.get('content')
        if name and content:
            meta_data[name] = content
    return meta_data

def extract_headings(self, html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    headings = {}
    for i in range(1, 7):
        headings[f'h{i}'] = [h.get_text(strip=True) for h in soup.find_all(f'h{i}')]
    return headings
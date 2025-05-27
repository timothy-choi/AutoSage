import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_search_results(url: str, max_results: int = 10) -> List[Dict[str, str]]:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        for result in soup.select("a"):
            href = result.get("href")
            title = result.get_text(strip=True)
            if href and title and href.startswith("http"):
                results.append({"title": title, "url": href, "snippet": ""})
                if len(results) >= max_results:
                    break

        return results

    except Exception as e:
        print(f"Error scraping search results: {e}")
        return []
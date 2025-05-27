import requests
from typing import List, Dict


def search_web_duckduckgo_api(query: str, max_results: int = 10) -> List[Dict[str, str]]:
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [{"title": data.get("Heading", ""), "url": data.get("AbstractURL", ""), "snippet": data.get("Abstract", "")}]
    except:
        return []


def search_web_bing(query: str, api_key: str, max_results: int = 10) -> List[Dict[str, str]]:
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": max_results}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("webPages", {}).get("value", []):
        results.append({
            "title": item.get("name"),
            "url": item.get("url"),
            "snippet": item.get("snippet")
        })
    return results


def search_web_google(query: str, api_key: str, cse_id: str, max_results: int = 10) -> List[Dict[str, str]]:
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "num": min(max_results, 10)
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("items", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("link"),
            "snippet": item.get("snippet")
        })
    return results

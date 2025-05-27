import requests
from typing import List, Dict


def site_search_google(query: str, site: str, api_key: str, cse_id: str, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Perform a site-specific search using Google Custom Search API.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    full_query = f"site:{site} {query}"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": full_query,
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


def site_search_bing(query: str, site: str, api_key: str, max_results: int = 10) -> List[Dict[str, str]]:
    url = "https://api.bing.microsoft.com/v7.0/search"
    full_query = f"site:{site} {query}"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": full_query, "count": max_results}

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


def site_search_duckduckgo(query: str, site: str, max_results: int = 10) -> List[Dict[str, str]]:
    try:
        full_query = f"site:{site} {query}"
        url = f"https://api.duckduckgo.com/?q={full_query}&format=json&no_redirect=1&no_html=1"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [{"title": data.get("Heading", ""), "url": data.get("AbstractURL", ""), "snippet": data.get("Abstract", "")}]
    except:
        return []
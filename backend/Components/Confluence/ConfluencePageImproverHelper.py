import requests
from bs4 import BeautifulSoup
from config import CONFLUENCE_API_BASE, CONFLUENCE_API_HEADERS

def fetch_page_content(page_id: str) -> dict:
    url = f"{CONFLUENCE_API_BASE}/content/{page_id}?expand=body.storage,version"
    response = requests.get(url, headers=CONFLUENCE_API_HEADERS)
    response.raise_for_status()
    return response.json()

def improve_html_content(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    if not soup.find('h2', string='Summary'):
        summary = soup.new_tag('h2')
        summary.string = 'Summary'
        summary_paragraph = soup.new_tag('p')
        summary_paragraph.string = 'This page has been auto-enhanced for clarity and structure.'
        soup.body.insert(0, summary_paragraph)
        soup.body.insert(0, summary)

    for h in soup.find_all(['h3', 'h4', 'h5']):
        h.name = 'h2'

    for br in soup.find_all('br'):
        if not br.next_sibling:
            br.extract()

    return str(soup)

def improve_confluence_page(page_id: str) -> dict:
    try:
        page_data = fetch_page_content(page_id)
        old_content = page_data['body']['storage']['value']
        new_content = improve_html_content(old_content)

        update_payload = {
            "id": page_id,
            "type": "page",
            "title": page_data["title"],
            "version": {
                "number": page_data["version"]["number"] + 1
            },
            "body": {
                "storage": {
                    "value": new_content,
                    "representation": "storage"
                }
            }
        }

        update_url = f"{CONFLUENCE_API_BASE}/content/{page_id}"
        update_response = requests.put(update_url, headers=CONFLUENCE_API_HEADERS, json=update_payload)
        update_response.raise_for_status()

        return {"success": True, "message": f"Page {page_id} improved successfully."}
    except Exception as e:
        return {"success": False, "error": str(e)}
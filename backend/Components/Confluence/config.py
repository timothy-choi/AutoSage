import os


def base64_encode(s: str) -> str:
    import base64
    return base64.b64encode(s.encode()).decode()

CONFLUENCE_API_BASE = os.getenv("CONFLUENCE_API_BASE", "https://your-domain.atlassian.net/wiki/rest/api")

CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL", "your-email@example.com")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN", "your-api-token")

CONFLUENCE_AUTH_HEADERS = {
    "Authorization": f"Basic {os.getenv('CONFLUENCE_AUTH', '')}" or 
                     f"Basic {os.environ.get('BASIC_AUTH_HEADER')}" or
                     f"Basic {base64_encode(CONFLUENCE_EMAIL + ':' + CONFLUENCE_API_TOKEN)}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
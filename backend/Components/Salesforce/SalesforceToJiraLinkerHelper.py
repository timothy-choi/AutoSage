import requests

def fetch_salesforce_records(instance_url, access_token, object_type, fields, limit=10):
    soql = f"SELECT {', '.join(fields)} FROM {object_type} LIMIT {limit}"
    url = f"{instance_url}/services/data/v60.0/query?q={soql}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch Salesforce data: {response.text}")

    return response.json().get("records", [])


def build_salesforce_record_link(instance_url, object_type, record_id):
    return f"{instance_url}/{record_id}"


def post_comment_to_jira(jira_base_url, jira_auth, issue_key, comment_body):
    url = f"{jira_base_url}/rest/api/3/issue/{issue_key}/comment"
    headers = {
        "Authorization": f"Basic {jira_auth}",
        "Content-Type": "application/json"
    }
    payload = {"body": comment_body}
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to post comment to Jira: {response.text}")

    return response.json()
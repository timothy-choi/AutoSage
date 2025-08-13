from flask import Blueprint, request, jsonify
from SalesforceToJiraLinkerHelper import (
    fetch_salesforce_records,
    build_salesforce_record_link,
    post_comment_to_jira
)

salesforce_to_jira_bp = Blueprint("salesforce_to_jira", __name__)

@salesforce_to_jira_bp.route("/salesforce/to/jira", methods=["POST"])
def link_salesforce_to_jira():
    try:
        data = request.get_json()

        records = fetch_salesforce_records(
            instance_url=data["instance_url"],
            access_token=data["access_token"],
            object_type=data["object_type"],
            fields=data["fields"],
            limit=data.get("limit", 5)
        )

        results = []
        for record in records:
            link = build_salesforce_record_link(
                data["instance_url"], data["object_type"], record["Id"]
            )

            summary = " | ".join(f"{f}: {record.get(f, '')}" for f in data["fields"] if f != "Id")
            comment_body = f"*Salesforce Record Linked:*\n[{summary}|{link}]"

            for issue_key in data["issue_keys"]:
                response = post_comment_to_jira(
                    data["jira_base_url"], data["jira_auth"], issue_key, comment_body
                )
                results.append({
                    "issue": issue_key,
                    "record_id": record["Id"],
                    "comment_id": response.get("id")
                })

        return jsonify({"success": True, "linked": results})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
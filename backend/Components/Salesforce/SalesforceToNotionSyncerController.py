from flask import Blueprint, request, jsonify
from SalesforceToNotionSyncerHelper import fetch_salesforce_records, create_notion_page

salesforce_to_notion_syncer_bp = Blueprint("salesforce_to_notion_syncer", __name__)

@salesforce_to_notion_syncer_bp.route("/salesforce/to/notion", methods=["POST"])
def salesforce_to_notion():
    try:
        data = request.get_json()

        salesforce_records = fetch_salesforce_records(
            data["instance_url"],
            data["access_token"],
            data["object_type"],
            data["fields"],
            data.get("limit", 10)
        )

        responses = []
        for record in salesforce_records:
            res = create_notion_page(
                data["notion_token"],
                data["database_id"],
                record,
                data["field_mapping"]
            )
            responses.append(res)

        return jsonify({"success": True, "synced": len(responses), "details": responses})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
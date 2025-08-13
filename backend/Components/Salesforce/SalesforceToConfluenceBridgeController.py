from flask import Blueprint, request, jsonify
from SalesforceToConfluenceBridgeHelper import (
    fetch_salesforce_records,
    format_records_as_confluence_table,
    update_confluence_page
)

salesforce_to_confluence_bp = Blueprint("salesforce_to_confluence", __name__)

@salesforce_to_confluence_bp.route("/salesforce/to/confluence", methods=["POST"])
def bridge_salesforce_to_confluence():
    try:
        data = request.get_json()

        records = fetch_salesforce_records(
            instance_url=data["instance_url"],
            access_token=data["access_token"],
            object_type=data["object_type"],
            fields=data["fields"],
            limit=data.get("limit", 50)
        )

        html_table = format_records_as_confluence_table(records, data["fields"])

        result = update_confluence_page(
            base_url=data["confluence_base_url"],
            auth=data["confluence_basic_auth"],
            page_id=data["confluence_page_id"],
            title=data["confluence_page_title"],
            html_content=html_table
        )

        return jsonify({"success": True, "message": "Page updated", "page": result["id"]})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
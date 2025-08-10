from flask import Blueprint, request, jsonify
from SalesforceFileLinkerHelper import link_file_to_salesforce_record

salesforce_file_linker_bp = Blueprint("salesforce_file_linker", __name__)

@salesforce_file_linker_bp.route("/salesforce/file/link", methods=["POST"])
def link_file_controller():
    data = request.json
    required_keys = ["instance_url", "access_token", "content_document_id", "linked_entity_id"]

    if not all(key in data for key in required_keys):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = link_file_to_salesforce_record(
        instance_url=data["instance_url"],
        access_token=data["access_token"],
        content_document_id=data["content_document_id"],
        linked_entity_id=data["linked_entity_id"],
        visibility=data.get("visibility", "AllUsers")
    )

    status_code = 200 if result.get("success") else 500
    return jsonify(result), status_code
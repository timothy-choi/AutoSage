from flask import Blueprint, request, jsonify
from ConfluenceToGoogleDriveExporterHelper import export_confluence_page_to_gdrive

confluence_to_gdrive_exporter_bp = Blueprint("confluence_to_gdrive_exporter", __name__)

@confluence_to_gdrive_exporter_bp.route("/confluence/export_to_gdrive", methods=["POST"])
def export_to_gdrive():
    data = request.get_json()
    if "page_id" not in data:
        return jsonify({"success": False, "error": "Missing 'page_id'"}), 400

    result = export_confluence_page_to_gdrive(
        page_id=data["page_id"],
        folder_id=data.get("folder_id")
    )

    return jsonify(result), 200 if result.get("success") else 500
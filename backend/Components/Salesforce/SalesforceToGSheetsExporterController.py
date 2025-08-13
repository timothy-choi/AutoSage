from flask import Blueprint, request, jsonify
from SalesforceToGSheetsExporterHelper import fetch_salesforce_records, get_sheets_service, export_to_gsheet

salesforce_to_gsheets_exporter_bp = Blueprint("salesforce_to_gsheets_exporter", __name__)

@salesforce_to_gsheets_exporter_bp.route("/salesforce/to/google-sheets", methods=["POST"])
def export_salesforce_to_google_sheets():
    try:
        data = request.get_json()

        records = fetch_salesforce_records(
            instance_url=data["instance_url"],
            access_token=data["access_token"],
            object_type=data["object_type"],
            fields=data["fields"],
            limit=data.get("limit", 100)
        )

        sheets_service = get_sheets_service(data["service_account_info"])
        export_to_gsheet(
            service=sheets_service,
            spreadsheet_id=data["spreadsheet_id"],
            sheet_name=data["sheet_name"],
            records=records,
            fields=data["fields"]
        )

        return jsonify({"success": True, "message": f"{len(records)} records exported to Google Sheets."})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
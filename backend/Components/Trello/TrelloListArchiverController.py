from flask import Blueprint, request, jsonify
from TrelloListArchiverHelper import archive_trello_list

trello_list_archiver_bp = Blueprint("trello_list_archiver", __name__)

@trello_list_archiver_bp.route("/trello/list/archive", methods=["POST"])
def trello_list_archiver():
    try:
        data = request.get_json()

        result = archive_trello_list(
            api_key=data["api_key"],
            token=data["token"],
            list_id=data["list_id"]
        )

        return jsonify({"success": True, "archived_list": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
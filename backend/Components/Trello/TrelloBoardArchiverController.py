from flask import Blueprint, request, jsonify
from TrelloBoardArchiverHelper import archive_trello_board

trello_board_archiver_bp = Blueprint("trello_board_archiver", __name__)

@trello_board_archiver_bp.route("/trello/board/archive", methods=["POST"])
def trello_board_archiver():
    try:
        data = request.get_json()

        result = archive_trello_board(
            api_key=data["api_key"],
            token=data["token"],
            board_id=data["board_id"],
            archive_lists=data.get("archive_lists", False)
        )

        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
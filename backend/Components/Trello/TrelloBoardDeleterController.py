from flask import Blueprint, request, jsonify
from TrelloBoardDeleterHelper import delete_trello_board

trello_board_deleter_bp = Blueprint("trello_board_deleter", __name__)

@trello_board_deleter_bp.route("/trello/board/delete", methods=["POST"])
def trello_board_deleter():
    try:
        data = request.get_json()

        result = delete_trello_board(
            api_key=data["api_key"],
            token=data["token"],
            board_id=data["board_id"]
        )

        return jsonify({"success": True, "result": result})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
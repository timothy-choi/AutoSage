from flask import Blueprint, request, jsonify
from TrelloBoardCreatorHelper import create_trello_board

trello_board_creator_bp = Blueprint("trello_board_creator", __name__)

@trello_board_creator_bp.route("/trello/board/create", methods=["POST"])
def trello_board_creator():
    try:
        data = request.get_json()

        board = create_trello_board(
            api_key=data["api_key"],
            token=data["token"],
            board_name=data["board_name"],
            default_lists=data.get("default_lists", True),
            desc=data.get("desc"),
            org_id=data.get("org_id"),
            permission_level=data.get("permission_level", "private")
        )

        return jsonify({"success": True, "board": board})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
from flask import Blueprint, request, jsonify
from TrelloBoardClonerHelper import clone_trello_board

trello_board_cloner_bp = Blueprint("trello_board_cloner", __name__)

@trello_board_cloner_bp.route("/trello/board/clone", methods=["POST"])
def trello_board_cloner():
    try:
        data = request.get_json()

        result = clone_trello_board(
            api_key=data["api_key"],
            token=data["token"],
            source_board_id=data["source_board_id"],
            name=data.get("name"),
            keep_cards=data.get("keep_cards", True),
            keep_lists=data.get("keep_lists", True),
            keep_members=data.get("keep_members", False)
        )

        return jsonify({"success": True, "result": result})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
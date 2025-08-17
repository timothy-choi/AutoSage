from flask import Blueprint, request, jsonify
from TrelloCardCommenterHelper import comment_on_trello_card

trello_card_commenter_bp = Blueprint("trello_card_commenter", __name__)

@trello_card_commenter_bp.route("/trello/card/comment", methods=["POST"])
def trello_card_commenter():
    try:
        data = request.get_json()

        result = comment_on_trello_card(
            api_key=data["api_key"],
            token=data["token"],
            card_id=data["card_id"],
            comment_text=data["comment_text"]
        )

        return jsonify({"success": True, "comment": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
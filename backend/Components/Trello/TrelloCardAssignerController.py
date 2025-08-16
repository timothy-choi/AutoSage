from flask import Blueprint, request, jsonify
from TrelloCardAssignerController import assign_members_to_card

trello_card_assigner_bp = Blueprint("trello_card_assigner", __name__)

@trello_card_assigner_bp.route("/trello/card/assign", methods=["POST"])
def trello_card_assigner():
    try:
        data = request.get_json()

        assigned = assign_members_to_card(
            api_key=data["api_key"],
            token=data["token"],
            card_id=data["card_id"],
            member_ids=data["member_ids"]
        )

        return jsonify({"success": True, "assigned": assigned})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
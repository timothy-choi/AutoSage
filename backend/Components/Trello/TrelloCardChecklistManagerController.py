from flask import Blueprint, request, jsonify
from TrelloCardChecklistManagerHelper import create_checklist, add_checklist_item

trello_card_checklist_manager_bp = Blueprint("trello_card_checklist_manager", __name__)

@trello_card_checklist_manager_bp.route("/trello/card/checklist", methods=["POST"])
def manage_checklist():
    try:
        data = request.get_json()
        api_key = data["api_key"]
        token = data["token"]
        card_id = data["card_id"]
        checklist_name = data["checklist_name"]
        items = data.get("items", [])

        checklist = create_checklist(api_key, token, card_id, checklist_name)
        checklist_id = checklist["id"]
        added_items = []

        for item in items:
            result = add_checklist_item(api_key, token, checklist_id, item["name"], item.get("checked", False))
            added_items.append(result)

        return jsonify({
            "success": True,
            "checklist": checklist,
            "items_added": added_items
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
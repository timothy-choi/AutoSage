import requests

def send_slack_message(webhook_url: str, message: str):
    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()
    return {"status": "sent", "message": message}

def format_trello_event(payload: dict) -> str:
    action = payload.get("action", {})
    type_ = action.get("type", "Unknown")
    data = action.get("data", {})
    user = action.get("memberCreator", {}).get("fullName", "Someone")

    if type_ == "createCard":
        card_name = data.get("card", {}).get("name", "")
        list_name = data.get("list", {}).get("name", "")
        return f"🆕 {user} created card *{card_name}* in list *{list_name}*."

    elif type_ == "commentCard":
        card_name = data.get("card", {}).get("name", "")
        comment = action.get("data", {}).get("text", "")
        return f"💬 {user} commented on card *{card_name}*: \"{comment}\""

    elif type_ == "updateCard":
        card_name = data.get("card", {}).get("name", "")
        list_before = data.get("listBefore", {}).get("name")
        list_after = data.get("listAfter", {}).get("name")
        if list_before and list_after:
            return f"🔀 {user} moved *{card_name}* from *{list_before}* to *{list_after}*."
        return f"✏️ {user} updated card *{card_name}*."

    elif type_ == "addMemberToCard":
        card_name = data.get("card", {}).get("name", "")
        member = data.get("member", {}).get("fullName", "a member")
        return f"👤 {user} added *{member}* to card *{card_name}*."

    return f"⚡ Trello event by {user}: {type_}"
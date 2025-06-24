import requests

def send_connection_invitation_real(
    access_token: str,
    recipient_urn: str,
    message: str | None = None
) -> dict:
    url = "https://api.linkedin.com/v2/network/invitations"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "invitee": {
            "com.linkedin.voyager.growth.invitation.InviteeProfile": {
                "profileId": recipient_urn.split(":")[-1]
            }
        }
    }

    if message:
        payload["message"] = message

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return {
            "status": "sent",
            "recipient": recipient_urn,
            "response_code": response.status_code
        }
    except Exception as e:
        return {
            "status": "error",
            "recipient": recipient_urn,
            "message": str(e)
        }


def send_bulk_connection_requests(
    access_token: str,
    recipient_urns: list[str],
    message: str | None = None
) -> list[dict]:
    results = []
    for urn in recipient_urns:
        result = send_connection_invitation_real(access_token, urn, message)
        results.append(result)
    return results
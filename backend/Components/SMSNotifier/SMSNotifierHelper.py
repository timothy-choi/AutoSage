from twilio.rest import Client
import os

def send_sms(
    account_sid: str,
    auth_token: str,
    from_number: str,
    to_number: str,
    message: str
) -> str:
    try:
        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        return msg.sid
    except Exception as e:
        raise RuntimeError(f"Failed to send SMS: {e}")
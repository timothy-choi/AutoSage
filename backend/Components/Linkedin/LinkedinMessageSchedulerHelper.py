import time
from LinkedinMessageSenderHelper import send_message_to_connection

def schedule_linkedin_message(
   public_identifier: str,
   message_text: str,
   scheduled_unix_time: int
):
    current_time = int(time.time())
    delay = scheduled_unix_time - current_time
    if delay > 0:
        time.sleep(delay)

    return send_message_to_connection(public_identifier, message_text)
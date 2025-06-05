import subprocess

def send_imessage(recipient: str, message: str, group: bool = False) -> str:
    if group:
        recipients = [r.strip() for r in recipient.split(",")]
        apple_script = '''
        tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set chatGroup to make new text chat with properties {{participants:{participants}}}
            send "{message}" to chatGroup
        end tell
        '''.replace("{message}", message)

        participant_str = "{" + ",".join([f'"{r}"' for r in recipients]) + "}"
        apple_script = apple_script.replace("{participants}", participant_str)
    else:
        apple_script = f'''
        tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy "{recipient}" of targetService
            send "{message}" to targetBuddy
        end tell
        '''

    process = subprocess.run(["osascript", "-e", apple_script], capture_output=True, text=True)

    if process.returncode != 0:
        raise RuntimeError(f"Failed to send iMessage: {process.stderr.strip()}")

    return "iMessage sent successfully."
import platform
import subprocess
import os
import importlib.util
from typing import Optional

def push_notification(title: str, message: str, timeout: Optional[int] = 5):
    current_os = platform.system()

    if current_os == "Darwin":  # macOS
        command = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", command])

    elif current_os == "Windows":
        try:
            if importlib.util.find_spec("win10toast") is not None:
                from win10toast import ToastNotifier #type: ignore
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=timeout)
            else:
                raise ImportError("win10toast not installed")
        except ImportError:
            ps_script = f'''
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]
            $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
            $toastXml = $template.GetXml()
            $textNodes = $toastXml.GetElementsByTagName("text")
            $textNodes.Item(0).AppendChild($toastXml.CreateTextNode("{title}")) > $null
            $textNodes.Item(1).AppendChild($toastXml.CreateTextNode("{message}")) > $null
            $toast = [Windows.UI.Notifications.ToastNotification]::new($template)
            $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Python Script")
            $notifier.Show($toast)
            '''
            subprocess.run(["powershell", "-Command", ps_script], shell=True)

    elif current_os == "Linux":
        subprocess.run(["notify-send", title, message, f"--expire-time={timeout * 1000}"])

    else:
        print(f"Notifications not supported on this OS: {current_os}")
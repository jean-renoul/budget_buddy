from plyer import notification

class Notification:
    def __init__(self, title, message):
        self.title = title
        self.message = message

    def send(self):
        notification.notify(
            title=self.title,
            message=self.message,
            timeout=10
        )
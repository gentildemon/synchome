import notify2

class Notifier():

    ICON_ERROR="/usr/share/icons/gnome/scalable/status/network-error-symbolic.svg"
    ICON_REFRESH="/usr/share/icons/gnome/scalable/actions/view-refresh-symbolic.svg"
    ICON_OK="/usr/share/icons/gnome/scalable/emblems/emblem-default-symbolic.svg"

    def __init__(self, app_name):
        notify2.init(app_name)

    def notify_info(self, title, message, icon=""):
        notification = notify2.Notification(title, message, icon)
        notification.set_category("transfer")
        notification.show()

    def notify_error(self, title, message):
        notification = notify2.Notification(title, message, self.ICON_ERROR)
        notification.set_category("transfer.error")
        notification.set_urgency(notify2.URGENCY_CRITICAL)
        notification.show()



def test_notifier():
    """Test function for Notifier"""
    notifier = Notifier("test.Notifier")
    notifier.notify_info("Success", "Success message", Notifier.ICON_OK)
    notifier.notify_error("Error", "Error message")

if __name__ == "__main__":
    test_notifier()

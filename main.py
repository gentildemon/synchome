import appindicator
import notifier

import gui
import sync
from profile import ProfilesList

APP_NAME="SyncHome"


def main():
    my_notifier = notifier.Notifier(APP_NAME)
    my_synchronizer = sync.Synchronizer(my_notifier)

    ind = appindicator.Indicator(APP_NAME,
                                 "network-idle",
                                 appindicator.CATEGORY_APPLICATION_STATUS)
    ind.set_status(appindicator.STATUS_ACTIVE)
    ind.set_attention_icon("network-error")

    profiles = ProfilesList.GetProfiles()

    # create a menu
    app = gui.AppMenu(my_synchronizer)
    menu = app.create_main_menu(profiles)
    ind.set_menu(menu)

    # prepare signal handler
    #signal.signal(signal.SIGHUP, signal_handler)
    #save_pid()

    app.main()


if __name__ == "__main__":
    main()

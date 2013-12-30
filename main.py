# coding=utf-8

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

    app = gui.AppMenu(my_synchronizer, profiles)
    menu = app.get_main_menu()
    ind.set_menu(menu)

    app.main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Exiting..."

# coding=utf-8

import appindicator
import notifier

import app_menu
import sync

import network

from profile import ProfilesList

APP_NAME = "SyncHome"


def main():
    my_notifier = notifier.Notifier(APP_NAME)
    my_synchronizer = sync.Synchronizer(my_notifier)

    ind = appindicator.Indicator(APP_NAME,
                                 "network-idle",
                                 appindicator.CATEGORY_APPLICATION_STATUS)
    ind.set_status(appindicator.STATUS_ACTIVE)
    ind.set_attention_icon("network-error")

    profiles = ProfilesList.GetProfiles()

    app = app_menu.AppMenu(my_synchronizer, profiles)
    menu = app.get_main_menu()
    ind.set_menu(menu)

    def sync_all(connected):
        if connected == True:
            app.sync_all()

    nm = network.Network()
    sync_all(nm.is_connected())

    nm.listen_to_state_changes(sync_all)

    app.main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Exiting..."

import gobject
import gtk
import profile as Profile

from filebrowser import OpenFileBrowser

ICON_OK="/usr/share/icons/gnome/48x48/emblems/emblem-default.png"
ICON_ERROR="/usr/share/icons/gnome/scalable/status/dialog-error-symbolic.svg"
ICON_UNKNOWN="/usr/share/icons/gnome/scalable/status/dialog-warning-symbolic.svg"

BROWSE_LOCAL_LABEL = 'Explorer'
BROWSE_REMOTE_LABEL = 'Explorer sur le serveur'

SYNC_AUTO_LABEL = 'Synchroniser'
SYNC_NOAUTO_LABEL = 'Synchroniser (interactif)'

SYNC_ALL_LABEL = 'Tout synchroniser'
EXIT_LABEL = 'Quitter'


class AppMenu():

    def __init__(self, synchronizer, profiles):
        self.__synchronizer = synchronizer
        self.__profiles = profiles
        self.__main_menu = self.create_main_menu(profiles)

    def get_main_menu(self):
        return self.__main_menu

    def get_profile_submenu(self, menu_item, profile):
        menu = gtk.Menu()

        item = gtk.MenuItem(BROWSE_LOCAL_LABEL)
        item.connect("activate", AppMenu.BrowseLocalDir, profile)
        menu.append(item)

        item = gtk.MenuItem(BROWSE_REMOTE_LABEL)
        item.connect("activate", AppMenu.BrowseRemoteDir, profile)
        menu.append(item)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        item = gtk.MenuItem(SYNC_AUTO_LABEL)
        item.connect("activate", self.sync_profile, menu_item, profile, True)
        menu.append(item)

        item = gtk.MenuItem(SYNC_NOAUTO_LABEL)
        item.connect("activate", self.sync_profile, menu_item, profile, False)
        menu.append(item)

        return menu

    def get_profile_menuitem(self, profile):
        item = gtk.ImageMenuItem(profile.getname())
        item.set_always_show_image(True)

        self.update_profile_status(item, profile)

        submenu = self.get_profile_submenu(item, profile)
        item.set_submenu(submenu)

        return item

    def create_main_menu(self, profiles):
        menu = gtk.Menu()

        for profile in profiles:
            menuitem = self.get_profile_menuitem(profile)
            menu.append(menuitem)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menu_item = gtk.MenuItem(SYNC_ALL_LABEL)
        menu.append(menu_item)
        menu_item.connect("activate", self.sync_all)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menu_item = gtk.MenuItem(EXIT_LABEL)
        menu.append(menu_item)
        menu_item.connect("activate", self.exit)

        menu.show_all()

        return menu

    def sync_profile(self, menuitem, parent_menu_item, profile, auto):
        self.__synchronizer.sync(profile, auto)
        self.update_profile_status(parent_menu_item, profile)

    def sync_all(self, menuitem):
        self.__synchronizer.sync_all(self.__profiles)
        for profile in self.__profiles:
            for item in menuitem.parent.children():
                if item.get_label().startswith("%s (" % profile.getname()):
                    self.update_profile_status(item, profile)

    def update_profile_status(self, menu_item, profile):
        status = profile.getstatus()
        if status == Profile.Profile.OK:
            icon = ICON_OK
        elif status == Profile.Profile.ERROR:
            icon = ICON_ERROR
        else:
            icon = ICON_UNKNOWN

        image = menu_item.get_image()
        image.set_from_file(icon)
        image.show()
        menu_item.set_label(profile.getname() + " (" + profile.getupdatetime() + ")")

    @classmethod
    def BrowseLocalDir(cls, menuitem, profile):
        OpenFileBrowser(profile.getlocaldir())

    @classmethod
    def BrowseRemoteDir(cls, menuitem, profile):
        OpenFileBrowser(profile.getremotedir())

    def exit(*args):
        gtk.main_quit()

    def main(self):
        gtk.main()


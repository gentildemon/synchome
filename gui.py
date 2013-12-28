import gobject
import gtk
import profile

from filebrowser import OpenFileBrowser

ICON_OK="/usr/share/icons/gnome/48x48/emblems/emblem-default.png"

BROWSE_LOCAL_LABEL = 'Explorer'
BROWSE_REMOTE_LABEL = 'Explorer sur le serveur'

SYNC_AUTO_LABEL = 'Synchroniser'
SYNC_NOAUTO_LABEL = 'Synchroniser (interactif)'

SYNC_ALL_LABEL = 'Tout synchroniser'
EXIT_LABEL = 'Quitter'

class AppMenu():

    __synchronizer = None

    def __init__(self, synchronizer):
        AppMenu.__synchronizer = synchronizer

    def get_profile_submenu(self, profile):
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
        item.connect("activate", AppMenu.SyncProfile, profile, True)
        menu.append(item)

        item = gtk.MenuItem(SYNC_NOAUTO_LABEL)
        item.connect("activate", AppMenu.SyncProfile, profile, False)
        menu.append(item)

        return menu

    def get_profile_menuitem(self, profile):
        submenu = self.get_profile_submenu(profile)

        item = gtk.ImageMenuItem(profile.getname())
        item.set_always_show_image(True)

        AppMenu.UpdateProfileStatus(item, profile)

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
        menu_item.connect("activate", AppMenu.SyncAll)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menu_item = gtk.MenuItem(EXIT_LABEL)
        menu.append(menu_item)
        menu_item.connect("activate", AppMenu.ExitMenu)

        menu.show_all()

        return menu

    @classmethod
    def UpdateProfileStatus(cls, menu_item, profile):
        status = profile.getstatus()
        if status == Profile.OK:
            icon = ICON_OK
        elif status == Profile.ERROR:
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

    @classmethod
    def SyncProfile(cls, menuitem, profile, auto):
        cls.__synchronizer.sync(profile, auto)

    @classmethod
    def SyncAll(*args):
        # TODO
        pass

    @classmethod
    def ExitMenu(*args):
        gtk.main_quit()

    def main(self):
        gtk.main()


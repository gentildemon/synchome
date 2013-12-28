import gobject
import gtk
import profile

from filebrowser import OpenFileBrowser

ICON_OK="/usr/share/icons/gnome/48x48/emblems/emblem-default.png"



class AppMenu():


    def get_profile_submenu(self, profile):
        menu = gtk.Menu()

        browse_label = "Explorer"
        item = gtk.MenuItem(browse_label)
        item.connect("activate", AppMenu.BrowseLocalDir, profile)
        menu.append(item)

        browse_label = "Explorer sur le serveur"
        item = gtk.MenuItem(browse_label)
        item.connect("activate", AppMenu.BrowseRemoteDir, profile)
        menu.append(item)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        sync_label = "Synchroniser"
        item = gtk.MenuItem(sync_label)
        item.connect("activate", AppMenu.SyncProfile, profile, True)
        menu.append(item)

        sync_term_label = "Synchroniser (interactif)"
        item = gtk.MenuItem(sync_term_label)
        item.connect("activate", AppMenu.SyncProfile, profile, False)
        menu.append(item)

        return menu

    def get_profile_menuitem(self, profile):
        submenu = self.get_profile_submenu(profile)
        myimage = gtk.image_new_from_file(ICON_OK)

        item = gtk.ImageMenuItem(profile.getname())
        item.set_image(myimage)
        item.set_always_show_image(True)
        #update_status(item)

        item.set_submenu(submenu)
        return item

    def create_main_menu(self, profiles):
        menu = gtk.Menu()

        for profile in profiles:
            menuitem = self.get_profile_menuitem(profile)
            menu.append(menuitem)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        synchro_all_label = "Tout synchroniser"
        menu_item = gtk.MenuItem(synchro_all_label)
        menu.append(menu_item)
        menu_item.connect("activate", AppMenu.SyncAll)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        exit_label = "Quitter"
        menu_item = gtk.MenuItem(exit_label)
        menu.append(menu_item)
        menu_item.connect("activate", AppMenu.ExitMenu)

        menu.show_all()

        return menu

    @classmethod
    def BrowseLocalDir(cls, menuitem, profile):
        OpenFileBrowser(profile.getlocaldir())

    @classmethod
    def BrowseRemoteDir(cls, menuitem, profile):
        OpenFileBrowser(profile.getremotedir())

    @classmethod
    def SyncProfile(cls, menuitem, profile, auto):
        print "%s : %s" % (profile.getname(), auto)

    @classmethod
    def SyncAll(*args):
        # TODO
        pass

    @classmethod
    def ExitMenu(*args):
        gtk.main_quit()

    def main(self):
        gtk.main()


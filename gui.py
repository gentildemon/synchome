import gobject
import gtk
import profile


class AppMenu():


    def get_submenu(self, profile):
        menu = gtk.Menu()

        sync_label = "Synchroniser"
        item = gtk.MenuItem(sync_label)
        item.connect("activate", sync_profile, profile)
        menu.append(item)

        browse_label = "Explorer"
        item = gtk.MenuItem(browse_label)
        item.connect("activate", browse_profile, profile)
        menu.append(item)

        browse_label = "Explorer sur le serveur"
        item = gtk.MenuItem(browse_label)
        item.connect("activate", browse_remote_profile, profile)
        menu.append(item)

        sync_term_label = "Synchroniser (interactif)"
        item = gtk.MenuItem(sync_term_label)
        item.connect("activate", sync_term_profile, profile)
        menu.append(item)

        return menu

    def create_main_menu(self, profiles):
        menu = gtk.Menu()

        #for profile in profiles:
        #    submenu = self.get_submenu(profile)
            
        

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        synchro_all_label = "Tout synchroniser"
        menu_item = gtk.MenuItem(synchro_all_label)
        menu.append(menu_item)
        menu_item.connect("activate", AppMenu.SyncAll, None)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        exit_label = "Quitter"
        menu_item = gtk.MenuItem(exit_label)
        menu.append(menu_item)
        menu_item.connect("activate", AppMenu.ExitMenu, None)

        menu.show_all()

        return menu

    @classmethod
    def SyncAll(*args):
        # TODO
        pass

    @classmethod
    def ExitMenu(*args):
        gtk.main_quit()


    def main(self):
        gtk.main()


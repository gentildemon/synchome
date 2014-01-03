import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop

class Network:
    SERVICE = 'org.freedesktop.NetworkManager'
    OBJECT_PATH= '/org/freedesktop/NetworkManager'
    INTERFACE = SERVICE
    STATE_CONNECTED_GLOBAL = 70

    STATE_SIGNAL = 'StateChanged'
    STATE_PROPERTY = 'State'

    def __init__(self):
        DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()
        self.handler = None

    def __state_is_connected(self, state):
        if state == self.STATE_CONNECTED_GLOBAL:
            return True
        return False

    def __my_handler(self, state):
        connected = self.__state_is_connected(state)
        self.handler(connected)

    def listen_to_state_changes(self, handler):
        self.handler = handler
        self.bus.add_signal_receiver(self.__my_handler,
                                self.STATE_SIGNAL,
                                self.INTERFACE)

    def is_connected(self):
        proxy = self.bus.get_object(self.SERVICE, self.OBJECT_PATH)
        prop = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
        state = prop.Get(self.INTERFACE, self.STATE_PROPERTY)
        return self.__state_is_connected(state)


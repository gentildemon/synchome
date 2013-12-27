import os
import commands
import subprocess
import notify2

APP_NAME="SyncHome"

class Notifier():

    ICON_ERROR="/usr/share/icons/gnome/scalable/status/network-error-symbolic.svg"
    ICON_REFRESH="/usr/share/icons/gnome/scalable/actions/view-refresh-symbolic.svg"
    ICON_OK="/usr/share/icons/gnome/scalable/emblems/emblem-default-symbolic.svg"

    def __init__(self):
        notify2.init(APP_NAME)

    def notify_info(self, title, message, icon=""):
        notification = notify2.Notification(title, message, icon)
        notification.set_category("transfer")
        notification.show()

    def notify_error(self, title, message):
        notification = notify2.Notification(title, message, self.ICON_ERROR)
        notification.set_category("transfer.error")
        notification.set_urgency(notify2.URGENCY_CRITICAL)
        notification.show()


class Profile():

    UNISON_PREF_DIR = os.environ['HOME'] + "/.unison/"
    BROWSER_BIN = "/usr/bin/nautilus"

    def __init__(self, name):
        self.__name = name
        self.__configpath = self.UNISON_PREF_DIR + name + '.prf'
        self.__statuspath = self.UNISON_PREF_DIR + name + '.status'
        self.__localdir = self.__getlocaldir()
        self.__remotedir = self.__getremotedir()
        self.__status = 'unknown'
        self.__utime = 'unknown'

    def __getlocaldir(self):
        cmd = "grep '^root = /' " + self.__configpath + " | cut -d= -f2"
        _status, output = commands.getstatusoutput(cmd)
        return output

    def __getremotedir(self):
        cmd = "grep '^root = ssh' " + self.__configpath + " | cut -d= -f2"
        _status, output = commands.getstatusoutput(cmd)
        return output

    def getname(self):
        """Return the name of the profile"""
        return self.__name

    def getlocaldir(self):
        return self.__localdir

    def getremotedir(self):
        return self.__remotedir

    def __browse(self, directory):
        cmd = self.BROWSER_BIN + " " + directory
        subprocess.call(cmd, shell=True)

    def browse_local(self):
        self.__browse(self.__localdir)

    def browse_remote(self):
        self.__browse(self.__remotedir)

    def read_status_from_file(self):
        date = ""
        try:
            f = open(statusfile)
            content = f.readlines()
            self.__status = content[0][:-1]
            self.__utime = content[1][:-1]
            f.close()
        except IOError:
            print "Fail to read from " + statusfile



    @classmethod
    def GetNames(cls):
        names = []
        files = os.listdir(cls.UNISON_PREF_DIR)

        for f in files:
            if f[-4:] == ".prf" and f != "default.prf":
                profile = f[:-4]
                names.append(profile)
        return names



def testprofile():
    profiles = Profile.GetNames()
    for profilename in profiles:
        profile = Profile(profilename)
        print "[%s]\n local = %s\n remote = %s" % (profile.getname(), profile.getlocaldir(), profile.getremotedir())

def testnotifier():
    notifier = Notifier()
    notifier.notify_info("/home/test", "Synchronisation OK", Notifier.ICON_OK)
    notifier.notify_error("Home/test2", "Synchro KO")


if __name__ == "__main__":
    testprofile()
    testnotifier()


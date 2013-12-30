# coding=utf-8

import datetime
import subprocess


class Synchronizer():

    def __init__(self, notifier):
        self.__notifier = notifier

    def __test_server(self, profile):
        retcode = subprocess.call(['unison', '-testserver', profile.getname()])
        if retcode != 0:
            self.__notifier.notify_error(profile.getname(),
                            "Server indisponible, synchronisation impossible")
            return False

        return True
        
    def __notify_result(self, retcode, profile):
        currenttime = datetime.datetime.now()
        if retcode == 0:
            self.__notifier.notify_info(profile.getname(),
                            "synchronisation ok", self.__notifier.ICON_OK)
        else:
            self.__notifier.notify_error(profile.getname(),
                            "échec de la synchronisation. Les conflits doivent être résolus manuellement")
        profile.update_status(retcode, currenttime)

    def __sync_auto(self, profile):
        retcode = subprocess.call(['unison', '-batch', profile.getname()])
        self.__notify_result(retcode, profile)

    def __sync_noauto(self, profile):
        retcode = subprocess.call(['gnome-terminal',
                                "--title=Synchronisation interactive - %s" % profile.getname(),
                                '--command', 
                               "sh -c 'unison %s; ret=$?; read var; exit $ret'" % profile.getname()])
        self.__notify_result(retcode, profile)

    def sync(self, profile, auto):

        ret = self.__test_server(profile)
        if not ret:
            return False

        if auto:
            ret = self.__sync_auto(profile)
        else:
            ret = self.__sync_noauto(profile)

        return ret

    def sync_all(self, profiles):
        for profile in profiles:
            ret = self.sync(profile, True)
            if ret == False:
                return False

import os
import commands


class ProfileParser():

    def __init__(self, profilepath):
        self.__configpath = profilepath
        self.__localdir = self.__getlocaldir()
        self.__remotedir = self.__getremotedir()

    def __getlocaldir(self):
        cmd = "grep '^root = /' " + self.__configpath + " | cut -d= -f2"
        _status, output = commands.getstatusoutput(cmd)
        return output

    def __getremotedir(self):
        cmd = "grep '^root = ssh' " + self.__configpath + " | cut -d= -f2"
        _status, output = commands.getstatusoutput(cmd)
        return output

    def getlocaldir(self):
        return self.__localdir

    def getremotedir(self):
        return self.__remotedir


class Profile():

    OK = 'Ok'
    ERROR = 'Error'
    UNKNOWN = 'Unknown'

    def __init__(self, name, localdir, remotedir, statusfile):
        self.__name = name
        self.__localdir = localdir
        self.__remotedir = remotedir
        self.__status = Profile.UNKNOWN
        self.__utime = 'unknown'
        self.__statusfile = statusfile
        self.init_status()

    def getname(self):
        """Return the name of the profile"""
        return self.__name

    def getlocaldir(self):
        return self.__localdir

    def getremotedir(self):
        return self.__remotedir

    def getstatus(self):
        return self.__status

    def getupdatetime(self):
        return self.__utime

    def init_status(self):
        date = ""
        with open(self.__statusfile) as sf:
            content = sf.readlines()
            status = content[0][:-1]
            self.__status = content[0][:-1]
            self.__utime = content[1][:-1]

    def update_status(self, retcode, currenttime):
        if retcode == 0:
            self.__status = Profile.OK
        else:
            self.__status = Profile.ERROR
        with open(self.__statusfile, 'w') as sf:
            sf.writelines((self.__status, currenttime.strftime("%A %e %B, %X")))

    def print_info(self):
        print "[%s]\n local = %s\n remote = %s" % (self.getname(),
             self.getlocaldir(), self.getremotedir())
        print " status = %s (%s)" % (self.__status, self.__utime)


class ProfilesList():

    UNISON_PREF_DIR = os.environ['HOME'] + '/.unison/'

    @classmethod
    def GetProfiles(cls):
        profiles = []
        files = os.listdir(cls.UNISON_PREF_DIR)

        for f in files:
            if f[-4:] == '.prf' and f != 'default.prf':
                fullpath = cls.UNISON_PREF_DIR + '/' + f
                profilename = f[:-4]
                statusfile = cls.UNISON_PREF_DIR + '/' + profilename + '.status'
                pf_parser = ProfileParser(fullpath)
                profile = Profile(profilename,
                                    pf_parser.getlocaldir(), 
                                    pf_parser.getremotedir(),
                                    statusfile)
                profiles.append(profile)
        return profiles


def test_profile():
    profiles = ProfilesList.GetProfiles()
    for profile in profiles:
        profile.print_info()


if __name__ == "__main__":
    test_profile()


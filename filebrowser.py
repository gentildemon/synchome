import subprocess

BROWSER_BIN = "/usr/bin/nautilus"

def OpenFileBrowser(directory):
    cmd = BROWSER_BIN + " " + directory
    subprocess.call(cmd, shell=True)


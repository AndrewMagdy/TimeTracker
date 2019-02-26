import sys
import time
import threading
from subprocess import Popen, PIPE

from AppKit import NSApplication, NSApp, NSWorkspace
from Foundation import NSObject, NSLog
from PyObjCTools import AppHelper
from Quartz import kCGWindowListOptionOnScreenOnly, kCGNullWindowID, CGWindowListCopyWindowInfo


active_title = {
    "chrome": "tell application \"Google Chrome\" to return title of active tab of front window"}


def getBundleIdentifier():
    #print(NSWorkspace.sharedWorkspace().runningApplications())
    apps = NSWorkspace.sharedWorkspace().runningApplications()
    for app in apps:
        if app.isActive():
            print app.localizedName()


def getBrowserTabTitle(bundleIdentifier):
    script = active_title[bundleIdentifier]
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE,
              stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(script)
    print(stdout, stderr)
    return stdout


def isBrowser(bundleIdentifier):
    return bundleIdentifier in active_title


def main():
    bundleIdentifier = getBundleIdentifier()
    tabTitle = getBrowserTabTitle(
        bundleIdentifier) if isBrowser(bundleIdentifier) else ""
    print (bundleIdentifier, tabTitle)
    threading.Timer(1, main).start()


if __name__ == '__main__':
    main()

import threading
import time

from AppKit import NSApplication, NSApp, NSWorkspace
from Foundation import NSObject, NSLog
from PyObjCTools import AppHelper
from Quartz import kCGWindowListOptionOnScreenOnly, kCGNullWindowID, CGWindowListCopyWindowInfo
from Foundation import NSRunLoop, NSDate


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        workspace = NSWorkspace.sharedWorkspace()
        activeApps = workspace.runningApplications()
        curr_app = workspace.frontmostApplication()
        for app in activeApps:
            if app.isActive():
                options = kCGWindowListOptionOnScreenOnly
                windowList = CGWindowListCopyWindowInfo(options,
                                                        kCGNullWindowID)
                for window in windowList:
                    NSLog('%@', window)
                    break
                break
        AppHelper.stopEventLoop()


def main():
    NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()


if __name__ == '__main__':
    time.sleep(5)
    main()

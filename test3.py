from PyObjCTools import AppHelper
from Foundation import NSObject, NSKeyValueObservingOptionNew, NSKeyValueChangeNewKey
from Foundation import NSRunLoop, NSDate
from AppKit import NSApplication, NSApp, NSWorkspace

from subprocess import Popen, PIPE
import threading
import json


isBrowser = False
localizedName = None
active_url = None


def getBrowserTabTitle():
    global localizedName
    global isBrowser
    if not isBrowser:
        return
    script = active_url[localizedName]
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE,
              stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(script)
    print(stdout, stderr)
    threading.Timer(1, getBrowserTabTitle).start()


class Observer(NSObject):
    def observeValueForKeyPath_ofObject_change_context_(self, path, object, changeDescription, context):
        global localizedName
        global isBrowser
        frontmostApplication = changeDescription[NSKeyValueChangeNewKey]
        localizedName = frontmostApplication.localizedName()
        bundleIdentifier = frontmostApplication.bundleIdentifier()
        print (localizedName, bundleIdentifier)
        isBrowser = False
        if (localizedName in active_url):
            isBrowser = True
            getBrowserTabTitle()


class FrontMostAppObserver:
    def __init__(self):
        self.observer = Observer.new()
        NSWorkspace.sharedWorkspace().addObserver_forKeyPath_options_context_(
            self.observer, "frontmostApplication", NSKeyValueObservingOptionNew, 0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        NSWorkspace.sharedWorkspace().removeObserver_forKeyPath_(
            self.observer, "frontmostApplication")


def loadJson():
    global active_url
    with open('scripts.json') as f:
        active_url = json.load(f)


def main():
    loadJson()
    with FrontMostAppObserver() as frontMostAppObserver:
        AppHelper.runConsoleEventLoop(installInterrupt=True)


if __name__ == '__main__':
    main()

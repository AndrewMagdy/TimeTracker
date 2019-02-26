import sys
import json
import threading
if sys.platform == "darwin":
    from PyObjCTools import AppHelper
    from Foundation import NSObject, NSKeyValueObservingOptionNew, NSKeyValueChangeNewKey
    from Foundation import NSRunLoop, NSDate
    from AppKit import NSApplication, NSApp, NSWorkspace
    from subprocess import Popen, PIPE


active_url = None


class Observer(NSObject):
    def observe_(self, callback):
        self.callback = callback
        return self

    def observeValueForKeyPath_ofObject_change_context_(self, path, object, changeDescription, context):
        self.callback(changeDescription[NSKeyValueChangeNewKey])


class FrontMostAppObserver:
    def __init__(self):
        self.observer = Observer.alloc().init().observe_(self.observerCallback)
        NSWorkspace.sharedWorkspace().addObserver_forKeyPath_options_context_(
            self.observer, "frontmostApplication", NSKeyValueObservingOptionNew, 0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        NSWorkspace.sharedWorkspace().removeObserver_forKeyPath_(
            self.observer, "frontmostApplication")

    def observerCallback(self, frontmostApplication):
        global active_url
        self.localizedName = frontmostApplication.localizedName()
        self.bundleIdentifier = frontmostApplication.bundleIdentifier()
        self.isBrowser = True if self.localizedName in active_url else False
        if (self.isBrowser):
            self.getBrowserTabTitle()

    def getBrowserTabTitle(self):
        global active_url
        if not self.isBrowser:
            return
        script = active_url[self.localizedName]
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE,
                  stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(script)
        print(stdout, stderr)
        threading.Timer(1, self.getBrowserTabTitle).start()


def loadJson():
    global active_url
    with open('scripts.json') as f:
        active_url = json.load(f)


def main():
    if sys.platform == "darwin":
        loadJson()
        with FrontMostAppObserver() as frontMostAppObserver:
            AppHelper.runConsoleEventLoop(installInterrupt=True)

if __name__ == '__main__':
    main()

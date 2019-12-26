import json
import time
import threading
from urllib.parse import urlparse

from PyObjCTools import AppHelper
from Foundation import NSObject, NSKeyValueObservingOptionNew, NSKeyValueChangeNewKey
from Foundation import NSRunLoop, NSDate
from AppKit import NSApplication, NSApp, NSWorkspace
from subprocess import Popen, PIPE


class Observer(NSObject):
    def observe_(self, callback):
        self.callback = callback
        return self

    def observeValueForKeyPath_ofObject_change_context_(self, path, object, changeDescription, context):
        self.callback(changeDescription[NSKeyValueChangeNewKey])


class FrontMostAppObserver:
    lastActivityBundleIdentifier = None
    lastActivityLocalizedName = None
    lastActivityIsBrowser = None
    lastActivityUrl = None
    lastActivityTimestamp = None
    db = None

    def __init__(self, db):
        self.db = db
        self.loadBrowserScripts()
        self.setupObserver()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        NSWorkspace.sharedWorkspace().removeObserver_forKeyPath_(
            self.observer, "frontmostApplication")

    def setupObserver(self):
        # Invoke callback with initial app
        self.observerCallback(
            NSWorkspace.sharedWorkspace().frontmostApplication())

        self.observer = Observer.alloc().init().observe_(self.observerCallback)
        NSWorkspace.sharedWorkspace().addObserver_forKeyPath_options_context_(
            self.observer, "frontmostApplication", NSKeyValueObservingOptionNew, 0)

    def loadBrowserScripts(self):
        with open('scripts.json') as f:
            self.browserScripts = json.load(f)

    def observerCallback(self, frontmostApplication):
        self.localizedName = frontmostApplication.localizedName()
        self.bundleIdentifier = frontmostApplication.bundleIdentifier()
        self.isBrowser = True if self.localizedName in self.browserScripts else False
        
        if self.isBrowser:
            self.browserCallback()
        else:
            self.addEntry()

    def execAppleScript(self, script):
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE,
                  stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(script)
        if not stderr:
            return stdout

    def browserCallback(self):
        if not self.isBrowser:
            self.url = None
            return

        browserScript = self.browserScripts[self.localizedName]
        self.url = self.execAppleScript(browserScript)
        
        if self.lastActivityUrl != self.url or self.lastActivityBundleIdentifier != self.bundleIdentifier:
            self.addEntry()
        
        threading.Timer(5, self.browserCallback).start() # Keep polling while browser is open

    def addEntry(self):
        currTime = time.time()

        print (self.lastActivityBundleIdentifier, self.lastActivityLocalizedName,
               self.lastActivityIsBrowser, self.lastActivityUrl, self.lastActivityTimestamp, currTime)
        
        if self.lastActivityBundleIdentifier: 
            self.db.addEntry(self.lastActivityBundleIdentifier,self.lastActivityLocalizedName,
                self.lastActivityTimestamp, currTime, self.lastActivityIsBrowser, self.lastActivityUrl)

        self.lastActivityBundleIdentifier = self.bundleIdentifier
        self.lastActivityLocalizedName = self.localizedName
        self.lastActivityIsBrowser = self.isBrowser
        self.lastActivityTimestamp = currTime
        if self.isBrowser:
            self.lastActivityUrl = self.url
            # uri_parsed = urlparse(uri)
            # domain = '{uri.netloc}'.format(uri=uri_parsed)
        else:
            self.lastActivityUrl = None


def runMac(db):
    with FrontMostAppObserver(db):
        AppHelper.runConsoleEventLoop(installInterrupt=True)

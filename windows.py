import win32gui
import threading

def runWindows():
    # http://stackoverflow.com/a/608814/562769
    window = win32gui.GetForegroundWindow()
    active_window_name = win32gui.GetWindowText(window)
    print(active_window_name)
    threading.Timer(1, runWindows).start()
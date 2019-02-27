import sys
if sys.platform == "darwin":
    from mac import runMac 


def main():
    if sys.platform == "darwin":
        runMac()
    elif sys.platform in ['Windows', 'win32', 'cygwin']:
        # http://stackoverflow.com/a/608814/562769
        import win32gui
        window = win32gui.GetForegroundWindow()
        active_window_name = win32gui.GetWindowText(window)
        print(active_window_name)


if __name__ == '__main__':
    main()

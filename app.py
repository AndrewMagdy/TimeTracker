import sys
if sys.platform == "darwin":
    from mac import runMac 
elif sys.platform in ['Windows', 'win32', 'cygwin']:
    from windows import runWindows

def main():
    if sys.platform == "darwin":
        runMac()
    elif sys.platform in ['Windows', 'win32', 'cygwin']:
        runWindows()

if __name__ == '__main__':
    main()

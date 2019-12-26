import sys
from db import DB

if sys.platform == "darwin":
    from mac import runMac 
elif sys.platform in ['Windows', 'win32', 'cygwin']:
    from windows import runWindows

def main():
    #initDB()
    db = DB()
    if sys.platform == "darwin":
        runMac(db)
    elif sys.platform in ['Windows', 'win32', 'cygwin']:
        runWindows()

if __name__ == '__main__':
    main()
 
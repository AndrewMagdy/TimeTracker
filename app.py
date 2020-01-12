import sys
from threading import Thread
from webServer import app

if sys.platform == "darwin":
    from mac import runMac 
elif sys.platform in ['Windows', 'win32', 'cygwin']:
    from windows import runWindows

def flaskThread():
    app.run(debug=True, use_reloader=False)
    
def main():
    thread = Thread(target = flaskThread, args = [])
    thread.start()
    thread.join()

    if sys.platform == "darwin":
        runMac()
    elif sys.platform in ['Windows', 'win32', 'cygwin']:
        runWindows()

if __name__ == '__main__':
    main()
 
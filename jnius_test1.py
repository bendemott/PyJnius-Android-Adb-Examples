"""
jnius_test1.py Tests
--------------------
Heres a list of the code-tasks we perform in this script. 

Once you have connected a device you can run the scripts using ``python jnius_test1.py``

-    (done) Test autoclass functionality
-    (done) Test autoclass with built-in java objects
-    (done) Test ChimpChat AdbBackend
-    (done) Test adb connection using waitForConnection
-    (done) Test IChimpDevice interface
-    (done) Retrieve device properties

**Troubleshooting:**

    - To see if your device is being seen you should use the adb command line first and execute
    
      ``adb devices``
      
    - You must have **usb debugging** enabled on your device, or NO device will be found.
    - If you get a ``BrokenPipe`` exception printed on the command line, you may need to unlock the device manually before running this script.  Sometimes the adb conneciton can break if the device sleeps too quickly.

    
"""
import sys
from jnius import autoclass


__author__ = "Ben DeMott"


def main(argv=None):
    System = autoclass('java.lang.System')
    print "\nClass Path:", System.getProperty('java.class.path')
    AdbBackend = autoclass('com.android.chimpchat.adb.AdbBackend')

    adb = AdbBackend()
    print "\nAdbBackend Object: ", adb

    TIMEOUT = 5000 # (ms)
    ANY_DEVICE = '.*'  #This could be the device serial number also.
    device = adb.waitForConnection(TIMEOUT, ANY_DEVICE)
    if not device:
        print "NO DEVICE FOUND"
        quit()

    # IChimpDevice http://code.google.com/p/aster/source/browse/src/com/android/chimpchat/adb/AdbChimpDevice.java
    # IDevice is a property of IChimpDevice - IDevice offers a lot more features.

    print "DEVICE: ", device
    mod = device.getProperty('build.model')
    print "Model:", mod
    # This returns a Java Collection, this object is not converted automatically into a python type
    collection = device.getPropertyList()
    # Pretty much any iterable in Java can be converted to an Array using 'toArray' - this results in a native python list
    props = collection.toArray()
    # this will be a list
    print "\nAnd here's our native Python List:"
    print type(props)

    print "\nAndroid Device Properties:"
    for p in props:
            print p.ljust(25), device.getProperty(p)


if __name__ == "__main__":
    sys.exit(main(argv=sys.argv))
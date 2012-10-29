"""

jnius_test2.py Tests
--------------------
Heres a list of the code-tasks we perform in this script. 

Once you have connected a device you can run the scripts using ``python jnius_test2.py``

-    (done) Test ChimpChat ADB interaction
-    (done) Build MonkeyRunner classes from ChimpChat class objects
-    (done) Test starting an activiy
-    (done) Detect if package is installed?
-    (done) Get device build properties (key/val)
-    (done) Test screenshot (takeScreenshot, convertToBytes)
-    (todo) Test installing package ?? (for hotpatching the device?)
    


"""

import sys
import time
import json
from pprint import pprint

from jnius import autoclass

__author__ = "Ben DeMott"
__date__ = "Oct 21 2012"

ADB_LOCATION = '/opt/santoku/android-sdk-linux/platform-tools/adb'
ACTIVITY = 'com.android.browser.BrowserActivity'
FORCE_NEW_BRIDGE = False
PORT_FORWARD_LOCAL = 8000
PORT_FORWARD_REMOTE = 8000
DEVICE_CONNECT_TRIES = 5

def main(argv=None):
    # Note that this is the class-path... by default in pyjnius it will be your current working directory.
    # You should have unpacked the jar files in the instructions so that there is an 'org' folder at this
    # path.
    System = autoclass('java.lang.System')
    print "Class Path:", System.getProperty('java.class.path')

    # Normally we get the backend using 
    # AdbBackend = autoclass('com.android.chimpchat.adb.AdbBackend')
    # But lets do it the hard way... to get more features.

    AndroidDebugBridge = autoclass('com.android.ddmlib.AndroidDebugBridge')
    AdbChimpDevice = autoclass('com.android.chimpchat.adb.AdbChimpDevice')

    # Here you can see how the Android Debug Bridge is instantiated 
    # http://code.google.com/p/aster/source/browse/src/com/android/chimpchat/adb/AdbBackend.java
    AndroidDebugBridge.init(False)
    bridge = AndroidDebugBridge.createBridge(ADB_LOCATION, FORCE_NEW_BRIDGE)


    # This method returns a Java List of IDevice instances.
    # http://code.google.com/p/aster/source/browse/src/com/android/ddmlib/IDevice.java
    # ideviceslist = bridge.getDevices()

    # we can't just call it directly though, as you'll notice in
    # http://code.google.com/p/aster/source/browse/src/com/android/chimpchat/adb/AdbBackend.java
    # The code ultimately calls bridge.GetDevices() inside of a loop.
    ideviceslist = []
    for s in range(DEVICE_CONNECT_TRIES):
        time.sleep(1)
        ideviceslist = bridge.getDevices()
        if ideviceslist:
            break

    idevicesdict = {}
    for device in ideviceslist:
        serial = device.getSerialNumber()
        idevicesdict[serial] = device

    if not ideviceslist:
        return "No Devices"

    print "\nFound Devices (serials): ", idevicesdict.keys()

    device = ideviceslist[0]
    print "\nUsing first device", device

    print "\nForwarding ports"
    # Beging forwarding on the device - this is needed to make
    # the http interface and commands between the host and the client work properly.
    device.createForward(PORT_FORWARD_LOCAL, PORT_FORWARD_REMOTE)

    # Lets check to see if the device is ready.
    if not device.isOnline():
        return "\nDevice is not ready"

    print "\nGetting Device Clients"
    clients = device.getClients()
    print clients

    props = {}
    propsmap = device.getProperties()
    propskeys = propsmap.keySet().toArray()
    for key in propskeys:
        val = propsmap.get(key)
        props[key] = val

    pprint( props )

    # Write the properties to file
    filename = "%s_%s" % (props['ro.product.manufacturer'], props['ro.product.model'])
    filename = filename.replace(' ', '')
    fp = open(filename+'.json', mode='w')
    json.dumps(props, fp)

    # Chimp Device offers a few utilities that IDevice doesn't - so it can be useful.
    # you can get IChimpDevice from IDevice like this...
    # http://code.google.com/p/aster/source/browse/src/com/android/chimpchat/adb/AdbChimpDevice.java
    chimpdevice  = AdbChimpDevice(device)
    chimpmanager = chimpdevice.getManager()

    # You unlock the device, by waking it... and then simulating a drag.
    # Let's UNLOCK THE DEVICE (this won't work on devices with other security mechanisms)
    chimpdevice.wake()
    chimpdevice.drag(130, 620, 350, 620, 1.0, 120)

    time.sleep(2)

    # ------------------------------------------------------------
    # Taking a Screenshot
    # ------------------------------------------------------------
    img = chimpdevice.takeSnapshot()
    #ibytes = img.convertToBytes('png')  # returns a list of pixel info
    img.writeToFile(filename+'_screen.png', 'png')

    # ------------------------------------------------------------
    # Execute shell command
    # Get device package info
    # ------------------------------------------------------------
    # See http://en.androidwiki.com/wiki/ADB_Shell_Command_Reference
    # for more information on shell commands
    
    print "\nListing Packages"
    packages = chimpdevice.shell("pm list packages")
    print packages

    #device.executeShellCommand() #<-- this is another way to run shell commands
    result = chimpdevice.shell("pm path com.android.browser")
    print "Package Install Path: ", result
    if result.strip():
        print "Browser is installed !"
    else:
        return "Package '{0}' not installed - quitting".format(ACTIVITY)
    
    
    # ------------------------------------------------------------
    # Start the Android Agent
    # ------------------------------------------------------------
    # Get access to the Array and HashMap class objects in Java
    ArrayList = autoclass('java.util.ArrayList')
    HashMap   = autoclass('java.util.HashMap')
    

    print "\nStarting '{0}' Activity!".format(ACTIVITY)
    # Let's setup the individual arguments needed to manually call 
    # startActivity() 
    # We are going to call the Android devices activity to start the browser.
    uri        = None
    action     = "android.intent.action.MAIN"
    data       = None
    mimeType   = None
    categories = ArrayList()
    extras     = HashMap()
    pkg        = "com.android.browser"
    activity   = "BrowserActivity";
    component  = pkg + "/." + activity; #Not really sure why the naming for 'component' is like this.
    flags = 0  # we won't be sending any flags.

    chimpdevice.startActivity(uri, action, data, mimeType, categories, extras, component, flags)




if __name__ == '__main__':
    sys.exit(main(sys.argv))
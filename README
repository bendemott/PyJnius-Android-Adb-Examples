=============================================
Using PyJnius with ChimpChat and MonkeyRunner
=============================================
    How to access Android-Device Api's in Python with ease, and elegance.
    
    - This simple project is aimed at familiarizing people with the pyjnius_ project, a sub-project of kivy_.

    - This project does **not** require the use of Jython
    
    
MonkeyRunner/Chimpchat
----------------------
    MonkeyRunner and ChimpChat are classes used by the android debug bridge logic to interactive with android devices over usb.
    MonkeyRunner is an abstraction around ChimpChat, ChimpChat offering more features and more access to the device than MonkeyRunner.
    Both sets of classes can be used to connect to and communicate with Android devices over usb.

Android Debug Bridge
~~~~~~~~~~~~~~~~~~~~
    The **Android Debug Bridge** is a tool that comes with the Android Development Kit that allows you to communicate with an Android Device connected to a computer through a usb cable.  Once connected you can use the ``adb`` program to issue commands to a device and simulate user-behaviors.
    
    The adb command line tool works great but it has a few draw backs if you want to perform multiple complex tasks quickly inside a Python program.  We can overcome these problems by interacting with the Java classes that ADB uses directly, and that is exactly what we are going to do with the example scripts included in this project.

    This project may also be useful for those attempting to automate application tests on an android device within Python.

Android Device Debugging
~~~~~~~~~~~~~~~~~~~~~~~~
    Note that in order to make use of any of the work we will be doing, **usb-debugging** must be first enabled on the device.
    If usb-debugging is not enabled, adb will not even be able to *see* the device.
        
Installing PyJnius
------------------
    **Install JDK 6 or 7:**
    
    |    ``sudo apt-get install openjdk-7-jdk``
        
    **Python dependencies (you probably already have these)** - ``pip``, ``setuptools``, ``cython``
    
    |    ``sudo apt-get install python-pip``
    |    ``sudo pip install setuptools``
    |    ``sudo pip install cython``
       
    **Install PyJnius Package**
    
    |    ``sudo pip install jnius``
    
Get Android-Sdk, and Setup Jars
-------------------------------
    This part is optional to get ``pyjnius`` working, but is required to run the tests we have prepared to interact with our android device using python instead of the ``android-debug-bridge`` (*adb*) command line tool.
    
    Because ``pyjnius`` cannot resolve the contents of jar files in addition to downloading jar files, we pust unpack them (*using the* ``jar`` *command*) to make it so ``pyjnius`` can *see* them.

----------

    **Get Android-Sdk and Jar Libraries**:

    -    Download the android-sdk-linux_ package (*make sure you choose linux as the platform*).
        
    -    untar/gz the package and you should now have a 'android-sdk-linux' directory.
        
    -    cd to the directory where you want to run this script from

         ``cd /project/jnius_tests``
        
    -    copy ``monkeyrunner.jar`` from the **android-sdk-linux** package you just extracted

         ``cp android-sdk-linux/tools/lib/monkeyrnner.jar ./``
    
    **copy** ``chimpchat``, ``ddmlib``, ``guavalib``, **and** ``sdklib`` **into your working directory**:

        |    ``cp android-sdk-linux/tools/lib/chimpchat.jar ./``
        |    ``cp android-sdk-linux/tools/lib/ddmlib.jar ./``
        |    ``cp android-sdk-linux/tools/lib/guavalib.jar ./``
        |    ``cp android-sdk-linux/tools/lib/sdklib.jar ./``
    
    **Unpack the Jars into the working directory**:
    
        |    ``jar -xf chipmchat.jar``
        |    ``jar -xf ddmlib.jar``
        |    ``jar -xf guavalib.jar``
        |    ``jar -xf sdklib.jar``
    
    
.. _android-sdk-linux: developer.android.com/sdk/index.html
.. _pyjnius: https://github.com/kivy/pyjnius
.. _kivy: http://kivy.org

Scripts
-------

jnius_test2.py Tests
~~~~~~~~~~~~~~~~~~~~
Heres a list of the code-tasks we perform in this script. 

Once you have connected a device you can run the scripts using ``python jnius_test2.py``

-    (done) Make use of the MAP object in Java
-    (done) Handle Java Iterable objects that don't convert to native Python types  (*solved using .toArray*)
-    (done) Test ChimpChat ADB interaction
-    (done) Build MonkeyRunner classes from ChimpChat class objects
-    (done) Test starting an activiy
-    (done) Detect if package is installed?
-    (done) Get device build properties (key/val)
-    (done) Test screenshot (takeScreenshot, convertToBytes)
-    (todo) Test installing package ?? (for hotpatching the device?)
    
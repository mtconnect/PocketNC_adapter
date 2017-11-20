# PocketNC_adapter
An implementation of the PocketNC adapter.

Introduction
------------
A python adapter "adapter.py" for PocketNC is shared which provides an interface for the PocketNC to become MTConnect compliant. The adapter allows the use of MTConnect agent to make the PocketNC MTconnect compliant. The steps to install and implement MTConnect agent can be found at https://github.com/mtconnect/mtconnect-agent.

Implementation
--------------
Download the "adapter.py" in the beaglebone black Debian OS of PocketNC. update the port information in the "adapter.py" to the port number available on your device.

`PORT = 7878`

Once the information in the "adapter.py" file is updated, this python script needs to be used as a service so that the adapter is active everytime the PocketNC is powered on. In order to enable this enter the following code in the beaglebone terminal:

`sudo nano .\bashrc`

In the .bashrc shell script, goto the end of the file and add the following line:

`nohup python /home/pocketnc/adapter.py > /dev/null 2>&1 &`

assuming that the location of the "adapter.py" file is "/home/pocketnc/adapter.py". Edit this line appropriately.

Next time when the PocketNC is restarted, the adapter will be running as a service behind the scenes.

Verification
------------

One way to verify from a Windows OS whether the data is being pushed out of the PocketNC, is using Putty.

Putty can be downloaded from "https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html"

Once Putty is installed on the Windows system. Open Putty.exe.

Enter the IP address of the PocketNC as the Host Name and the Port initially set in the "adapter.py".
Set the Connection Type to Telnet and click on Open.

You should see data appearing in the following (SHDR) format:

`2014-01-16T04:13:38.704Z|Xabs|52.83
2014-01-16T04:13:38.704Z|Yabs|-14`

DataItems
---------
Following Data Items have been included in the adapter:

1.  Accumulated Time : Total Time
2.  Accumulated Time : Auto Time
3.  Accumulated Time : Cut Time
4.  Absolute X position
5.  Absolute Y position
6.  Absolute Z position
7.  Absolute A position
8.  Absolute B position
9.  Rotary Velocity 
10. Emergency Stop
11. Execution State
12. Power State
13. Line
14. Program
15. Path Feed Override
16. Spindle Feed Override
17. Tool Number
18. Controller Mode

MTConnect
---------
For more information on the MTConnect standard and the dataitems included within the standard please visit
http://www.mtconnect.org/

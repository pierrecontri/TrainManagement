# TrainManagement

This program is about Train Remote Control.
If you have a Numeric or Analogic train at home, and you already have electric switch, lights and other composants,
you will use this program to control the train by PC.
Start, stop, change way, ...

In a future, a video recorder will give you back inforamtions on your PC.

Solaris, BSD, Linux or Windows plateforme compatible.

Using a Raspberry Pi2 B+ or Pi3 to manage IO directly,
you can append an Arduino if you want to split in many layers the control part.

The UI will interact by web services (protocol http or pipe -prefered-) in a first time under WebBrowser.
A second UI will create in GTK+ for multi-plateform. A third maybe for mobiles (but not sure cause doublons with Web Browser).

In Raspberry, install the requests and smbus python libraries like:
(as su -u root)
apt-get install pip3
pip3 install web
pip3 install requests
pip3 install smbus

If you want to skip the RaspBerry part and use directly your Linux with the I2C and Arduino, install:
(as su -u root)
apt-get install pip3
pip3 install web
pip3 install requests
pip3 install smbus2 (new link to replace the smbus-cffi package)
pip3 install pysmbus

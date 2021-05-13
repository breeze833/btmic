# Bluetooth Mic on Raspberry Pi Zero W (Gadget Mode)

RPi0 can be configured to work as a gadget. This approach is to use RPi0 as an USB Audio adapter.

Once the RPi0 is plugged into the PC, it boots and enables it as an audio gadget.
The gadget has two interfaces. On the PC side, we see an UAC1 audio device and can capture audio
from it. On the RPi0 side, we see an ALSA device that we can feed the audio data to.

When the bluetooth mic is connected, the RPi0 creates an audio source for capturing the sound.
We can establish a forwarding channel from the bluetooth source to the ALSA sink.
By the help of the PulseAudio system, the audio-forwarding can be achieved via a loopback module.

The above is the concpet of the RPi0 based system. There are some minior issues such as how to
detect the connection of the bluetooth headset. Please refer to the script files. They require
the knowledge of udev etc.

## Installation

The packages should be installed in the system:
 *   python3
 *   pulseaudio and pulseaudio-module-bluetooth
 *   bluez
 *   zram-tools (optional)
     * enable zram swap
     * uninstall dphys swap file

As the ``root``, set up the files:
 *   Edit ``/boot/config.txt`` to enable gadget mode
     *   add a line at the end of the file ``dtoverlay=dwc2``
 *   Edit ``/etc/modules`` to load the modules for configfs UAC1 configuration
     *   ``dwc2``
     *   ``libcomposite``
 *   Copy ``/root/bin/setup_uac1.sh``
 *   Modify ``/etc/rc.local`` and add a line to execute the above script
     *   sample file is provided
 *   Use ``raspi-config`` to configure automatic console login

As the user ``pi``, set up the files:
 *   ``pip install pyudev``
 *   Copy ``/home/pi/bin/*``
 *   Modify ``/home/pi/.profile`` to execute the ``/home/pi/bin/start_headset_mon.sh``
     *   sample file is provided
 *   Determine the address of your bluetooth headset
     *   many ways to do
 *   Modify the headset address in ``/home/pi/bin/setup_headset.sh``
 *   Execute the ``/home/pi/bin/setup_headset.sh``
     *   you need to put the headset in discoverable mode
     *   the script will pair and trust it
 *   Modify the headset address in ``/home/pi/bin/headset_mon.py``

As the ``root``, shutdown the system.

## Using the System
 *   Plug the RPi0 to the PC.
 *   When the LED flashes fast, it is waiting for the headset.
 *   Turn on the headset.
 *   When the LED stops flashing, it is connected.
 *   Turn off the headset and the LED starts flashing fast.
 *   Currently we don't have a way to shutdown the system without login. Simply unplug the RPi0. My experience is that it is pretty safe.

## Known Issues
 *   Sometimes the headset becomes unpaired and need re-setup.
 *   If you encounter audio glitch or out-of-sync, reconnect the headset (turn off and on).

## References
 1.  [COMPOSITE USB GADGETS ON THE RASPBERRY PI ZERO](http://www.isticktoit.net/?p=1383)
 1.  [Using ``bluetoothctl`` to connect a device](https://wiki.archlinux.org/title/bluetooth)

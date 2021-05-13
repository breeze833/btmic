# Bluetooth Mic on Raspberry Pi 3 Model A

The concept of the bluetooth microphone system is based on 
forwarding the headset audio source to the on-board audio sink.
RPi3A has a physical audio output jack. By connecting it to the PC's
audio input jack, we can record the audio or loopback the audio directly
from the PC's configuration. This eliminates the driver installation issue.

Routing the headset audio-in to the on-board audio-out can be done by
loading the PulseAudio loopback module. The Pi3A is powerful enough
for this task and thus the transmission delay is low (RPi1 also works, but
the loopback ``latency_msec`` parameter may need to be enlarged to 200).

## Installation

The packages should be installed in the system:
 *   python3
 *   pulseaudio and pulseaudio-module-bluetooth
 *   bluez
 *   zram-tools (optional)
     * enable zram swap
     * uninstall dphys swap file

As the ``root``, set up the files:
 *   Add the user ``pi`` to the ``bluetooth`` group
 *   Use ``raspi-config`` to configure 
     *   automatic console login
     *   default audio output through audio jack

As the user ``pi``, set up the files:
 *   Copy ``/home/pi/bin/*``
 *   Copy ``/home/pi/.config/*``
 *   Determine the address of your bluetooth headset
     *   many ways to do
 *   Modify the headset address in ``/home/pi/bin/setup_headset.sh``
 *   Execute the ``/home/pi/bin/setup_headset.sh``
     *   you need to put the headset in discoverable mode
     *   the script will pair and trust it
 *   Modify the headset address in ``/home/pi/bin/headsetmon``
 *   ``systemctl --user enable pulseaudio``
 *   ``systemctl --user enable headsetmon``

As the ``root``, shutdown the system.

## Using the System
 *   Connect the audio from RPi3A to the PC.
 *   Turn on RPi3A.
 *   When the system is ready, a prompt sound is played. If you loopback the PC's audio-in to audio-out, you will hear it.
 *   Turn on the headset.
 *   When the headset is connected, the prompt sound will be played.
 *   When the headset is disconnected, the prompt sound will be played.
 *   Currently we don't have a way to shutdown the system without login. Simply unplug the RPi3A. My experience is that it is pretty safe.

## Known Issues
 *   Sometimes the headset becomes unpaired and need re-setup.
 *   If you encounter audio glitch or out-of-sync, reconnect the headset (turn off and on).


# Bluetooth Mic

The purpose of the project is to use a bluetooth headset as the microphone to the PC sound system.
If your PC or laptop has bluetooth enabled, you may simply set up the wireless mic via the system configuration.
However, I have to use the public PCs in the computer rooms for remote teaching serssions.
Setting up the bluetooth connection on a public PC is frustrating. Sometimes the bluetooth dongle does not work
due to driver installation failure, and sometimes the connections are not easy to establish.

The approach for solving the issues is to use a Raspberry Pi as the intermidiate forwarder.
Of course it introduces transmission delay but we can put most of the configuration complexity on the RPi.

#!/bin/bash
HEADSET_ADDR="82:52:E0:24:16:95"
bluetoothctl remove $HEADSET_ADDR
timeout 20 bluetoothctl scan on
bluetoothctl pair $HEADSET_ADDR
bluetoothctl trust $HEADSET_ADDR
bluetoothctl connect $HEADSET_ADDR

pacmd set-card-profile bluez_card.${HEADSET_ADDR//:/_} headset_head_unit

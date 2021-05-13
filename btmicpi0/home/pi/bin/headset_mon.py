#!/usr/bin/env python3
from pyudev import Context, Monitor, Devices
import subprocess
import time
import logging

def wait_bt_headset_add(input_monitor, bt_addr):
    device = input_monitor.poll()
    while device!=None:
        r = get_inputdev_info(device)
        if r!=None and r[1]==bt_addr:
            return (r[0], r[2])
        device = input_monitor.poll()

def get_inputdev_info(device):
    if device.action!='add' or device.device_node==None or device.sys_name==None: return None
    d = Devices.from_sys_path(device.context, device.sys_path[:device.sys_path.rfind(device.sys_name)])
    try:
        return (d.sys_path, d.attributes.asstring('name').upper(), device.device_node)
    except:
        return None

def wait_bt_headset_remove(input_monitor, sys_path):
    device = input_monitor.poll()
    while device!=None:
        if device.action=='remove' and device.sys_path==sys_path:
            break
        device = input_monitor.poll()

def monitor_bt_headset(**config):
    context = Context()
    monitor = Monitor.from_netlink(context)
    monitor.filter_by('input')
    while True:
        led0_headset_off()
        sys_path, device_node = wait_bt_headset_add(monitor, config['headset_addr'])
        pa_lo_idx = start_sound_forwarding(device_node=device_node, **config)
        led0_headset_on()
        wait_bt_headset_remove(monitor, sys_path)
        stop_sound_forwarding(pa_lo_idx=pa_lo_idx, **config)

def start_sound_forwarding(**config):
    logging.info('headset connected')
    logging.debug('events from {0}'.format(config['device_node']))
    r = subprocess.run(['pacmd', 'suspend-sink', config['rpi0_pa_sink'], '1'])
    while True:
        r = subprocess.run(['pactl', 'load-module', 'module-loopback', 
            'source={0}'.format(config['headset_pa_source']), 
            'sink={0}'.format(config['rpi0_pa_sink']), 'latency_msec=50'], capture_output=True)
        if r.returncode!=0:
            time.sleep(1)
        else:
            logging.debug(str(r))
            break
    pa_lo_idx = int(r.stdout)
    r = subprocess.run(['pacmd', 'suspend-sink', config['rpi0_pa_sink'], '0'])
    return pa_lo_idx

def stop_sound_forwarding(**config):
    logging.info('headset disconnected')
    r = subprocess.run(['pacmd', 'unload-module', str(config['pa_lo_idx'])])

def led0_headset_on():
    subprocess.run(['headset_on_indicator.sh'], shell=True)
    

def led0_headset_off():
    subprocess.run(['headset_off_indicator.sh'], shell=True)

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    config = {'headset_addr':'82:52:E0:24:16:95',
            'headset_pa_source':'bluez_source.28_52_E0_24_16_95.headset_head_unit',
            'rpi0_pa_sink':'alsa_output.platform-20980000.usb.analog-mono'
            }
    try:
        monitor_bt_headset(**config)
    except KeyboardInterrupt as e:
        logging.info('Terminated by user')
    except:
        logging.exception('Unexpected termination', exc_info=True)

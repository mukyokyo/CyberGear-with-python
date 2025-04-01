#!/usr/bin/env python3
#
import can
from cybergear import *

#with CyberGear(can.Bus(interface='socketcan', channel='can0')) as cg, :
#with CyberGear(can.Bus(interface='gs_usb', channel=0x606f, index=0, bitrate=1000000)) as cg:
with CyberGear(can.Bus(interface='slcan', channel='\\\\.\\com16', bitrate=1000000, sleep_after_open=0)) as cg:
#with CyberGear(can.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=1000000)) as cg:
  for id in range(0, 0x80):
    if cg.type0(id) != None:
      print(id, ':Find')

#!/usr/bin/env python
#
import os, time
from cybergear import *

#cg = CyberGear(can.Bus(interface='socketcan', channel='can0'))
cg = CyberGear(can.Bus(interface='gs_usb', channel=0x606f, index=0, bitrate=1000000))
#cg = CyberGear(can.Bus(interface='slcan', channel='\\\\.\\com11', bitrate=1000000, sleep_after_open=0))

for id in range(0, 0x80):
  if cg.type0(id) != None:
    print(id, ':Find')
cg.shutdown()

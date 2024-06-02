#!/usr/bin/python3
#
import os, time
from cg1 import *

cg = CyberGear()
for id in range(0, 0x80):
  if cg.type0(id) != None:
    print(id, ':Find')
cg.shutdown()

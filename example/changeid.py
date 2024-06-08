#!/usr/bin/python3
#
import sys
from cybergear import *

if len(sys.argv) == 3:
  try:
    arg = sys.argv[1:]
    previd = int(arg[0])
    newid = int(arg[1])
    if (previd >= 0) and (previd <= 0x7f) and (newid >= 0) and (newid <= 0x7f) and (previd != newid):
      cg = CyberGear()
      print('stop')
      cg.type4(previd, True, echo = True)
      print('change id')
      cg.type7(previd, newid, echo = True)
      print('read')
      cg.type0(newid, echo = True)
    else:
      print('ERR:There is some kind of mistake.')
    cg.shutdown()
  except:
    print('ERR:There is some problem.')


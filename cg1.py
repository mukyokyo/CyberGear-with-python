#!/usr/bin/python3
#
# cg1.py
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: (C) 2024 mukyokyo

import math, can
from struct import pack, unpack, iter_unpack

class CyberGear:
  def __init__(self):
    self.__canbus = can.interface.Bus(channel='can0', bustype='socketcan', extended = True)
    self.__myid = 0x55

  def __send_recieve(self, cmd, id, id_opt, data = (0,0,0,0,0,0,0,0), echo = False):
    if id <= 0x7f:
      try:
        msg = can.Message(arbitration_id = (id & 0xffff) | (((id_opt | (self.__myid & 0xffff)) & 0xffffffff) << 8) | ((cmd & 0x1f) << 24), data = data)
        if echo: print(f'TX: id=${msg.arbitration_id:08x} data=',':'.join(format(x, '02x') for x in msg.data))
        self.__canbus.send(msg)
        r = self.__canbus.recv(timeout=0.05)
        if r != None:
          if echo: print(f'RX: id=${r.arbitration_id:08X} data=', ':'.join(format(x, '02x') for x in r.data))
          return r
      except:
        pass

  # get unique identifier
  def type0(self, id, echo = False):
    r = self.__send_recieve(0, id, 0, echo = echo)
    if r != None:
      return list(*iter_unpack('>Q', bytes(r.data)))[0]

  # controle mode
  def type1(self, id, torque, angle, speed, Kp, Kd, echo = False):
    r = self.__send_recieve(1, id, torque, bytes(pack('>HHHH', angle, speed, Kp, Kd)), echo = echo)
    if r != None:
      return list(*iter_unpack('>HHHH', bytes(r)))

  # feedback
  def type2(self, id, echo = False):
    r = self.__send_recieve(2, id, 0, echo = echo)
    if r != None:
      return r.arbitration_id, tuple(*iter_unpack('>HHHH', bytes(r)))

  # enable
  def type3(self, id, echo = False):
    r = self.__send_recieve(3, id, 0, echo = echo)
    if r != None:
      return list(*iter_unpack('>HHHH', bytes(r)))

  # shutdown
  def type4(self, id, fault = False, echo = False):
    r = self.__send_recieve(4, id, 0, (1 if fault else 0,0,0,0,0,0,0,0), echo = echo)
    if r != None:
      return list(*iter_unpack('>HHHH', bytes(r)))

  # set zero position
  def type6(self, id, echo = False):
    r = self.__send_recieve(6, id, 0, (1,0,0,0,0,0,0,0), echo = echo)
    if r != None:
      return list(*iter_unpack('>HHHH', bytes(r)))

  # change id
  def type7(self, id, newid, echo = False):
    if newid <= 0x7f:
      return self.__send_recieve(7, id, newid << 16, echo = echo)

  # read param
  def type17B(self, id, index, echo = False):
    r = self.__send_recieve(17, id, 0, bytes(pack('<Hxxxxxx', index)), echo = echo)
    if r != None:
      return list(*iter_unpack('<HxxBxxx', bytes(r)))

  def type17W(self, id, index, echo = False):
    r = self.__send_recieve(17, id, 0, bytes(pack('<Hxxxxxx', index)), echo = echo)
    if r != None:
      return list(*iter_unpack('<HxxHxx', bytes(r)))

  def type17L(self, id, index, echo = False):
    r = self.__send_recieve(17, id, 0, bytes(pack('<Hxxxxxx', index)), echo = echo)
    if r != None:
      return list(*iter_unpack('<HxxL', bytes(r)))

  def type17f(self, id, index, echo = False):
    r = self.__send_recieve(17, id, 0, bytes(pack('<Hxxxxxx', index)), echo = echo)
    if r != None:
      return list(*iter_unpack('<Hxxf', bytes(r)))

  # write param
  def type18(self, id, index, data, echo = False):
    r = self.__send_recieve(18, id, 0, bytes(pack('<HxxL', index, data)), echo = echo)
    if r != None:
      return list(*iter_unpack('>HHHH', bytes(r)))

  def type18f(self, id, index, data, echo = False):
    r = self.__send_recieve(18, id, 0, bytes(pack('<Hxxf', index, data)), echo = echo)
    if r != None:
      return list(*iter_unpack('>HHHH', bytes(r)))

  def shutdown(self):
    self.__canbus.shutdown()

if __name__ == "__main__":
  import sys, math, time
  import numpy as np

  cg = CyberGear()
  id = 0

  def float_to_uint(x : float, x_min : float, x_max : float):
    if (x > x_max): x = x_max
    elif (x < x_min): x = x_min
    return int((x - x_min) * 65535 / (x_max - x_min))

  def uint_to_float(x : int, x_min : float, x_max : float):
    return float(x / 65535 * (x_max - x_min) + x_min)

  def get_unique_identifier(echo = False):
    return cg.type0(id, echo = echo)

  def get_freedback(echo = False):
    r = cg.type2(id, echo = echo)
    if r != None:
      return (
        (r[0] >> 16) & 0xff,
        uint_to_float(r[1][0], -4 * math.pi, 4 * math.pi),
        uint_to_float(r[1][1], -30, 30),
        uint_to_float(r[1][2], -12, 12),
        uint_to_float(r[1][3], 0, 6553.5)
      )
    return None

  def start_motor(echo = False):
    cg.type3(id, echo = echo)

  def stop_motor(fault = False, echo = False):
    cg.type4(id, fault, echo = echo)

  def set_newid(newid, echo = False):
    cg.type7(id, newid, echo = echo)

  def set_runmode(m, echo = False):
    stop_motor(id)
    cg.type18(id, 0x7005, m, echo = echo)

  def set_speed_limit(v,echo = False):
    cg.type18f(id, 0x7017, v, echo = echo)

  def set_current_limit(v, echo = False):
    cg.type18f(id, 0x7018, v, echo = echo)

  def set_zero_position(echo = False):
    cg.type6(id, echo = echo)

  def set_current_ref(v, echo = False):
    cg.type18f(id, 0x7006, v, echo = echo)

  def set_speeed_ref(v, echo = False):
    cg.type18f(id, 0x700A, v, echo = echo)

  def set_position_ref(v, echo = False):
    cg.type18f(id, 0x7016, v, echo = echo)

  print('start')

  for i in (0x7005, 0x7006, 0x700A, 0x700B, 0x7010, 0x7011, 0x7014, 0x7016, 0x7017, 0x7018, 0x7019, 0x701a, 0x701b, 0x701c, 0x701d, 0x701e, 0x701f, 0x7020):
    if i == 0x7005:
      r = cg.type17B(id, i)
      if r != None: print(hex(i),hex(r[1]>>0))
    else:
      r = cg.type17f(id, i)
      if r != None: print(hex(i),f'{r[1]:7.3f}')

  print(get_unique_identifier())
  stop_motor(True)

  # kp:0~500 = 0~65535
  # kd:0~5 = 0~65535
  # pos:-4pi~+4pi = 0~65535
  # spd:-30rad/s~+30rad/s = 0~65535
  # trq:-12Nm~+12Nm = 0~65535
  try:
    set_runmode(1)
    set_speed_limit(5.0)
    set_current_limit(2.0)
    start_motor()
    set_zero_position()
    for p in tuple(range(0, 100, 5)) + tuple(range(100, -100, -10)) + tuple(range(-100, 0, 5)):
      set_position_ref(p * 4 * math.pi / 100)

      t = time.time() + 500 / 1000.0
      while t > time.time():
        fb = get_freedback()
        if fb:
          print(f'{p * 4 * math.pi / 100:6.2f} ${fb[0]:02x} {fb[1]:6.2f} {fb[2]:6.2f} {fb[3]:6.2f} {fb[4]:6.1f}', end='        \r')
    stop_motor()

    set_runmode(2)
    set_current_limit(2.0)
    start_motor()
    for s in tuple(range(0, 30, 1)) + tuple(range(30, -30, -1)) + tuple(range(-30, 0, 1)):
      set_speeed_ref(s)
      t = time.time() + 500 / 1000.0
      while t > time.time():
        fb = get_freedback()
        if fb != None:
          print(f'{s:6.2f} ${fb[0]:02x} {fb[1]:6.2f} {fb[2]:6.2f}{fb[3]:6.2f} {fb[4]:6.1f}', end='        \r')
    stop_motor()

  except KeyboardInterrupt:
    pass

  stop_motor()

  cg.shutdown()
  print()

#!/usr/bin/python3
#
# cg1.py
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: (C) 2024 mukyokyo

import math, can
from struct import pack, unpack, iter_unpack

class CyberGear:
  INDEX_run_mode      = (0x7005, 'B')
  INDEX_iq_ref        = (0x7006, 'f')
  INDEX_spd_ref       = (0x700a, 'f')
  INDEX_limit_torque  = (0x700b, 'f')
  INDEX_cur_kp        = (0x7010, 'f')
  INDEX_cur_ki        = (0x7011, 'f')
  INDEX_cur_filt_gain = (0x7014, 'f')
  INDEX_loc_ref       = (0x7016, 'f')
  INDEX_limit_spd     = (0x7017, 'f')
  INDEX_limit_cur     = (0x7018, 'f')
  INDEX_mechPos       = (0x7019, 'f')
  INDEX_iqf           = (0x701a, 'f')
  INDEX_mechVel       = (0x701b, 'f')
  INDEX_VBUS          = (0x701c, 'f')
  INDEX_rotation      = (0x701d, 'h')
  INDEX_loc_kp        = (0x701e, 'f')
  INDEX_spd_kp        = (0x701f, 'f')
  INDEX_spd_ki        = (0x7020, 'f')

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
      return self.__send_recieve(7, id, newid << 8, echo = echo)

  # read param
  def type17(self, id, index, width = 'B', echo = False):
    r = self.__send_recieve(17, id, 0, bytes(pack('<Hxxxxxx', index)), echo = echo)
    if r != None:
      match width:
        case 'B':
          return tuple(*iter_unpack('<HxxBxxx', bytes(r.data)))[1]
        case 'h':
          return tuple(*iter_unpack('<Hxxhxx', bytes(r.data)))[1]
        case 'H':
          return tuple(*iter_unpack('<HxxHxx', bytes(r.data)))[1]
        case 'l':
          return tuple(*iter_unpack('<Hxxl', bytes(r.data)))[1]
        case 'L':
          return tuple(*iter_unpack('<HxxL', bytes(r.data)))[1]
        case 'f':
          return tuple(*iter_unpack('<Hxxf', bytes(r.data)))[1]

  # write param
  def type18(self, id, index, data, width = 'B', echo = False):
    r = None
    match width:
      case 'B':
        r = self.__send_recieve(18, id, 0, bytes(pack('<HxxBxxx', index, data)), echo = echo)
      case 'h':
        r = self.__send_recieve(18, id, 0, bytes(pack('<Hxxhxx', index, data)), echo = echo)
      case 'H':
        r = self.__send_recieve(18, id, 0, bytes(pack('<HxxHxx', index, data)), echo = echo)
      case 'l':
        r = self.__send_recieve(18, id, 0, bytes(pack('<Hxxl', index, data)), echo = echo)
      case 'L':
        r = self.__send_recieve(18, id, 0, bytes(pack('<HxxL', index, data)), echo = echo)
      case 'f':
        r = self.__send_recieve(18, id, 0, bytes(pack('<Hxxf', index, data)), echo = echo)
    if r != None:
      return list(*iter_unpack('>HHHH', bytes(r)))

  def shutdown(self):
    self.__canbus.shutdown()

if __name__ == "__main__":
  import sys, math, time
  import numpy as np

  cg = CyberGear()
  id = 1

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
    cg.type18(id, CyberGear.INDEX_run_mode[0], m, width = CyberGear.INDEX_run_mode[1], echo = echo)

  def set_zero_position(echo = False):
    cg.type6(id, echo = echo)

  def set_iq_ref(v, echo = False):
    cg.type18(id, CyberGear.INDEX_iq_ref[0], v, width = CyberGear.INDEX_iq_ref[1], echo = echo)

  def set_spd_ref(v, echo = False):
    cg.type18(id, CyberGear.INDEX_spd_ref[0], v, width = CyberGear.INDEX_spd_ref[1], echo = echo)

  def set_limit_torque(v, echo = False):
    cg.type18(id, CyberGear.INDEX_limit_torque[0], v, width = CyberGear.INDEX_limit_torque[1], echo = echo)

  def set_cur_kp(v, echo = False):
    cg.type18(id, CyberGear.INDEX_cur_kp[0], v, width = CyberGear.INDEX_cur_kp[1], echo = echo)

  def set_cur_ki(v, echo = False):
    cg.type18(id, CyberGear.INDEX_cur_ki[0], v, width = CyberGear.INDEX_cur_ki[1], echo = echo)

  def set_cur_filt_gain(v, echo = False):
    cg.type18(id, CyberGear.INDEX_cur_filt_gain[0], v, width = CyberGear.INDEX_cur_filt_gain[1], echo = echo)

  def set_loc_ref(v, echo = False):
    cg.type18(id, CyberGear.INDEX_loc_ref[0], v, width = CyberGear.INDEX_loc_ref[1], echo = echo)

  def set_limit_spd(v, echo = False):
    cg.type18(id, CyberGear.INDEX_limit_spd[0], v, width = CyberGear.INDEX_limit_spd[1], echo = echo)

  def set_limit_cur(v, echo = False):
    cg.type18(id, CyberGear.INDEX_limit_cur[0], v, width = CyberGear.INDEX_limit_cur[1], echo = echo)

  def set_rotation(v, echo = False):
    cg.type18(id, CyberGear.INDEX_rotation[0], v, width = CyberGear.INDEX_rotation[1],echo = echo)

  def get_rotation(echo = False):
    return cg.type17(id, CyberGear.INDEX_rotation[0], width = CyberGear.INDEX_rotation[1], echo = echo)

  def dump():
    for i in (CyberGear.INDEX_run_mode, CyberGear.INDEX_iq_ref, CyberGear.INDEX_spd_ref, CyberGear.INDEX_limit_torque, CyberGear.INDEX_cur_kp, CyberGear.INDEX_cur_ki, CyberGear.INDEX_cur_filt_gain, CyberGear.INDEX_loc_ref, CyberGear.INDEX_limit_spd, CyberGear.INDEX_limit_cur, CyberGear.INDEX_mechPos, CyberGear.INDEX_iqf, CyberGear.INDEX_mechVel, CyberGear.INDEX_VBUS, CyberGear.INDEX_rotation, CyberGear.INDEX_loc_kp, CyberGear.INDEX_spd_kp, CyberGear.INDEX_spd_ki):
      r = cg.type17(id, i[0], width = i[1])
      if r != None:
        match i[1]:
          case 'B':
            print(f'${i[0]:04x} ${r:02x}')
          case 'f':
            print(f'${i[0]:04x} {r:.3f}')
          case 'h':
            print(f'${i[0]:04x} {r}')

  print('start')

  dump()
  print(get_unique_identifier())
  stop_motor(True)

#  set_newid(0x7f)

  # pos:-4pi~+4pi = 0~65535
  # spd:-30rad/s~+30rad/s = 0~65535
  # trq:-12Nm~+12Nm = 0~65535
  try:
    print('MIT Ctrl mode')
    set_runmode(0)
    set_limit_spd(5.0)
    set_limit_cur(2.0)
    set_zero_position()
    start_motor()
    for p in tuple(range(32767, 65535, 1024)) + tuple(range(65535, 0, -1024)) + tuple(range(0, 32767, 1024)):
      cg.type1(id, 0, p, 0, 1500, 2000)
      t = time.time() + 500 / 1000.0
      while t > time.time():
        fb = get_freedback()
        if fb:
          print(f'{p:6d} ${fb[0]:02x} {fb[1]:6.2f} {fb[2]:6.2f} {fb[3]:6.2f} {fb[4]:6.1f}', end='        \r')
        time.sleep(0.01)

    print('position mode')
    set_runmode(1)
    set_limit_spd(5.0)
    set_limit_cur(2.0)
    start_motor()
    for p in tuple(range(0, 100, 5)) + tuple(range(100, -100, -10)) + tuple(range(-100, 0, 5)):
      set_loc_ref(p * 4 * math.pi / 100)
      t = time.time() + 500 / 1000.0
      while t > time.time():
        fb = get_freedback()
        if fb:
          print(f'{p * 4 * math.pi / 100:6.2f} ${fb[0]:02x} {fb[1]:6.2f} {fb[2]:6.2f} {fb[3]:6.2f} {fb[4]:6.1f}', end='        \r')
        time.sleep(0.01)

    print('\nspeed mode')
    set_runmode(2)
    set_limit_cur(2.0)
    start_motor()
    for s in tuple(range(0, 30, 1)) + tuple(range(30, -30, -1)) + tuple(range(-30, 0, 1)):
      set_spd_ref(s)
      t = time.time() + 500 / 1000.0
      while t > time.time():
        fb = get_freedback()
        if fb != None:
          print(f'{s:6.2f} ${fb[0]:02x} {fb[1]:6.2f} {fb[2]:6.2f}{fb[3]:6.2f} {fb[4]:6.1f}', end='        \r')
        time.sleep(0.01)

    print('\ncurrent mode')
    set_runmode(3)
    start_motor()
    for c in tuple(range(0, 23, 1)) + tuple(range(23, -23, -1)) + tuple(range(-23, 0, 1)):
      set_iq_ref(c)
      t = time.time() + 200 / 1000.0
      while t > time.time():
        fb = get_freedback()
        if fb != None:
          print(f'{c:6.2f} ${fb[0]:02x} {fb[1]:6.2f} {fb[2]:6.2f}{fb[3]:6.2f} {fb[4]:6.1f}', end='        \r')
        time.sleep(0.01)

  except KeyboardInterrupt:
    pass

  stop_motor()

  cg.shutdown()
  print()

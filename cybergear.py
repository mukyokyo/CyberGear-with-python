#!/usr/bin/env python
#
# cybergear.py
# Libraries for some CyberGear protocols.
# The firmware version of Cybergear must be at least 1.2.1.5.
#
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: (C) 2025 mukyokyo

import math, can, time
from struct import pack, unpack, iter_unpack

class CyberGear:
  INDEX_Name            = (0x0000, '')
  INDEX_BarCode         = (0x0001, '')
  INDEX_BootCodeVersion = (0x1000, '')
  INDEX_BootBuildDate   = (0x1001, '')
  INDEX_BootBuildTime   = (0x1002, '')
  INDEX_AppCodeVersion  = (0x1003, '')
  INDEX_AppGitVersion   = (0x1004, '')
  INDEX_AppBuildDate    = (0x1005, '')
  INDEX_AppBuildTime    = (0x1006, '')
  INDEX_AppCodeName     = (0x1007, '')
  INDEX_echoPara1       = (0x2000, 'H')
  INDEX_echoPara2       = (0x2001, 'H')
  INDEX_echoPara3       = (0x2002, 'H')
  INDEX_echoPara4       = (0x2003, 'H')
  INDEX_echoFreHz       = (0x2004, 'I')
  INDEX_MechOffset      = (0x2005, 'f')
  INDEX_MechPos_init    = (0x2006, 'f')
  INDEX_limit_torque    = (0x2007, 'f')
  INDEX_I_FW_MAX        = (0x2008, 'f')
  INDEX_motor_index     = (0x2009, 'B')
  INDEX_CAN_ID          = (0x200a, 'B')
  INDEX_CAN_MASTER      = (0x200b, 'B')
  INDEX_CAN_TIMEOUT     = (0x200c, 'I')
  INDEX_motorOverTemp   = (0x200d, 'h')
  INDEX_overTempTime    = (0x200e, 'I')
  INDEX_GearRatio       = (0x200f, 'f')
  INDEX_Tq_caliType     = (0x2010, 'B')
  INDEX_cur_filt_gain   = (0x2011, 'f')
  INDEX_cur_kp          = (0x2012, 'f')
  INDEX_cur_ki          = (0x2013, 'f')
  INDEX_spd_kp          = (0x2014, 'f')
  INDEX_spd_ki          = (0x2015, 'f')
  INDEX_loc_kp          = (0x2016, 'f')
  INDEX_spd_filt_gain   = (0x2017, 'f')
  INDEX_limit_spd       = (0x2018, 'f')
  INDEX_limit_cur       = (0x2019, 'f')

  INDEX_timeUse0        = (0x3000, 'H')
  INDEX_timeUse1        = (0x3001, 'H')
  INDEX_timeUse2        = (0x3002, 'H')
  INDEX_timeUse3        = (0x3003, 'H')
  INDEX_encoderRaw      = (0x3004, 'h')
  INDEX_mcuTemp         = (0x3005, 'h')
  INDEX_motorTemp       = (0x3006, 'h')
  INDEX_vBus            = (0x3007, 'H')
  INDEX_adc1Offset      = (0x3008, 'i')
  INDEX_adc2Offset      = (0x3009, 'i')
  INDEX_adc1Raw         = (0x300a, 'H')
  INDEX_adc2Raw         = (0x300b, 'H')
  INDEX_VBUS            = (0x300c, 'f')
  INDEX_cmdId           = (0x300d, 'f')
  INDEX_cmdIq           = (0x300e, 'f')
  INDEX_cmdlocref       = (0x300f, 'f')
  INDEX_cmdspdref       = (0x3010, 'f')
  INDEX_cmdTorque       = (0x3011, 'f')
  INDEX_cmdPos          = (0x3012, 'f')
  INDEX_cmdVel          = (0x3013, 'f')
  INDEX_rotation        = (0x3014, 'h')
  INDEX_modPos          = (0x3015, 'f')
  INDEX_mechPos         = (0x3016, 'f')
  INDEX_mechVel         = (0x3017, 'f')
  INDEX_elecPos         = (0x3018, 'f')
  INDEX_ia              = (0x3019, 'f')
  INDEX_ib              = (0x301a, 'f')
  INDEX_ic              = (0x301b, 'f')
  INDEX_tick            = (0x301c, 'I')
  INDEX_phaseOrder      = (0x301d, 'B')
  INDEX_iqf             = (0x301e, 'f')
  INDEX_boardTemp       = (0x301f, 'h')
  INDEX_iq              = (0x3020, 'f')
  INDEX_id              = (0x3021, 'f')
  INDEX_faultSta        = (0x3022, 'I')
  INDEX_warnSta         = (0x3023, 'I')
  INDEX_drv_fault       = (0x3024, 'I')
  INDEX_drv_temp        = (0x3025, 'h')
  INDEX_Uq              = (0x3026, 'f')
  INDEX_Ud              = (0x3027, 'f')
  INDEX_dtc_u           = (0x3028, 'f')
  INDEX_dtc_v           = (0x3029, 'f')
  INDEX_dtc_w           = (0x302a, 'f')
  INDEX_v_bus           = (0x302b, 'f')
  INDEX_v_ref           = (0x302c, 'f')
  INDEX_torque_fdb      = (0x302d, 'f')
  INDEX_rated_i         = (0x302e, 'f')
  INDEX_limit_i         = (0x302f, 'f')

  INDEX_run_mode        = (0x7005, 'B')
  INDEX_iq_ref          = (0x7006, 'f')
  INDEX_spd_ref         = (0x700a, 'f')
  INDEX_limit_torque_2  = (0x700b, 'f')
  INDEX_cur_kp_2        = (0x7010, 'f')
  INDEX_cur_ki_2        = (0x7011, 'f')
  INDEX_cur_filt_gain_2 = (0x7014, 'f')
  INDEX_loc_ref         = (0x7016, 'f')
  INDEX_limit_spd_2     = (0x7017, 'f')
  INDEX_limit_cur_2     = (0x7018, 'f')
  INDEX_mechPos_2       = (0x7019, 'f')
  INDEX_iqf_2           = (0x701a, 'f')
  INDEX_mechVel_2       = (0x701b, 'f')
  INDEX_VBUS_2          = (0x701c, 'f')
  INDEX_rotation_2      = (0x701d, 'h')
  INDEX_loc_kp_2        = (0x701e, 'f')
  INDEX_spd_kp_2        = (0x701f, 'f')
  INDEX_spd_ki_2        = (0x7020, 'f')

  def __init__(self, bus):
    self.__canbus = bus
    self.__myid = 0xfd
    self.__alarm = list()
    self.__rmes = list()
    self.rxflush()

  @property
  def alarm(self):
    r = self.__alarm
    self.__alarm = []
    return r

  def rxflush(self):
    t = time.time() + 1.0
    while not (self.__canbus.recv(timeout=0) is None):
      if time.time() > t: return

  def __send(self, cmd, id, id_opt, data : bytes = (0,0,0,0,0,0,0,0), echo = False) -> bool:
    if id <= 0x7f:
      try:
        msg = can.Message(arbitration_id = (id & 0xff) | ((id_opt & 0xffff) << 8) | ((cmd & 0x1f) << 24), data = data, is_extended_id = True)
        self.__canbus.send(msg, timeout = 0.1)
        if echo: print(f'TX: id=${msg.arbitration_id:08x} data=',':'.join(format(x, '02x') for x in msg.data))
      except can.CanError:
        return False
      else:
        return True
    return False

  def __recv(self, tout = 0.05, echo = False) -> bytes:
    t = time.time() + tout
    while time.time() < t:
      try:
        r = self.__canbus.recv(timeout=0.001)
        if r != None:
          if r.is_rx:
            if echo: print(f'RX: id=${r.arbitration_id:08x} data=', ':'.join(format(x, '02x') for x in r.data))
            typ = (r.arbitration_id >> 24) & 0xff
            if typ == 21:
              self.__alarm += [(r.arbitration_id >> 8) & 0xff, list(*iter_unpack('<Q', bytes(r.data)))[0]],
            elif typ == 22:
              pass
            else:
              return r
      except can.CanError:
        pass

  def __send_recieve(self, cmd, id, id_opt, data : bytes = (0,0,0,0,0,0,0,0), echo = False) -> bytes:
    if self.__send(cmd, id, id_opt, data, echo = echo):
      r = self.__recv(tout = 0.05, echo = echo)
      if r != None:
        if ((r.arbitration_id >> 8) & 0xff == id):
          return r

  # get unique identifier
  def type0(self, id, echo = False):
    r = self.__send_recieve(0, id, self.__myid, echo = echo)
    if r != None:
      if ((r.arbitration_id >> 24) & 0xff == 0):
        return list(*iter_unpack('<Q', bytes(r.data)))[0]

  # controle mode
  def type1(self, id, torque, angle, speed, Kp, Kd, echo = False):
    r = self.__send_recieve(1, id, torque, bytes(pack('>HHHH', angle, speed, Kp, Kd)), echo = echo)
    if r != None:
      if ((r.arbitration_id >> 24) & 0xff == 2):
        return list(*iter_unpack('>HHHH', bytes(r)))

  # feedback
  def type2(self, id, echo = False):
    r = self.__send_recieve(2, id, self.__myid, echo = echo)
    if r != None:
      if ((r.arbitration_id >> 24) & 0xff == 2):
        return r.arbitration_id, tuple(*iter_unpack('>HHHH', bytes(r)))

  # enable
  def type3(self, id, echo = False):
    r = self.__send_recieve(3, id, self.__myid, echo = echo)
    if r != None:
      if ((r.arbitration_id >> 24) & 0xff == 2):
        return list(*iter_unpack('>HHHH', bytes(r)))

  # shutdown
  def type4(self, id, fault = False, echo = False):
    r = self.__send_recieve(4, id, self.__myid, (1 if fault else 0,0,0,0,0,0,0,0), echo = echo)
    if r != None:
      if ((r.arbitration_id >> 24) & 0xff == 2):
        return list(*iter_unpack('>HHHH', bytes(r)))

  # set zero position
  def type6(self, id, echo = False):
    r = self.__send_recieve(6, id, self.__myid, (1,0,0,0,0,0,0,0), echo = echo)
    if r != None:
      if ((r.arbitration_id >> 24) & 0xff == 2):
        return list(*iter_unpack('>HHHH', bytes(r)))

  # change id
  def type7(self, id, newid, echo = False):
    if newid <= 0x7f:
      if self.__send(7, id, (newid << 8) | self.__myid, (0,0,0,0,0,0,0,0), echo = echo):
        r = self.__recv(tout = 0.05, echo = echo)
        if r != None:
          if ((r.arbitration_id >> 8) & 0xff == newid):
            return list(*iter_unpack('<Q', bytes(r.data)))[0]


      return self.__send_recieve(7, id, (newid << 8) | self.__myid, echo = echo)

  # read config
  def type9(self, id, index, echo = False):
    s = bytes()
    if self.__send(9, id, self.__myid, bytes(pack('<Hxxxxxx', index)), echo):
      lcnt = 3
      cnt = 0
      t = time.time() + 0.1
      while lcnt >= cnt and time.time() < t:
        r = self.__recv(tout = 0.05, echo = echo)
        if r != None:
          if (r.arbitration_id >> 8) & 0xff == id and (r.arbitration_id >> 24) & 0xff == 9:
            d = (tuple(*iter_unpack('<HBBBBBB', bytes(r.data))))
            s += bytes(d[3:7])
            match d[1]:
              case 0x00:  #uint8
                lcnt = 0
              case 0x02:  #uint16
                lcnt = 0
              case 0x03:  #int16
                lcnt = 0
              case 0x04:  #uint32
                lcnt = 0
              case 0x05:  #int32
                lcnt = 0
              case 0x06:  #float
                lcnt = 0
              case 0x0a:  #str
                lcnt = 3
            cnt+=1
      if 'd' in locals():
        match d[1]:
          case 0x00:  #uint8
            return tuple(*iter_unpack('<Bxxx', s))[0]
          case 0x02:  #uint16
            return tuple(*iter_unpack('<Hxx', s))[0]
          case 0x03:  #int16
            return tuple(*iter_unpack('<hxx', s))[0]
          case 0x04:  #uint32
            return tuple(*iter_unpack('<I', s))[0]
          case 0x05:  #int32
            return tuple(*iter_unpack('<i', s))[0]
          case 0x06:  #float
            return tuple(*iter_unpack('<f', s))[0]
          case 0x0a:  #str
            ss = s.decode('utf-8', 'replace').split('\0')
            return ss[0]

  # read param
  def type17(self, id, index, width = 'B', echo = False):
    r = self.__send_recieve(17, id, self.__myid, bytes(pack('<Hxxxxxx', index)), echo = echo)
    if r != None:
      if ((r.arbitration_id >> 24) & 0xff == 17):
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
      if ((r.arbitration_id >> 24) & 0xff == 2):
        return list(*iter_unpack('>HHHH', bytes(r)))

  # read raw config
  def type19(self, id, echo = False):
    if self.__send(19, id, self.__myid, (0xC4, 0x7F, 0x31, 0x31, 0x30, 0x33, 0x31, 0x04), echo = echo):
      s = bytes()
      t = time.time() + 5.0
      while True:
        if time.time() > t:
          break
        r = self.__recv(tout = 0.05, echo = echo)
        if r != None:
          if ((r.arbitration_id >> 8) & 0xff == id) and ((r.arbitration_id >> 24) & 0xff == 19):
            d = (tuple(*iter_unpack('<HBBBBBB', bytes(r.data))))
            if r.arbitration_id & 0xf0000 != 0x90000:
              s += bytes(d[1:7])
            else:
              break;
      return s

  # set baudrate
  def type22(self, id, baud, echo = False):
    if baud >= 1 and baud <= 4:
      if self.__send(22, id, self.__myid, (baud, 0, 0, 0, 0, 0, 0, 0), echo = echo):
        r = self.__recv(tout = 0.05, echo = echo)
        if r != None:
          if ((r.arbitration_id >> 8) & 0xff == id) and ((r.arbitration_id >> 24) & 0xff == 0):
            return list(*iter_unpack('<Q', bytes(r.data)))[0]

  # write param by index
  def set_item_value (self, id, ind : tuple[int ,int] , val, echo = False) -> bool:
    return self.type18(id, ind[0], val, ind[1], echo = echo) != None

  # read param by index
  def get_item_value (self, id, ind : tuple[int ,int], echo = False):
    return self.type17(id, ind[0], ind[1], echo = echo)

  def shutdown(self):
    self.__canbus.shutdown()


if __name__ == "__main__":
  import sys, math, time

  def float_to_uint(x : float, x_min : float, x_max : float):
    if (x > x_max): x = x_max
    elif (x < x_min): x = x_min
    return int((x - x_min) * 65535 / (x_max - x_min))

  def uint_to_float(x : int, x_min : float, x_max : float):
    return float(x / 65535 * (x_max - x_min) + x_min)

  def get_unique_identifier(cg, id, echo = False):
    return cg.type0(id, echo = echo)

  def get_feedback(cg, id, echo = False):
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

  def start_motor(cg, id, echo = False):
    return cg.type3(id, echo = echo)

  def stop_motor(cg, id, fault = False, echo = False):
    return cg.type4(id, fault, echo = echo)

  def set_newid(cg, id, newid, echo = False):
    return cg.type7(id, newid, echo = echo)

  def set_runmode(cg, id, m, echo = False):
    if stop_motor(cg, id) != None:
      return cg.set_item_value(id, CyberGear.INDEX_run_mode, m, echo = echo)

  def set_zero_position(cg, id, echo = False):
    return cg.type6(id, echo = echo)

  def dump1(cg, id, echo = False):
    result = ()
    for i in (0x0,0x1,0x1000,0x1001,0x1002,0x1003,0x1004,0x1005,0x1006,0x1007,0x2000,0x2001,0x2002,0x2003,0x2004,0x2005,0x2006,0x2007,0x2008,0x2009,0x200a,0x200b,0x200c,0x200d,0x200e,0x200f,0x2010,0x2011,0x2012,0x2013,0x2014,0x2015,0x2016,0x2017,0x2018,0x2019,0x3000,0x3001,0x3002,0x3003,0x3004,0x3005,0x3006,0x3007,0x3008,0x3009,0x300a,0x300b,0x300c,0x300d,0x300e,0x300f,0x3010,0x3011,0x3012,0x3013,0x3014,0x3015,0x3016,0x3017,0x3018,0x3019,0x301a,0x301b,0x301c,0x301d,0x301e,0x301f,0x3020,0x3021,0x3022,0x3023,0x3024,0x3025,0x3026,0x3027,0x3028,0x3029,0x302a,0x302b,0x302c,0x302d,0x302e,0x302f):
      d = cg.type9(id, i)
      if echo: print(f'${i:04x} {d}')
      result += (i,d),
    return result

  def dump2(cg, id, echo = False):
    result = ()
    for ind in (cg.INDEX_run_mode, cg.INDEX_iq_ref, cg.INDEX_spd_ref, cg.INDEX_limit_torque_2, cg.INDEX_cur_kp_2, cg.INDEX_cur_ki_2, cg.INDEX_cur_filt_gain_2, cg.INDEX_loc_ref, cg.INDEX_limit_spd_2, cg.INDEX_limit_cur_2, cg.INDEX_mechPos_2, cg.INDEX_iqf_2, cg.INDEX_mechVel_2, cg.INDEX_VBUS_2, cg.INDEX_rotation_2, cg.INDEX_loc_kp_2, cg.INDEX_spd_kp_2, cg.INDEX_spd_ki_2):
      r =  cg.get_item_value(id, ind)
      if r != None:
        result += (ind[0], r),
        if echo:
          match ind[1]:
            case 'B':
              print(f'${ind[0]:04x} ${r:02x}')
            case 'f':
              print(f'${ind[0]:04x} {r:.3f}')
            case 'h':
              print(f'${ind[0]:04x} {r}')
    return result

  def getmembystr(cg, id, indxess):
    s = ''
    dat = []
    for ind in indxess:
      if ind[0] > 0x7000:
        dat += (ind[0], cg.type17(id, ind[0], width = ind[1])),
      else:
        dat += (ind[0], cg.type9(id, ind[0])),
    for d in dat:
      n: Optional[int | str | float] = d[1]
      match n:
        case int():
          s += f'${d[0]:04x}:{d[1]:>8d} '
        case float():
          s += f'${d[0]:04x}:{d[1]:>9.2f} '
        case _:
          s += f'${d[0]:04x}:{d[1]} '
    return(s)

  print('start')

  cg = CyberGear(can.Bus(interface='socketcan', channel='can0'))
#  cg = CyberGear(can.Bus(interface='gs_usb', channel=0x606f, index=0, bitrate=1000000))
#  cg = CyberGear(can.Bus(interface='slcan', channel='\\\\.\\com11', bitrate=1000000, sleep_after_open=0))

  try:
    id1 = 1

    cg.rxflush()

    stop_motor(cg, id1, True)
    uid = get_unique_identifier(cg, id1)
    print('device uid:', hex(uid) if uid != None else uid)
    dump1(cg, id1, echo=True)
    dump2(cg, id1, echo=True)

    input('Press the Enter key.')

    #set_newid(cg, id1, id1)

    set_zero_position(cg, id1)

    print('MIT Ctrl mode')
    set_runmode(cg, id1, 0)
    cg.set_item_value(id1, cg.INDEX_limit_spd, 5.0)
    cg.set_item_value(id1, cg.INDEX_limit_cur, 2.0)
    start_motor(cg, id1)
    for p in tuple(range(32767, 65535, 1024)) + tuple(range(65535, 0, -1024)) + tuple(range(0, 32767, 1024)):
      '''
      trq: 0~65535 =- 12Nm~+12Nm
      pos: 0~65535 = -4pi~+4pi
      spd: 0~65535 = -30rad/s~+30rad/s
      Kp : 0~65535 = 0.0~500.0
      Kd : 0~65535 = 0.0~5.0
      '''
      cg.type1(id1, 32767, p, 32767, 50, 100)
      t = time.time() + 500 / 1000.0
      while t > time.time():
        print(f'\r<{id1}> pos:{p:>6d} {getmembystr(cg, id1,(cg.INDEX_boardTemp, cg.INDEX_iq, cg.INDEX_mechPos,cg.INDEX_mechVel,cg.INDEX_rotation))}\033[K', end='')
        a = cg.alarm
        if a != []:
          print(f'\n{a}')
        time.sleep(0.01)

    print('\nposition mode')
    set_runmode(cg, id1, 1)
    cg.set_item_value(id1, cg.INDEX_limit_spd, 20.0)
    cg.set_item_value(id1, cg.INDEX_limit_cur, 2.0)
    start_motor(cg, id1)
    for p in tuple(range(0, 100, 5)) + tuple(range(100, -100, -10)) + tuple(range(-100, 0, 5)):
      pos = p * 4 * math.pi / 100
      cg.set_item_value(id1, cg.INDEX_loc_ref, pos)
      t = time.time() + 500 / 1000.0
      while t > time.time():
        print(f'\r<{id1}> pos:{pos:>6.2f} {getmembystr(cg, id1,(cg.INDEX_boardTemp, cg.INDEX_iq, cg.INDEX_mechPos,cg.INDEX_mechVel,cg.INDEX_rotation))}\033[K', end='')
        a = cg.alarm
        if a != []:
          print(f'\n{a}')
        time.sleep(0.01)

    print('\nspeed mode')
    set_runmode(cg, id1, 2)
    cg.set_item_value(id1, cg.INDEX_limit_cur, 2.0)
    start_motor(cg, id1)
    for s in tuple(range(0, 30, 1)) + tuple(range(30, -30, -1)) + tuple(range(-30, 0, 1)):
      cg.set_item_value(id1, cg.INDEX_spd_ref, s)
      t = time.time() + 500 / 1000.0
      while t > time.time():
        print(f'\r<{id1}> velo:{s:>6.2f} {getmembystr(cg, id1,(cg.INDEX_boardTemp, cg.INDEX_iq, cg.INDEX_mechPos,cg.INDEX_mechVel,cg.INDEX_rotation))}\033[K', end='')
        a = cg.alarm
        if a != []:
          print(f'\n{a}')
        time.sleep(0.01)

    print('\ncurrent mode')
    set_runmode(cg, id1, 3)
    start_motor(cg, id1)
    for c in tuple(range(0, 23, 1)) + tuple(range(23, -23, -1)) + tuple(range(-23, 0, 1)):
      cg.set_item_value(id1, cg.INDEX_iq_ref, c)
      t = time.time() + 200 / 1000.0
      while t > time.time():
        print(f'\r<{id1}> cur:{c:>6.2f} {getmembystr(cg, id1,(cg.INDEX_boardTemp, cg.INDEX_iq, cg.INDEX_mechPos,cg.INDEX_mechVel,cg.INDEX_rotation))}\033[K', end='')
        a = cg.alarm
        if a != []:
          print(f'\n{a}')
        time.sleep(0.01)

  except KeyboardInterrupt:
    pass

  print()

  stop_motor(cg, id1)

  cg.shutdown()

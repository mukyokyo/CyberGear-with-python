#!/usr/bin/env python
#
# cybergear.py
# Libraries for some CyberGear protocols.
# The firmware version of Cybergear must be at least 1.2.1.5.
#
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: (C) 2024-2025 mukyokyo

import math, can, time
from struct import pack, unpack, iter_unpack

class CyberGear:
  _fields_ = (
    { 'name':'Name',            'code':0x0000, 'format':'',  'unit':''},
    { 'name':'BarCode',         'code':0x0001, 'format':'',  'unit':''},
    { 'name':'BootCodeVersion', 'code':0x1000, 'format':'',  'unit':''},
    { 'name':'BootBuildDate',   'code':0x1001, 'format':'',  'unit':''},
    { 'name':'BootBuildTime',   'code':0x1002, 'format':'',  'unit':''},
    { 'name':'AppCodeVersion',  'code':0x1003, 'format':'',  'unit':''},
    { 'name':'AppGitVersion',   'code':0x1004, 'format':'',  'unit':''},
    { 'name':'AppBuildDate',    'code':0x1005, 'format':'',  'unit':''},
    { 'name':'AppBuildTime',    'code':0x1006, 'format':'',  'unit':''},
    { 'name':'AppCodeName',     'code':0x1007, 'format':'',  'unit':''},
    { 'name':'echoPara1',       'code':0x2000, 'format':'H', 'unit':''},
    { 'name':'echoPara2',       'code':0x2001, 'format':'H', 'unit':''},
    { 'name':'echoPara3',       'code':0x2002, 'format':'H', 'unit':''},
    { 'name':'echoPara4',       'code':0x2003, 'format':'H', 'unit':''},
    { 'name':'echoFreHz',       'code':0x2004, 'format':'I', 'unit':''},
    { 'name':'MechOffset',      'code':0x2005, 'format':'f', 'unit':''},
    { 'name':'MechPos_init',    'code':0x2006, 'format':'f', 'unit':''},
    { 'name':'limit_torque',    'code':0x2007, 'format':'f', 'unit':''},
    { 'name':'I_FW_MAX',        'code':0x2008, 'format':'f', 'unit':''},
    { 'name':'motor_index',     'code':0x2009, 'format':'B', 'unit':''},
    { 'name':'CAN_ID',          'code':0x200a, 'format':'B', 'unit':''},
    { 'name':'CAN_MASTER',      'code':0x200b, 'format':'B', 'unit':''},
    { 'name':'CAN_TIMEOUT',     'code':0x200c, 'format':'I', 'unit':''},
    { 'name':'motorOverTemp',   'code':0x200d, 'format':'h', 'unit':'*10degC'},
    { 'name':'overTempTime',    'code':0x200e, 'format':'I', 'unit':''},
    { 'name':'GearRatio',       'code':0x200f, 'format':'f', 'unit':''},
    { 'name':'Tq_caliType',     'code':0x2010, 'format':'B', 'unit':''},
    { 'name':'cur_filt_gain',   'code':0x2011, 'format':'f', 'unit':''},
    { 'name':'cur_kp',          'code':0x2012, 'format':'f', 'unit':''},
    { 'name':'cur_ki',          'code':0x2013, 'format':'f', 'unit':''},
    { 'name':'spd_kp',          'code':0x2014, 'format':'f', 'unit':''},
    { 'name':'spd_ki',          'code':0x2015, 'format':'f', 'unit':''},
    { 'name':'loc_kp',          'code':0x2016, 'format':'f', 'unit':''},
    { 'name':'spd_filt_gain',   'code':0x2017, 'format':'f', 'unit':''},
    { 'name':'limit_spd',       'code':0x2018, 'format':'f', 'unit':''},
    { 'name':'limit_cur',       'code':0x2019, 'format':'f', 'unit':''},

    { 'name':'timeUse0',        'code':0x3000, 'format':'H', 'unit':''},
    { 'name':'timeUse1',        'code':0x3001, 'format':'H', 'unit':''},
    { 'name':'timeUse2',        'code':0x3002, 'format':'H', 'unit':''},
    { 'name':'timeUse3',        'code':0x3003, 'format':'H', 'unit':''},
    { 'name':'encoderRaw',      'code':0x3004, 'format':'h', 'unit':''},
    { 'name':'mcuTemp',         'code':0x3005, 'format':'h', 'unit':'*10degC'},
    { 'name':'motorTemp',       'code':0x3006, 'format':'h', 'unit':'*10degC'},
    { 'name':'vBus',            'code':0x3007, 'format':'H', 'unit':'mV'},
    { 'name':'adc1Offset',      'code':0x3008, 'format':'i', 'unit':''},
    { 'name':'adc2Offset',      'code':0x3009, 'format':'i', 'unit':''},
    { 'name':'adc1Raw',         'code':0x300a, 'format':'H', 'unit':''},
    { 'name':'adc2Raw',         'code':0x300b, 'format':'H', 'unit':''},
    { 'name':'VBUS',            'code':0x300c, 'format':'f', 'unit':'V'},
    { 'name':'cmdId',           'code':0x300d, 'format':'f', 'unit':'A'},
    { 'name':'cmdIq',           'code':0x300e, 'format':'f', 'unit':'A'},
    { 'name':'cmdlocref',       'code':0x300f, 'format':'f', 'unit':'rad'},
    { 'name':'cmdspdref',       'code':0x3010, 'format':'f', 'unit':'rad/s'},
    { 'name':'cmdTorque',       'code':0x3011, 'format':'f', 'unit':''},
    { 'name':'cmdPos',          'code':0x3012, 'format':'f', 'unit':'rad'},
    { 'name':'cmdVel',          'code':0x3013, 'format':'f', 'unit':'rad/s'},
    { 'name':'rotation',        'code':0x3014, 'format':'h', 'unit':''},
    { 'name':'modPos',          'code':0x3015, 'format':'f', 'unit':'rad'},
    { 'name':'mechPos',         'code':0x3016, 'format':'f', 'unit':'rad'},
    { 'name':'mechVel',         'code':0x3017, 'format':'f', 'unit':'rad/s'},
    { 'name':'elecPos',         'code':0x3018, 'format':'f', 'unit':''},
    { 'name':'ia',              'code':0x3019, 'format':'f', 'unit':'A'},
    { 'name':'ib',              'code':0x301a, 'format':'f', 'unit':'A'},
    { 'name':'ic',              'code':0x301b, 'format':'f', 'unit':'A'},
    { 'name':'tick',            'code':0x301c, 'format':'I', 'unit':''},
    { 'name':'phaseOrder',      'code':0x301d, 'format':'B', 'unit':''},
    { 'name':'iqf',             'code':0x301e, 'format':'f', 'unit':'A'},
    { 'name':'boardTemp',       'code':0x301f, 'format':'h', 'unit':'*10degC'},
    { 'name':'iq',              'code':0x3020, 'format':'f', 'unit':'A'},
    { 'name':'id',              'code':0x3021, 'format':'f', 'unit':'A'},
    { 'name':'faultSta',        'code':0x3022, 'format':'I', 'unit':''},
    { 'name':'warnSta',         'code':0x3023, 'format':'I', 'unit':''},
    { 'name':'drv_fault',       'code':0x3024, 'format':'I', 'unit':''},
    { 'name':'drv_temp',        'code':0x3025, 'format':'h', 'unit':''},
    { 'name':'Uq',              'code':0x3026, 'format':'f', 'unit':''},
    { 'name':'Ud',              'code':0x3027, 'format':'f', 'unit':''},
    { 'name':'dtc_u',           'code':0x3028, 'format':'f', 'unit':''},
    { 'name':'dtc_v',           'code':0x3029, 'format':'f', 'unit':''},
    { 'name':'dtc_w',           'code':0x302a, 'format':'f', 'unit':''},
    { 'name':'v_bus',           'code':0x302b, 'format':'f', 'unit':'V'},
    { 'name':'v_ref',           'code':0x302c, 'format':'f', 'unit':'V'},
    { 'name':'torque_fdb',      'code':0x302d, 'format':'f', 'unit':'Nm'},
    { 'name':'rated_i',         'code':0x302e, 'format':'f', 'unit':'A'},
    { 'name':'limit_i',         'code':0x302f, 'format':'f', 'unit':'A'},

    { 'name':'run_mode',        'code':0x7005, 'format':'B', 'unit':'A'},
    { 'name':'iq_ref',          'code':0x7006, 'format':'f', 'unit':'rad/s'},
    { 'name':'spd_ref',         'code':0x700a, 'format':'f', 'unit':'Nm'},
    { 'name':'limit_torque_2',  'code':0x700b, 'format':'f', 'unit':''},
    { 'name':'cur_kp_2',        'code':0x7010, 'format':'f', 'unit':''},
    { 'name':'cur_ki_2',        'code':0x7011, 'format':'f', 'unit':''},
    { 'name':'cur_filt_gain_2', 'code':0x7014, 'format':'f', 'unit':''},
    { 'name':'loc_ref',         'code':0x7016, 'format':'f', 'unit':'rad'},
    { 'name':'limit_spd_2',     'code':0x7017, 'format':'f', 'unit':'rad/s'},
    { 'name':'limit_cur_2',     'code':0x7018, 'format':'f', 'unit':'A'},
    { 'name':'mechPos_2',       'code':0x7019, 'format':'f', 'unit':'rad'},
    { 'name':'iqf_2',           'code':0x701a, 'format':'f', 'unit':'A'},
    { 'name':'mechVel_2',       'code':0x701b, 'format':'f', 'unit':'rad/s'},
    { 'name':'VBUS_2',          'code':0x701c, 'format':'f', 'unit':'V'},
    { 'name':'rotation_2',      'code':0x701d, 'format':'h', 'unit':'turn'},
    { 'name':'loc_kp_2',        'code':0x701e, 'format':'f', 'unit':''},
    { 'name':'spd_kp_2',        'code':0x701f, 'format':'f', 'unit':''},
    { 'name':'spd_ki_2',        'code':0x7020, 'format':'f', 'unit':''}
  )

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

  def __send(self, cmd, id, id_opt, data : bytes = b'', echo = False) -> bool:
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

  def __send_recieve(self, cmd, id, id_opt, data : bytes = b'', echo = False) -> bytes:
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
    r = self.__send_recieve(4, id, self.__myid, (1 if fault else 0,), echo = echo)
    if r != None:
      if ((r.arbitration_id >> 24) & 0xff == 2):
        return list(*iter_unpack('>HHHH', bytes(r)))

  # set zero position
  def type6(self, id, echo = False):
    r = self.__send_recieve(6, id, self.__myid, (1,), echo = echo)
    if r != None:
      if ((r.arbitration_id >> 24) & 0xff == 2):
        return list(*iter_unpack('>HHHH', bytes(r)))

  # change id
  def type7(self, id, newid, echo = False):
    if newid <= 0x7f:
      if self.__send(7, id, (newid << 8) | self.__myid, b'', echo = echo):
        r = self.__recv(tout = 0.05, echo = echo)
        if r != None:
          if ((r.arbitration_id >> 8) & 0xff == newid):
            return list(*iter_unpack('<Q', bytes(r.data)))[0]

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
      if self.__send(22, id, self.__myid, (baud,), echo = echo):
        r = self.__recv(tout = 0.05, echo = echo)
        if r != None:
          if ((r.arbitration_id >> 8) & 0xff == id) and ((r.arbitration_id >> 24) & 0xff == 0):
            return list(*iter_unpack('<Q', bytes(r.data)))[0]

  # write param by name
  def set_item_value (self, id, name_or_code : str | int , val, echo = False) -> bool:
    if type(name_or_code) is str:
      f = next(filter(lambda d: d['name'] == name_or_code, self._fields_), None)
      if f:
        return self.type18(id, f['code'], val, f['format'], echo = echo) != None
    else:
      f = next(filter(lambda d: d['code'] == name_or_code, self._fields_), None)
      if f:
        return self.type18(id, f['code'], val, f['format'], echo = echo) != None

  # read param by name
  def get_item_value (self, id, name_or_code : str | int, echo = False):
    if type(name_or_code) is str:
      f = next(filter(lambda d: d['name'] == name_or_code, self._fields_), None)
      if f:
        if f['code'] > 0x7000:
          return f, self.type17(id, f['code'], f['format'], echo = echo)
        else:
          return f, self.type9(id, f['code'])
    else:
      f = next(filter(lambda d: d['code'] == name_or_code, self._fields_), None)
      if f:
        if f['code'] > 0x7000:
          return f, self.type17(id, f['code'], f['format'], echo = echo)
        else:
          return f, self.type9(id, f['code'])

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
      return cg.set_item_value(id, 'run_mode', m, echo = echo)

  def set_zero_position(cg, id, echo = False):
    return cg.type6(id, echo = echo)

  def dump(cg, id, echo = False):
    result = ()
    lst = (
      'Name', 'BarCode', 'BootCodeVersion', 'BootBuildDate', 'BootBuildTime', 'AppCodeVersion', 'AppGitVersion', 'AppBuildDate', 'AppBuildTime', 'AppCodeName',
      'echoPara1', 'echoPara2', 'echoPara3', 'echoPara4', 'echoFreHz', 'MechOffset', 'MechPos_init', 'limit_torque', 'I_FW_MAX', 'motor_index', 'CAN_ID', 'CAN_MASTER', 'CAN_TIMEOUT', 'motorOverTemp', 'overTempTime', 'GearRatio', 'Tq_caliType', 'cur_filt_gain', 'cur_kp', 'cur_ki', 'spd_kp', 'spd_ki', 'loc_kp', 'spd_filt_gain', 'limit_spd', 'limit_cur', 'timeUse0', 'timeUse1', 'timeUse2', 'timeUse3', 'encoderRaw', 'mcuTemp', 'motorTemp', 'vBus', 'adc1Offset', 'adc2Offset', 'adc1Raw', 'adc2Raw', 'VBUS', 'cmdId', 'cmdIq', 'cmdlocref', 'cmdspdref', 'cmdTorque', 'cmdPos', 'cmdVel', 'rotation', 'modPos', 'mechPos', 'mechVel', 'elecPos', 'ia', 'ib', 'ic', 'tick', 'phaseOrder', 'iqf', 'boardTemp', 'iq', 'id', 'faultSta', 'warnSta', 'drv_fault', 'drv_temp', 'Uq', 'Ud', 'dtc_u', 'dtc_v', 'dtc_w', 'v_bus', 'v_ref', 'torque_fdb', 'rated_i', 'limit_i',
      'run_mode', 'iq_ref', 'spd_ref', 'limit_torque_2', 'cur_kp_2', 'cur_ki_2', 'cur_filt_gain_2', 'loc_ref', 'limit_spd_2', 'limit_cur_2', 'mechPos_2', 'iqf_2', 'mechVel_2', 'VBUS_2', 'rotation_2', 'loc_kp_2', 'spd_kp_2', 'spd_ki_2'
    )
    for l in lst:
      r =  cg.get_item_value(id, l)
      if r != None:
        if echo:
          match r[0]['format']:
            case 'B':
              print(f'${r[0]["code"]:04x} {r[0]["name"]:15}: ${r[1]:02x}{r[0]["unit"]}')
            case 'f':
              print(f'${r[0]["code"]:04x} {r[0]["name"]:15}: {r[1]:.3f}{r[0]["unit"]}')
            case 'h':
              print(f'${r[0]["code"]:04x} {r[0]["name"]:15}: {r[1]}{r[0]["unit"]}')
            case _:
              print(f'${r[0]["code"]:04x} {r[0]["name"]:15}: {r[1]}{r[0]["unit"]}')
    return result

  def getvaluebystr(cg, id, names):
    s = ''
    dat = []
    for name in names:
      dat += cg.get_item_value(id, name),
    for d in dat:
      match d[0]['format']:
        case 'I':
          s += f'${d[0]["code"]:04x}:{d[1]:>8d}{d[0]["unit"]} '
        case 'f':
          s += f'${d[0]["code"]:04x}:{d[1]:>9.2f}{d[0]["unit"]} '
        case _:
          s += f'${d[0]["code"]:04x}:{d[1]}{d[0]["unit"]} '
    return(s)

  print('start')

#  cg = CyberGear(can.Bus(interface='socketcan', channel='can0'))
  cg = CyberGear(can.Bus(interface='gs_usb', channel=0x606f, index=0, bitrate=1000000))
#  cg = CyberGear(can.Bus(interface='slcan', channel='\\\\.\\com11', bitrate=1000000, sleep_after_open=0))
#  cg = CyberGear(can.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=1000000))

  try:
    target_id = 1

    cg.rxflush()

    stop_motor(cg, target_id, True)
    uid = get_unique_identifier(cg, target_id)
    print('device uid:', hex(uid) if uid != None else uid)
    dump(cg, target_id, echo=True)

    input('Press the Enter key.')

    #set_newid(cg, target_id, target_id)

    set_zero_position(cg, target_id)

    print('MIT Ctrl mode')
    set_runmode(cg, target_id, 0)
    cg.set_item_value(target_id, 'limit_spd', 5.0)
    cg.set_item_value(target_id, 'limit_cur', 2.0)
    start_motor(cg, target_id)
    for p in tuple(range(32767, 65535, 1024)) + tuple(range(65535, 0, -1024)) + tuple(range(0, 32767, 1024)):
      '''
      trq: 0~65535 =- 12Nm~+12Nm
      pos: 0~65535 = -4pi~+4pi
      spd: 0~65535 = -30rad/s~+30rad/s
      Kp : 0~65535 = 0.0~500.0
      Kd : 0~65535 = 0.0~5.0
      '''
      cg.type1(target_id, 32767, p, 32767, 50, 100)
      t = time.time() + 500 / 1000.0
      while t > time.time():
        print(f'\r<{target_id}> pos:{p:>6d} {getvaluebystr(cg, target_id,("boardTemp", "iq", "mechPos", "mechVel", "rotation"))}\033[K', end='')
        a = cg.alarm
        if a != []:
          print(f'\n{a}')
        time.sleep(0.01)

    print('\nposition mode')
    set_runmode(cg, target_id, 1)
    cg.set_item_value(target_id, 'limit_spd', 20.0)
    cg.set_item_value(target_id, 'limit_cur', 2.0)
    start_motor(cg, target_id)
    for p in tuple(range(0, 100, 5)) + tuple(range(100, -100, -10)) + tuple(range(-100, 0, 5)):
      pos = p * 4 * math.pi / 100
      cg.set_item_value(target_id, 'loc_ref', pos)
      t = time.time() + 500 / 1000.0
      while t > time.time():
        print(f'\r<{target_id}> tpos:{pos:>6.2f} {getvaluebystr(cg, target_id,("boardTemp", "iq", "mechPos", "mechVel", "rotation"))}\033[K', end='')
        a = cg.alarm
        if a != []:
          print(f'\n{a}')
        time.sleep(0.01)

    print('\nspeed mode')
    set_runmode(cg, target_id, 2)
    cg.set_item_value(target_id, 'limit_cur', 2.0)
    start_motor(cg, target_id)
    for s in tuple(range(0, 30, 1)) + tuple(range(30, -30, -1)) + tuple(range(-30, 0, 1)):
      cg.set_item_value(target_id, 'spd_ref', s)
      t = time.time() + 500 / 1000.0
      while t > time.time():
        print(f'\r<{target_id}> tvel:{s:>6.2f} {getvaluebystr(cg, target_id,("boardTemp", "iq", "mechPos", "mechVel", "rotation"))}\033[K', end='')
        a = cg.alarm
        if a != []:
          print(f'\n{a}')
        time.sleep(0.01)

    print('\ncurrent mode')
    set_runmode(cg, target_id, 3)
    start_motor(cg, target_id)
    for c in tuple(range(0, 23, 1)) + tuple(range(23, -23, -1)) + tuple(range(-23, 0, 1)):
      cg.set_item_value(target_id, 'iq_ref', c)
      t = time.time() + 200 / 1000.0
      while t > time.time():
        print(f'\r<{target_id}> tcur:{c:>6.2f} {getvaluebystr(cg, target_id,("boardTemp", "iq", "mechPos", "mechVel", "rotation"))}\033[K', end='')
        a = cg.alarm
        if a != []:
          print(f'\n{a}')
        time.sleep(0.01)

  except KeyboardInterrupt:
    pass

  print()

  stop_motor(cg, target_id)

  cg.shutdown()

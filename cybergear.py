#!/usr/bin/env python3
#
# cybergear.py
# Libraries for some CyberGear protocols.
# The firmware version of Cybergear must be at least 1.2.1.5.
#
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: (C) 2024-2025 mukyokyo

import can, time, math
from threading import Lock
from struct import pack, unpack, iter_unpack

class CyberGear:
  _fields_ = (
    { 'name':'Name',            'code':0x0000, 'format':'s', 'unit':''},
    { 'name':'BarCode',         'code':0x0001, 'format':'s', 'unit':''},
    { 'name':'BootCodeVersion', 'code':0x1000, 'format':'s', 'unit':''},
    { 'name':'BootBuildDate',   'code':0x1001, 'format':'s', 'unit':''},
    { 'name':'BootBuildTime',   'code':0x1002, 'format':'s', 'unit':''},
    { 'name':'AppCodeVersion',  'code':0x1003, 'format':'s', 'unit':''},
    { 'name':'AppGitVersion',   'code':0x1004, 'format':'s', 'unit':''},
    { 'name':'AppBuildDate',    'code':0x1005, 'format':'s', 'unit':''},
    { 'name':'AppBuildTime',    'code':0x1006, 'format':'s', 'unit':''},
    { 'name':'AppCodeName',     'code':0x1007, 'format':'s', 'unit':''},
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
    { 'name':'limit_spd',       'code':0x2018, 'format':'f', 'unit':'rad/s'},
    { 'name':'limit_cur',       'code':0x2019, 'format':'f', 'unit':'A'},

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
    { 'name':'cmdTorque',       'code':0x3011, 'format':'f', 'unit':'Nm'},
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
    { 'name':'drv_temp',        'code':0x3025, 'format':'h', 'unit':'degC'},
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

    { 'name':'run_mode',        'code':0x7005, 'format':'B', 'unit':''},
    { 'name':'iq_ref',          'code':0x7006, 'format':'f', 'unit':'A'},
    { 'name':'spd_ref',         'code':0x700a, 'format':'f', 'unit':'rad/s'},
    { 'name':'limit_torque_2',  'code':0x700b, 'format':'f', 'unit':'Nm'},
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

  def __init__(self, bus, lock = None):
    self.__canbus = bus
    self.__myid = 0xfd
    self.__alarm = list()
    self.__rmes = list()
    if lock == None:
      self.__lock = Lock()
    else:
      self.__lock = lock
    self.rxflush()

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  @property
  def lock(self):
    return self.__lock

  @property
  def alarm(self):
    r = self.__alarm
    self.__alarm = []
    return r

  def rxflush(self):
    t = time.time() + 5.0
    while not (self.__canbus.recv(timeout=0) is None):
      if time.time() > t: return

  def __makeaid (self, cmd:int, id:int, id_opt:int, mask = 0xffffffff) -> tuple:
    return (id & 0xff) | ((id_opt & 0xffff) << 8) | ((cmd & 0x1f) << 24), mask

  def __send(self, cmd : int, id : int, id_opt : int, data : bytes = bytes(8), echo = False) -> bool:
    if id <= 0x7f:
      try:
        msg = can.Message(arbitration_id = self.__makeaid(cmd, id, id_opt)[0], data = data, is_extended_id = True)
        self.__canbus.send(msg, timeout = 0.1)
        if echo: print(f'TX: id=${msg.arbitration_id:08x} data=',':'.join(format(x, '02x') for x in msg.data))
      except can.CanError:
        return False
      else:
        return True
    return False

  def __recv(self, tout = 0.05, matchaid = (0, 0), echo = False) -> bytes:
    t = time.time() + tout
    while time.time() < t:
      try:
        r = self.__canbus.recv(timeout=0.001)
        if r != None:
          if r.is_rx:
            if echo: print(f'RX: id=${r.arbitration_id:08x} data=', ':'.join(format(x, '02x') for x in r.data))
            typ = (r.arbitration_id >> 24) & 0xff
            if typ == 21:
              self.__alarm.append(((r.arbitration_id >> 8) & 0xff, r.timestamp, tuple(*iter_unpack('<Q', bytes(r.data)))[0]))
            elif typ == 22:
              pass
            if (matchaid != (0,0)):
              if (r.arbitration_id & matchaid[1]) == matchaid[0]:
                return r
            else:
              return r
      except can.CanError:
        pass

  def type0(self, id : int, echo = False) -> int:
    """
    get unique identifier

    parameters
    -------------
    id : int
      node id
    """

    with self.__lock:
      if self.__send(0, id, self.__myid, echo = echo):
        r = self.__recv(matchaid = self.__makeaid(0, 0xfe, id), echo = echo)
        if r != None:
          return tuple(*iter_unpack('<Q', bytes(r.data)))[0]

  def type1(self, id : int, torque : int, angle : int, speed : int, Kp : int, Kd : int, echo = False) -> tuple:
    """
    controle mode

    parameters
    -------------
    id : int
      node id
    torque : int
      0~65535 =- 12Nm~+12Nm
    angle : int
      0~65535 = -4pi~+4pi
    speed : int
      0~65535 = -30rad/s~+30rad/s
    Kp : int
      0~65535 = 0.0~500.0
    Kd : int
      0~65535 = 0.0~5.0
    """

    with self.__lock:
      if self.__send(1, id, torque, bytes(pack('>HHHH', angle, speed, Kp, Kd)), echo = echo):
        r = self.__recv(matchaid = self.__makeaid(2, self.__myid, id, 0xff00ffff), echo = echo)
        if r != None:
          return ((r.arbitration_id & 0xff0000) >> 16,) + tuple(*iter_unpack('>HHHH', bytes(r)))


  def type2(self, id : int, echo = False) -> tuple:
    """
    feedback

    parameters
    -------------
    id : int
      node id
    """
    with self.__lock:
      if self.__send(2, id, self.__myid, echo = echo):
        r = self.__recv(matchaid = self.__makeaid(2, self.__myid, id, 0xff00ffff), echo = echo)
        if r != None:
          return ((r.arbitration_id & 0xff0000) >> 16,) + tuple(*iter_unpack('>HHHH', bytes(r)))

  def type3(self, id : int, echo = False) -> tuple:
    """
    enable

    parameters
    -------------
    id : int
      node id
    """
    with self.__lock:
      if self.__send(3, id, self.__myid, echo = echo):
        r = self.__recv(matchaid = self.__makeaid(2, self.__myid, id, 0xff00ffff), echo = echo)
        if r != None:
          return ((r.arbitration_id & 0xff0000) >> 16,) + tuple(*iter_unpack('>HHHH', bytes(r)))

  def type4(self, id : int, fault = False, echo = False) -> tuple:
    """
    shutdown

    parameters
    -------------
    id : int
      node id
    fault: bool
      Clear fault
    """
    with self.__lock:
      if self.__send(4, id, self.__myid, (1 if fault else 0, 0,0,0,0,0,0,0), echo = echo):
        r = self.__recv(matchaid = self.__makeaid(2, self.__myid, id, 0xff00ffff), echo = echo)
        if r != None:
          return ((r.arbitration_id & 0xff0000) >> 16,) + tuple(*iter_unpack('>HHHH', bytes(r)))

  def type6(self, id : int, echo = False) -> tuple:
    """
    set zero position

    parameters
    -------------
    id : int
      node id
    """
    with self.__lock:
      if self.__send(6, id, self.__myid, (1,0,0,0,0,0,0,0), echo = echo):
        r = self.__recv(matchaid = self.__makeaid(2, self.__myid, id, 0xff00ffff), echo = echo)
        if r != None:
          return ((r.arbitration_id & 0xff0000) >> 16,) + tuple(*iter_unpack('>HHHH', bytes(r)))

  def type7(self, id : int, newid : int, echo = False) -> int:
    """
    change id

    parameters
    -------------
    id : int
      node id
    newid : int
      new node id
    """
    with self.__lock:
      if newid <= 0x7f:
        if self.__send(7, id, (newid << 8) | self.__myid, echo = echo):
          r = self.__recv(matchaid = self.__makeaid(0, 0xfe, id), echo = echo)
          if r != None:
            return tuple(*iter_unpack('<Q', bytes(r.data)))[0]

  def type9(self, id : int, index : int, echo = False):
    """
    read config

    parameters
    -------------
    id : int
      node id
    index : int
      index (0~0x302f)
    """
    s = bytes()
    with self.__lock:
      if self.__send(9, id, self.__myid, bytes(pack('<Hxxxxxx', index)), echo):
        lcnt = 3
        cnt = 0
        t = time.time() + 0.1
        while lcnt >= cnt:
          if time.time() > t: return
          r = self.__recv(matchaid = self.__makeaid(9, self.__myid, id), echo = echo)
          if r != None:
            d = (tuple(*iter_unpack('<HBBBBBB', bytes(r.data))))
            if index == d[0]:
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

        if ('d' in locals()) and (lcnt + 1 == cnt):
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
              return s.decode('utf-8', 'replace')

  def type17(self, id : int, index : int, width = 'B', echo = False) -> None | int | float:
    """
    read param

    parameters
    -------------
    id : int
      node id
    index : int
      index (0x7000~)
    width : str
      unpack format string
    """
    with self.__lock:
      if self.__send(17, id, self.__myid, bytes(pack('<Hxxxxxx', index)), echo = echo):
        r = self.__recv(matchaid = self.__makeaid(17, self.__myid, id, 0xff00ffff), echo = echo)
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
            case 'I':
              return tuple(*iter_unpack('<HxxL', bytes(r.data)))[1]
            case 'f':
              return tuple(*iter_unpack('<Hxxf', bytes(r.data)))[1]

  def type18(self, id : int, index : int, data : int | float, width = 'B', echo = False) -> tuple:
    """
    write param

    parameters
    -------------
    id : int
      node id
    index : int
      index
    data : int | float
      data value
    width : str
      pack format string
    """
    match width:
      case 'B':
        b = bytes(pack('<HxxBxxx', index, data))
      case 'h':
        b = bytes(pack('<Hxxhxx', index, data))
      case 'H':
        b = bytes(pack('<HxxHxx', index, data))
      case 'l':
        b = bytes(pack('<Hxxl', index, data))
      case 'I':
        b = bytes(pack('<HxxL', index, data))
      case 'f':
        b = bytes(pack('<Hxxf', index, data))

    with self.__lock:
      if self.__send(18, id, self.__myid, b, echo = echo):
        r = self.__recv(matchaid = self.__makeaid(2, self.__myid, id, 0xff00ffff), echo = echo)
        if r != None:
          return ((r.arbitration_id & 0xff0000) >> 16,) + tuple(*iter_unpack('>HHHH', bytes(r)))

  def type19(self, id : int, echo = False) -> bytes:
    """
    read raw config

    parameters
    -------------
    id : int
      node id
    """
    with self.__lock:
      if self.__send(19, id, self.__myid, (0xC4, 0x7F, 0x31, 0x31, 0x30, 0x33, 0x31, 0x04), echo = echo):
        s = bytes()
        t = time.time() + 5.0
        maid = self.__makeaid(19, self.__myid, id, 0xff00ffff)
        while True:
          if time.time() > t:
            break
          r = self.__recv(matchaid = maid, echo = echo)
          if r != None:
            d = (tuple(*iter_unpack('<HBBBBBB', bytes(r.data))))
            if r.arbitration_id & 0xff0000 != 0x090000:
              s += bytes(d[1:7])
            else:
              break;
        return s

  def type22(self, id : int, baud : int, echo = False) -> int:
    """
    set baudrate

    parameters
    -------------
    id : int
      node id
    baud : int
      new baudrate (1:1M, 2:500k, 3:250k, 4:125k[bps])
    """
    if baud >= 1 and baud <= 4:
      with self.__lock:
        if self.__send(22, id, self.__myid, (baud,0,0,0,0,0,0,0), echo = echo):
          r = self.__recv(matchaid = self.__makeaid(0, 0xfe, id), echo = echo)
          if r != None:
            return tuple(*iter_unpack('<Q', bytes(r.data)))[0]

  def set_item (self, id : int, name_or_code : str | int , val, echo = False) -> bool:
    """
    write param by name
    """
    if type(name_or_code) is str:
      f = next(filter(lambda d: d['name'] == name_or_code, self._fields_), None)
      if f:
        return self.type18(id, f['code'], val, f['format'], echo = echo) != None
    else:
      f = next(filter(lambda d: d['code'] == name_or_code, self._fields_), None)
      if f:
        return self.type18(id, f['code'], val, f['format'], echo = echo) != None

  def get_item (self, id : int, name_or_code : str | int, echo = False):
    """
    read param by name
    """
    if type(name_or_code) is str:
      f = next(filter(lambda d: d['name'] == name_or_code, self._fields_), None)
      if f:
        if f['code'] >= 0x7000:
          return f, self.type17(id, f['code'], f['format'], echo = echo)
        else:
          return f, self.type9(id, f['code'], echo = echo)
    else:
      f = next(filter(lambda d: d['code'] == name_or_code, self._fields_), None)
      if f:
        if f['code'] >= 0x7000:
          return f, self.type17(id, f['code'], f['format'], echo = echo)
        else:
          return f, self.type9(id, f['code'], echo = echo)

  def float_to_uint(self, x : float, x_min : float, x_max : float):
    if (x > x_max): x = x_max
    elif (x < x_min): x = x_min
    return int((x - x_min) * 65535 / (x_max - x_min))

  def uint_to_float(self, x : int, x_min : float, x_max : float):
    return float(x / 65535 * (x_max - x_min) + x_min)

  def get_uid(self, id, echo = False):
    """
    get unique id
    """
    return self.type0(id, echo = echo)

  def get_feedback(self, ids : int | list | tuple, echo = False) -> tuple:
    """
    get feedback
    """
    def fb(id, echo = echo):
      r = self.type2(id, echo = echo)
      print(r)
      if r != None:
        return (
          (r[0] >> 16) & 0xff,
          self.uint_to_float(r[1][0], -4 * math.pi, 4 * math.pi),
          self.uint_to_float(r[1][1], -30, 30),
          self.uint_to_float(r[1][2], -12, 12),
          self.uint_to_float(r[1][3], 0, 6553.5)
        )

    if not (isinstance(ids, tuple) or isinstance(ids, list)):
      return fb(ids, echo = echo)
    else:
      return [(id, fb(id, echo = echo)) for id in ids]

  def start_motor(self, ids : int | list | tuple, echo = False) -> bool | tuple:
    """
    enable motor
    """
    if not (isinstance(ids, tuple) or isinstance(ids, list)):
      return (self.type3(ids, echo = echo) != None)
    else:
      return [(self.type3(id, echo = echo) != None) for id in ids]

  def stop_motor(self, ids : int | list | tuple, fault = False, echo = False) -> bool | tuple:
    """
    stop motor
    """
    if not (isinstance(ids, tuple) or isinstance(ids, list)):
      return (self.type4(ids, fault, echo = echo) != None)
    else:
      return [(self.type4(id, fault, echo = echo) != None) for id in ids]

  def set_newid(self, id : int, newid : int, echo = False) -> int:
    """
    set new id
    """
    if id != newid:
      if self.get_feedback(newid, echo = echo) == None:
        return self.type7(id, newid, echo = echo)

  def scan(self, show = False, echo = False):
    """
    set run mode
    """
    result = ()
    for id in range(0, 0x80):
      r = cg.type0(id, echo = echo)
      if r != None:
        if show:
          print(f'find:{id}')
        result += id,
    return result

  def set_runmode(self, ids : int | list | tuple, m : int, echo = False) -> bool:
    """
    set run mode
    """
    self.stop_motor(ids)
    if not (isinstance(ids, tuple) or isinstance(ids, list)):
      return self.set_item(ids, 'run_mode', m, echo = echo)
    else:
      return [self.set_item(id, 'run_mode', m, echo = echo) for id in ids]

  def set_home_pos(self, ids : int | list | tuple, echo = False) -> bool:
    """
    set zero position
    """
    if not (isinstance(ids, tuple) or isinstance(ids, list)):
      return (self.type6(ids, echo = echo) != None)
    else:
      return [(self.type6(id, echo = echo) != None) for id in ids]

  def dump(self, id : int, show = False, echo = False):
    """
    dump items
    """
    result = ()
    items = (
      'Name', 'BarCode', 'BootCodeVersion', 'BootBuildDate', 'BootBuildTime', 'AppCodeVersion', 'AppGitVersion', 'AppBuildDate', 'AppBuildTime', 'AppCodeName',
      'echoPara1', 'echoPara2', 'echoPara3', 'echoPara4', 'echoFreHz', 'MechOffset', 'MechPos_init', 'limit_torque', 'I_FW_MAX', 'motor_index', 'CAN_ID', 'CAN_MASTER', 'CAN_TIMEOUT', 'motorOverTemp', 'overTempTime', 'GearRatio', 'Tq_caliType', 'cur_filt_gain', 'cur_kp', 'cur_ki', 'spd_kp', 'spd_ki', 'loc_kp', 'spd_filt_gain', 'limit_spd', 'limit_cur', 'timeUse0', 'timeUse1', 'timeUse2', 'timeUse3', 'encoderRaw', 'mcuTemp', 'motorTemp', 'vBus', 'adc1Offset', 'adc2Offset', 'adc1Raw', 'adc2Raw', 'VBUS', 'cmdId', 'cmdIq', 'cmdlocref', 'cmdspdref', 'cmdTorque', 'cmdPos', 'cmdVel', 'rotation', 'modPos', 'mechPos', 'mechVel', 'elecPos', 'ia', 'ib', 'ic', 'tick', 'phaseOrder', 'iqf', 'boardTemp', 'iq', 'id', 'faultSta', 'warnSta', 'drv_fault', 'drv_temp', 'Uq', 'Ud', 'dtc_u', 'dtc_v', 'dtc_w', 'v_bus', 'v_ref', 'torque_fdb', 'rated_i', 'limit_i',
      'run_mode', 'iq_ref', 'spd_ref', 'limit_torque_2', 'cur_kp_2', 'cur_ki_2', 'cur_filt_gain_2', 'loc_ref', 'limit_spd_2', 'limit_cur_2', 'mechPos_2', 'iqf_2', 'mechVel_2', 'VBUS_2', 'rotation_2', 'loc_kp_2', 'spd_kp_2', 'spd_ki_2'
    )
    for item in items:
      r =  self.get_item(id, item, echo = echo)
      if r != None:
        if r[1] != None:
          result += (r[0]["code"], r[0]["name"], r[1]),
          if show:
            match r[0]['format']:
              case 'B':
                print(f'${r[0]["code"]:04x} {r[0]["name"]:15}: ${r[1]:02x} {r[0]["unit"]}')
              case 'f':
                print(f'${r[0]["code"]:04x} {r[0]["name"]:15}: {r[1]:.3f} {r[0]["unit"]}')
              case _:
                print(f'${r[0]["code"]:04x} {r[0]["name"]:15}: {r[1]} {r[0]["unit"]}')
    return result

  def get_items_as_str(self, id : int, names : list | tuple, echo = False):
    """
    get items value as string
    """
    s = ''
    dat = ()
    for name in names:
      dat += self.get_item(id, name, echo = echo),
    for d in dat:
      if d[1] != None:
        match d[0]['format']:
          case 'I':
            s += f'${d[0]["code"]:04x}:{d[1]:>8d}{d[0]["unit"]} '
          case 'f':
            s += f'${d[0]["code"]:04x}:{d[1]:>9.2f}{d[0]["unit"]} '
          case _:
            s += f'${d[0]["code"]:04x}:{d[1]}{d[0]["unit"]} '
      else:
        s += f'${d[0]["code"]:04x}:{d[1]}{d[0]["unit"]} '
    return(s)


if __name__ == "__main__":
  import sys, time

  print('start')

#  with CyberGear(can.Bus(interface='socketcan', channel='can0')) as cg, :
#  with CyberGear(can.Bus(interface='gs_usb', channel=0x606f, index=0, bitrate=1000000)) as cg:
  with CyberGear(can.Bus(interface='slcan', channel='\\\\.\\com16', bitrate=1000000, sleep_after_open=0)) as cg:
#  with CyberGear(can.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=1000000)) as cg:

    try:
      target_id = 1

      '''
      print('type0=', cg.type0(target_id, echo=True))
      print('type1=', cg.type1(target_id, 32767, 32767, 32767, 0, 0, echo=True))
      print('type2=', cg.type2(target_id, echo=True))
      print('type3=', cg.type3(target_id, echo=True))
      print('type4=', cg.type4(target_id, True, echo=True))
      print('type6=', cg.type6(target_id, echo=True))
      print('type7=', cg.type7(target_id, target_id, echo=True))
      print('type9=', cg.type9(target_id, 0, echo=True))
      print('type17=', cg.type17(target_id, 0x7005, 'B', echo=True))
      print('type18=', cg.type18(target_id, 0x7005, 0, 'B', echo=True))
      print('type19=', cg.type19(target_id, echo=True))
      print('type22=', cg.type22(target_id, 1, echo=True))
      input('Press the Enter key.')
      '''

      print('stop motor:', cg.stop_motor(target_id))
      print('uid:', cg.get_uid(target_id))
      print('set home pos:', cg.set_home_pos(target_id))

      cg.dump(target_id, True)

      input('Press the Enter key.')

      print('MIT Ctrl mode')
      cg.set_runmode(target_id, 0)
      cg.set_item(target_id, 'limit_spd_2', 5.0)
      cg.set_item(target_id, 'limit_cur_2', 2.0)
      cg.start_motor(target_id)
      for p in tuple(range(32767, 65535, 1024)) + tuple(range(65535, 0, -1024)) + tuple(range(0, 32767, 1024)):
        cg.type1(target_id, 32767, p, 32767, 50, 100)
        t = time.time() + 500 / 1000.0
        while t > time.time():
          print(f'\r<{target_id}> pos:{p:>6d} {cg.get_items_as_str(target_id,("VBUS", "boardTemp", "iq", "mechPos", "mechVel", "rotation"))}\033[K', end='')
          a = cg.alarm
          if a != []:
            print(f'\n{a}')
          time.sleep(0.05)

      print('\nposition mode')
      cg.set_runmode(target_id, 1)
      cg.set_item(target_id, 'limit_spd_2', 20.0)
      cg.set_item(target_id, 'limit_cur_2', 2.0)
      cg.start_motor(target_id)
      for p in tuple(range(0, 100, 5)) + tuple(range(100, -100, -10)) + tuple(range(-100, 0, 5)):
        pos = p * 4 * math.pi / 100
        cg.set_item(target_id, 'loc_ref', pos)
        t = time.time() + 500 / 1000.0
        while t > time.time():
          print(f'\r<{target_id}> tpos:{pos:>6.2f} {cg.get_items_as_str(target_id,("VBUS", "boardTemp", "iq", "mechPos", "mechVel", "rotation"))}\033[K', end='')
          a = cg.alarm
          if a != []:
            print(f'\n{a}')
          time.sleep(0.05)

      print('\nspeed mode')
      cg.set_runmode(target_id, 2)
      cg.set_item(target_id, 'limit_cur_2', 2.0)
      cg.start_motor(target_id)
      for s in tuple(range(0, 30, 1)) + tuple(range(30, -30, -1)) + tuple(range(-30, 0, 1)):
        cg.set_item(target_id, 'spd_ref', s)
        t = time.time() + 500 / 1000.0
        while t > time.time():
          print(f'\r<{target_id}> tvel:{s:>6.2f} {cg.get_items_as_str(target_id,("VBUS", "boardTemp", "iq", "mechPos", "mechVel", "rotation"))}\033[K', end='')
          a = cg.alarm
          if a != []:
            print(f'\n{a}')
          time.sleep(0.05)

      print('\ncurrent mode')
      cg.set_runmode(target_id, 3)
      cg.start_motor(target_id)
      for c in tuple(range(0, 23, 1)) + tuple(range(23, -23, -1)) + tuple(range(-23, 0, 1)):
        cg.set_item(target_id, 'iq_ref', c)
        t = time.time() + 200 / 1000.0
        while t > time.time():
          print(f'\r<{target_id}> tcur:{c:>6.2f} {cg.get_items_as_str(target_id,("VBUS", "boardTemp", "iq", "mechPos", "mechVel", "rotation"))}\033[K', end='')
          a = cg.alarm
          if a != []:
            print(f'\n{a}')
          time.sleep(0.05)

    except KeyboardInterrupt:
      pass

    print()

    cg.stop_motor(target_id)

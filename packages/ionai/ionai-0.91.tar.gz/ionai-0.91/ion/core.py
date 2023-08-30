#
# [name] ion.core.py
#
# Written by Yoshikazu NAKAJIMA
#

import sys
import json
import pprint  # リストや辞書を整形して出力
import datetime
import copy
from typing import Union
from nkj.str import *
import nkj.time as nt

ANYSTR = '_ANY'

NULL_SLOT = NULLSTR

_DEFAULT_NAMESPACE = 'https://www.tmd.ac.jp/bmi/'
_DEFAULT_SLOT = None
_DEFAULT_STRSLOT = NULL_SLOT

#-- global variance

__NAMESPACE = _DEFAULT_NAMESPACE

#-- global functions

def namespace(s=None):
	global __NAMESPACE
	if (s is None):
		return __NAMESPACE
	elif (type(s) is str):
		__NAMESPACE = s
		return True
	else:
		return False

def is_anystr(s:str):
	return True if (s == ANYSTR) else False

def anystr(s:str):
	return is_anystr(s)

def nullslot(slot):
	if (slot is None):
		return True
	else:
		return nullstr(slot)

def not_nullslot(slot):
	return not nullstr(slot)

def is_nullslot(slot):
	return nullslot(slot)

def isnot_nullslot(slot):
	return not_nullslot(slot)

def dictslot_equalsto(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 == dictslot2)

def dictslot_included(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 <= dictslot2)

def dictslot_includes(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 >= dictslot2)

def semantics_equalsto(sem1, sem2):
	if (sem1 is None):
		return False
	if (sem2 is None):
		return False

def nullslot(slot):
	if (slot is None):
		True
	return nullstr(slot)

def not_nullslot(slot):
	return not nullstr(slot)

def is_nullslot(slot):
	return nullslot(slot)

def isnot_nullslot(slot):
	return not_nullslot(slot)

def dictslot_equalsto(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 == dictslot2)

def dictslot_included(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 <= dictslot2)

def dictslot_includes(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 >= dictslot2)

def semantics_equalsto(sem1, sem2):
	if (sem1 is None):
		return False
	if (sem2 is None):
		return False
	return (sem1 == sem2)

def semantics_included(sem1, sem2):
	if (sem1 is None):
		return False
	if (sem2 is None):
		return False
	return (sem1 <= sem2)

def semantics_includes(sem1, sem2):
	if (sem1 is None):
		return False
	if (sem2 is None):
		return False
	return (sem1 >= sem2)

#-- classes

class core:
	_classname = 'ion.core'

	def __init__(self):
		ldprint2('core.__init__()')

	@classmethod
	def getClassName(cls):
		return core._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

class strslot(core, str):
	_classname = 'ion.strslot'

	def __new__(cls, val:str=_DEFAULT_STRSLOT):
		ldprint2('__new__()')
		val = NULL_SLOT if (val is None) else val
		self = super().__new__(cls, val)
		return self

	def __init__(self, val=_DEFAULT_STRSLOT):
		ldprint2('__init__()')
		super(core, self).__init__()

	def __eq__(self, second):
		ldprint('--> strslot.__eq__()')
		ldprint2(second)
		if (type(second) == str):
			ldprint2('str: \'{}\''.format(second))
			ldprint('<-- strslot.__eq__()')
			return True if (is_anystr(self.str) or is_anystr(second)) else (self.str == second)
		else:
			ldprint2('str: \'{0}\' ({1})'.format(second, type(second)))
			ldprint('<-- strslot.__eq__()')
			return True if (is_anystr(self.str) or is_anystr(second.str)) else (self.str == second.str)

	# __ne__() は実装しなくても、__eq__() から自動で実装されるので定義しない．

	def __lt__(self, second):
		if (is_anystr(self.str)):  # 自身が any なら True を返す．
			return True
		t = type(second)

		if (t == tuple or t == list):  # second がリストなら、要素に含まれるか判定
			ldprint2('this: \'{}\''.format(self.str))
			ldprint2('list: {}'.format(second))
			if (type(second[0]) == str):
				return self.str in second
			else:
				flag = False
				for slot in second:
					if (self.str == slot.str):
						flag = True
						break
				return flag
		elif (t == str):  # second が文字列なら、文字列の一部に含まれるか判定
			if (is_anystr(second)):  # 相手が any なら True を返す
				return True
			else:
				return (self.str in second) and self.__ne__(second)
		else:
			if (is_anystr(second.str)):  # 相手が any なら True を返す
				return True
			else:
				return (self.str in second.str) and self.__ne__(second)

	def __le__(self, second):
		return (self.__lt__(second) or self.__eq__(second))

	def __gt__(self, second):
		if (is_anystr(self.str)):  # 自身が any なら True を返す．
			return True
		if (type(second) == str):
			return (second in self.str) and self.__ne__(second)
		else:
			return (second.str in self.str) and self.__ne__(second)

	def __ge__(self, second):
		return (self.__gt__(second) or self.__eq__(second))

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	"""
	___NOT_IMPLEMENTED
	def set(self, val):
		ldprint('--> set(\'{}\')'.format(val))
		self = strslot(val)
		ldprint('<-- set()')
	"""

	def get(self):  # null 文字のとき、None へ変換．
		if (is_nullstr(self)):
			return None
		else:
			return self

	@property
	def str(self) -> str:  # string クラスへ強制変換
		return str(self)

	def equalsto(self, second):
		return self.__eq__(second)

	def not_equalto(self, second):
		return self.equalsto(second)

	def included(self, second):
		return self.__le__(second)

	def not_included(self, second):
		return not self.included(second)

	def includes(self, second):
		return self.__ge__(second)

	def not_includes(self, second):
		return not self.includes(second)

	def startswith(self, second):
		if (is_anystr(self.str)):
			return True
		if (type(second) == str):
			if (is_anystr(second)):
				return True
			return self.str.startswith(second)
		else:
			if (is_anystr(second.str)):
				return True
			return self.str.startswith(second.str)

	def endswith(self, second):
		if (is_anystr(self.str)):
			return True
		if (type(second) == str):
			if (is_anystr(second)):
				return True
			return self.str.endswith(second)
		else:
			if (is_anystr(second.str)):
				return True
			return self.str.endswith(second.str)

	def startsfor(self, second):
		if (is_anystr(self.str)):
			return True
		if (type(second) == str):
			if (is_anystr(second)):
				return True
			return second.startswith(self.str)
		else:
			if (is_anystr(second.str)):
				return True
			return second.str.startswith(self.str)

	def starts(self, second):
		return self.startsfor(second)

	def ends(self, second):
		if (is_anystr(self.str)):
			return True
		if (type(second) == str):
			if (is_anystr(second)):
				return True
			return second.endswith(self.str)
		else:
			if (is_anystr(second.str)):
				return True
			return second.str.endswith(self.str)

	def endsfor(self, second):
		return self.ends(second)

	def getPrintString(self, title=None):
		s = self.str
		return s

	@property
	def printstr(self):
		return self.getPrintString()

class slot(strslot):
	_classname = 'ion.slot'

	def __new__(cls, val=_DEFAULT_SLOT):
		return super().__new__(cls, val)

	def __init__(self, val=_DEFAULT_SLOT):
		super().__init__(val)

	@classmethod
	def getClassName(cls):
		return cls._classname

	def get(self):  # null 文字のとき、None へ変換．int および float のとき、それぞれ int、float へ変換．
		s = self
		if (s == ''):
			return None
		elif (is_intstr(s)):
			return int(s)
		elif (is_floatstr(s)):
			return float(s)
		else:
			return self

_KEY_UNKNOWN = 'unknown'
_KEY_FILENAME = 'filename'

class dictslot(core, dict):
	_classname = 'ion.dictslot'

	def __init__(self, val:Union[dict, tuple, list, str, None]=None):
		ldprint('--> dictslot.__init__()')
		ldprint0('val: \'{0}\' ({1})'.format(val, type(val)))
		dict.__init__(self)
		if (type(val) == dictslot or type(val) == sislot or type(val) == tislot or type(val) == dictslot):
			val = dict(val)
		d = todict(val)
		for key, value in d.items():
			self.__setitem__(key, value)
		ldprint('<-- dictslot.__init__()')

	# 一致性は、両方の辞書に共通する keys に対して、それらの values が全一致したとき（ただし、any 一致は認める）に一致とみなす
	# 片方のリストにある key がもう一方のリストにない時には、ない方のリスト要素を any とみなす = すなわち、「指定なし」＝any として、その key については一致とみなす

	def __eq__(self, second:Union[dict, str, None]):
		if (second is None):  # second が None なら True
			return True
		if (type(second) == str):
			second = json.loads(second)  # str -> dict
		if (is_nulldict(self) or is_nulldict(second)):  # どちらかの辞書に要素がなければ True
			return True
		"""
		anditems = [(key, value) for key, value in self.items() if (slot(value) == slot(second.get(key)))]  # value を slot として一致性比較 = any 一致を認める
		print(anditems)
		"""
		mismatchitems = [(key, value, second.get(key)) for key, value in self.items() if (slot(value) != slot(second.get(key)))]  # value を slot として一致性比較 = any 一致を認める
		if (is_nulllist(mismatchitems)):
			return True
		else:
			return False

	def __lt__(self, second:Union[dict, str, None]):
		if (second is None):
			return False
		if (type(second) == str):
			second = json.loads(second)  # str -> dict
		if (is_nulldict(self) or is_nulldict(second)):  # どちらかの辞書に要素がなければ False
			return False
		mismatchitems = [(key, value, second.get(key)) for key, value in self.items() if (slot(value) < slot(second.get(key)))]  # value を slot として被包含性比較 = any 包含を認める
		if (is_nulllist(mismatchitems)):
			return False
		else:
			return True

	def __le__(self, second:Union[dict, str, None]):
		return (self.__lt__(second) or self.__eq__(second))

	def __gt__(self, second:Union[dict, str, None]):
		if (second is None):
			return False
		if (type(second) == str):
			second = json.loads(second)  # str -> dict
		if (is_nulldict(self) or is_nulldict(second)):  # どちらかの辞書に要素がなければ False
			return False
		mismatchitems = [(key, value, second.get(key)) for key, value in self.items() if (slot(value) > slot(second.get(key)))]  # value を slot として被包含性比較 = any 包含を認める
		if (is_nulllist(mismatchitems)):
			return False
		else:
			return True

	def __ge__(self, second:Union[dict, str, None]):
		return (self.__gt__(second) or self.__eq__(second))

	@classmethod
	def getClassName(cls):
		return dictslot._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def equalsto(self, second):
		return self.__eq__(second)

	def not_equalto(self, second):
		return self.equalsto(second)

	def included(self, second):
		return self.__le__(second)

	def not_included(self, second):
		return not self.included(second)

	def includes(self, second):
		return self.__ge__(second)

	def not_includes(self, second):
		return not self.includes(second)

	def getPrintString(self, title=None):
		s = ''
		if (title is not None):
			s += '--- {} ---\n'.format(title)
		s += json.dumps(self)  # dict -> str
		if (title is not None):
			s += '\n---'
		return s

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.getPrintString()

	def print(self, title=None):
		if (title is not None):
			print('--- {} ---'.format(title))
		pprint.pprint(self.printstr)
		if (title is not None):
			print('---', flush=True)
		else:
			sys.stdout.flush()

	# json.{loads(), dumps()}: dict データと string データの変換
	# json.{load(), dump()}:   JSON ファイルの読み書き

	def load(self, filename=None):
		filename = self.getFilename() if (filename is None) else filename
		if (filename is None):
			return False
		with open(filename) as f:
			self = json.load(f)

	def save(self, filename=None):
		filename = self.getFilename() if (filename is None) else filename
		if (filename is None):
			return False
		with open(filename, 'wt') as f:  # テキストモードで書き出し
			json.dump(self, f)

_KEY_TIME = 'time'
_KEY_TIMEPERIOD = 'time_period'
_TIMEDESCRIPTION = '%Y-%m-%d %H:%M:%S.%f'

def key_time():
	return _KEY_TIME

def key_timeperiod():
	return _KEY_TIMEPERIOD

class sislot(dictslot):  # spatial identifier
	_classname = 'ion.sislot'

	def __init__(self, val:Union[dict, tuple, list, str, None]=None):
		super().__init__(val)

	@classmethod
	def getClassName(cls):
		return dictslot._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

class tislot(dictslot):  # temporal identifier
	_classname = 'ion.tislot'

	def __init__(self, val:Union[dict, tuple, list, str, None]=None):
		super().__init__(val)
		if (self.time is None):
			self.update_time()

	"""
	def __lt__(self, second:sislot):  # 記号の意味としては、本来は等価を含まないが、実装の都合上、ここでは含むものとする
		return self.__le__(second)
	"""

	def __le__(self, second:sislot):
		return self.included(second)

	"""
	def __gt__(self, second:sislot):  # 記号の意味としては、本来は等価を含まないが、実装の都合上、ここでは含むものとする
		return self.__ge__(second)
	"""

	def __ge__(self, second:sislot):
		return self.includes(second)

	@classmethod
	def getClassName(cls):
		return dictslot._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def time(self):
		return self.get(_KEY_TIME)

	@time.setter
	def time(self, t):
		if (t is None):
			del self[_KEY_TIME]
		else:
			self[_KEY_TIME] = t

	@property
	def timeperiod(self):
		return self.get(_KEY_TIMEPERIOD)

	@timeperiod.setter
	def timeperiod(self, tp):
		ldprint0('--> timeperiod.setter(\'{}\')'.format(tp))
		if (tp is None):
			del self[_KEY_TIMEPERIOD]
		else:
			self[_KEY_TIMEPERIOD] = tp

	def update_time(self):
		self.time = datetime.datetime.now().strftime(_TIMEDESCRIPTION)  # python datetime のデフォルト書式で記述

	def clear_timeperiod(self):
		self.timeperiod = None

	def included(self, second:sislot):
		if (self.time is None or second.time is None):  # 記述がないときは any とみなして True
			return True
		if (is_anystr(self.time) or is_anystr(second.time)):  # どちらかが any のときは True. any は基本的には記述なしで対応するのでできるだけ使用しないこと．
			return True
		return (self == second) or (nt.time(self.time, self.timeperiod) <= nt.time(second.time, second.timeperiod))

	def includes(self, second:sislot):
		if (self.time is None or second.time is None):  # 記述がないときは any とみなして True
			return True
		if (is_anystr(self.time) or is_anystr(second.time)):  # どちらかが any のときは True. any は基本的には記述なしで対応するのでできるだけ使用しないこと．
			return True
		return (self == second) or (nt.time(self.time, self.timeperiod) >= nt.time(second.time, second.timeperiod))

class optslot(dictslot):  # optional identifier
	pass

_KEY_DATAFORMAT = 'format'
_KEY_DATAUNIT = 'unit'

def key_format():
	return _KEY_DATAFORMAT

def key_unit():
	return _KEY_DATAUNIT

class datapropslot(dictslot):  # data properties
	_classname = 'ion.datapropslot'

	def __init__(self, val:Union[dict, str, None]=None):
		super().__init__(val)

	@classmethod
	def getClassName(cls):
		return dictslot._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def format(self):
		return self.get(_KEY_DATAFORMAT)

	@format.setter
	def format(self, f):
		if (f is None):
			del self[_KEY_DATAFORMAT]
		self[_KEY_DATAFORMAT] = f

	@property
	def unit(self):
		return self.get(_KEY_DATAUNIT)

	@unit.setter
	def unit(self, u):
		if (u is None):
			del self[_KEY_DATAUNIT]
		self[_KEY_DATAUNIT] = u

class databody(core):
	_classname = 'ion.databody'

	def __init__(self, val):
		self._data = None

	@classmethod
	def getClassName(cls):
		return databody._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def get(self):
		return self._data

	def set(self, d):
		if (type(d) is str):
			if (d == NULLSTR):
				d = None
		self._data = d

	@property
	def data(self):
		return self.get()

	@data.setter
	def data(self, d):
		self.set(d)

class entity(slot):
	pass

class baseentity(slot):
	pass

class role(slot):
	pass

class spatial(sislot):
	pass

class si(sislot):
	pass

class temporal(tislot):
	pass

class ti(tislot):
	pass

class optional(optslot):
	pass

class opt(optslot):
	pass

class oi(optslot):
	pass

class semantics():
	_classname = 'ion.semantics'

	def __init__(self, entity=None, baseentity=None, role=None, si=None, ti=None, opt=None, namespace=None):
		ldprint('--> semantics.__init__(\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\')'.format(entity, baseentity, role, si, ti, opt, namespace))
		self.setNameSpace(namespace)
		ldprint('namespace:   \'{}\''.format(self.namespace))
		ldprint('entity:      \'{}\''.format(entity))
		ldprint('base entity: \'{}\''.format(baseentity))
		ldprint('role:        \'{}\''.format(role))
		ldprint('si:          \'{}\''.format(si))
		ldprint('ti:          \'{}\''.format(ti))
		ldprint('options:     \'{}\''.format(opt))
		self._entity = slot(entity)       # entity
		self._bentity = slot(baseentity)  # base entity (optional)
		self._role = slot(role)           # role
		self._si = sislot(si)             # spatial identifier
		self._ti = tislot(ti)             # temporal identifier
		self._optional = dictslot(opt)    # optional properties
		ldprint('<-- semantics.__init__()')

	def __str__(self, second):
		return self.getPrintString()

	def __eq__(self, second):
		r = True
		r &= (self.entity == second.entity)
		r &= (self.baseentity == second.baseentity)
		r &= (self.role == second.role)
		if (any(self.si)):
			r &= (self.si == second.si)
		if (any(self.ti)):
			r &= (self.ti == second.ti)
		if (any(self.optional)):
			r &= (self.optional == second.optional)
		return r

	def __lt__(self, second):
		return (self.__lt__(second) and not self.__eq__(second))

	def __le__(self, second):
		r = True
		r &= (self.entity <= second.entity)
		r &= (self.baseentity <= second.baseentity)
		r &= (self.role <= second.role)
		if (any(self.si)):
			r &= (self.si <= second.si)
		if (any(self.ti)):
			r &= (self.ti <= second.ti)
		if (any(self.optional)):
			r &= (self.optional <= second.optional)
		return r

	def __gt__(self, second):
		return (self.__gt__(second) and not self.__eq__(second))

	def __ge__(self, second):
		r = True
		r &= (self.entity >= second.entity)
		r &= (self.baseentity >= second.baseentity)
		r &= (self.role >= second.role)
		if (any(self.si)):
			r &= (self.si >= second.si)
		if (any(self.ti)):
			r &= (self.ti >= second.ti)
		if (any(self.optional)):
			r &= (self.optional >= second.optional)
		return r

	@classmethod
	def getClassName(cls):
		return semantics._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def getNameSpace(self):
		if (self._namespace is not None):
			return self._namespace
		else:
			return namespace()  # call global function

	def setNameSpace(self, ns):
		self._namespace = ns

	@property
	def namespace(self):
		return self.getNameSpace()

	@namespace.setter
	def namespace(self, ns):
		self.setNameSpace(ns)

	@property
	def ns(self):
		return self.namespace

	@ns.setter
	def ns(self, ns_):
		self.namespace = ns_

	@property
	def entity(self):
		return self._entity

	@entity.setter
	def entity(self, val:Union[str, None]):
		self._entity = entity(val)

	@property
	def e(self):
		return self.entity

	@e.setter
	def e(self, val:Union[str, None]):
		self.entity = val

	@property
	def baseentity(self):
		return self._bentity

	@baseentity.setter
	def baseentity(self, val:Union[str, None]):
		self._bentity = baseentity(val)

	@property
	def bentity(self):
		return self.baseentity

	@bentity.setter
	def bentity(self, val:Union[str, None]):
		self.baseentity = val

	@property
	def be(self):
		return self.baseentity

	@be.setter
	def be(self, val:Union[str, None]):
		self.baseentity = val

	@property
	def role(self):
		return self._role

	@role.setter
	def role(self, val:Union[str, None]):
		self._role = role(val)

	@property
	def r(self):
		return self.role

	@r.setter
	def r(self, val:Union[str, None]):
		self.role = val

	@property
	def spatialidentifier(self):
		return self.si

	@spatialidentifier.setter
	def spatialidentifier(self, si):
		self.si = si

	@property
	def si(self):
		#return self._si if (any(self._si)) else None
		return self._si

	@si.setter
	def si(self, si_):
		self._si = si(si_)

	@property
	def s(self):
		return self.si

	@s.setter
	def s(self, si):
		self.si = s

	@property
	def temporalidentifier(self):
		return self.ti

	@temporalidentifier.setter
	def temporalidentifier(self, ti):
		self.ti = ti

	@property
	def ti(self):
		#return self._ti if (any(self._ti)) else None
		return self._ti

	@ti.setter
	def ti(self, ti_):
		self._ti = ti(ti_)

	@property
	def t(self):
		return self.ti

	@t.setter
	def t(self, t):
		self.ti = t

	@property
	def optionalidentifier(self):
		return self.optional

	@optionalidentifier.setter
	def optionalidentifier(self, o):
		self.optional = o

	@property
	def oi(self):
		return self.optional

	@oi.setter
	def oi(self, o):
		self.optional = o

	@property
	def optional(self):
		#return self._optional if (any(self._optional)) else None
		return self._optional

	@optional.setter
	def optional(self, o):
		self._optional = optional(o)

	@property
	def opt(self):
		return self.optional

	@opt.setter
	def opt(self, o):
		self.optional = o

	@property
	def o(self):
		return self.optional

	@o.setter
	def o(self, o_):
		self.optional = o_

	def equalsto(self, second):
		return self.__eq__(second)

	def not_equalto(self, second):
		return self.equalsto(second)

	def included(self, second):
		return self.__le__(second)

	def not_included(self, second):
		return not self.included(second)

	def includes(self, second):
		return self.__ge__(second)

	def not_includes(self, second):
		return not self.includes(second)

	def getPrintString(self, title=None):
		s = ''
		if (title is not None):
			s += '--- {} ---\n'.format(title)
		s += 'entity:      \'{}\'\n'.format(self.entity)
		s += 'base entity: \'{}\'\n'.format(self.baseentity)
		s += 'role:        \'{}\'\n'.format(self.role)
		if (any(self.si)):
			s += 'si:          '
			s += self.si.getPrintString()
			s += '\n'
		if (any(self.ti)):
			s += 'ti:          '
			s += self.ti.getPrintString()
			s += '\n'
		if (any(self.optional)):
			s += 'optional:    '
			s += self.optional.getPrintString()
			s += '\n'
		if (title is not None):
			s += '---'
		return s

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.getPrintString()

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

class data_property(datapropslot):
	pass

class dataproperty(data_property):
	pass

class data_storage(core):  # The class name of 'data' is prohibited and might be used in python system.
	_classname = 'ion.data'

	def __init__(self, body=None, property=None, namespace=None):
		ldprint('--> data.__init__(, \'{0}\', \'{1}\')'.format(property, namespace))
		self.setNameSpace(namespace)
		ldprint('namespace:   \'{}\''.format(self.namespace))
		super().__init__()
		self._body = databody(body)
		self._property = datapropslot(property)
		ldprint('<-- data.__init__()')

	@classmethod
	def getClassName(cls):
		return data_storage._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def getNameSpace(self):
		if (self._namespace is not None):
			return self._namespace
		else:
			return namespace()  # call global function

	def setNameSpace(self, ns):
		self._namespace = ns

	@property
	def namespace(self):
		return self.getNameSpace()

	@namespace.setter
	def namespace(self, ns):
		self.setNameSpace(ns)

	@property
	def ns(self):
		return self.namespace

	@ns.setter
	def ns(self, ns_):
		self.namespace = ns_

	@property
	def databody(self):
		return self._body.get()

	@databody.setter
	def databody(self, d):
		self._body.set(d)

	@property
	def dbody(self):
		return self.databody

	@dbody.setter
	def dbody(self, d):
		self.databody = d

	@property
	def db(self):
		return self.databody

	@db.setter
	def db(self, d):
		self.databody = d

	@property
	def body(self):
		return self.databody

	@body.setter
	def body(self, d):
		self.databody = d

	@property
	def b(self):
		return self.databody

	@b.setter
	def b(self, d):
		self.databody = d

	@property
	def dataproperty(self):
		return self._property

	@dataproperty.setter
	def dataproperty(self, p):
		self._property = p

	@property
	def dproperty(self):
		return self.dataproperty

	@dproperty.setter
	def dproperty(self, p):
		self.dataproperty = p

	@property
	def dp(self):
		return self._property

	@dp.setter
	def dp(self, p):
		self.dataproperty = p

	# 'property' is not available for the name of 'class property' in python

	@property
	def p(self):
		return self._property

	@p.setter
	def p(self, p_):
		self.dataproperty = p_

	@property
	def dataformat(self):
		return self.dataproperty.format

	@dataformat.setter
	def dataformat(self, f):
		self.dataproperty.format = f

	@property
	def format(self):
		return self.dataformat

	@format.setter
	def format(self, f):
		self.dataformat = f

	@property
	def f(self):
		return self.dataformat

	@f.setter
	def f(self, f):
		self.dataformat = f

	@property
	def df(self):
		return self.dataformat

	@df.setter
	def df(self, f):
		self.dataformat = f

	@property
	def dataunit(self):
		return self.dataproperty.unit

	@dataunit.setter
	def dataunit(self, u):
		self.dataproperty.unit = u

	@property
	def unit(self):
		return self.dataunit

	@unit.setter
	def unit(self, u):
		self.dataunit = u

	@property
	def u(self):
		return self.dataunit

	@u.setter
	def u(self, u):
		self.dataunit = u

	@property
	def du(self):
		return self.dataunit

	@du.setter
	def du(self, u):
		self.dataunit = u

	def getPrintString(self, title=None):
		s = ''
		if (title is not None):
			s += '--- {} ---\n'.format(title)
		s += 'data body:     '
		if (self.databody is None):
			s += 'None\n'
		else:
			s += '{} bytes'.format(self.databody.__sizeof__())
			if (type(self.databody) == str):
				s += ' (\'{0}\', {1} characters)'.format(self.databody, len(self.databody))
			s += '\n'
		s += 'data property: '
		s += self.dataproperty.getPrintString()
		if (title is not None):
			s += '\n---'
		return s

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.getPrintString()

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

class datastorage(data_storage):  # alias
	pass

class query():
	_classname = 'ion.query'

	def __init__(self, semantics=None, dataproperty=None):
		ldprint('--> query.__init__()')
		ldprint('semantics:     {}'.format(semantics))
		ldprint('data property: {}'.format(dataproperty))
		self.setQuery((semantics, dataproperty))
		if (lib_debuglevel() > 0):
			semantics.print('semantics')
			dataproperty.print('data properties')
		ldprint('<-- query.__init__()')

	def getQuery(self):
		return (self.getSemantics(), self.getDataProperty())  # tuple

	def setQuery(self, q):
		if (type(q) == tuple or type(q) == list):
			self.setSemantics(q[0])
			self.setDataProperty(q[1])
		else:
			__ERROR__

	def __eq__(self, second):
		r = True
		r &= (self.semantics == second.semantics)
		r &= (self.dataproperty == second.dataproperty)
		return r

	def __lt__(self, second):
		return (self.__lt__(second) and not self.__eq__(second))

	def __le__(self, second):
		r = True
		r &= (self.semantics <= second.semantics)
		r &= (self.dataproperty <= second.dataproperty)
		return r

	def __gt__(self, second):
		return (self.__gt__(second) and not self.__eq__(second))

	def __ge__(self, second):
		r = True
		r &= (self.semantics >= second.semantics)
		r &= (self.dataproperty >= second.dataproperty)
		return r

	@property
	def query(self):
		return self.getQuery()

	@query.setter
	def query(self, q):
		self.setQuery(q)

	@property
	def q(self):
		return self.guery

	@q.setter
	def q(self, q):
		self.query = q

	def getSemantics(self):
		return self._semantics

	def setSemantics(self, sem):
		self._semantics = semantics() if (sem is None) else sem.copy()

	@property
	def semantics(self):
		return self.getSemantics()

	@semantics.setter
	def semantics(self, sem):
		self.setSemantics(sem)

	@property
	def sem(self):
		return self.semantics

	@sem.setter
	def sem(self, sem_):
		self.semantics = sem_

	@property
	def s(self):
		return self.semantics

	@s.setter
	def s(self, sem_):
		self.semantics = sem_

	def getDataProperty(self):
		return self._dataprop

	def setDataProperty(self, dp):
		self._dataprop = data_property() if (dp is None) else dp

	@property
	def dataproperty(self):
		return self.getDataProperty()

	@dataproperty.setter
	def dataproperty(self, dp):
		self.setDataProperty(dp)

	@property
	def data_property(self):
		return self.dataproperty

	@data_property.setter
	def data_property(self, dp):
		self.dataproperty = dp

	@property
	def dp(self):
		return self.dataproperty

	@dp.setter
	def dp(self, dp):
		self.dataproperty = dp

	def equalsto(self, second):
		return self.__eq__(second)

	def not_equalto(self, second):
		return self.equalsto(second)

	def included(self, second):
		return self.__le__(second)

	def not_included(self, second):
		return not self.included(second)

	def includes(self, second):
		return self.__ge__(second)

	def not_includes(self, second):
		return not self.includes(second)

	@property
	def entity(self):
		return self.semantics.entity

	@entity.setter
	def entity(self, e):
		self.semantics.entity = e

	@property
	def e(self):
		return self.entity

	@e.setter
	def e(self, e_):
		self.entity = e_

	@property
	def baseentity(self):
		return self.semantics.baseentity

	@baseentity.setter
	def baseentity(self, be):
		self.semantics.baseentity = be

	@property
	def be(self):
		return self.baseentity

	@be.setter
	def be(self, be_):
		self.baseentity = be_

	@property
	def role(self):
		return self.semantics.role

	@role.setter
	def role(self, r):
		self.semantics.role = r

	@property
	def r(self):
		return self.role

	@r.setter
	def r(self, r_):
		self.role = r_

	@property
	def si(self):
		return self.semantics.si

	@si.setter
	def si(self, si_):
		self.semantics.si = si_

	@property
	def ti(self):
		return self.semantics.ti

	@ti.setter
	def ti(self, ti_):
		self.semantics.ti = ti_

	@property
	def optional(self):
		return self.semantics.optional

	@optional.setter
	def optional(self, o):
		self.semantics.optional = o

	@property
	def opt(self):
		return self.optional

	@opt.setter
	def opt(self, o):
		self.optional = o

	@property
	def o(self):
		return self.optional

	@o.setter
	def o(self, o_):
		self.optional = o_

	@property
	def dataformat(self):
		return self.dataproperty.format

	@dataformat.setter
	def dataformat(self, f):
		self.dataproperty.format = f

	@property
	def format(self):
		return self.dataformat

	@format.setter
	def format(self, f):
		self.dataformat = f

	@property
	def f(self):
		return self.dataformat

	@f.setter
	def f(self, f):
		self.dataformat = f

	@property
	def df(self):
		return self.dataformat

	@df.setter
	def df(self, f):
		self.dataformat = f

	@property
	def dataunit(self):
		return self.dataproperty.unit

	@dataunit.setter
	def dataunit(self, u):
		self.dataproperty.unit = u

	@property
	def unit(self):
		return self.dataunit

	@unit.setter
	def unit(self, u):
		self.dataunit = u

	@property
	def u(self):
		return self.dataunit

	@u.setter
	def u(self, u):
		self.dataunit = u

	@property
	def du(self):
		return self.dataunit

	@du.setter
	def du(self, u):
		self.dataunit = u

	def getPrintString(self, title=None):
		s = ''
		if (title is not None):
			s += '--- {} ---\n'.format(title)
		s += '- semantics\n'
		s += self.semantics.getPrintString()
		s += '- data property\n'
		s += self.dataproperty.getPrintString()
		if (title is not None):
			s += '\n---'
		return s

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.getPrintString()

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

class ion(core):
	_classname = 'ion.ion'

	def __init__(self):
		self._semantics = semantics()
		self._data = data_storage()

	@classmethod
	def getClassName(cls):
		return ion._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def namespace(self):
		return namespace()  # call global function

	@namespace.setter
	def namespace(self, ns):
		namespace(ns)  # call global function

	@property
	def ns(self):
		return self.namespace

	@ns.setter
	def ns(self, ns_):
		self.namespace = ns_

	@property
	def semantics(self):
		return self._semantics

	@semantics.setter
	def semantics(self, s):
		self._semantics = s

	@property
	def s(self):
		return self.semantics

	@s.setter
	def s(self, s_):
		self.semantics = s_

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self, d):
		self._data = d

	@property
	def d(self):
		return self._data

	@d.setter
	def d(self, d_):
		self._data = d_

	@property
	def entity(self):
		return self.s.entity

	@entity.setter
	def entity(self, e):
		self.s.entity = e

	@property
	def e(self):
		return self.entity

	@e.setter
	def e(self, e_):
		self.entity = e_

	@property
	def baseentity(self):
		return self.s.baseentity

	@baseentity.setter
	def baseentity(self, be):
		self.s.baseentity = be

	@property
	def bentity(self):
		return self.baseentity

	@bentity.setter
	def bentity(self, be):
		self.baseentity = be

	@property
	def be(self):
		return self.baseentity

	@be.setter
	def be(self, be_):
		self.baseentity = be_

	@property
	def role(self):
		return self.s.role

	@role.setter
	def role(self, r):
		self.s.role = r

	@property
	def r(self):
		return self.role

	@r.setter
	def r(self, r_):
		self.role = r_

	@property
	def spatialidentifier(self):
		return self.s.spatialidentifier

	@spatialidentifier.setter
	def spatialidentifier(self, si):
		self.s.spatialidentifier = si

	@property
	def si(self):
		return self.spatialidentifier

	@si.setter
	def si(self, si_):
		self.spatialidentifier = si_

	@property
	def temporalidentifier(self):
		return self.s.temporalidentifier

	@temporalidentifier.setter
	def temporalidentifier(self, ti):
		self.s.temporalidentifier = ti

	@property
	def ti(self):
		return self.temporalidentifier

	@ti.setter
	def ti(self, ti_):
		self.temporalidentifier = ti_

	@property
	def optional(self):
		return self.s.optional

	@optional.setter
	def optional(self, o):
		self.s.optional = o

	@property
	def opt(self):
		return self.optional

	@opt.setter
	def opt(self, o):
		self.optional = o

	@property
	def o(self):
		return self.optional

	@o.setter
	def o(self, o_):
		self.optional = o_

	@property
	def databody(self):
		return self.d.databody

	@databody.setter
	def databody(self, db):
		self.d.databody = db

	@property
	def dbody(self):
		return self.databody

	@dbody.setter
	def dbody(self, db):
		self.databody = db

	@property
	def db(self):
		return self.databody

	@db.setter
	def db(self, db_):
		self.databody = db_

	@property
	def dataproperty(self):
		return self.d.dataproperty

	@dataproperty.setter
	def dataproperty(self, dp):
		self.d.dataproperty = dp

	@property
	def dproperty(self):
		return self.dataproperty

	@dproperty.setter
	def dproperty(self, dp):
		self.dataproperty = dp

	@property
	def dp(self):
		return self.dataproperty

	@dp.setter
	def dp(self, dp_):
		self.dataproperty = dp_

	@property
	def dataformat(self):
		return self.dataproperty.format

	@dataformat.setter
	def dataformat(self, f):
		self.dataproperty.format = f

	@property
	def format(self):
		return self.dataformat

	@format.setter
	def format(self, f):
		self.dataformat = f

	@property
	def f(self):
		return self.dataformat

	@f.setter
	def f(self, f):
		self.dataformat = f

	@property
	def df(self):
		return self.dataformat

	@df.setter
	def df(self, f):
		self.dataformat = f

	@property
	def dataunit(self):
		return self.dataproperty.unit

	@dataunit.setter
	def dataunit(self, u):
		self.dataproperty.unit = u

	@property
	def unit(self):
		return self.dataunit

	@unit.setter
	def unit(self, u):
		self.dataunit = u

	@property
	def u(self):
		return self.dataunit

	@u.setter
	def u(self, u):
		self.dataunit = u

	@property
	def du(self):
		return self.dataunit

	@du.setter
	def du(self, u):
		self.dataunit = u

	def getQuery(self):
		return query((self.semantics, self.dataproperty))

	def setQuery(self, q):
		self.semantics = q.semantics
		self.dataproperty = q.dataproperty

	@property
	def query(self):
		return self.getQuery()

	@query.setter
	def query(self, q):
		self.setQuery(q)

	@property
	def q(self):
		return self.query

	@q.setter
	def q(self, q_):
		self.query = q_

#-- main

if (__name__ == '__main__'):
	_DEBUGLEVEL = 1
	lib_debuglevel(_DEBUGLEVEL)
	debuglevel(_DEBUGLEVEL)

	# namespace

	if (True):
		print('\n-- NAMESPACE --')
		dprint('namespace: \'{}\''.format(namespace()))
		namespace('test_namespace')
		dprint('namespace: \'{}\''.format(namespace()))

	# test for slot class

	if (False):
		print('\n-- SLOT CLASS --')
		sl = slot()
		dprint('classname: \'{}\''.format(sl.getClassName()))
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		print('\n--')
		sl = slot('test')
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		print('\n--')
		sl = slot('-30')
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		print('\n--')
		sl = slot('-3.14')
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		print('\n--')
		sl = slot('-3.14e+3')
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		if (False):  # ___NOT_IMPLEMENTED
			print('\n-- test')
			sl.set('2.71828')
			dprint('classname: \'{}\''.format(sl.classname))
			dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
			dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
			dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

	# test for semantics class

	if (True):
		print('\n-- SEMANTICS CLASS --')
		sem = semantics('test_ent_', None, None)
		dprint('classname: \'{}\''.format(sem.classname))
		sem.print('semantics')

		print('\n--')
		dprint('namespace: \'{}\''.format(sem.namespace))
		sem.namespace = 'test_namespace2'
		dprint('namespace: \'{}\''.format(sem.namespace))
		sem.ns = 'test_namespace3'
		dprint('namespace: \'{}\''.format(sem.ns))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.entity.classname))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity, type(sem.entity)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.str, type(sem.entity.str)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.get(), type(sem.entity.get())))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.entity.classname))
		sem.entity = slot('test_ent')  # 代入時は必ず slot 形式にキャストしてから代入すること．直接、string データを代入すると、sem.entity が string 型になってしまう。
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity, type(sem.entity)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.str, type(sem.entity.str)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.get(), type(sem.entity.get())))
		if (True):
			dprint('Is equal to \'{0}\': {1}'.format('test_entXXX', sem.entity == 'test_ent/XXX'))
			dprint('Is equal to \'{0}\': {1}'.format('test_ent', sem.entity == 'test_ent'))
			dprint('Is equal to \'{0}\': {1}'.format('test_e', sem.entity == 'test_e'))
			dprint('Is equal to \'{0}\': {1}'.format('dummy', sem.entity == 'dummy'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_ent/XXX', sem.entity != 'test_ent/XXX'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_ent', sem.entity != 'test_ent'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_e', sem.entity != 'test_e'))
			dprint('Is not equal to \'{0}\': {1}'.format('dummy', sem.entity != 'dummy'))
			dprint('Is included in \'{0}\': {1}'.format('test_ent/XXX', sem.entity < 'test_ent/XXX'))
			dprint('Is included in \'{0}\': {1}'.format('test_ent', sem.entity < 'test_ent'))
			dprint('Is included in \'{0}\': {1}'.format('test_e', sem.entity < 'test_e'))
			dprint('Is included in \'{0}\': {1}'.format('dummy', sem.entity < 'dummy'))
			dprint('Is included in \'{0}\': {1}'.format(['dummy'], sem.entity < ['dummy']))
			dprint('Is included in \'{0}\': {1}'.format('[\'test_ent\', \'dummy\']', sem.entity < ['test_ent', 'dummy']))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_ent/XXX', sem.entity <= 'test_ent/XXX'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_ent', sem.entity <= 'test_ent'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_e', sem.entity <= 'test_e'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('dummy', sem.entity <= 'dummy'))
			dprint('Does include \'{0}\': {1}'.format('test_ent/XXX', sem.entity > 'test_ent/XXX'))
			dprint('Does include \'{0}\': {1}'.format('test_ent', sem.entity > 'test_ent'))
			dprint('Does include \'{0}\': {1}'.format('test_e', sem.entity > 'test_e'))
			dprint('Does include \'{0}\': {1}'.format('dummy', sem.entity > 'dummy'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_ent/XXX', sem.entity >= 'test_ent/XXX'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_ent', sem.entity >= 'test_ent'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_e', sem.entity >= 'test_e'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('dummy', sem.entity >= 'dummy'))
			dprint('Does start with \'{0}\': {1}'.format('test_ent/XXX', sem.entity.startswith('test_ent/XXX')))
			dprint('Does start with \'{0}\': {1}'.format('test_ent', sem.entity.startswith('test_ent')))
			dprint('Does start with \'{0}\': {1}'.format('test_e', sem.entity.startswith('test_e')))
			dprint('Does start with \'{0}\': {1}'.format('dummy', sem.entity.startswith('dummy')))
			dprint('Does start for \'{0}\': {1}'.format('test_ent/XXX', sem.entity.starts('test_ent/XXX')))
			dprint('Does start for \'{0}\': {1}'.format('test_ent', sem.entity.starts('test_ent')))
			dprint('Does start for \'{0}\': {1}'.format('test_e', sem.entity.starts('test_e')))
			dprint('Does start for \'{0}\': {1}'.format('dummy', sem.entity.starts('dummy')))
			dprint('Does end with \'{0}\': {1}'.format('XXX/test_ent', sem.entity.endswith('XXX/test_ent')))
			dprint('Does end with \'{0}\': {1}'.format('test_ent', sem.entity.endswith('test_ent')))
			dprint('Does end with \'{0}\': {1}'.format('test_e', sem.entity.endswith('test_e')))
			dprint('Does end with \'{0}\': {1}'.format('dummy', sem.entity.endswith('dummy')))
			dprint('Does end \'{0}\': {1}'.format('XXX/test_ent', sem.entity.ends('XXX/test_ent')))
			dprint('Does end \'{0}\': {1}'.format('test_ent', sem.entity.ends('test_ent')))
			dprint('Does end \'{0}\': {1}'.format('test_e', sem.entity.ends('test_e')))
			dprint('Does end \'{0}\': {1}'.format('dummy', sem.entity.ends('dummy')))

		print('\n--')
		sem.entity = slot(ANYSTR)  # 代入時は必ず slot 形式にキャストしてから代入すること．直接、string データを代入すると、sem.entity が string 型になってしまう。
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity, type(sem.entity)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.str, type(sem.entity.str)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.get(), type(sem.entity.get())))
		if (True):
			dprint('Is equal to \'{0}\': {1}'.format('test_entXXX', sem.entity == 'test_ent/XXX'))
			dprint('Is equal to \'{0}\': {1}'.format('test_ent', sem.entity == 'test_ent'))
			dprint('Is equal to \'{0}\': {1}'.format('test_e', sem.entity == 'test_e'))
			dprint('Is equal to \'{0}\': {1}'.format('dummy', sem.entity == 'dummy'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_ent/XXX', sem.entity != 'test_ent/XXX'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_ent', sem.entity != 'test_ent'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_e', sem.entity != 'test_e'))
			dprint('Is not equal to \'{0}\': {1}'.format('dummy', sem.entity != 'dummy'))
			dprint('Is included in \'{0}\': {1}'.format('test_ent/XXX', sem.entity < 'test_ent/XXX'))
			dprint('Is included in \'{0}\': {1}'.format('test_ent', sem.entity < 'test_ent'))
			dprint('Is included in \'{0}\': {1}'.format('test_e', sem.entity < 'test_e'))
			dprint('Is included in \'{0}\': {1}'.format('dummy', sem.entity < 'dummy'))
			dprint('Is included in \'{0}\': {1}'.format(['dummy'], sem.entity < ['dummy']))
			dprint('Is included in \'{0}\': {1}'.format('[\'test_ent\', \'dummy\']', sem.entity < ['test_ent', 'dummy']))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_ent/XXX', sem.entity <= 'test_ent/XXX'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_ent', sem.entity <= 'test_ent'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_e', sem.entity <= 'test_e'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('dummy', sem.entity <= 'dummy'))
			dprint('Does include \'{0}\': {1}'.format('test_ent/XXX', sem.entity > 'test_ent/XXX'))
			dprint('Does include \'{0}\': {1}'.format('test_ent', sem.entity > 'test_ent'))
			dprint('Does include \'{0}\': {1}'.format('test_e', sem.entity > 'test_e'))
			dprint('Does include \'{0}\': {1}'.format('dummy', sem.entity > 'dummy'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_ent/XXX', sem.entity >= 'test_ent/XXX'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_ent', sem.entity >= 'test_ent'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_e', sem.entity >= 'test_e'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('dummy', sem.entity >= 'dummy'))
			dprint('Does start with \'{0}\': {1}'.format('test_ent/XXX', sem.entity.startswith('test_ent/XXX')))
			dprint('Does start with \'{0}\': {1}'.format('test_ent', sem.entity.startswith('test_ent')))
			dprint('Does start with \'{0}\': {1}'.format('test_e', sem.entity.startswith('test_e')))
			dprint('Does start with \'{0}\': {1}'.format('dummy', sem.entity.startswith('dummy')))
			dprint('Does start for \'{0}\': {1}'.format('test_ent/XXX', sem.entity.starts('test_ent/XXX')))
			dprint('Does start for \'{0}\': {1}'.format('test_ent', sem.entity.starts('test_ent')))
			dprint('Does start for \'{0}\': {1}'.format('test_e', sem.entity.starts('test_e')))
			dprint('Does start for \'{0}\': {1}'.format('dummy', sem.entity.starts('dummy')))
			dprint('Does end with \'{0}\': {1}'.format('XXX/test_ent', sem.entity.endswith('XXX/test_ent')))
			dprint('Does end with \'{0}\': {1}'.format('test_ent', sem.entity.endswith('test_ent')))
			dprint('Does end with \'{0}\': {1}'.format('test_e', sem.entity.endswith('test_e')))
			dprint('Does end with \'{0}\': {1}'.format('dummy', sem.entity.endswith('dummy')))
			dprint('Does end \'{0}\': {1}'.format('XXX/test_ent', sem.entity.ends('XXX/test_ent')))
			dprint('Does end \'{0}\': {1}'.format('test_ent', sem.entity.ends('test_ent')))
			dprint('Does end \'{0}\': {1}'.format('test_e', sem.entity.ends('test_e')))
			dprint('Does end \'{0}\': {1}'.format('dummy', sem.entity.ends('dummy')))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.bentity.classname))
		dprint('bentity:   \'{0}\' ({1})'.format(sem.bentity, type(sem.bentity)))
		dprint('bentity:   \'{0}\' ({1})'.format(sem.bentity.str, type(sem.bentity.str)))
		dprint('bentity:   \'{0}\' ({1})'.format(sem.bentity.get(), type(sem.bentity.get())))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.role.classname))
		dprint('role:      \'{0}\' ({1})'.format(sem.role, type(sem.role)))
		dprint('role:      \'{0}\' ({1})'.format(sem.role.str, type(sem.role.str)))
		dprint('role:      \'{0}\' ({1})'.format(sem.role.get(), type(sem.role.get())))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.si.classname))
		dprint('si:      \'{0}\' ({1})'.format(sem.si, type(sem.si)))
		dprint('si:      \'{0}\' ({1})'.format(sem.si.printstr, type(sem.si.printstr)))
		dprint('si:      \'{0}\' ({1})'.format(sem.si.pstr, type(sem.si.pstr)))
		if (True):
			sem.si.print()
			sem.si.print('si')
		if (True):
			sem.si['format'] = 'tmdu/bmi/nakajima'
			sem.si['unit'] = 'radian'
			sem.si['time'] = {'time': '2023/08/22,21:12:27', 'period': '60', 'period_unit': 'seconds'}
			pprint.pprint(sem.si)
			sem.si.save('test.json')
			sem.si.load('test.json')
			sem.si.print('\'test.json\'')
			print('-- json.dumps() --')
			print(json.dumps(sem.si))
			print('--', flush=True)
			print('-- pprint.pprint() --')
			pprint.pprint(sem.si, indent=1, width=1)
			print('--', flush=True)

		print('\n--')
		dprint('classname: \'{}\''.format(sem.ti.classname))
		dprint('ti:      \'{0}\' ({1})'.format(sem.ti, type(sem.ti)))
		dprint('ti:      \'{0}\' ({1})'.format(sem.ti.printstr, type(sem.ti.printstr)))
		dprint('ti:      \'{0}\' ({1})'.format(sem.ti.pstr, type(sem.ti.pstr)))

	# test for data class

	if (True):
		print('\n-- DATA(_STORAGE) CLASS --')
		data = data_storage()
		dprint('classname: \'{}\''.format(data.classname))

	# test for ion class

	if (True):
		print('\n-- iON CLASS --')
		ion = ion()
		dprint('classname: \'{}\''.format(ion.classname))

#
# [name]  time.py
# [class] nkj.time
# [exec]  py -m nkj.time
#
# Written by Yoshikazu NAKAJIMA
#

from typing import Union
from nkj.str import *
import time as pytime
import datetime

_DEFAULT_TIMEPERIOD = 0.0

class time():

	def __init__(self, val=None, tp=None):
		ldprint('--> time.__init__({0}, {1})'.format(val, tp))
		if (val is None):
			dt = None
		elif (type(val) == tuple or type(val) == list):
			dt = val[0]
			if (tp is None):  # tp の指定がないときのみ、val に指定された time period を反映（val の第2引数よりも tp の入力を優先）
				tp = val[1]
		elif (type(val) == time):
			dt = val.datetime
			if (tp is None):  # tp の指定がないときのみ、val (time 形式) に指定された time period を反映（第1引数 time クラス内の timeperiod よりも tp の入力を優先）
				tp = val.timeperiod
		else:
			dt = val

		if (dt is None):
			self._datetime = datetime.datetime.now()
		elif (type(dt) == datetime.datetime):
			self._datetime = dt
		elif (type(dt) == float):
			self._datetime = datetime.datetime.fromtimestamp(dt)  # UNIX time
		else:
			__ERROR__NOTIMPLEMENTED

		if (self._datetime is None):
			ldprint('WARNING: NULL datetime')
			return

		ldprint2('datetime:   {}'.format(self._datetime))
		ldprint2('timeperiod: {0} ({1})'.format(tp, type(tp)))

		if (tp is None):
			self._timeperiod = _DEFAULT_TIMEPERIOD
		elif (type(tp) == float):
			self._timeperiod = tp
		elif (type(timeperiod) == int):
			self._timeperiod = float(tp)
		elif (type(timeperiod) == time):
			self._timeperiod = tp.timestamp - self.timestamp  # end

		ldprint('datetime:   {}'.format(self._datetime))
		ldprint('timeperiod: {}'.format(self._timeperiod))

		ldprint('<-- time.__init__()')

	def __add__(self, second):
		ldprint('--> time.__add()')
		ldprint('self:   {0} ({1})'.format(self.get(), type(self.get())))
		ty = type(second)
		ldprint2('second.type: {}'.format(type(second)))
		if (ty == float):
			ldprint('second: {0} ({1})'.format(second, type(second)))
			ldprint('<-- time.__add__()')
			return time(self.timestamp + second)
		elif (ty == int):
			ldprint('second: {0} ({1})'.format(second, type(second)))
			ldprint('<-- time.__add__()')
			return time(self.timestamp + float(second))
		else:
			ldprint('<-- time.__add__(): None (ERROR)')
			return None

	def __sub__(self, second):
		ldprint('--> time.__sub__()')
		ldprint('self:   {0} ({1})'.format(self.get(), type(self.get())))
		ty = type(second)
		ldprint2('second.type: {}'.format(type(second)))
		if (ty == time):
			ldprint('second: {0} ({1})'.format(second.get(), type(second)))
			ldprint('<-- time.__sub__()')
			return self.timestamp - second.timestamp  # return float
		elif (ty == datetime.datetime):
			ldprint('second: {0} ({1})'.format(second, type(second)))
			ldprint('<-- time.__sub__()')
			return self.timestamp - second.timestamp()  # return float
		elif (ty == float):
			ldprint('<-- time.__sub__()')
			return datetime.datetime.fromtimestamp(self.timestamp - second)  # return datetime
		elif (ty == int):
			ldprint('<-- time.__sub__()')
			return datetime.datetime.fromtimestamp(self.timestamp - float(second))  # return datetime
		else:
			ldprint('<-- time.__sub__(): None (ERROR)')
			return None

	def set(self, val):
		ldprint('--> time.set({0}, {1})'.format(val, type(val)))
		ty = type(val)
		if (ty == datetime.datetime):
			self._datetime = val
		elif (ty == float):
			self._datetime = datetime.datetime.fromtimestamp(val)
		else:
			self._datetime = None  # __ERROR__UNKNOWNTYPE
		ldprint('<-- time.set()')

	def get(self):
		return self._datetime

	@property
	def timeperiod(self):
		return self._timeperiod

	@timeperiod.setter
	def timeperiod(self, tp):
		self._timeperiod = tp

	@property
	def start(self):
		return self

	@start.setter
	def start(self, val):
		self.set(val)

	@property
	def end(self):
		ldprint('self.start:      {}'.format(self.start.datetime))
		ldprint('self.datetime:   {}'.format(self.datetime))
		ldprint('self.timestamp:  {}'.format(self.timestamp))
		ldprint('self.timeperiod: {}'.format(self.timeperiod))
		ldprint(self.timestamp + self.timeperiod)
		ldprint(self + self.timeperiod)
		return self.start + self.timeperiod

	@end.setter
	def end(self, val):
		self.set(val - self.start)

	def update(self):
		self.set(datetime.datetime.now())
		return self.get()

	def refresh(self):
		return self.update()

	def now(self):
		return self.update()

	@property
	def datetime(self):
		return self.get()

	@datetime.setter
	def datetime(self, val:datetime):
		self.set(val)

	@property
	def timestamp(self):
		return self.get().timestamp()

	@timestamp.setter
	def timestamp(self, val):
		self.set(val)

	def includes(self, t):
		ty = type(t)
		ldprint2('type: {}'.format(ty))
		if (ty == time):
			ldprint2('second: {0} ({1})'.format(t.datetime, type(t)))
			ts_start = t.timestamp
			ts_end = t.end.timestamp
		elif (ty == datetime.datetime):
			ts_start = t.timestamp()
			ts_end = ts_start  # time period should be 0
		else:  # UNIX time
			ts_start = t
			ts_end = ts_start  # time period should be 0
		ldprint2('start: {}'.format(ts_start))
		ldprint2('end:   {}'.format(ts_end))
		td_start = ts_start - self.timestamp
		td_end = ts_end - self.end.timestamp
		return True if (td_start >= 0.0 and td_end <= 0.0) else False

	def included(self, t):
		ty = type(t)
		ldprint2('type: {}'.format(ty))
		if (ty == time):
			ts_start = t.timestamp
			ts_end = t.end.timestamp
		elif (ty == datetime.datetime):
			ts_start = t.timestamp()
			ts_end = ts_start  # time period should be 0
		else:  # UNIX time
			ts_start = t
			ts_end = ts_start  # time period should be 0
		td_start = ts_start - self.timestamp
		td_end = ts_end - self.end.timestamp
		return True if (td_start <= 0.0 and td_end >= 0.0) else False

#-- main

if (__name__ == '__main__'):

	_DEBUGLEVEL = 0
	_LIB_DEBUGLEVEL = 0
	debuglevel(_DEBUGLEVEL)
	lib_debuglevel(_LIB_DEBUGLEVEL)

	t = time()
	print('get():      {}'.format(t.get()))
	print('now():      {} (updated)'.format(t.now()))
	print('get():      {} (not updated)'.format(t.get()))
	print('datetime:   {} (not updated)'.format(t.datetime))
	print('timestamp:  {} (not updated)'.format(t.timestamp))

	print('\n--')
	print('t:       {}'.format(t.datetime))
	print('t + 3:   {}'.format(t + 3))
	print('t + 0.1: {}'.format(t + 0.1))
	print('t - 3:   {}'.format(t - 3))
	print('t - 0.1: {}'.format(t - 0.1))

	print('\n--')
	t.timeperiod = 3.0
	print('t:            {}'.format(t.datetime))
	print('t.start:      {}'.format(t.start.datetime))
	print('t.timeperiod: {}'.format(t.timeperiod))
	print('t.end:        {}'.format(t.end))

	print('\n--')

	def func():
		pytime.sleep(0.1)

	t1 = time()
	print('Start time: {0} ({1})'.format(t1.datetime, type(t1)))
	func()
	t2 = time()
	print('End time:   {0} ({1})'.format(t2.datetime, type(t2)))
	print('computation time: {}'.format(t2 - t1))

	print('\n--')
	print('includes: {}'.format(t1.includes(t1)))
	print('includes: {}'.format(t1.includes(t2)))
	print('includes: {}'.format(t2.includes(t1)))
	print('included: {}'.format(t1.included(t1)))
	print('included: {}'.format(t1.included(t2)))
	print('included: {}'.format(t2.included(t1)))

	print('\n--')
	t1.timeperiod = 1.0
	print('includes: {}'.format(t1.includes(t1)))
	print('includes: {}'.format(t1.includes(t2)))
	print('includes: {}'.format(t2.includes(t1)))
	print('included: {}'.format(t1.included(t1)))
	print('included: {}'.format(t1.included(t2)))
	print('included: {}'.format(t2.included(t1)))

	print('\n--')
	t = time(t1)  # t1 は timeperiod が設定されている
	print('t1: {0} - {1}'.format(t1.datetime, t1.end.datetime))
	print('t:  {0} - {1}'.format(t.datetime, t.end.datetime))
	t = time(t2)  # t2 は timeperiod が設定されていない
	print('t2: {0} - {1}'.format(t2.datetime, t2.end.datetime))
	print('t:  {0} - {1}'.format(t.datetime, t.end.datetime))

	print('\n--')
	t = time((t1.datetime, 3.0))  # timeperiod を指定して設定．tuple 形式で初期化指定
	dprint('t.datetime:     {}'.format(t.datetime))
	dprint('t.timeperiod:   {}'.format(t.timeperiod))
	dprint('t.end.datetime: {}'.format(t.end.datetime))
	print('t:  {0} - {1}'.format(t.datetime, t.end.datetime))
	t = time([t1.datetime, 3.0])  # timeperiod を指定して設定．list 形式で初期化指定
	dprint('t.datetime:     {}'.format(t.datetime))
	dprint('t.timeperiod:   {}'.format(t.timeperiod))
	dprint('t.end.datetime: {}'.format(t.end.datetime))
	print('t:  {0} - {1}'.format(t.datetime, t.end.datetime))
	t = time(t1, 5.0)  # timeperiod を指定して設定．time 形式と tp=float で初期化指定
	dprint('t.datetime:     {}'.format(t.datetime))
	dprint('t.timeperiod:   {}'.format(t.timeperiod))
	dprint('t.end.datetime: {}'.format(t.end.datetime))
	print('t:  {0} - {1}'.format(t.datetime, t.end.datetime))
	t = time((t1.datetime, 3.0), 5.0)  # timeperiod を指定して設定．tuple 形式と tp=float でで初期化指定
	dprint('t.datetime:     {}'.format(t.datetime))
	dprint('t.timeperiod:   {}'.format(t.timeperiod))
	dprint('t.end.datetime: {}'.format(t.end.datetime))
	print('t:  {0} - {1}'.format(t.datetime, t.end.datetime))
	t = time([t1.datetime, 3.0], 5.0)  # timeperiod を指定して設定．list 形式と tp=float でで初期化指定
	dprint('t.datetime:     {}'.format(t.datetime))
	dprint('t.timeperiod:   {}'.format(t.timeperiod))
	dprint('t.end.datetime: {}'.format(t.end.datetime))
	print('t:  {0} - {1}'.format(t.datetime, t.end.datetime))

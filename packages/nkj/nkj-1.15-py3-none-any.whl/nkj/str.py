#
# [name] nkj.str.py
# [purpose] nkj.str library
# [exec] python -m nkj.str
#
# Written by Yoshikazu NAKAJIMA (Wed Sep 23 14:38:26 JST 2020)
#

__DEBUGLEVEL = 0
__LIB_DEBUGLEVEL = 0

NULLSTR = ''
CR = '\r' # 行頭へ復帰
LF = '\n' # 改行
CRLF = '\r\n'

PRINTEND_CR = CR
PRINTEND_LF = LF
PRINTEND_CRLF = CRLF
PRINTEND_NONE = ''
DEFAULT_PRINTEND = PRINTEND_LF
DEFAULT_BRACKET = '\"'  # {'\'', '\"'}
DEFAULT_DOTPRINT = True

import os
import sys
import re
import numpy as np
import json
from typing import Union

_BRACKET = DEFAULT_BRACKET
_VERBOSE_DOTPRINT = DEFAULT_DOTPRINT
_VERBOSE_DOTPRINT_COUNTER = 0

# str

def is_nullstr(s):
	if (s is None):
		return False
	else:
		return (s == NULLSTR)

def nullstr(s):
	return is_nullstr(s)

def is_intstr(s):
	try:
		int(s, 10)
	except ValueError:
		return False
	else:
		return True

def is_floatstr(s):  # float に変換可能かどうかをテストして判定しているので、int の場合も True を返す．
	try:
		float(s)
	except ValueError:
		return False
	else:
		return True

def is_truefloatstr(s):
	try:
		float(s)
	except ValueError:
		return False
	else:
		return (not is_intstr(s))

def intstr(s):
	return is_intstr(s)

def floatstr(s):
	return is_floatstr(s)

def truefloatstr(s):
	return is_truefloatstr(s)

def is_intstr_re(s):  # 正規表現 (Regular expression, re) バージョン
	p = '[-+]?\d+'
	return True if re.fullmatch(p, s) else False

def is_floatstr_re(s):
	p = '[-+]?(\d+\.?\d* | \.\d+)([eE][-+]?\d+)?'
	return True if re.fullmatch(p, s) else False

def intstr_re(s):
	return is_intstr_re(s)

def floatstr_re(s):
	return is_floatstr_re(s)

# tuple

def is_nulltuple(t):
	return not isnot_nulltuple(t)

def isnot_nulltuple(t):
	return any(t)

def nulltuple(t):
	return is_nulltuple(t)

def not_nulltuple(t):
	return not nulllist(t)

# list

def is_nulllist(d):
	return not isnot_nulllist(d)

def isnot_nulllist(l):
	return any(l)

def nulllist(d):
	return is_nulllist(d)

def not_nulllist(d):
	return not nulllist(d)

# dict

def is_nulldict(d):
	return not isnot_nulldict(d)

def isnot_nulldict(d):
	return any(d)  # 組み込み関数 any() を用いて NULL 判定（空判定）する

def nulldict(d):
	return is_nulldict(d)

def not_nulldict(d):
	return not nulldict(d)

# json

def is_jsonstr(s:str):
	ldprint('--> nkj.str.is_jsonstr(\'{}\')'.format(s))
	try:
		json.loads(s)
	except json.JSONDecodeError as jde:
		ldprint('<-- nkj.str.is_jsonstr(): {}'.format(False))
		return False
	else:
		ldprint('<-- nkj.str.is_jsonstr(): {}'.format(True))
		return True

def isnot_jsonstr(s:str):
	return not is_jsonstr(s)

def jsonstr(s:str):
	return is_jsonstr(s)

def not_jsonstr(s:str):
	return isnot_jsonstr(s)

def todict(s:Union[dict, tuple, list, str, None]):
	ldprint('--> nkj.str.todict(\'{0}\' ({1}))'.format(s, type(s)))
	ldprint0('val: \'{0}\' ({1})'.format(s, type(s)))
	if (s is None):
		d = {}
	elif (type(s) == dict):
		d = s.copy()
	elif (type(s) == set):
		d = {}
		s = list(s)
		d[s[0]] = s[1]
	elif (type(s) == tuple or type(s) == list):
		if (len(s) != 2):
			raise ValueError('Illegal format for dict component')
		d = {}
		d[s[0]] = s[1]
	elif (type(s) == str):
		if (is_jsonstr(s)):
			d = json.loads(val)
		else:
			s = s.split(',')
			if (len(s) == 2):
				d = {}
				d[s[0]] = s[1]
			else:
				ldprint('\'{0}\' ({1})'.format(s, type(s)))
				raise ValueError('Illegal data format')
	else:
		ldprint('\'{0}\' ({1})'.format(s, type(s)))
		d = s.copy()
	ldprint('<-- nkj.str.todict()')
	return d

# debug printing

def debuglevel(level=None):
	global __DEBUGLEVEL
	if (level is None):
		return __DEBUGLEVEL
	else:
		__DEBUGLEVEL = level
		return True

def lib_debuglevel(level=None):
	global __LIB_DEBUGLEVEL
	if (level is None):
		return __LIB_DEBUGLEVEL
	else:
		__LIB_DEBUGLEVEL = level
		return True

def verbose_dotprint(flag=None, interval=None):
	global _VERBOSE_DOTPRINT
	global _VERBOSE_DOTPRINT_COUNTER
	if (flag is None):
		if (_VERBOSE_DOTPRINT is True):
			if (interval == None):
				print(".", end='', file=sys.stderr)
				sys.stderr.flush()
			elif (_VERBOSE_DOTPRINT_COUNTER >= interval - 1):
				print(".", end='', file=sys.stderr)
				sys.stderr.flush()
				_VERBOSE_DOTPRINT_COUNTER = 0
			else:
				_VERBOSE_DOTPRINT_COUNTER += 1
	elif (flag == 'end'):
		print("", file=sys.stderr)
def intstr(s):
	return is_intstr(s)

def is_intstr_re(s):  # 正規表現 (Regular expression, re) バージョン
	p = '[-+]?\d+'
	return True if re.fullmatch(p, s) else False

def is_floatstr_re(s):
	p = '[-+]?(\d+\.?\d* | \.\d+)([eE][-+]?\d+)?'
	return True if re.fullmatch(p, s) else False

def debuglevel(level=None):
	global __DEBUGLEVEL
	if (level is None):
		return __DEBUGLEVEL
	else:
		__DEBUGLEVEL = level
		return True

def lib_debuglevel(level=None):
	global __LIB_DEBUGLEVEL
	if (level is None):
		return __LIB_DEBUGLEVEL
	else:
		__LIB_DEBUGLEVEL = level
		return True

def verbose_dotprint(flag=None, interval=None):
	global _VERBOSE_DOTPRINT
	global _VERBOSE_DOTPRINT_COUNTER
	if (flag is None):
		if (_VERBOSE_DOTPRINT is True):
			if (interval == None):
				print(".", end='', file=sys.stderr)
				sys.stderr.flush()
			elif (_VERBOSE_DOTPRINT_COUNTER >= interval - 1):
				print(".", end='', file=sys.stderr)
				sys.stderr.flush()
				_VERBOSE_DOTPRINT_COUNTER = 0
			else:
				_VERBOSE_DOTPRINT_COUNTER += 1
	elif (flag == 'end'):
		print("", file=sys.stderr)
def intstr(s):
	return is_intstr(s)

def is_intstr_re(s):  # 正規表現 (Regular expression, re) バージョン
	p = '[-+]?\d+'
	return True if re.fullmatch(p, s) else False

def is_floatstr_re(s):
	p = '[-+]?(\d+\.?\d* | \.\d+)([eE][-+]?\d+)?'
	return True if re.fullmatch(p, s) else False

def debuglevel(level=None):
	global __DEBUGLEVEL
	if (level is None):
		return __DEBUGLEVEL
	else:
		__DEBUGLEVEL = level
		return True

def lib_debuglevel(level=None):
	global __LIB_DEBUGLEVEL
	if (level is None):
		return __LIB_DEBUGLEVEL
	else:
		__LIB_DEBUGLEVEL = level
		return True

def verbose_dotprint(flag=None, interval=None):
	global _VERBOSE_DOTPRINT
	global _VERBOSE_DOTPRINT_COUNTER
	if (flag is None):
		if (_VERBOSE_DOTPRINT is True):
			if (interval == None):
				print(".", end='', file=sys.stderr)
				sys.stderr.flush()
			elif (_VERBOSE_DOTPRINT_COUNTER >= interval - 1):
				print(".", end='', file=sys.stderr)
				sys.stderr.flush()
				_VERBOSE_DOTPRINT_COUNTER = 0
			else:
				_VERBOSE_DOTPRINT_COUNTER += 1
	elif (flag == 'end'):
		print("", file=sys.stderr)
		sys.stderr.flush()
	elif (flag == 'flag'):
		return _VERBOSE_DOTPRINT
	elif (flag == 'enable'):
		_VERBOSE_DOTPRINT = True
	elif (flag == 'disable'):
		_VERBOSE_DOTPRINT = False
	else:
		_VERBOSE_DOTPRINT = flag
		return True

def bracket(type=None):
	global _BRACKET
	if (type is None):
		return _BRACKET
	else:
		if (type == 1):
			_BRACKET = '\''
		elif (type == 2):
			_BRACKET = '\"'
		else:
			print_error("Illegal bracket type. ERROR#: NKJSTR-00055.")

def str_bracket(in_str, type=1):
	if (in_str is None):
		s = bracket() + bracket()
	elif (in_str == ""):
		s = bracket() + bracket()
	else:
		s = bracket() + str(in_str) + bracket()
	return s

def str_float(in_str):
	return "{0:8.3f}".format(in_str)

def concat(strlist):
	retstr = NULLSTR
	if (len(strlist) != 0):
		for i in range(len(strlist)):
			if (strlist[i] != None and strlist[i] != NULLSTR):
				retstr += str(strlist[i])
	return retstr

def concat_path(pathlist):
	retstr = NULLSTR
	for path in pathlist[:-1]:
		dprint3(["PATH: ", str_bracket(path)])
		if (path[-1] != '/'):
			path += '/'
		retstr = concat([retstr, path])
	dprint3(["PATH: ", str_bracket(pathlist[-1])])
	retstr += pathlist[-1]
	return retstr

def print_usage(msg):
	print("Usage: python " + sys.argv[0] + " " + msg, flush=True)
	sys.stdout.flush()

def print_message(msg):
	print(msg, flush=True)
	sys.stdout.flush()

def print_warning(msg):
	print("WARNING: " + msg, flush=True)
	sys.stdout.flush()

def print_error(msg):
	print("ERROR: " + msg, flush=True)
	sys.stdout.flush()

def _dprint(level, strlist, end=DEFAULT_PRINTEND): # '_' で始まる関数は import * で読み込まれない
	if (__DEBUGLEVEL >= level):
		message = NULLSTR
		for i in range(len(strlist)):
			s = str(strlist[i])
			if (s != NULLSTR):
				message += s
			else:
				message += "NULL"
		print(message, flush=True, end=end)
		sys.stdout.flush()
	else:
		pass

def _ldprint(level, strlist, end=DEFAULT_PRINTEND):
	if (__LIB_DEBUGLEVEL >= level):
		message = NULLSTR
		for i in range(len(strlist)):
			s = str(strlist[i])
			if (s != NULLSTR):
				message += s
			else:
				message += "NULL"
		print(message, flush=True, end=end)
		sys.stdout.flush()
	else:
		pass

def dprint0(strlist, end=DEFAULT_PRINTEND):
	_dprint(0, strlist, end)

def dprint1(strlist, end=DEFAULT_PRINTEND):
	_dprint(1, strlist, end)

def dprint2(strlist, end=DEFAULT_PRINTEND):
	_dprint(2, strlist, end)

def dprint3(strlist, end=DEFAULT_PRINTEND):
	_dprint(3, strlist, end)

def dprint(strlist, end=DEFAULT_PRINTEND):
	dprint1(strlist, end)

def ldprint0(strlist, end=DEFAULT_PRINTEND):
	_ldprint(0, strlist, end)

def ldprint1(strlist, end=DEFAULT_PRINTEND):
	_ldprint(1, strlist, end)

def ldprint2(strlist, end=DEFAULT_PRINTEND):
	_ldprint(2, strlist, end)

def ldprint3(strlist, end=DEFAULT_PRINTEND):
	_ldprint(3, strlist, end)

def ldprint(strlist, end=DEFAULT_PRINTEND):
	ldprint1(strlist, end)

def is_none(str):
	if (str is None):
		return True
	elif (str == NULLSTR):
		return True
	else:
		return False

def isnot_none(str):
	return (not isNone(str))

def extract_float(istr):
	strs = re.findall(r"[-]*[0-9][0-9]*[.]*[0-9]*[e+-]*[0-9]*", istr)
	vals = []
	for s in strs:
		vals.append(float(s))
	return np.array(vals)

def atoi(s):
	return int(s.strip())

def linestr2int(s_line):
	dlist = []
	for s in s_line.split(','):
		dlist.append(atoi(s))
	return dlist

def l2i(linestr):
	return linestr2int(linestr)

def atof(s):
	return float(s.strip())

def linestr2float(s_line):
	linestr = s_line.split(',')
	if (len(linestr) == 1):
		linestr = s_line.split(' ')
	dlist = []
	for s in linestr:
		dlist.append(atof(s))
	return dlist

def l2f(linestr):
	return linestr2float(linestr)


#-- main

if __name__ == '__main__':
	import os
	import sys

	sys.path.append(os.path.abspath(".."))

	import nkj.core as nc
	print(["ROOTPATH: ", nc.rootpath()])

	import nkj.str as ns
	ns.debuglevel(5)
	ns.dprint(["test1, ", "test2, ", "test3"])

	"""
	debuglevel(5)
	"""
	print("test")
	__DEBUGLEVEL = 5
	dprint(["test, ", "test2, ", ""])

	print(concat_path(["test", "test2"]))
	print(concat_path(["test/", "test2"]))
	print(concat_path(["test/", "test2", "test3"]))

	print(linestr2float('   0.00123, 2.345,  -12.356'))

	for s in ['5', '-3', '2.71828', '-2.71828', '-3.14e+2', '4.tadfa']:
		print('\'{0}\' is int:        {1}'.format(s, is_intstr(s)))
		print('\'{0}\' is float:      {1}'.format(s, is_floatstr(s)))
		print('\'{0}\' is true float: {1}'.format(s, is_truefloatstr(s)))

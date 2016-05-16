# -*- coding: utf-8 -*-
'''
Utility module
'''

# 1. django

# 2. system
import datetime

# 3. 3rd party

def	date2str(data, name):
	'''
	@param data:dict
	@param name:str
	'''
	data[name] = data[name].strftime('%d.%m.%Y') if data[name] else ''

def	str2date(data, name):
	'''
	@param data:dict
	@param name:str
	'''
	data[name] = datetime.datetime.strptime(data[name], '%d.%m.%Y').date() if data[name] else None

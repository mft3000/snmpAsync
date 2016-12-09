#!/usr/bin/env python

########## ver 0.2
#
# 0.1 first init
# 0.2 add print_table()
#

import collections, json

from texttable import *

tree = lambda: collections.defaultdict(tree)

class table(object):

	_field_list = []
	_keys_list = []

	tab = tree()

	dt = Texttable()

	def __init__(self, name = ''):
		
		self.name = name

	def add_fields_name(self, field):

		n = field.index('.')
		self._field_list.append(field[:n])
		return field[:n]

	def add_keys_name(self, field):

		n = field.index('.') + 1
		self._keys_list.append(field[n:])
		return field[n:]

	def show_fileds_list(self):
		
		result = list(set(self._field_list))
		return result

	def show_keys_list(self):
		
		result = list(set(self._keys_list))
		return result

	def add_values(self, key, field, value):

		self.tab[key][field] = value

	def show_values_json(self):

		return json.dumps(self.tab, sort_keys=True, indent=4, separators=(',', ': '))

	def print_table(self):

		table = []
		table.append(list(set(self._field_list)))
		line = []
		for x in self.tab:
			for y in self.tab[x]:
				line.append( str(self.tab[x][y]) )
			table.append(line)
			line = []

		# print table
		self.dt.add_rows(table)
		print self.dt.draw()

#!/usr/bin/env python

########## ver 0.31
#
# 0.1 first init
# 0.2 add print_table()
# 0.3 add sql, snmp to json, json to sql, sql to json
# 0.31 fix bug in multiple obj init
#

import collections, json

from texttable import *
import sqlite3

tree = lambda: collections.defaultdict(tree)

# ++++++++++++++++++++  
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# --------------------  

class table(object):

	def __init__(self, name = ''):
		
		self.name = name
		
		self._field_list = []
		self._keys_list = []

		self.tab = tree()

		self.dt = Texttable(max_width=150)

		self.s = sql(self.name)
		self.s.connect()

	def add_fields_name(self, field):

		n = field.index('.')
		self._field_list.append(field[:n])
		return field[:n]

	def add_keys_name(self, field):

		n = field.index('.') + 1
		self._keys_list.append(field[n:])
		return field[n:]

	def show_fields_list(self):
		
		result = list(set(self._field_list))
		return result

	def erase_fileds_list(self):
		
		self._field_list = []

	def show_keys_list(self):
		
		result = list(set(self._keys_list))
		return result

	def add_values(self, key, field, value):

		self.tab[key][field] = value

	def show_values_json(self):

		return json.dumps(self.tab, sort_keys=True, indent=4, separators=(',', ': '))

	# def print_table(self):

	# 	table = []
	# 	table.append(list(set(self._field_list)))
	# 	line = []
	# 	for x in self.tab:
	# 		for y in self.tab[x]:
	# 			line.append( str(self.tab[x][y]) )
	# 		table.append(line)
	# 		line = []

	# 	print table
	# 	self.dt.add_rows(table)
	# 	print self.dt.draw()

	def populate_sql_table(self):

		table_data = []
		self._field_list.append('-')
		table_data.append(list(set(self._field_list)))
		self.s.create_table(self.name, list(set(self._field_list)))
		line = []
		keys = []
		for key in self.tab:
			for x in self.tab[key]:
				keys.append( str(x) )
				line.append( str(self.tab[key][x]) )
			keys.append( '-' )
			line.append( key )

			# print len(keys), keys
			# print len(line), line
			self.s.load_row(self.name, keys, line)
			table_data.append(line)
			line = []
			keys = []

	def print_sql_table(self, print_mode = 'texttable'):
		data_from_json = self.s.select_table(self.name)
		if print_mode == 'list':
			print data_from_json
		elif print_mode == 'texttable':
			self.dt.add_rows(data_from_json)
			print self.dt.draw()
		elif print_mode == 'json':
			print self.s.select_table_as_json(self.name)

	def erase_table(self):

		self.s.drop_table(self.name)

def dict_factory(cursor, row):
    js = tree()
    for idx, col in enumerate(cursor.description):
    	if col[0] == '-':
    		i = idx
    		break
    for idx, col in enumerate(cursor.description):
        if col[0] == '-':
            continue
        else:
            js[row[i]][col[0]] = row[idx]
    # for idx, col in enumerate(cursor.description):
    #     js[col[0]] = row[idx]
    return js

class sql(object):
	
    file = ''
    conn = ''

    def __init__(self, file):
            self.file = file

    def connect(self):

            self.conn = sqlite3.connect(self.file + '.sqlite3')

    def create_table(self, name, field_list):

		cur = self.conn.cursor()

		sql = "CREATE TABLE IF NOT EXISTS %s (\'%s\' TEXT NULL DEFAULT '');" % (name, "' TEXT NULL DEFAULT '', '".join(field_list))

		# print sql
		cur.executescript(sql)
		self.conn.commit()

    def drop_table(self, name):

		cur = self.conn.cursor()

		sql = "DROP TABLE IF EXISTS " + name + ";"

		cur.executescript(sql)
		self.conn.commit()

  #   def query(self, sql):

		# cur = self.conn.cursor()

		# cur.execute(sql)

		# self.conn.commit()
	
    def returnID(self, table, condition, value):

		cur = self.conn.cursor()
						
		sql = 'SELECT * FROM ' + table + ' WHERE ' + condition + ' = \'' + value + '\';'
		# logging.debug( sql )

		cur.execute(sql)
						
		return cur.fetchone()
			 
    def load_row(self, table, keys_list, data_lists):

        cur = self.conn.cursor()

        sql = "INSERT INTO %s (\'%s\') VALUES (\'%s\');" % (table, "', '".join(keys_list), "', '".join(data_lists))
        # print sql

        logging.debug(sql)
        cur.execute(sql)
        self.conn.commit()

        logging.info("loading row to sql...DONE")

    def select_table(self, table_name):

        cur = self.conn.cursor()

        sql_code = "SELECT * FROM %s " % (table_name)

        cur.execute(sql_code)
        logging.debug(sql_code)

        filed_names = tuple(map(lambda x: x[0], cur.description))
        rows = cur.fetchall()

        return [filed_names] + rows

    def select_table_as_json(self, table_name):

        self.conn.row_factory = dict_factory
        cur = self.conn.cursor()

        sql_code = "SELECT * FROM %s " % (table_name)

        cur.execute(sql_code)
        logging.debug(sql_code)

        # filed_names = tuple(map(lambda x: x[0], cur.description))
        rows = cur.fetchall()

        return json.dumps(rows, sort_keys=True, indent=4, separators=(',', ': '))

    def close(self):

        self.conn.close()
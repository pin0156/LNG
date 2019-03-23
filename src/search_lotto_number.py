#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import json
from optparse import OptionParser

class LNG:
	def __init__(self, dic_file_name):
		self.lotto_dic = self.load_lotto_dic(dic_file_name)

	def load_lotto_dic(self, file_name):
		with open(file_name, 'r') as json_file:
			try:
				json_data = json.load(json_file)
				return json_data
			except:
				sys.stderr.write('can not load '+file_name+' file \n')
				exit(-1)

	def search_lotto_dic(self, key):
		try:
			return self.lotto_dic[key]
		except:
			return None

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("--lotto_dic", dest="lotto_dic", help="lotto_dic", metavar="lotto_dic")
	(options, args) = parser.parse_args()

	lotto_dic_path = options.lotto_dic
	if lotto_dic_path == None:
		lotto_dic_path = '../data/lotto_statistics.json'

	lng = LNG(lotto_dic_path)

	while 1:
		try:
			line = sys.stdin.readline()
		except KeyboardInterrupt:
			break
		if not line:
			break
		line = line.strip()
                line = line.replace(' ','')
                line = sorted([int(i) for i in line.split(',')])
                line = [str(i) for i in line]
                line = ','.join(line)
		if line == '' : continue
		val = lng.search_lotto_dic(line)
		print json.dumps(val, ensure_ascii=False, encoding='utf-8') + '\n'

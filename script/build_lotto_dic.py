#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import json
import itertools
import operator

def get_lotto_num(data):
	num_list = [ int(data['drwtNo1']), int(data['drwtNo2']), int(data['drwtNo3']), int(data['drwtNo4']), int(data['drwtNo5']), int(data['drwtNo6']) ]
	return num_list

def make_key_val(lotto_num_list, statistics):
	list_size = len(lotto_num_list)
	i = 1;
	while i < list_size:
		key_list = [list(x) for x in itertools.combinations(lotto_num_list, i)]
		#print key_list
		for key in key_list:
			val_list = list(set(lotto_num_list) - set(key))
			#print key, val_list
			key_str = ','.join(str(x) for x in key)
			for val in val_list:
				#print key_str, val
				try:
					statistics[key_str]
				except KeyError:
					statistics[key_str] = dict()
				try:
					statistics[key_str][val]
				except KeyError:
					statistics[key_str][val] = 0
				statistics[key_str][val] += 1
		i += 1

def print_statistics(statistics):
	res = dict()
	for key in sorted(statistics.keys()):
		val_list = [ str(k)+':'+str(v) for k, v in sorted(sorted(statistics[key].items(), key=lambda x: int(x[0])), key=lambda x : int(x[1]), reverse=True ) ]
		res[key] = val_list

	print json.dumps(res, ensure_ascii=False, encoding='utf-8') + '\n'
if __name__ == '__main__':
	statistics = dict()
	while 1:
		try:
			line = sys.stdin.readline()
		except KeyboardInterrupt:
			break
		if not line:
			break
		line = line.strip()
		if line == '' : continue
		data = json.loads(line)
		lotto_num_list = get_lotto_num(data)
		#print lotto_num_list
		make_key_val(lotto_num_list, statistics);
	print_statistics(statistics)

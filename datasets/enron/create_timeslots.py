#!/usr/bin/env python

import csv
from datetime import datetime
from collections import namedtuple

edge = namedtuple("edge", ["from_node", "to_node"])
month_year = namedtuple("month_year", ["year", "month"])

def is_time_ok(time):
	return time > 909762180 and time < 1026473760

def build_dict(filename):
	dictionary = dict()
	with open(filename) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			start, end, timestamp = int(row[0]), int(row[1]), int(row[2])
			
			if not is_time_ok(timestamp):
				continue
			
			time = datetime.fromtimestamp(timestamp)
			MY = month_year(month=time.month, year=time.year)
			E = edge(from_node=start, to_node=end)

			if MY in dictionary:
				dictionary[MY].append(E)
			else:
				dictionary[MY] = [E]

	return dictionary

def write_to_files(timeslots):
	for key in timeslots.keys():
		filename = str(key.month) + '-' + str(key.year) +'.csv'
		with open('timeslots/' + filename, 'w') as f:
			for edge in timeslots[key]:
				f.write("%s,%s\n" % (edge.from_node, edge.to_node))

def count_filtered(filename):
	count = 0
	with open(filename) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			start, end, timestamp = int(row[0]), int(row[1]), int(row[2])
			
			if not is_time_ok(timestamp):
				count += 1
	return count

D = build_dict('edges_cleaned.csv')
write_to_files(D)

# print count_filtered('edges_cleaned.csv')
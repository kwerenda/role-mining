# -*- coding: utf-8 -*-

import snap
from datetime import date, datetime
from collections import defaultdict
from itertools import chain


class HepReader(object):
    def __init__(self):
        self._stripped_11s = 0
        pass

    DATE_FORMAT = '%Y-%m-%d'


    @staticmethod
    def _date_from_id(node_id):
        node_id = str(node_id).zfill(7)
        year = int(node_id[:2])
        year = 1900 + year if year > 20 else 2000 + year
        return date(year=year, month=int(node_id[2:4]), day=1)

    def _strip11s(self, node_id, node_date):
        node_id = node_id.lstrip('0')
        if node_id.startswith('11'):
            # some 11s might be misleading (eg 12/2001)
            if len(node_id) >= 7 or len(node_id) == 6 and node_date.year == 2000:
                node_id = node_id[2:]
                self._stripped_11s += 1
        return node_id

    def clean_data(self, filename_edges, filename_dates, write_to_file=False):
        """Read data from raw file, remove 11s and duplicates, optionally write results to new file"""
        # read raw file line by line
        with open(filename_dates) as fnodes:
            nodes = [line.strip().split() for line in fnodes.readlines() if not line.startswith('#')]
        print "Raw nodes with dates: ", len(nodes)

        edges = self.read_edges(filename_edges)
        print "Raw edges: ", len(edges)

        # remove 11s
        cleaned_nodes = []
        for node in nodes:
            node_id = node[0].lstrip('0')
            cit_date = datetime.strptime(node[1], self.DATE_FORMAT).date()
            cleaned_node_id = self._strip11s(node_id, cit_date).zfill(7)
            cleaned_nodes.append((cleaned_node_id, cit_date))
        entries_removed = len(nodes) - len(cleaned_nodes)
        nodes = cleaned_nodes
        print "Nodes after removing 11s: ", len(nodes), " removed: ", entries_removed, " affected: ", self._stripped_11s

        # search for duplicate or inconsistent dates
        different_date = 0
        duplicates = 0
        dates = {}  # {node_id : [dates]}
        for node in nodes:
            node_id = int(node[0])
            node_date = node[1]
            if node_id in dates:
                duplicates += 1
                if node_date != dates[node_id]:
                    dates[node_id] = min(dates[node_id], node_date)
                    different_date += 1
            else:
                dates[node_id] = node_date

        print "Nodes after removing duplicates: {} Removed: {}, duplicates: {}, inconsistencies: {}" \
            .format(len(dates.keys()), len(nodes) - len(dates.keys()), duplicates, different_date)

        nr_edges_raw = len(edges)
        edges = list(set([(int(e[0]), (e[1])) for e in edges]))
        print "Removed duplicate edges: {}".format(nr_edges_raw - len(edges))

        # check for inconsistencies between id and date
        inconsistencies = 0
        for node_id in dates:
            date_from_id = self._date_from_id(node_id)
            if dates[node_id].year != date_from_id.year or dates[node_id].month != date_from_id.month:
                inconsistencies += 1
                # print "Inconsistent date, node id: {} date: {} date from id: {}".format(node_id, dates[node_id],
                # date_from_id)

        # print results to "cleaned" file
        if write_to_file:
            with open(filename_dates.replace('.txt', '') + '-cleaned.txt', 'w') as fout:
                for node_id, cit_date in sorted(dates.iteritems(), key=lambda e: e[1]):
                    fout.write("{:07d}\t{}\n".format(node_id, cit_date))
                print "Written to ", fout.name

        print "Inconsistent dates: ", inconsistencies

        #find all nodes in edges file
        nodes_with_edges = set(chain(*edges))
        print "Number of distinct nodes found in edges file: ", len(nodes_with_edges)

        nodes_with_edges_but_no_date = nodes_with_edges.difference(set(dates.keys()))
        print "Number of nodes with edges but without defined date ", len(nodes_with_edges_but_no_date)

        nodes_with_date_but_no_edges = set(dates.keys()).difference(nodes_with_edges)
        print "Number of nodes with date but no edges", len(nodes_with_date_but_no_edges)

        #print only nodes with edges to separate file, correct date if possible
        if write_to_file:
            with open(filename_dates.replace('.txt', '.nodes'), 'w') as fout:
                for node_id in sorted(nodes_with_edges):
                    try:
                        node_date = dates[node_id]
                    except KeyError:
                        node_date = self._date_from_id(node_id)
                    fout.write("{:07d}\t{}\n".format(node_id, node_date))

                print "Nodes with dates writen to ", fout.name


    @classmethod
    def read_dates(cls, filename_dates):
        """Read nodes with dates from file as dict: {node_id : date}"""
        dates = {}  # {node_id : year}
        with open(filename_dates) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                [node_id, cit_date] = line.split()
                dates[int(node_id)] = datetime.strptime(cit_date, cls.DATE_FORMAT).date()
        return dates

    @classmethod
    def read_edges(cls, filename):
        """Read edges into list of tuples of ints"""
        edges = []
        with open(filename) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                [source_node, dest_node] = line.split()
                edges.append((int(source_node), int(dest_node)))
        return edges

    @staticmethod
    def split_to_timeslots(dates, edges, timeslots):
        slots = defaultdict(list)  # {slot : [edges]}
        for edge in edges:
            date_e = dates[edge[0]]
            # find slot
            i = 0
            n_slots = len(timeslots)
            while i < n_slots and date_e >= timeslots[i]:
                i += 1
            slots[timeslots[i - 1]].append(edge)
        return slots

    @classmethod
    def split_by_year(cls, dates, edges, write_to_file=False, base_filename=""):
        years = [date(year=y, month=01, day=01) for y in range(1992, 2004)]
        slots = cls.split_to_timeslots(dates, edges, years)
        lines = 0
        if write_to_file:
            for year in slots:
                with open(base_filename.replace('.txt', '-{}.edges'.format(year.year)), 'w') as fout:
                    for edge in slots[year]:
                        fout.write("{:07d}\t{:07d}\n".format(edge[0], edge[1]))
                        lines += 1
            print "Lines written", lines
        return slots

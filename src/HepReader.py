# -*- coding: utf-8 -*-


from datetime import date, datetime
from collections import defaultdict
from itertools import chain


class Node(object):
    def __init__(self, nid, ndate, communities):
        self.nid = nid
        self.communities = communities
        self.ndate = ndate
        self.roles = dict()


class HepReader(object):
    def __init__(self, filename_edges, filename_dates, filename_communities):
        self._stripped_11s = 0
        self._filename_edges = filename_edges
        self._filename_dates = filename_dates
        self.edges = self.read_edges(self._filename_edges)
        self.dates = self.read_dates(self._filename_dates)
        self.communities = self.read_communities(filename_communities)
        pass

    DATE_FORMAT = '%Y-%m-%d'

    def get_edges(self):
        return self.edges

    def get_nodes(self):
        """Return nodes as list of Node objects with dates and communities"""
        return {node_id: Node(node_id, self.dates[node_id], self.communities[node_id]) for node_id in self.dates}

    def get_nodes_from_edges_only(self):
        used_nodes = set(chain(*self.edges))
        return {node_id: Node(node_id, self.dates[node_id], self.communities[node_id])
                for node_id in self.dates if node_id in used_nodes}

    @staticmethod
    def get_for_year(year):
        return HepReader("datasets/hepth/timeslots/cit-HepTh-{}.edges".format(year),
                   "datasets/hepth/cit-HepTh.dates",
                   "datasets/hepth/communities/cit-HepTh-{}.communities".format(year))




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

    def clean_data(self, write_to_file=False):
        """Read data from raw file, remove 11s and duplicates, optionally write results to new file"""
        # read raw file line by line
        with open(self._filename_dates) as fnodes:
            nodes = [line.strip().split() for line in fnodes.readlines() if not line.startswith('#')]
        print "Raw nodes with dates: ", len(nodes)


        print "Raw edges: ", len(self.edges)

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

        nr_edges_raw = len(self.edges)
        edges = list(set([(int(e[0]), (e[1])) for e in self.edges]))
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
            with open(self._filename_dates.replace('.txt', '') + '-cleaned.txt', 'w') as fout:
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
        new_nodes_filename = self._filename_dates.replace('.txt', '.nodes')
        if write_to_file:
            with open(new_nodes_filename, 'w') as fout:
                for node_id in sorted(nodes_with_edges):
                    try:
                        node_date = dates[node_id]
                    except KeyError:
                        node_date = self._date_from_id(node_id)
                    fout.write("{:07d}\t{}\n".format(node_id, node_date))

                print "Nodes with dates writen to ", fout.name
                return fout.name
        return new_nodes_filename



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

    @classmethod
    def read_communities(cls, filename):
        """Read nodes with communities from file as dict: {node_id : [community_id]}"""
        communities = defaultdict(list)
        with open(filename) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                [node_id, community] = line.split()
                communities[int(node_id)].append(int(community))
        return communities


    def split_to_timeslots(self,timeslots):
        slots = defaultdict(list)  # {slot : [edges]}
        for edge in self.edges:
            date_e = self.dates[edge[0]]
            # find slot
            i = 0
            n_slots = len(timeslots)
            while i < n_slots and date_e >= timeslots[i]:
                i += 1
            slots[timeslots[i - 1]].append(edge)
        return slots

    def split_by_year(self, write_to_file=False, base_filename=""):
        years = [date(year=y, month=01, day=01) for y in range(1992, 2004)]
        slots = self.split_to_timeslots(years)
        lines = 0
        if write_to_file:
            for year in slots:
                with open(base_filename.replace('.txt', '-{}.edges'.format(year.year)), 'w') as fout:
                    for edge in slots[year]:
                        fout.write("{:07d}\t{:07d}\n".format(edge[0], edge[1]))
                        lines += 1
            print "Lines written", lines
        return slots

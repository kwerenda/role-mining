# -*- coding: utf-8 -*-

import snap
from datetime import date, datetime
from collections import defaultdict
from itertools import chain
from sys import stdout
from pprint import pprint


class HepReader:
    def __init__(self):
        self._stripped_11s = 0
        pass

    DATE_FORMAT = '%Y-%m-%d'


    @staticmethod
    def _date_from_id(node_id):
        node_id = str(node_id).rjust(7, '0')
        new_date = datetime.strptime(node_id[:4], "%y%m").date()
        year = int(node_id[:2])
        year = 1900 + year if year > 20 else 2000 + year
        # return date(year=year, month=int(node_id[2:4]), day=1)
        return new_date

    def _strip11s(self, node_id, date):
        node_id = node_id.lstrip('0')
        if node_id.startswith('11'):
            # some 11s might be misleading (eg 12/2001)
            if len(node_id) >= 7 or len(node_id) == 6 and date.year == 2000:
                node_id = node_id[2:]
                self._stripped_11s += 1
        return node_id

    def clean_data(self, filename_edges, filename_dates, print_results=False):
        """Read data from raw file, remove 11s and duplicates, optionally write results to new file"""
        # read raw file line by line
        with open(filename_dates) as fnodes:
            nodes = [line.strip().split() for line in fnodes.readlines() if not line.startswith('#')]
        print "Raw nodes with dates: ", len(nodes)

        with open(filename_edges) as fedges:
            edges = [line.strip().split() for line in fedges.readlines() if not line.startswith('#')]
        print "Raw edges: ", len(edges)

        # remove 11s
        cleaned_nodes = []
        for node in nodes:
            node_id = node[0].lstrip('0')
            cit_date = datetime.strptime(node[1], self.DATE_FORMAT).date()
            cleaned_node_id = self._strip11s(node_id, cit_date).rjust(7, '0')
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
            date = node[1]
            if node_id in dates:
                duplicates += 1
                if date != dates[node_id]:
                    dates[node_id] = min(dates[node_id], date)
                    different_date += 1
            else:
                dates[node_id] = date

        print "Nodes after removing duplicates: {} Removed: {}, duplicates: {}, inconsistencies: {}" \
            .format(len(dates.keys()), len(nodes) - len(dates.keys()), duplicates, different_date)

        # check for inconsistencies between id and date
        inconsistencies = 0
        for node_id in dates:
            date_from_id = self._date_from_id(node_id)
            if dates[node_id].year != date_from_id.year or dates[node_id].month != date_from_id.month:
                inconsistencies += 1
                # print "Inconsistent date, node id: {} date: {} date from id: {}".format(node_id, dates[node_id], date_from_id)

        print "Inconsistent dates: ", inconsistencies

        #print results to "cleaned" file
        if print_results:
            with open(filename_dates.replace('.txt', '') + '-cleaned.txt', 'w') as fout:
                for node_id, cit_date in sorted(dates.iteritems(), key=lambda e: e[1]):
                    fout.write("{}\t{}\n".format(str(node_id).rjust(7, '0'), cit_date))
                print "Written to ", fout.name

    def read_dates(self, filename_dates):
        """Read nodes with dates from file as dict: {node_id : date}"""
        dates = {}  # {node_id : year}
        with open(filename_dates) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                [node_id, date] = line.split()
                dates[int(node_id)] = date.strptime(date, self.DATE_FORMAT)
        return dates

    def read_edges(self, filename):
        """Read edges into list of tuples"""
        edges = []
        with open(filename) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                [source_node, dest_node] = line.split()
                source_node, dest_node = int(source_node), int(dest_node)
                edges.append((source_node, dest_node))
        return edges

    def split_to_timeslots(self, dates, edges, timeslots):
        slots = defaultdict(list)  # {slot : [edges]}
        for edge in edges:
            self._get_year(edge[0], dates, stdout)
            date = dates[edge[0]]

            # i = 0
            #
            # while date >= timeslots[i]:
            # i += 1
            # slots[timeslots[i-1]].append(edge)
            #
            for slot in reversed(timeslots):
                if date >= slot:
                    slots[slot].append(edge)
                    break
        return slots


    def split_to_time_slots_files(self, filename_edges, filename_dates):
        dates = self.read_dates(filename_dates)
        edges = self.read_edges(filename_edges)
        # time slots by years
        slots = defaultdict(list)  # {year : [ (source, target)]}
        with open("czasowy.txt", 'w') as infofile:
            for sourceNode, destNode in edges:
                year_source = self._get_year(sourceNode, dates, infofile)[0]
                slots[year_source].append("{0}\t{1}\n".format(sourceNode, destNode))


        for year in slots:
            with open("datasets/cit-HepTh/split/cit-HepTh-" + str(year) + ".edges", "w") as f:
                for line in slots[year]:
                    f.write(line)

        print u"Węzły występujące w edges, ale nie w pliku z datami: ", self._get_year.noDate
        print u"Węzły z przypisanym innym rokiem, niż ten który by wynikał z ich id: ", self._get_year.differentYear


        # read dates to memory
        # while reading edges assign to dffirent timeslots based on dates
        # optional - save each node to the separate file, as data file and graph file
        # create nodes for each graph


    def main(self):
        all_data = snap.LoadEdgeList(snap.PNGraph, "datasets/cit-HepTh/cit-HepTh.txt", 0, 1, '\t')  # traverse the nodes
        for NI in all_data.Nodes():
            print "node id %d with out-degree %d and in-degree %d" % (
                NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())
            # traverse the edges
            # for EI in allData.Edges():
            # print "edge (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
            # # traverse the edges by nodes
            # for NI in allData.Nodes():
            # for Id in NI.GetOutEdges():
            # print "edge (%d %d)" % (NI.GetId(), Id)
            # # allData = TNGraph.New()
            # #     TNGraph_Load


            # if __name__ == '__main__':
            # print("hello!")
            # # getMany()
            # # removeOnes("datasets/cit-HepTh/cit-HepTh-dates.txt")
            # # split_to_time_slots("datasets/cit-HepTh/cit-HepTh.txt", "datasets/cit-HepTh/cit-HepTh-dates-cleaned.txt")
            # clean_data("datasets/cit-HepTh/cit-HepTh.txt", "datasets/cit-HepTh/cit-HepTh-dates.txt")
            # print("bye!")



            #zrobic method chaining albo obiekt, na ktorym mozna wykonywac rozne przeksztalcenia
            #zapisuje i odczytuje z pliku

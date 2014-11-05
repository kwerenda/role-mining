# -*- coding: utf-8 -*-

import snap
from datetime import datetime
from collections import defaultdict
from itertools import chain
from sys import stdout


DATE_FORMAT = '%Y-%m-%d'


def detect_comunities(year, g):
    CmtyV = snap.TCnComV()
    modularity = snap.CommunityCNM(g, CmtyV)
    # for Cmty in CmtyV:
    # print ("Community: ")
    # for NI in Cmty:
    # print NI
    print("The modularity of the network in year {0} is {1}".format(year, modularity))


def detect_comunities_in_timeslots():
    base_filename = "datasets/cit-HepTh/split/cit-HepTh-"
    for year in range(1992, 2004):
        filename = base_filename + str(year) + '.txt'
        # g = snap.LoadEdgeList(snap.PNEANet, filename, 0, 1)
        g = snap.LoadEdgeList(snap.PUNGrah, filename, 0, 1)
        detect_comunities(year, g)


def clean_data(filename_edges, filename_dates):

    # read raw
    with open(filename_dates) as fnodes:
        nodes = [line.strip() for line in fnodes.readlines() if not line.startswith('#')]
    print "Raw nodes with dates: ", len(nodes)

    with open(filename_edges) as fedges:
        edges = [line.strip() for line in fedges.readlines() if not line.startswith('#')]
    print "Raw edges: ", len(edges)

    #   remove 11s
    nodes_without_11s = []
    s11 = 0
    for node in nodes:
        node_id, date = node.split()
        node_id = node_id.lstrip('0')
        date = datetime.strptime(date, DATE_FORMAT)
        if node_id.startswith('11'):
            if len(node_id) >= 7 or len(node_id) == 6 and date.year == 2000:
                s11 += 1
                node_id = node_id[2:].rjust(7, '0')
                nodes_without_11s.append(node_id + "\t" + node.split()[1])
        else:
            nodes_without_11s.append(node)
    removed = len(nodes) - len(nodes_without_11s)
    nodes = nodes_without_11s
    print "Nodes after removing 11s: ", len(nodes), " removed: ", removed, " affected: ", s11

    # search for duplicate or inconsitent dates
    different_date = 0
    duplicates = 0
    dates = {}  # {node_id : date}
    for node in nodes:
        [node_id, date] = node.split()
        date = datetime.strptime(date, DATE_FORMAT)
        node_id = int(node_id)
        if node_id in dates:
            duplicates += 1
            if dates[node_id] != date:
                # print "Different date for node: {}! In dict: {}, read: {}".format(node_id, dates[node_id], date)
                dates[node_id] = min(date, dates[node_id])
                different_date += 1
        else:
            dates[node_id] = date

    print "Nodes after removing duplicates: {} Removed: {}, duplicates: {}, inconsistencies: {}"\
        .format(len(dates.keys()), len(nodes) - len(dates.keys()), duplicates, different_date)

    with open(filename_dates.replace('.txt', '') + '-cleaned-dupl.txt', 'w') as fout:
        for node in nodes:
            fout.write(node + "\n")






def rewrite_dates_without_ones(filename):
    """Rewrite all entries to new file without leading 11s in ids"""
    with open(filename) as f, open(filename.replace('.txt', '') + '-cleaned.txt', 'w') as fout:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                new_line = line
            else:
                [node_id, date] = line.split()
                if node_id.startswith('11'):
                    node_id = node_id[2:]
                new_line = node_id + '\t' + date
            fout.write(new_line + '\n')


def read_dates(filename_dates):
    """Read nodes with dates from file as dict: {node_id : date}"""
    dates = {}  # {node_id : year}
    with open(filename_dates) as f:
        for line in f:
            if line.startswith('#'):
                continue
            [node_id, date] = line.split()
            dates[int(node_id)] = datetime.strptime(date, DATE_FORMAT)
    return dates

def read_edges(filename):
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


def _get_year_and_month(node_id):
    node_id = str.rjust(str(node_id), 7, '0')
    year = int(node_id[:2])
    year = 1900 + year if year > 20 else 2000 + year
    month = int(node_id[2:4])
    return year, month


def _get_year(node_id, dates, file_out):
    try:
        year = dates[node_id].year
    except KeyError:
        file_out.write(str(node_id) + " nie ma przypisanej daty! Generacja\n")
        year, month = _get_year_and_month(node_id)
        dates[node_id] = datetime(year=year, month=month, day=01)
        _get_year.noDate += 1
    # check if there are any discrepancies
    if dates[node_id].year != _get_year_and_month(node_id)[0]:
        file_out.write("Assumption error! For " + str(node_id) + " year is " + str(
            dates[node_id].year) + " and you think it's " + str(_get_year_and_month(node_id)[0]))
        _get_year.differentYear += 1
    return year


_get_year.noDate = 0
_get_year.differentYear = 0


def rewrite_dates_include_generated(filename_edges, filename_dates):
    edges = read_edges(filename_edges)
    dates = read_dates(filename_dates)

    with open(filename_dates.replace('.txt', '-all.txt')) as fout:
        unique_nodes_in_graph = set(chain(*edges))

        for node in set(chain(*edges)):  # all nodes
            date = _get_year(node, dates, stdout)
            # fout.




# def get_all_nodes(filename_edges):
#     graph = snap.LoadEdgeList(snap.PNGraph, filename_edges, 0, 1, '\t')
#     graph.



def split_to_time_slots(filename_edges, filename_dates):
    dates = read_dates(filename_dates)
    edges = read_edges(filename_edges)
    # time slots by years
    slots = defaultdict(list)  # {year : [ (source, target)]}
    with open("czasowy.txt", 'w') as infofile:
        for sourceNode, destNode in edges:
            year_source = _get_year(sourceNode, dates, infofile)
            slots[year_source].append("{0}\t{1}\n".format(sourceNode, destNode))

    # with open(filenameEdges) as f, open("czasowy.txt", 'w') as fout:
    #     for line in f:
    #         if line.startswith('#'):
    #             continue
    #         [sourceNode, destNode] = line.split()
    #         sourceNode, destNode = int(sourceNode), int(destNode)
    #         yearSource = _getYear(sourceNode, dates, fout)
    #         slots[yearSource].append(line)

    for year in slots:
        with open("datasets/cit-HepTh/split/cit-HepTh-" + str(year) + ".edges", "w") as f:
            for line in slots[year]:
                f.write(line)

    print u"Węzły występujące w edges, ale nie w pliku z datami: ", _get_year.noDate
    print u"Węzły z przypisanym innym rokiem, niż ten który by wynikał z ich id: ", _get_year.differentYear


    # read dates to memory
    # while reading edges assign to dffirent timeslots based on dates
    # optional - save each node to the separate file, as data file and graph file
    # create nodes for each graph


def main():
    all_data = snap.LoadEdgeList(snap.PNGraph, "datasets/cit-HepTh/cit-HepTh.txt", 0, 1, '\t')  # traverse the nodes
    for NI in all_data.Nodes():
        print "node id %d with out-degree %d and in-degree %d" % (
            NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())
        # traverse the edges
        # for EI in allData.Edges():
        # print "edge (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
        # # traverse the edges by nodes
        # for NI in allData.Nodes():
        #     for Id in NI.GetOutEdges():
        #         print "edge (%d %d)" % (NI.GetId(), Id)
        #         # allData = TNGraph.New()
        #         #     TNGraph_Load


if __name__ == '__main__':
    print("hello!")
    # getMany()
    # removeOnes("datasets/cit-HepTh/cit-HepTh-dates.txt")
    # split_to_time_slots("datasets/cit-HepTh/cit-HepTh.txt", "datasets/cit-HepTh/cit-HepTh-dates-cleaned.txt")
    clean_data("datasets/cit-HepTh/cit-HepTh.txt", "datasets/cit-HepTh/cit-HepTh-dates.txt")
    print("bye!")



#zrobic method chaining albo obiekt, na ktorym mozna wykonywac rozne przeksztalcenia
#zapisuje i odczytuje z pliku
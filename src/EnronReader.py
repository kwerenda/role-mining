# -*- coding: utf-8 -*-

from graph_tool.all import *
from collections import Counter
import pylab as P
from math import isnan
import csv

class Network(object):
    def __init__(self, filename):
        from_file = self.read_timeslot(filename)

        self.graph = from_file[0]
        self.label2index = from_file[1]
        self.label = from_file[2]
        self.communities = from_file[3]

    def add_vertex(self, v_label, label2index, label, graph):
        if v_label not in label2index:
            v = graph.add_vertex()
            label2index[v_label] = v
            label[v] = v_label
        return label2index, label, graph

    def read_timeslot(self, filename):
        dataset_path = "../datasets/enron/timeslots/"
        community_path = "../datasets/enron/communities/"

        g = Graph()
        label = g.new_vertex_property("int32_t")
        community = g.new_vertex_property("int32_t")
        label2index = dict()
        
        with open(dataset_path + filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                v1_label, v2_label = int(row[0]), int(row[1])
                
                self.add_vertex(v1_label, label2index, label, g)
                self.add_vertex(v2_label, label2index, label, g)
                
                v1, v2 = label2index[v1_label], label2index[v2_label]
                g.add_edge(v1, v2)
        
        with open(community_path + filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == "Id":
                    continue

                v_label, comm = int(row[0]), int(row[1])
                v = label2index[v_label]
                community[v] = comm

        return g, label2index, label, community

def filter_community(community_label, community_pmap, g):
    in_group = g.new_vertex_property("bool")
    for v in g.vertices():
        if community_pmap[v] == community_label:
            in_group[v] = True
        else:
            in_group[v] = False
    return in_group

def plot_hist(data):
    # P.hist(data, bins=50, range=(0, 1))
    P.hist(data, bins=50)
    # P.xscale('log')
    # P.yscale('log', nonposy='clip')


def filtered(data, size):
    # data = [x for x in data if x != 0]
    # if len(data) > size:
    #     data = data[:size]
    return sorted(data, reverse=True)[:size]
    # return data

if __name__ == '__main__':

    timeslot = "4-2001.csv"
    community_nr = 16 # (20, 1156), (3, 930), (12, 859), (15, 763), (62, 756), (17, 530), (16, 472)
    comm_size = 472

    N = Network(timeslot)#.read_timeslot("10-2001.csv")
    print "Loaded"


    print Counter(N.communities.get_array().tolist()).most_common(30)

    group_filter = filter_community(community_nr, N.communities, N.graph)

    N.graph.set_vertex_filter(group_filter)



    closeness = graph_tool.centrality.closeness(N.graph).get_array().tolist()

    max_eigenval, eigenvec = graph_tool.centrality.eigenvector(N.graph)
    # eigenvector = [x/max_eigenval for x in eigenvec.get_array().tolist()]  #normalize!
    eigenvector = eigenvec.get_array().tolist()

    betw, _edges = graph_tool.centrality.betweenness(N.graph, norm=True)
    betweenness = betw.get_array().tolist()


    P.suptitle("Centrality measures for community nr {} in 1997".format(community_nr))
    # P.figure()

    #CZYM JEST NAN W CLOSENESS?


    print "nans", len([x for x in closeness if isnan(x)])
    closeness = [0 if isnan(x) else x for x in closeness]
    # closeness = [x for x in closeness if not isnan(x)]
    closeness = filtered(closeness, comm_size)
    print "closeness", closeness
    print "non zeros", len([x for x in closeness if x != 0])
    P.subplot(2, 2, 1)

    plot_hist(closeness)
    P.xlabel("Closeness centrality")
    P.ylabel("Number of nodes (total={})".format(len(closeness)))

    # pagrerank = filtered(pagerank, comm_size)
    # print "pagerank", pagerank
    # P.subplot(2, 2, 2)
    # plot_hist(pagerank)
    # P.xlabel("Pagerank centrality")
    # P.ylabel("Number of nodes (total={})".format(len(pagerank)))

    counts, degrees = vertex_hist(N.graph, "in", float_count=False)
    print "counts : ", len(counts), counts
    print "degrees: ", len(degrees), degrees
    counts = list(counts)
    counts.append(0)
    P.subplot(2, 2, 2)
    P.bar(degrees, counts, align='center', color="#348ABD")
    # P.hist(counts, bins=degrees, )
    P.xlabel("Degree centrality (in)")
    P.ylabel("Number of nodes (total={})".format(sum(counts)))
    P.xlim(0, max(degrees))

    betweenness = filtered(betweenness, comm_size)
    print "betweenness", betweenness
    P.subplot(2, 2, 3)
    plot_hist(betweenness)
    P.xlabel("Betweenness centrality")
    P.ylabel("Number of nodes (total={})".format(len(betweenness)))


    eigenvector = filtered(eigenvector, comm_size)
    print "eigenvector", eigenvector
    P.subplot(2, 2, 4)
    plot_hist(eigenvector)
    P.xlabel("Eigenvector centrality")
    P.ylabel("Number of nodes (total={})".format(len(eigenvector)))




    P.show()

    
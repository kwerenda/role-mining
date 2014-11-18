# -*- coding: utf-8 -*-

from graph_tool.all import *
from collections import Counter
import pylab as P
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

if __name__ == '__main__':
    N = Network("10-2001.csv")#.read_timeslot("10-2001.csv")
    print "Loaded"

    # print Counter(N.communities.get_array().tolist())

    group_filter = filter_community(2, N.communities, N.graph)

    N.graph.set_vertex_filter(group_filter)

    # pagerank = graph_tool.centrality.pagerank(N.graph).get_array().tolist()
    # print "pagerank"

    # P.figure()
    # P.hist(pagerank)
    # P.xscale('log')
    # P.yscale('log')
    # P.show()

    betw, _edges = graph_tool.centrality.betweenness(N.graph)
    betweenness = betw.get_array().tolist()
    print "betweenness"
    
    P.figure()
    P.hist(betweenness)
    P.xscale('log')
    P.yscale('log')
    P.show()

    # closeness = graph_tool.centrality.closeness(N.graph).get_array().tolist()
    # print "closeness"
    # print Counter(closeness)

    # P.figure()
    # P.hist(closeness)
    # P.xscale('log')
    # P.yscale('log')
    # P.show()

    # _eigenval, eigenvec = graph_tool.centrality.eigenvector(N.graph)
    # eigenvector = eigenvec.get_array().tolist()
    # print "eigenvector"
    
    # P.figure()
    # P.hist(eigenvector)
    # P.xscale('log')
    # P.yscale('log')
    # P.show()
    
    
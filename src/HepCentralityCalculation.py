
from HepReader import HepReader
from graph_tool.all import *
from collections import Counter
import pylab as P

class Network(object):
    def __init__(self, edges, nodes):
        new_struct = self.from_hep(edges, nodes)

        self.graph = new_struct[0]
        self.label2index = new_struct[1]
        self.label = new_struct[2]
        self.communities = new_struct[3]

    def add_vertex(self, v_label, v_comm, label2index, label, community, graph):
        if v_label not in label2index:
            v = graph.add_vertex()
            label2index[v_label] = v
            label[v] = v_label
            community[v] = v_comm
        return label2index, label, graph

    def from_hep(self, edges, nodes):

        g = Graph()
        label = g.new_vertex_property("int32_t")
        community = g.new_vertex_property("int32_t")
        label2index = dict()

        for v1_label, v2_label in edges:
            v1_comm, v2_comm = nodes[v1_label].communities[0], nodes[v2_label].communities[0]

            self.add_vertex(v1_label, v1_comm, label2index, label, community, g)
            self.add_vertex(v2_label, v2_comm, label2index, label, community, g)
            
            v1, v2 = label2index[v1_label], label2index[v2_label]
            g.add_edge(v1, v2)

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

    hp = HepReader.get_for_year(1997)
    nodes = hp.get_nodes()
    edges = hp.get_edges()

    N = Network(edges, nodes)

    group_filter = filter_community(4, N.communities, N.graph) # hardcode, 4 is the biggest group for 1997

    N.graph.set_vertex_filter(group_filter)

    pagerank = graph_tool.centrality.pagerank(N.graph).get_array().tolist()
    print "pagerank"

    size_dist = Counter(pagerank)
    print size_dist.most_common(50)

    x = sorted(size_dist.keys())
    y = [size_dist[v] for v in x]

    P.figure()
    P.bar(x, y, align='center')
    P.xlabel("Size of community [members]")
    P.ylabel("Number of communities")
    P.suptitle("Year {}\nNon-overlapping community size distribution".format(1997))
    P.xscale('log')
    P.show()


    P.figure()
    P.hist(pagerank)
    # P.xscale('log')
    # P.yscale('log')
    P.show()

    # betw, _edges = graph_tool.centrality.betweenness(N.graph)
    # betweenness = betw.get_array().tolist()
    # print "betweenness"
    
    # P.figure()
    # P.hist(betweenness)
    # # P.xscale('log')
    # # P.yscale('log')
    # P.show()

    # # closeness = graph_tool.centrality.closeness(N.graph).get_array().tolist()
    # # print "closeness"
    # # print Counter(closeness)

    # # P.figure()
    # # P.hist(closeness)
    # # # P.xscale('log')
    # # # P.yscale('log')
    # # P.show()

    # _eigenval, eigenvec = graph_tool.centrality.eigenvector(N.graph)
    # eigenvector = eigenvec.get_array().tolist()
    # print "eigenvector"
    
    # P.figure()
    # P.hist(eigenvector)
    # # P.xscale('log')
    # # P.yscale('log')
    # P.show()
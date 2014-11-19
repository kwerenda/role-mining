
from HepReader import HepReader
from graph_tool.all import *
from collections import Counter
import pylab as P
from math import isnan

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

    hp = HepReader.get_for_year(1997)
    nodes = hp.get_nodes()
    edges = hp.get_edges()

    N = Network(edges, nodes)

    # z palca z tmp1997!
    # c = (4, 665)
    # c = (46, 117)
    # c = (7, 262)
    # c = (58, 91)
    c = (50, 413)

    community_nr = c[0]
    comm_size = c[1]

    group_filter = filter_community(community_nr, N.communities, N.graph) # hardcode, 4 is the biggest group for 1997

    N.graph.set_vertex_filter(group_filter)

    # pagerank = graph_tool.centrality.pagerank(N.graph).get_array().tolist()

    closeness = graph_tool.centrality.closeness(N.graph).get_array().tolist()

    max_eigenval, eigenvec = graph_tool.centrality.eigenvector(N.graph)
    # eigenvector = [x/max_eigenval for x in eigenvec.get_array().tolist()]  #normalize!
    eigenvector = eigenvec.get_array().tolist()

    betw, _edges = graph_tool.centrality.betweenness(N.graph, norm=True)
    betweenness = betw.get_array().tolist()


    # print "pagerank"
    # print pagerank



    # size_dist = Counter(pagerank)
    # print size_dist.most_common(50)
    #
    # x = sorted(size_dist.keys())
    # y = [size_dist[v] for v in x]
    #




    P.suptitle("Centrality measures for community nr {} in 1997".format(community_nr))
    # P.figure()

    #CZYM JEST NAN W CLOSENESS?

    closeness = [0 if isnan(x) else x for x in closeness]
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

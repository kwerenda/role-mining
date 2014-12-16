import networkx as nx
from itertools import combinations
from Network import Network
from pprint import pprint

class XNetwork(object):
    """Yet another Network class, this time based on NetworkX"""
    def __init__(self, edges_file, communities_file=None, use_communities=True):
        self.graph = nx.read_edgelist(edges_file, create_using=nx.MultiGraph(), nodetype=int)
        if use_communities:
            if communities_file:
                comms = Network.get_communities_from_cf(communities_file)
                self.create_communities(comms)



    def create_communities(self, communities_list):
        for node in self.graph.nodes():
            self.graph.add_node(node, comm=set())
        # pprint(self.graph.nodes(data=True))
        for node, community in communities_list:
            self.graph.node[node]['comm'].add(community)


    def shortest_paths(self, v1, v2):
        try:
            l = nx.shortest_path_length(self.graph, v1, v2)
            paths = nx.all_shortest_paths(self.graph, v1, v2)
        except:
            paths = []
        return paths
        # try:
        #     return
        # except: # nx.NetworkXNoPath:
        # # except nx.NetworkXNoPath:
        #     return []


    def calculate_CBC(self, is_directed=True):
        """Calculate CBC for all nodes in network"""
        g = self.graph
        for node in g.nodes():
            g.add_node(node, cbc=0)   # initialise cdc = 0 for each node

        for v1, v2 in combinations(g.nodes(), 2):
            print "calculating for ", v1, "and", v2
            comms1 = g.node[v1]['comm']
            comms2 = g.node[v2]['comm']
            if comms1 and comms2 and comms1.isdisjoint(comms2):   # they are not the same community
                for path in self.shortest_paths(v1, v2):
                    for v in path[1:-1]:
                        g.node[v]['cbc'] += 1

        return sorted([[node, g.node[node]['cbc']] for node in g.nodes()], reverse=True, key=lambda e: e[1]);
        # if not is_directed:
        #     for v in self.graph.vertices():
        #         self.graph.vp['CDC'][v] /= 2




        #
        # cdc = self.graph.new_vertex_property('int32_t')
        # self.graph.vertex_properties['CDC'] = cdc
        # #set all to 0
        # for v in self.graph.vertices():
        #         self.graph.vp['CDC'][v] = 0
        #
        # # dla kazdej pary wezlow w grafie - (kolejnosc ma znaczenie w skierowanych)
        # for v1, v2 in product(self.graph.vertices(), self.graph.vertices()):
        #     v1_lab, v2_lab = self.label2index[v1], self.label2index[v2]
        #
        #     # jezeli community (c1) != commmunity (C2)
        #     if set(self.communities[v1_lab]).isdisjoint(set(self.communities[v2_lab])):
        #         #   dla kazdej najkrotszej sciezki p od c1 do c2
        #         for path in self.shortest_paths2(v1, v2):
        #             for v in path:
        #                 self.graph.vp['CDC'][v] += 1
        #
        # if not is_directed:
        #     for v in self.graph.vertices():
        #         self.graph.vp['CDC'][v] /= 2
        #
        #
        #

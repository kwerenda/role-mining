import networkx as nx
from itertools import combinations
from Network import Network
from pprint import pprint
from collections import defaultdict

class XNetwork(object):
    """Yet another Network class, this time based on NetworkX"""
    def __init__(self, edges_file, communities_file=None, use_communities=True):
        self.graph = nx.read_edgelist(edges_file, create_using=nx.MultiGraph(), nodetype=int)
        if use_communities:
            self.communities = defaultdict(set)
            if communities_file:
                comms = Network.get_communities_from_cf(communities_file)
                self.create_communities(comms)



    def create_communities(self, communities_list):

        for node in self.graph.nodes():
            self.graph.add_node(node, comm=set())
        # pprint(self.graph.nodes(data=True))
        for node, community in communities_list:
            self.graph.node[node]['comm'].add(community)
            self.communities[community].add(node)


    def shortest_paths(self, v1, v2):
        try:
            l = nx.shortest_path_length(self.graph, v1, v2)
            paths = nx.all_shortest_paths(self.graph, v1, v2)
        except:
            paths = []
        return paths

    def calculate_CBC(self, is_directed=False):
        """Calculate CBC for all nodes in network"""
        g = self.graph
        for node in g.nodes():  # initialise cdc = 0 for each node
            g.add_node(node, nbc=0)
            g.add_node(node, ds_count=set())

        for v1, v2 in combinations(g.nodes(), 2):
            # print "calculating for ", v1, "and", v2
            communities1, communities2 = g.node[v1]['comm'], g.node[v2]['comm']
            if communities1 and communities2 and communities1.isdisjoint(communities2):   # they are not the same community
                for path in self.shortest_paths(v1, v2):
                    for v in path[1:-1]:
                        g.node[v]['nbc'] += 1.0/min([len(self.communities[x]) for x in communities1.union(communities2)])
                        g.node[v]['ds_count'].update(communities1.union(communities2))

        mediator_score = [[node, g.node[node]['nbc']*len(g.node[node]['ds_count'])] for node in g.nodes()]
        score_sum = sum([x[1] for x in mediator_score])
        norm_ms = [[node, score/score_sum] for node, score in mediator_score]
        return sorted(norm_ms, reverse=True, key=lambda e: e[1])

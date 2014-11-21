
from collections import defaultdict
from HepReader import Node

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

Roles = enum("OUTSIDER", "LEADER", "OUTERMOST", "MEDIATOR")





class RoleMining(object):

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.communities = defaultdict(list) # {com_id : lista nodow}
        for node in self.nodes.values():
            for c in node.communities:
                self.communities[c].append(node)


    # def calculate_degree_centrality(self):
    #     pass
    #

    def create_communities_graphs(self):
        """Creates snap graphs from communities. Only edges between members of same commmunities are preserved"""
        pass
        # tu tworz graph-tool graf

    def calculate_betweenness_centrality(self):
        pass

    def caluculate_centrality(self):
        pass
        # for all communities
        # CloseCentr = snap.GetClosenessCentr(UGraph, NI.GetId())
        # print "node: %d centrality: %f" % (NI.GetId(), CloseCentr)

    def find_outsiders(self):
        for comm in sorted(self.communities.values(), key=len):
            print len(comm)
            if len(comm) == 1:
                print "outsider: ", comm[0]



        # g = snap.LoadEdgeList(snap.PNGraph, "/Users/bogna/dev/role-mining/datasets/hepth/timeslots/cit-HepTh-1992.edges", 0, 1, '\t')
        # snap.TNGraph()
        #
        # for NI in g.Nodes():
        #     print "node id %d with out-degree %d and in-degree %d" % (
        #         NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())
            # snap.TNGraph




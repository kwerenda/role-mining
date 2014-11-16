
import snap

class RoleMining(object):

    def __init__(self):
        pass

    def find(self):

        g = snap.LoadEdgeList(snap.PNGraph, "/Users/bogna/dev/role-mining/datasets/cit-HepTh/split/cit-HepTh-1992.edges", 0, 1, '\t')
        snap.TNGraph()

        for NI in g.Nodes():
            print "node id %d with out-degree %d and in-degree %d" % (
                NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())
            # snap.TNGraph




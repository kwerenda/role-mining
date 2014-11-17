from src.HepReader import HepReader
from src.RoleMining import RoleMining
import snap
import os

if __name__ == '__main__':


    hp = HepReader.get_for_year(1992)
    nodes = hp.get_nodes()
    edges = hp.get_edges()

    rm = RoleMining(nodes, edges)

    rm.find_outsiders()

        # hp.detect_communities()
    # g = snap.TNGraph( hp.edges)
    # for NI in g.Nodes():
    #          print "node id %d with out-degree %d and in-degree %d" % (
    #              NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())


from src.HepReader import HepReader
from src.RoleMining import RoleMining
import snap
import os

if __name__ == '__main__':

    base = "/Users/bogna/dev/role-mining/datasets/cit-HepTh/split/cit-HepTh-"
    for year in range(1994, 2004):
        filename = base + "{}[Nodes].csv".format(year)
        print year
        os.rename(filename, base + "{}.communities".format(year))



        # hp = HepReader("/Users/bogna/dev/role-mining/datasets/cit-HepTh/split/cit-HepTh-{}.edges".format(year), "/Users/bogna/dev/role-mining/datasets/cit-HepTh/cit-HepTh-dates.nodes")
        # hp.detect_communities()
    # g = snap.TNGraph( hp.edges)
    # for NI in g.Nodes():
    #          print "node id %d with out-degree %d and in-degree %d" % (
    #              NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())


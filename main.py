from src.Network import Network
from src import Plotter
import pylab as P
import matplotlib
from src.Reader import EnronReader

if __name__ == '__main__':
    min_days = 3
    for month in range(1, 13):
        e = EnronReader("datasets/enron/timeslots/{:02d}.edges".format(month))
        e.filter(min_days)
        e.write_filtered()

    # Plotter.plot_community_sizes(1997)


    #
    # N1 = Network('datasets/enron/timeslots/10-1999.edges')
    #
    # N2 = Network('datasets/hepth/timeslots/cit-HepTh-1999.edges',
    #              'datasets/hepth/communities/cit-HepTh-1999.communities')
    # k = 3
    # com_nr = 1
    # n = Network("datasets/enron/timeslots/08.edges", k=k)
    #             # "datasets/enron/communities/8-2001/k={}/directed_communities".format(k))
    #
    # n.filter_community(com_nr)
    #
    # Plotter.plot_centralities(n, title="Centrality measures for Enron 8-2001\nk={}, community nr {}".format(k, com_nr))

    #
    # N1.print_communities()
    # N2.print_communities()

    # print N1.graph.num_vertices(), N1.graph.num_edges()
    #
    # N1.filter_community(2)
    #
    # print N1.graph.num_vertices(), N1.graph.num_edges()
    #
    # plot_centralities(N1)
    #
    # N1.unfilter_graph()
    #
    # print N1.graph.num_vertices(), N1.graph.num_edges()

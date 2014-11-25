from src.Network import Network
from src.Plotter import plot_centralities

if __name__ == '__main__':

    N1 = Network('datasets/enron/timeslots/10-1999.edges')

    N2 = Network('datasets/hepth/timeslots/cit-HepTh-1999.edges',
                 'datasets/hepth/communities/cit-HepTh-1999.communities')

    N1.print_communities()
    N2.print_communities()

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
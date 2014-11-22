from src.Network import Network
from src.Plotter import plot_centralities

if __name__ == '__main__':

    N1 = Network('datasets/enron/timeslots/10-1999.edges',
                 'datasets/enron/communities/10-1999.communities')

    N2 = Network('datasets/hepth/timeslots/cit-HepTh-1999.edges',
                 'datasets/hepth/communities/cit-HepTh-1999.communities')

    print N1.graph.num_vertices(), N1.graph.num_edges()

    N1.filter_community(16)

    print N1.graph.num_vertices(), N1.graph.num_edges()

    plot_centralities(N2)

    N1.unfilter_graph()


    # hp = HepReader.get_for_year(1992)
    # nodes = hp.get_nodes()
    # edges = hp.get_edges()
    #
    # rm = RoleMining(nodes, edges)
    #
    # rm.find_outsiders()


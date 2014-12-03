from src.Network import Network
from src.RoleMining import RoleMining
from src import Plotter
import math
import pylab as P


def mine(month, com):
    N1 = Network('datasets/enron/timeslots/{:02d}-filtered2.edges'.format(month))
    N1.print_communities()
    N1.filter_community(com)
    R = RoleMining(N1)
    outsiders, leaders, outermosts = R.find_roles()
    clos = [x for x in R.closeness if not math.isnan(x)]
    Plotter.plot_fit_and_tails(clos, title="Leaders and outermosts, Enron\nmonth {}, community {}".format(month, com))
    P.savefig("/Users/bogna/Documents/ED/projekt/04/enron{}_{}.png".format(month, com))
    return R


if __name__ == '__main__':
    mine(12, 3)


    # N1 = Network('datasets/enron/timeslots/03-filtered2.edges')
    # N1.print_communities()
    # N1.filter_community(0)
    # R = RoleMining(N1)
    # outsiders, leaders, outermosts = R.find_roles()
    # print outsiders, leaders, outermosts

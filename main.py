from src.Network import Network
from src.RoleMining import RoleMining

if __name__ == '__main__':

    N1 = Network('datasets/enron/timeslots/03-filtered2.edges')
    N1.print_communities()
    N1.filter_community(0)
    R = RoleMining(N1)
    outsiders, leaders, outermosts = R.find_roles()
    print outsiders, leaders, outermosts
from collections import defaultdict
from src.Network import Network
from src.XNetwork import XNetwork
from src.RoleMining import RoleMining
from src import Plotter
import Reader
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
    # mine(12, 3)


    month = 12
    n = XNetwork("datasets/enron/timeslots/{:02d}-filtered2.edges".format(month),
                 communities_file="datasets/enron/communities/{:02d}-filtered2/k=3/directed_communities".format(month))
    nodes_with_cbc = n.calculate_CBC()

    cbc_by_node = {nid: cbc for nid, cbc in nodes_with_cbc}

    guys_tuples = Reader.read_lines("datasets/enron/enron_guys.txt")
    guys = {int(nid): email for nid, email in guys_tuples}
    guys_by_email = {email: int(nid) for nid, email in guys_tuples}

    all_cdc = cbc_by_node.values()
    P.hist(all_cdc)
    P.title("Enron - Mediator score distribution in month {}".format(month))
    P.xlabel("Mediator score")
    P.ylabel("Frequency")
    P.show()

    important_emails = [
        "jeff.dasovich@enron.com",
        "susan.scott@enron.com",
        "stanley.horton@enron.com",
        "kenneth.lay@enron.com",
        "mary.hain@enron.com",
        "d..steffes@enron.com",
        "k..allen@enron.com",
        "john.zufferli@enron.com",
        "kam.keiser@enron.com",
        "m..presto@enron.com",
        "jeff.skilling@enron.com",
        "e..haedicke@enron.com",
        "danny.mccarty@enron.com",
        "chris.dorland@enron.com",
        "barry.tycholiz@enron.com",
        "j..kean@enron.com",
        "shelley.corman@enron.com",
        "j.kaminski@enron.com",
        "louise.kitchen@enron.com",
        "steven.harris@enron.com",
        "mark.whitt@enron.com",
        "drew.fossum@enron.com",
        "gerald.nemec@enron.com",
        "sally.beck@enron.com",
        "tori.kuykendall@enron.com",
        "john.arnold@enron.com",
        "mike.grigsby@enron.com",
        "tana.jones@enron.com",
        "elizabeth.sager@enron.com",
        "kay.mann@enron.com",
        "bill.williams@enron.com",
        "kim.ward@enron.com",
        "stacy.dickson@enron.com",
        "kate.symes@enron.com",
        "lavorato@enron.com",
        "taylor@enron.com",
        "jason.williams@enron.com",
        "kimberly.watson@enron.com",
        "s..shively@enron.com",
        "mike.swerzbin@enron.com",
        "diana.scholtes@enron.com",
        "teb.lokey@enron.com",
        "rod.hayslett@enron.com",
        "james.derrick@enron.com",
        "scott.neal@enron.com",
        "michelle.lokay@enron.com",
        "paul.y.barbo@enron.com"
    ]
for email in important_emails:
    try:
        print "{}\t{:.4f}".format(email, cbc_by_node[guys_by_email[email]])
    except KeyError:
        print "{}\tX".format(email)

i = 0
print "month", month
print "-----------------------------------"
print "rank\tnode_id\temail\tMS"
print "-----------------------------------"
for n, cbc in nodes_with_cbc:
    i += 1
    if guys[n] not in important_emails:
        print "{}\t{}\t{}\t{:.4f}".format(i, n, guys[n], cbc)



    # n.print_communities()
    # print "Whole network: ", n.graph.num_vertices()
    # n.get_mediators()

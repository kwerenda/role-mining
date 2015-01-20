from collections import defaultdict
from src import Reader
from src.Network import Network, flatten_list
from src.XNetwork import XNetwork
from src.RoleMining import RoleMining
import src.Plotter
from numpy import mean, std
import networkx as nx
import pylab as P

the_lads = ['jeff.dasovich@enron.com', 'mary.hain@enron.com', 'shelley.corman@enron.com', 'louise.kitchen@enron.com', 'a..shankman@enron.com', 'barry.tycholiz@enron.com', 'tana.jones@enron.com', 'john.arnold@enron.com', 'lavorato@enron.com', 'greg.whalley@enron.com', 'd..steffes@enron.com', 'e..haedicke@enron.com', 'stanley.horton@enron.com', 'richard.shapiro@enron.com', 'andy.zipper@enron.com', 'scott.neal@enron.com', 'kenneth.lay@enron.com', 'sally.beck@enron.com', 'john.griffith@enron.com', 'jonathan.mckay@enron.com', 'kimberly.watson@enron.com']
the_losers = ['kam.keiser@enron.com', 'kevin.hyatt@enron.com', 'theresa.staab@enron.com', 'stephanie.panus@enron.com', 'mary.hain@enron.com', 'dan.hyvl@enron.com', 'lynn.blair@enron.com', 'kate.symes@enron.com', 'rosalee.fleming@enron.com', 'm..forney@enron.com', 'elizabeth.sager@enron.com', 'darrell.schoolcraft@enron.com', 'shelley.corman@enron.com', 'juan.hernandez@enron.com', 'joe.stepenovitch@enron.com', 'barry.tycholiz@enron.com', 'tori.kuykendall@enron.com', 'john.arnold@enron.com', 'susan.scott@enron.com', 'kay.mann@enron.com', 'drew.fossum@enron.com', 'jason.williams@enron.com', 'stanley.horton@enron.com', 'sara.shackleton@enron.com', 'michelle.lokay@enron.com', 'mark.mcconnell@enron.com', 'gerald.nemec@enron.com', 'debra.perlingiere@enron.com', 'mark.whitt@enron.com', 'cara.semperger@enron.com', 'charles.weldon@enron.com', 'errol.mclaughlin@enron.com', 'john.griffith@enron.com', 'chris.germany@enron.com', 'chris.dorland@enron.com', 'paul.y.barbo@enron.com', 'rick.buy@enron.com']

superpapers = [9711165, 9908142, 9906064, 9905111, 0005016, 5016, 9711200, 9802150, 9802109, 9905221, 9711162, 9803315]

def get_leaders_and_outermosts():
    guys = Reader.read_lines("datasets/enron/enron_guys.txt")
    guys = {int(nid) : email for nid, email in guys}

    global_leaders, global_outermosts = defaultdict(list), defaultdict(list)
    for month in xrange(1, 13):
        n = Network('datasets/enron/timeslots/{:02d}-filtered2.edges'.format(month),
                    is_directed=False,
                    use_communities=True)
        communities = set(flatten_list(n.communities.values()))
        month_leaders, month_outermosts = set(), set()
        for c in communities:
            n.filter_community([c])
            leaders, outermosts = RoleMining(n).find_roles()
            [month_leaders.add(leader) for leader in leaders]
            [month_outermosts.add(outer) for outer in outermosts]
            n.unfilter_graph()

        for l, c in month_leaders:
            global_leaders[l].append((month,c))
        for o, c in month_outermosts:
            global_outermosts[o].append((month, c))

    print
    for id, months in global_outermosts.items():
        if guys[id] in the_losers:
            print guys[id], months

def get_mediator_score_distribution():
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

    interesting_emails = [
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
    for email in interesting_emails:
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
        if guys[n] not in interesting_emails:
            print "{}\t{}\t{}\t{:.4f}".format(i, n, guys[n], cbc)

if __name__ == '__main__':
    get_mediator_score_distribution()
    

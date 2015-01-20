#!/usr/bin/env python

# -*- coding: utf-8 -*-

from datetime import datetime

import pylab as P
from src.Reader import HepReader
from src.RoleMining import RoleMining
from collections import Counter
from graph_tool import centrality, stats
from math import isnan
import matplotlib
import numpy as np
import matplotlib.mlab as mlab


def plot_hist(data):
    P.hist(data, bins=50)


def _filtered(data, size):
    return sorted(data, reverse=True)[:size]


def plot_fit_and_tails(closeness, title):
    """Plot closeness centrality distribution, fit Gauss and mark outermosts and leaders areas in plot"""
    P.suptitle(title)
    m, sd = np.mean(closeness), np.std(closeness)
    outer = m - sd
    if outer > 0:
        P.axvspan(0, outer, alpha=0.2, color='c', label="Outermosts")
    leaders = m + sd
    if leaders < 1:
        P.axvspan(leaders, 0.2, alpha=0.2, color='y', label="Leaders")
    P.hist(closeness, color='#AB717A')
    x = np.linspace(0, 0.2)
    P.plot(x, mlab.normpdf(x, m, sd), '--', color='k')
    # P.xticks(np.arange(0, 0.2, 0.01))
    P.legend()
    # P.xlim([0, 1])


def plot_directed_centralities(pr, auth, ev, katz, comm_size, comm_nr):
    """Plot different centrality metrics in one figure"""
    P.suptitle("Centralities for community nr: " + str(comm_nr))

    pagerank = _filtered(pr.values(), comm_size)
    P.subplot(2, 2, 1)
    plot_hist(pagerank)
    P.xlabel("Pagerank centrality")
    P.ylabel("Number of nodes (total={})".format(len(pagerank)))

    authority = _filtered(auth.values(), comm_size)
    P.subplot(2, 2, 2)
    plot_hist(authority)
    P.xlabel("Authority centrality")
    P.ylabel("Number of nodes (total={})".format(len(authority)))

    kz= _filtered(katz.values(), comm_size)
    P.subplot(2, 2, 3)
    plot_hist(kz)
    P.xlabel("Katz centrality")
    P.ylabel("Number of nodes (total={})".format(len(kz)))

    eigenvector = _filtered(ev.values(), comm_size)
    P.subplot(2, 2, 4)
    plot_hist(eigenvector)
    P.xlabel("Eigenvector centrality")
    P.ylabel("Number of nodes (total={})".format(len(eigenvector)))

    P.show()


def plot_centralities(network, title="Centrality measures"):
    g = network.graph
    comm_size = g.num_vertices()

    closeness = centrality.closeness(g).get_array().tolist()

    max_eigenval, eigenvec = centrality.eigenvector(g)
    # eigenvector = [x/max_eigenval for x in eigenvec.get_array().tolist()]  #normalize!
    eigenvector = eigenvec.get_array().tolist()

    betw, _edges = centrality.betweenness(g, norm=True)
    betweenness = betw.get_array().tolist()

    P.suptitle(title)
    # P.figure()
    print "nans", len([x for x in closeness if isnan(x)])
    closeness = [0 if isnan(x) else x for x in closeness]
    # closeness = [x for x in closeness if not isnan(x)]
    closeness = _filtered(closeness, comm_size)
    print "closeness", closeness
    print "non zeros", len([x for x in closeness if x != 0])
    P.subplot(2, 2, 1)

    plot_hist(closeness)
    P.xlabel("Closeness centrality")
    P.ylabel("Number of nodes (total={})".format(len(closeness)))

    counts, degrees = stats.vertex_hist(g, "in", float_count=False)
    print "counts : ", len(counts), counts
    print "degrees: ", len(degrees), degrees
    counts = list(counts)
    counts.append(0)
    P.subplot(2, 2, 2)
    P.bar(degrees, counts, align='center', color="#348ABD")
    # P.hist(counts, bins=degrees, )
    P.xlabel("Degree centrality (in)")
    P.ylabel("Number of nodes (total={})".format(sum(counts)))
    P.xlim(0, max(degrees))

    betweenness = _filtered(betweenness, comm_size)
    print "betweenness", betweenness
    P.subplot(2, 2, 3)
    plot_hist(betweenness)
    P.xlabel("Betweenness centrality")
    P.ylabel("Number of nodes (total={})".format(len(betweenness)))

    eigenvector = _filtered(eigenvector, comm_size)
    print "eigenvector", eigenvector
    P.subplot(2, 2, 4)
    plot_hist(eigenvector)
    P.xlabel("Eigenvector centrality")
    P.ylabel("Number of nodes (total={})".format(len(eigenvector)))
    P.show()


def _get_edges_per_slot():
    slots = {} # {year : edges}
    for year in range(1992, 2004):
        slots[year] = HepReader.read_edges("datasets/hepth/timeslots/cit-HepTh-{0}.edges".format(year))

    return slots


def autolabel(rects):
    """Attach text labels with value to histogram retangles"""
    for rect in rects:
        height = rect.get_height()
        P.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d' % int(height),
               ha='center', va='bottom')


def plot_community_sizes(year):
    """Plot community size distribution split into 4 subhistograms"""
    colors = matplotlib.colors.cnames.keys()
    prop = "directed_size_distribution"
    i = 0
    for k in range(3, 13):
        P.subplot(2, 2, (i+1) % 4)
        plot_community_size_distribution_from_cfinder(year, k, "directed_size_distribution", colors[i])
        i += 1
        P.legend()
        P.xlim([0, 100])
        P.xticks(range(0, 100, 5))
        P.suptitle("Community size distribution by size of k-clique" + " year: " + str(year))


def plot_community_size_distribution_from_cfinder(year, k, prop, color):
    """Plot community size distribution from CFinder cliques output files"""
    filename = "datasets/enron/communities/8-{0}/k={1}/{2}".format(year, k, prop)
    # filename = "datasets/hepth/communities/cit-HepTh-{0}/k={1}/{2}".format(year, k, prop)
    lines = HepReader.read_lines(filename)
    sizes = {int(size): int(count) for size, count in [line.split() for line in lines if len(line) != 0]}
    x = sizes.keys()
    y = sizes.values()

    P.bar(x, y, label="year:{}, k={}, max={}".format(year, k, max(x)), align='center', alpha=0.7, color=color)

    P.xlabel("Size of community [members]")
    P.ylabel("Number of communities")



def plot_community_size_distribution():
    """Plot overall distribution for HEP-formatted files"""
    sizes = Counter()
    all_sizes = []
    for year in range(1992, 2004):

        hp = HepReader.get_for_year(year)
        rm = RoleMining(hp.get_nodes(), hp.get_edges())
        sizes_of_communities = [len(c) for c in rm.communities.values()]
        all_sizes.extend(sizes_of_communities)
        counted = Counter(sizes_of_communities)
        sizes += counted

    min_size = 10
    max_size = max(all_sizes)

    year = "overall"

    P.xlabel("Size of community [members]")
    P.ylabel("Number of communities")
    P.suptitle("Year {}, communities bigger than 10 members\nNon-overlapping community size distribution".format(year))
    n, bins, patches = P.hist(filter(lambda x: x > min_size, all_sizes))
    autolabel(patches)
    P.xticks([min_size] + range(min_size-10, max_size + 1, 100) )
    P.xlim(min_size, max_size)
    P.show()


def plot_data_distribution():
    """Plot number of new papers and new citations per year, take Hep files as input"""
    minyear = 1992
    maxyear = 2003
    x = [datetime(year, 01, 01) for year in range(minyear, maxyear + 1)]
    x.extend([datetime(year, 06, 01) for year in range(minyear, maxyear + 1)])

    x.extend([datetime(year, 9, 1) for year in range(minyear, maxyear + 1)])
    x.extend([datetime(year, 12, 1) for year in range(minyear, maxyear + 1)])

    x = sorted(x)
    dates = HepReader.read_dates("/home/stpk/dev/role-mining/datasets/hepth/cit-HepTh-dates-cleaned.txt")
    edges = HepReader.read_edges("/home/stpk/dev/role-mining/datasets/hepth/cit-HepTh.txt")
    slots = HepReader.split_to_timeslots(dates, edges, x)
    for slot in slots.values():
        print len(slot)

    citats = [len(slots[t]) for t in x]
    print citats
    print x

    fig, ax = P.subplots()
    ax.xaxis_date()
    P.title("Nowe publikacje na kwartal")
    P.plot(x, citats, color='b', alpha=0.5, label="Nowe cytowania")
    ax.set_xticks(x)
    P.xticks(rotation=70)

    publications_per_slot = []
    for t in slots.keys():
        new_pubs = set([e[0] for e in slots[t]]) # unique
        publications_per_slot.append(len(new_pubs))

    P.plot(x, publications_per_slot, color="y", alpha=0.6, label="Nowe publikacje")
    P.legend(loc="upper left")
    P.show()

if __name__ == "__main__":
    plot_community_size_distribution()

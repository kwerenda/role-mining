#!/usr/bin/env python

# -*- coding: utf-8 -*-

from datetime import datetime

import pylab as P
from src.HepReader import HepReader
from src.RoleMining import RoleMining
from collections import Counter
from graph_tool import centrality, stats
from math import isnan
import matplotlib

def plot_hist(data):
    # P.hist(data, bins=50, range=(0, 1))
    P.hist(data, bins=50)
    # P.xscale('log')
    # P.yscale('log', nonposy='clip')


def filtered(data, size):
    # data = [x for x in data if x != 0]
    # if len(data) > size:
    #     data = data[:size]
    return sorted(data, reverse=True)[:size]
    # return data


def plot_centralities(network):
    g = network.graph
    comm_size = g.num_vertices()

    closeness = centrality.closeness(g).get_array().tolist()

    max_eigenval, eigenvec = centrality.eigenvector(g)
    # eigenvector = [x/max_eigenval for x in eigenvec.get_array().tolist()]  #normalize!
    eigenvector = eigenvec.get_array().tolist()

    betw, _edges = centrality.betweenness(g, norm=True)
    betweenness = betw.get_array().tolist()


    P.suptitle("Centrality measures")
    # P.figure()


    print "nans", len([x for x in closeness if isnan(x)])
    closeness = [0 if isnan(x) else x for x in closeness]
    # closeness = [x for x in closeness if not isnan(x)]
    closeness = filtered(closeness, comm_size)
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

    betweenness = filtered(betweenness, comm_size)
    print "betweenness", betweenness
    P.subplot(2, 2, 3)
    plot_hist(betweenness)
    P.xlabel("Betweenness centrality")
    P.ylabel("Number of nodes (total={})".format(len(betweenness)))

    eigenvector = filtered(eigenvector, comm_size)
    print "eigenvector", eigenvector
    P.subplot(2, 2, 4)
    plot_hist(eigenvector)
    P.xlabel("Eigenvector centrality")
    P.ylabel("Number of nodes (total={})".format(len(eigenvector)))

    P.show()


def get_edges_per_slot():
    slots = {} # {year : edges}
    for year in range(1992, 2004):
        slots[year] = HepReader.read_edges("datasets/hepth/timeslots/cit-HepTh-{0}.edges".format(year))

    return slots


def autolabel(rects):
    """attach some text labels"""
    for rect in rects:
        height = rect.get_height()
        P.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d' % int(height),
               ha='center', va='bottom')


def plot_community_sizes(year):
    colors = matplotlib.colors.cnames.keys()
    prop = "directed_size_distribution"
    # year = 1997
    i = 0
    for k in range(3, 13):
        # if (i+1) % 4 == 0:
        P.subplot(2, 2, (i+1) % 4)
        plot_community_size_distribution_from_cfnider(year, k, "directed_size_distribution", colors[i])
        i += 1
        P.legend()
        P.xlim([0, 100])
        P.xticks(range(0, 100, 5))
        P.suptitle("Community size distribution by size of k-clique" + " year: " + str(year))



def plot_community_size_distribution_from_cfnider(year, k, prop, color):
    filename = "datasets/enron/communities/8-{0}/k={1}/{2}".format(year, k, prop)
    # filename = "datasets/hepth/communities/cit-HepTh-{0}/k={1}/{2}".format(year, k, prop)
    lines = HepReader.read_lines(filename)
    sizes = {int(size): int(count) for size, count in [line.split() for line in lines if len(line) != 0]}
    x = sizes.keys()
    y = sizes.values()

    P.bar(x, y, label="year:{}, k={}, max={}".format(year, k, max(x)), align='center', alpha=0.7, color=color)

    # P.xlabel("Size of community [members]")
    # P.ylabel("Number of communities")



def plot_community_size_distribution():

    sizes = Counter()
    all_sizes = []
    for year in range(1992, 2004):
    # for year in range(1992, 2004):
    #     P.figure()

        hp = HepReader.get_for_year(year)
        rm = RoleMining(hp.get_nodes(), hp.get_edges())
        sizes_of_communities = [len(c) for c in rm.communities.values()]
        all_sizes.extend(sizes_of_communities)
        counted = Counter(sizes_of_communities)
        sizes += counted

    # years = 2004 - 1992
    # x = sorted(sizes.keys())
    min_size = 10
    max_size = max(all_sizes)
    # x = x[min_size:]
    # y = [sizes[v] for v in x]
    # stds = [sizes[i]/years for i in x]
    #
    year = "overall"


    P.xlabel("Size of community [members]")
    P.ylabel("Number of communities")
    P.suptitle("Year {}, communities bigger than 10 members\nNon-overlapping community size distribution".format(year))
        # P.yscale('log',  nonposy='clip')




    # bars = P.bar(x, y, align='center', color="m", yerr=stds, alpha=0.8)


    n, bins, patches = P.hist(filter(lambda x: x > min_size, all_sizes))
    autolabel(patches)
    # autolabel(bars)
    P.xticks([min_size] + range(min_size-10, max_size + 1, 100) )
    P.xlim(min_size, max_size)
    P.show()


def plot_citat_age():

    dates = HepReader.read_dates("/Users/bogna/dev/role-mining/datasets/hepth/cit-HepTh.dates")
    edges = HepReader.read_edges("/Users/bogna/dev/role-mining/datasets/hepth/cit-HepTh.txt")

    lens = []
    for edge in edges:
        dateSource = dates[edge[0]]
        dateDest = dates[edge[0]]
        lens.append((dateSource - dateDest).total_seconds()/60*60*24)
    print lens

    P.hist(lens, bins=10, histtype='bar')

    P.show()


def plot_smth():
    # P.style.xkcd()
    # slots = get_edges_per_slot()
    minyear = 1992
    maxyear = 2003
    x = [datetime(year, 01, 01) for year in range(minyear, maxyear + 1)]
    x.extend([datetime(year, 06, 01) for year in range(minyear, maxyear + 1)])

    x.extend([datetime(year, 9, 1) for year in range(minyear, maxyear + 1)])
    x.extend([datetime(year, 12, 1) for year in range(minyear, maxyear + 1)])


    x = sorted(x)
    dates = HepReader.read_dates("/Users/bogna/dev/role-mining/datasets/hepth/cit-HepTh-dates-cleaned-dupl.txt")
    edges = HepReader.read_edges("/Users/bogna/dev/role-mining/datasets/hepth/cit-HepTh.txt")
    slots = HepReader.split_to_timeslots(dates, edges, x)
    for slot in slots.values():
        print len(slot)

    # x = slots.keys()
    citats = [len(slots[t]) for t in x]
    print citats
    print x

    # x = [e.year for e in x]
    fig, ax = P.subplots()
    ax.xaxis_date()
    P.title("Nowe publikacje na kwartal")
    P.plot(x, citats, color='b', alpha=0.5, label="Nowe cytowania")
    # P.bar(x, citats, align='center', color='b', alpha=0.5, label = "Nowe cytowania")
    ax.set_xticks(x)
    P.xticks(rotation=70)

    # P.xticks(x)

    publications_per_slot = []
    for t in slots.keys():
        new_pubs = set([e[0] for e in slots[t]]) # unique
        publications_per_slot.append(len(new_pubs))

    # P.bar(x, publications_per_slot, align="center", color="y", alpha=0.6, label="Nowe publikacje")
    P.plot(x, publications_per_slot, color="y", alpha=0.6, label="Nowe publikacje")


    P.legend(loc="upper left")

    P.show()

    # P.figure()
    #
    # mu, sigma = 200, 25
    # # x = mu + sigma*P.randn(10000)
    # x = P.rand(10)*200
    # bins = [100, 125, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 275, 300]
    # n, bins, patches = P.hist(x)#, bins) #, bins, histtype='bar')
    # P.show()


    #
    # mu, sigma = 200, 25
    # x = mu + sigma*P.randn(10000)
    #
    # # the histogram of the data with histtype='step'
    # n, bins, patches = P.hist(x, 50, normed=1, histtype='stepfilled')
    # P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
    #
    # # add a line showing the expected distribution
    # y = P.normpdf( bins, mu, sigma)
    # l = P.plot(bins, y, 'k--', linewidth=1.5)
    #
    # #
    # # create a histogram by providing the bin edges (unequally spaced)
    # #
    #
    # P.figure()
    #
    # bins = [100,125,150,160,170,180,190,200,210,220,230,240,250,275,300]
    # # the histogram of the data with histtype='step'
    # n, bins, patches = P.hist(x, bins, normed=1, histtype='bar', rwidth=0.8)
    #
    # P.show()

if __name__ == "__main__":
    plot_community_size_distribution()

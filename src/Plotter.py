#!/usr/bin/env python

# -*- coding: utf-8 -*-

from datetime import datetime

import pylab as P



# liczba krawedzi per timeslot -> wykres

# plik ze wszystkimi datami
from src import HepReader


def get_edges_per_slot():
    slots = {} # {year : edges}
    for year in range(1992, 2004):
        slots[year] = HepReader.read_edges("datasets/cit-HepTh/split/cit-HepTh-{0}.edges".format(year))

    return slots

if __name__ == "__main__":

    dates = HepReader.read_dates("/Users/bogna/dev/role-mining/datasets/cit-HepTh/cit-HepTh-dates.nodes")
    edges = HepReader.read_edges("/Users/bogna/dev/role-mining/datasets/cit-HepTh/cit-HepTh.txt")

    lens = []
    for edge in edges:
        dateSource = dates[edge[0]]
        dateDest = dates[edge[0]]
        lens.append((dateSource - dateDest).total_seconds()/60*60*24)
    print lens

    P.hist(lens, bins=10, histtype='bar')
    P.show()


if __name__ != "__main__":
    # P.style.xkcd()
    # slots = get_edges_per_slot()
    minyear = 1992
    maxyear = 2003
    x = [datetime(year, 01, 01) for year in range(minyear, maxyear + 1)]
    x.extend([datetime(year, 06, 01) for year in range(minyear, maxyear + 1)])

    x.extend([datetime(year, 9, 1) for year in range(minyear, maxyear + 1)])
    x.extend([datetime(year, 12, 1) for year in range(minyear, maxyear + 1)])


    x = sorted(x)
    dates = HepReader.read_dates("/Users/bogna/dev/role-mining/datasets/cit-HepTh/cit-HepTh-dates-cleaned-dupl.txt")
    edges = HepReader.read_edges("/Users/bogna/dev/role-mining/datasets/cit-HepTh/cit-HepTh.txt")
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

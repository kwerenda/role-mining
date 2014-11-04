#!/usr/bin/env python

# -*- coding: utf-8 -*-

import numpy as np
import pylab as P
import miner


# liczba krawedzi per timeslot -> wykres

# plik ze wszystkimi datami


def get_edges_per_slot():
    slots = {} # {year : edges}
    for year in range(1992, 2004):
        slots[year] = miner.read_edges("datasets/cit-HepTh/split/cit-HepTh-{0}.edges".format(year))

    return slots

if __name__ == "__main__":
    # P.style.xkcd()
    slots = get_edges_per_slot()
    x = slots.keys()
    y = [len(slots[year]) for year in x]

    # P.plot(x, y)
    # P.hist(x, y)
    P.title("Liczba nowych cytatcji")
    P.bar(x, y, align='center')
    P.xticks(x)
    P.show()

    P.figure()

    mu, sigma = 200, 25
    # x = mu + sigma*P.randn(10000)
    x = P.rand(10)*200
    bins = [100, 125, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 275, 300]
    n, bins, patches = P.hist(x)#, bins) #, bins, histtype='bar')
    P.show()







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

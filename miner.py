__author__ = 'bogna'

import snap
from datetime import datetime
from collections import defaultdict




def removeOnes(filename):
    with open(filename) as f, open(filename.replace('.txt', '') + '-cleaned.txt', 'w') as fout:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                newLine = line
            else:
                [nodeId, date] = line.split()
                if nodeId.startswith('11'):
                    nodeId = nodeId[2:]
                newLine = nodeId + '\t' + date
            fout.write(newLine + '\n')

date_format = '%Y-%m-%d'

def readDates(filenameDates):
    dates = {} # {year : nodes}
    with open(filenameDates) as f:
        for line in f:
            if line.startswith('#'):
                continue
            [nodeId, date] = line.split()
            dates[int(nodeId)] = datetime.strptime(date, date_format)
    return dates

def getYearAndMonth(nodeId):
    nodeId = str.rjust(str(nodeId), 7, '0')
    year = int(nodeId[:2])
    year =  1900 + year if year > 20 else 2000 + year
    month = int(nodeId[2:4])
    return (year, month)



def getYear(nodeId, dates, fileOut):
    try:
        year = dates[nodeId].year
    except KeyError:
        fileOut.write(str(nodeId) + " nie ma przypisanej daty! Generacja\n")
        year, month = getYearAndMonth(nodeId)
        dates[nodeId] = datetime(year=year, month=month, day=01)
    #check if there are any exceptions
    if dates[nodeId].year != getYearAndMonth(nodeId)[0]:
        print("Assumption error! For " + str(nodeId) + " year is " + str(dates[nodeId].year) + " and you think it's " + str(getYearAndMonth(nodeId)[0]))
    return year


def readGraph(filenameEdges, filenameDates):
    dates = readDates(filenameDates)
    #time slots by years
    slots = defaultdict(list)  # {year : [ (source, target)]}
    sameYear = 0
    diffYear = 0
    with open(filenameEdges) as f, open("czasowy.txt", 'w') as fout:
        for line in f:
            if line.startswith('#'):
                continue
            [sourceNode, destNode] = line.split()
            sourceNode, destNode = int(sourceNode), int(destNode)
            yearSource = getYear(sourceNode, dates, fout)
            yearDest = getYear(destNode, dates, fout)
            slots[yearSource].append(line)
            if yearDest == yearSource:
                sameYear += 1
            else:
                diffYear += 1
            fout.write(str(yearSource) + ' -> ' + str(yearDest) + (" inny rok!" if yearSource != yearDest else "") + '\n')
    print("In same year: {0} In diff year: {1}".format(sameYear, diffYear))

    for year in slots:
        with open("datasets/cit-HepTh/split/cit-HepTh-" + str(year) + ".txt", "w") as f:
            for line in slots[year]:
                f.write(line)





    # read dates to memory
    # while reading edges assign to dffirent timeslots based on dates
    # optional - save each node to the separate file, as data file and graph file
    # create nodes for each graph

def detectComunities(year, g):
    CmtyV = snap.TCnComV()
    modularity = snap.CommunityCNM(g, CmtyV)
    # for Cmty in CmtyV:
    # print ("Community: ")
    # for NI in Cmty:
    #     print NI
    print("The modularity of the network in year {0} is {1}".format(year, modularity))

def getMany():
    base_filename = "datasets/cit-HepTh/split/cit-HepTh-"
    for year in range(1992, 2004):
        filename = base_filename + str(year) + '.txt'
        # g = snap.LoadEdgeList(snap.PNEANet, filename, 0, 1)
        g = snap.LoadEdgeList(snap.PUNGrah, filename, 0, 1)
        detectComunities(year, g)

def main():
    snap.LoadEdgeList()
    allData = snap.LoadEdgeList(snap.PNGraph, "datasets/cit-HepTh/cit-HepTh.txt", 0, 1, '\t')  # traverse the nodes
    for NI in allData.Nodes():
        print "node id %d with out-degree %d and in-degree %d" % (
            NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())
    # traverse the edges
    # for EI in allData.Edges():
    #     print "edge (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
    # # traverse the edges by nodes
    # for NI in allData.Nodes():
    #     for Id in NI.GetOutEdges():
    #         print "edge (%d %d)" % (NI.GetId(), Id)
    #         # allData = TNGraph.New()
    #         #     TNGraph_Load


if __name__ == '__main__':
    print("hello!")
    getMany()
    # removeOnes("datasets/cit-HepTh/cit-HepTh-dates.txt")
    # readGraph("datasets/cit-HepTh/cit-HepTh.txt", "datasets/cit-HepTh/cit-HepTh-dates-cleaned.txt")
    print("bye!")
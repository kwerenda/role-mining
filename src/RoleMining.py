from graph_tool import centrality
from math import isnan
from numpy import mean, std


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

Roles = enum("OUTSIDER", "LEADER", "OUTERMOST", "MEDIATOR")


class RoleMining(object):

    def __init__(self, network):
        self.network = network
        self.closeness = []

    def find_outsiders(self):
        outsiders = []
        g = self.network.graph
        communities = self.network.communities

        for v in g.vertices():
            label = g.vp['label'][v]
            if communities[label] == []:
                outsiders.append(label)

        return outsiders


    def find_leaders(self, closeness, threshold):
        leaders = []
        g = self.network.graph

        for v in g.vertices():
            if isnan(closeness[v]) or closeness[v] >= threshold:
                leaders.append(g.vp['label'][v])

        return leaders


    def find_outermosts(self, closeness, threshold):
        outermosts = []
        g = self.network.graph

        for v in g.vertices():
            if not isnan(closeness[v]) and closeness[v] <= threshold:
                outermosts.append(g.vp['label'][v])

        return outermosts


    def find_roles(self):
        g = self.network.graph
        outsiders = self.find_outsiders()
        closeness_pm = centrality.closeness(g)
        closeness = [closeness_pm[v] for v in g.vertices()]
        m, sd = mean(closeness), std(closeness)
        leaders = self.find_leaders(closeness_pm, m + 1 * sd)
        outermosts = self.find_outermosts(closeness_pm, m - 1 * sd)
        self.closeness = closeness
        return outsiders, leaders, outermosts



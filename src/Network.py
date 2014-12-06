from collections import defaultdict, Counter
from os import listdir
from graph_tool import Graph
import csv
from itertools import product
import graph_tool.topology as gt


class Network(object):
    def __init__(self, edges_file, communities_file=None, k=3, is_directed=True):
        edges = self.read_file(edges_file)
        if communities_file is None:
            path = edges_file.split('/')
            path[-2] = 'communities'
            path[-1] = path[-1][:-6]  # cut off the '.edges' part
            communities = self.get_communities_from_cf('/'.join(path), k)
        else:
            communities = self.read_file(communities_file)

        g, label2index = self.create_graph(edges, is_directed)

        filter_prop = g.new_vertex_property('bool')
        g.vertex_properties['filter'] = filter_prop

        # self.create_communities(communities, g, label2index)

        self.graph = g
        self.label2index = label2index
        self.communities = self.create_communities(communities)

    @classmethod
    def read_file(cls, filename):
        """Read file with pairs of ints into list of tuples"""
        pairs = []

        with open(filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if not row[0][0].isdigit():
                    continue
                p = int(row[0]), int(row[1])
                pairs.append(p)

        return pairs

    @classmethod
    def create_graph(cls, edges, is_directed=True):
        """Create a graph-tool type graph from a list of edges"""

        g = Graph()
        g.set_directed(is_directed)
        label2index = dict()
        label = g.new_vertex_property('int32_t')
        g.vertex_properties['label'] = label

        for v1_label, v2_label in edges:
            cls.add_vertex(v1_label, label2index, g)
            cls.add_vertex(v2_label, label2index, g)

            v1, v2 = label2index[v1_label], label2index[v2_label]
            g.add_edge(v1, v2)

        return g, label2index

    @classmethod
    def add_vertex(cls, v_label, label2index, graph):
        """Add a node to the graph if it's not there already"""
        if v_label not in label2index:
            v = graph.add_vertex()
            label2index[v_label] = v
            graph.vertex_properties["label"][v] = v_label

    @classmethod
    def get_communities_from_cf(cls, cf_dir, k):
        k_folder = "k={}".format(k)
        # k_folder = 'k=4' if 'k=4' in listdir(cf_dir) else 'k=3'
        tuples = []

        with open(cf_dir + '/' + k_folder + '/directed_communities') as f:
            for line in f:
                div = line.split(':')
                group = div[0].strip()
                if line.startswith('#') or group == '':
                    continue
                nodes = div[1].strip().split(' ')
                for n in nodes:
                    tuples.append((int(n), int(group)))
        return tuples


    @classmethod
    def create_communities(cls, communities_list):
        """Creates a property map with communities of all nodes"""
        communities = defaultdict(list)

        for v_lab, comm in communities_list:
            communities[v_lab].append(comm)

        return communities

    def filter_community(self, community_label):
        """Filter out one community from the graph"""
        g = self.graph
        l2i = self.label2index
        comm =self.communities

        for v_lab, v in l2i.items():
            if community_label in comm[v_lab]:
                g.vp['filter'][v] = True
            else:
                g.vp['filter'][v] = False

        g.set_vertex_filter(g.vp['filter'])

    def unfilter_graph(self):
        """Remove any filters from the graph"""
        self.graph.clear_filters()

    def print_communities(self):
        flatlist = [item for sublist in self.communities.values() for item in sublist]
        print Counter(flatlist)

    def shortest_paths(self, v1, v2):
        """Return ALL shortest paths between v1 and v2"""
        #TODO: !
        vertices, edges = gt.shortest_path(self.graph, v1, v2)
        return [vertices]


    def calculate_CBC(self, is_directed=True):
        """Calculate CBC for all nodes in network"""

        cdc = self.graph.new_vertex_property('int32_t')
        self.graph.vertex_properties['CDC'] = cdc
        #set all to 0
        for v in self.graph.vertices():
                self.graph.vp['CDC'][v] = 0

        # dla kazdej pary wezlow w grafie - kolejnosc ma znaczenie
        for v1, v2 in product(self.graph.vertices(), self.graph.vertices()):
            # jezeli community (c1) != commmunity (C2)
            if set(self.communities[v1]).isdisjoint(set(self.communities[v2])):
                #   dla kazdej najkrotszej sciezki p od c1 do c2
                for path in self.shortest_paths(v1, v2):
                    for v in path:
                        self.graph.vp['CDC'][v] += 1

        if not is_directed:
            for v in self.graph.vertices():
                self.graph.vp['CDC'][v] /= 2



from __future__ import division
from collections import defaultdict, Counter, deque
from graph_tool import Graph, centrality
import csv
from itertools import product, combinations
import graph_tool.topology as gt


class Network(object):
    def __init__(self, edges_file, communities_file=None, k=3, is_directed=True, use_communities=False, cfinder=True):
        edges = self.read_file(edges_file)



        if use_communities and communities_file is None:
            path = edges_file.split('/')
            path[-2] = 'communities'
            path[-1] = path[-1][:-6]  # cut off the '.edges' part
            k_folder = "k={}".format(k)
            cf_dir = '/'.join(path)
            communities = self.get_communities_from_cf(cf_dir + '/' + k_folder + '/directed_communities')
            # self.communities = self.get_communities_from_cf('/'.join(path), k)
            self.communities = self.create_communities(communities)
        elif communities_file is not None:
            if cfinder:
                communities = self.get_communities_from_cf(communities_file)
            else:
                communities = self.read_file(communities_file)
            self.communities = self.create_communities(communities)
        g, label2index = self.create_graph(edges, is_directed)
        filter_prop = g.new_vertex_property('bool')
        g.vertex_properties['filter'] = filter_prop

        # self.create_communities(communities, g, label2index)

        self.graph = g
        self.label2index = label2index


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
    def get_communities_from_cf(cls, filename):
        # k_folder = "k={}".format(k)
        # k_folder = 'k=4' if 'k=4' in listdir(cf_dir) else 'k=3'
        tuples = []

        # with open(cf_dir + '/' + k_folder + '/directed_communities') as f:
        with open(filename) as f:
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

    def filter_community(self, community_labels):
        """Filter out one community from the graph"""
        g = self.graph
        comm =self.communities

        for v in g.vertices():
            v_lab = g.vp['label'][v]
            if set(comm[v_lab]).isdisjoint(set(community_labels)):
                g.vp['filter'][v] = False
            else:
                g.vp['filter'][v] = True

        g.set_vertex_filter(g.vp['filter'])

    def unfilter_graph(self):
        """Remove any filters from the graph"""
        self.graph.clear_filters()

    def print_communities(self):
        flatlist = flatten_list(self.communities.values())
        print "communities", Counter(flatlist)

    def get_vertices_from_community(self, comm_nr):
        g, communities = self.graph, self.communities
        return [v for v in g.vertices() if comm_nr in communities[g.vp['label'][v]]]

    @staticmethod
    def shortest_paths(v1, v2):
        """Return ALL shortest paths between v1 and v2"""
        visited = set()
        paths = []

        # BFS
        queue = deque([(v1, [])])
        while queue:
            curr_v, curr_path = queue.popleft()

            # add no matter if it was previously visited
            visited.add(curr_v)
            if len(paths) == 0 or len(paths[0]) >= len(curr_path) + 1:

                if curr_v == v2:
                    # condition for v1 == v2
                    paths.append(curr_path + [v2]) if curr_path != [] else paths.append([])
                else:
                    # add all neighbours to the queue
                    new_path = curr_path + [curr_v]
                    queue.extend([(v, new_path) for v in curr_v.out_neighbours() if v not in visited])

        return paths

    def get_mediators(self):
        """Calculates and prints out (for now) NBC of the best nodes
        in all community combinations"""
        communities = set(flatten_list(self.communities.values()))
        done = dict()
        for c1, c2 in combinations(communities, 2):
            cpaths = []
            vgroup_1 = self.get_vertices_from_community(c1)
            vgroup_2 = self.get_vertices_from_community(c2)
            div = min(len(vgroup_1), len(vgroup_2))

            print "Calculating for communities: ", c1, c2
            for v1, v2 in product(vgroup_1, vgroup_2):
                print "Calc for nodes ", v1, v2
                if (v2, v1) not in done and (v1, v2) not in done:
                    print "====searching for shortest paths==="
                    shortest = self.shortest_paths(v1, v2)
                    cpaths.extend(shortest)
                    done[(v1, v2)] = shortest
                else:
                    shortest = done[(v1, v2)] if (v1, v2) in done else done[(v2, v1)]
                    cpaths.extend(shortest)

            flatlist = []
            for l in cpaths:
                flatlist.extend(l[1:-1])
            cnt = Counter(flatlist)

            print "Groups: ", c1, c2  # to be replaced if this function has some future
            print "id score"
            for node, cbc in cnt.most_common():
                print node, cbc/div

    def get_outsiders(self):
        pass

    def calculate_CBC(self, is_directed=True):
        """Calculate CBC for all nodes in network"""

        cdc = self.graph.new_vertex_property('int32_t')
        self.graph.vertex_properties['CDC'] = cdc
        #set all to 0
        for v in self.graph.vertices():
                self.graph.vp['CDC'][v] = 0

        # dla kazdej pary wezlow w grafie - kolejnosc ma znaczenie
        for v1, v2 in product(self.graph.vertices(), self.graph.vertices()):
            v1_lab, v2_lab = self.label2index[v1], self.label2index[v2]

            # jezeli community (c1) != commmunity (C2)
            if set(self.communities[v1_lab]).isdisjoint(set(self.communities[v2_lab])):
                #   dla kazdej najkrotszej sciezki p od c1 do c2
                for path in self.shortest_paths(v1, v2):
                    for v in path:
                        self.graph.vp['CDC'][v] += 1

        if not is_directed:
            for v in self.graph.vertices():
                self.graph.vp['CDC'][v] /= 2

    def get_wannabe_mediators(self):
        g, communities = self.graph, self.communities
        bigrouped = [v for v in g.vertices() if len(communities[g.vp['label'][v]]) > 1]

        for v in bigrouped:
            v_lab = g.vp['label'][v]

            self.filter_community(communities[v_lab])
            # node_betweenness, e_btwn= centrality.betweenness(g)
            # v_betweenness = node_betweenness[v]
            # betweenness = node_betweenness.get_array().tolist()
            # avg_betweenness = sum(betweenness) / len(betweenness)
            v_degree =  v.out_degree()
            degrees = [i.out_degree() for i in g.vertices()]
            avg_degree = sum(degrees) / len(degrees)
            self.unfilter_graph()

            ratio = v_degree / avg_degree
            # ratio = v_betweenness / avg_betweenness
            if ratio > 1:
                print "Bloke: ", v_lab, ratio



def flatten_list(l):
    return [item for sublist in l for item in sublist]

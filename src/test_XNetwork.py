from unittest import TestCase
from pprint import pprint
from src.XNetwork import XNetwork
class TestXNetwork(TestCase):

    def test_multi(self):
        n = XNetwork("datasets/test/test_multi.edges", communities_file="datasets/test/test_cbc.communities")
        self.assertEquals(n.graph.size(), 15)
        n.calculate_CBC()
        for node in n.graph.nodes():
            print node, n.graph.node[node]['cbc']


    def test_comms(self):
        n = XNetwork("datasets/test/test_cbc.edges", communities_file="datasets/test/test_cbc.communities")
        # pprint(n.graph.nodes(data=True))
        for node in [1, 2, 3, 4]:
            self.assertIn(0, n.graph.node[node]['comm'])
        for node in [7, 8, 9, 10]:
            self.assertIn(1, n.graph.node[node]['comm'])

    def test_cbc(self):
        n = XNetwork("datasets/test/test_cbc.edges", communities_file="datasets/test/test_cbc.communities")
        n.calculate_CBC()
        for node in [1, 2, 3, 7, 8, 9]:
            self.assertEquals(n.graph.node[node]['cbc'], 3)
        self.assertEquals(n.graph.node[5]['cbc'], 27)
        self.assertEquals(n.graph.node[6]['cbc'], 7)
        for node in n.graph.nodes():
            print node, n.graph.node[node]['cbc']


from unittest import TestCase
import graph_tool.draw as gw

from src.Network import Network


class TestNetwork(TestCase):

    def test_mediators(self):
        n = Network("datasets/test/test_cbc.edges", is_directed=False,
                    communities_file="datasets/test/test_cbc.communities")
        n.print_communities()
        n.get_mediators_NBC()

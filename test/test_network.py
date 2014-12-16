from unittest import TestCase
import graph_tool.draw as gw

from src.Network import Network


class TestNetwork(TestCase):

    def test_shortest_paths(self):
        e = Network("datasets/test/test_cbc.edges", is_directed=False)
        # g = e.graph
        # # pos = gw.sfdp_layout(g)
        # pos = gw.fruchterman_reingold_layout(g)
        # gw.graph_draw(g, pos=pos, output="graph-draw-sfdp.png", vertex_text=g.vertex_index, vertex_font_size=18)

    def test_mediators(self):
        n = Network("datasets/test/test_cbc.edges", is_directed=False,
                    communities_file="datasets/test/test_cbc.communities")
        n.print_communities()
        n.get_mediators()

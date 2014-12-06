from unittest import TestCase
import graph_tool.draw as gw

from src.Network import Network


class TestNetwork(TestCase):

    def test_shortest_paths(self):
        e = Network("datasets/test/test_cdc.edges", is_directed=False)

        g = e.graph
        pos = gw.sfdp_layout(g)
        gw.graph_draw(g, pos=pos, output="graph-draw-sfdp.pdf", vertex_text=g.vertex_index, vertex_font_size=18)


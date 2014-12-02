from unittest import TestCase

from src.Reader import EnronReader


class TestEnronReader(TestCase):

    def test_reader(self):
        e = EnronReader("datasets/test/testdata.edges")
        self.assertEqual(len(e.daysets[67]), 2)

    def test_filter(self):
        e = EnronReader("datasets/test/testdata.edges")
        e.filter(2)
        self.assertEqual(len(e.edges), 3)




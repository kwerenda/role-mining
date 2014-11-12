from unittest import TestCase
from HepReader import HepReader
from datetime import datetime, date


#TODO: change all datetime to date
class TestHepReader(TestCase):
    # def test_id_to_year_and_month(self):
    #     self.fail()

    def test__strip11s_too_shorts(self):
        r = HepReader()
        self.assertEqual(r._strip11s("0011999", datetime(2000, 11, 1)), "11999")
        self.assertEqual(r._strip11s("11999", datetime(2000, 11, 1)), "11999")

        self.assertEqual(r._strip11s("1199", datetime(2000, 1, 1)), "1199")

        self.assertEqual(r._strip11s("0112999", datetime(2001, 12, 1)), "112999")

    def test_strip11s_cross_cits(self):
        r = HepReader()
        self.assertEqual(r._strip11s("119807999", datetime(1998, 07, 1)), "9807999")
        self.assertEqual(r._strip11s("11107999", datetime(2001, 07, 1)), "107999")
        self.assertEqual(r._strip11s("11207999", datetime(2002, 07, 1)), "207999")
        self.assertEqual(r._strip11s("1112999", datetime(2000, 12, 1)), "12999")
        self.assertEqual(r._strip11s("117999", datetime(2000, 07, 1)), "7999")

    def test_date_from_id_zeros(self):
        self.assertEqual(HepReader._date_from_id("0001999"), date(2000, 01, 01))

    def test_date_from_id_no_zeros(self):
        self.assertEqual(HepReader._date_from_id("1999"), date(2000, 01, 01))

    def test_date_from_id_XXcent(self):
        self.assertEqual(HepReader._date_from_id("9901999"), date(1999, 01, 01))

    def test_date_from_id_regular(self):
        self.assertEqual(HepReader._date_from_id("212999"), date(2002, 12, 01))

    # def test_clean_data(self):
    #     self.fail()
    #
    # def test_read_dates(self):
    #     self.fail()
    #
    # def test_read_edges(self):
    #     self.fail()

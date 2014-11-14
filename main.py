__author__ = 'bogna'

from HepReader import HepReader

if __name__ == '__main__':
    hp = HepReader()
    hp.clean_data("datasets/cit-HepTh/cit-HepTh.txt", "datasets/cit-HepTh/cit-HepTh-dates.txt", write_to_file=False)
    dates = hp.read_dates("datasets/cit-HepTh/cit-HepTh-dates.nodes")
    edges = hp.read_edges("datasets/cit-HepTh/cit-HepTh.txt")
    hp.split_by_year(dates, edges, write_to_file=False, base_filename="datasets/cit-HepTh/split/cit-HepTh.txt")

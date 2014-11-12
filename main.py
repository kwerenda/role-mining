__author__ = 'bogna'

from HepReader import HepReader

if __name__ == '__main__':
    hp = HepReader()
    hp.clean_data("datasets/cit-HepTh/cit-HepTh.txt", "datasets/cit-HepTh/cit-HepTh-dates.txt", True)

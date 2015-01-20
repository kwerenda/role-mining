Role Mining
===========

The goal of the project was to determine and assign particular roles to different nodes in a network. Roles may indicate the importance of nodes in a community or type of their connection to various groups. They were predefined beforehand and mined in two datasets: Enron e-mail network and arxiv.org citation network of the Theoretical High Energy Physics (HepTh) domain.

Our work was based directly on the article [SSRM: Structural Social Role Mining for Dynamic Social Networks](http://webdocs.cs.ualberta.ca/~zaiane/postscript/Role-ASONAM14.pdf).

# Modules

`Plotter` - module written to generate figures found in documentation

`Network` - network representation based on [graph-tool](http://graph-tool.skewed.de/) 

`XNetwork` - network representation based on [NetworkX](https://networkx.github.io/)

`RoleMining` - role extraction (as described in paper)

`Reader` - reading and pre-processing input data

Other files:

`extract_communities.sh` - bash script extracting communities using CFinder from multiple graphs saved as edges file. New result directory is created for each input graph. ''

`matplotlibrc` - matplotlib configuration file with styles for graph plotting

# Datasets

Input data used in this project can be found in `datasets` directory. Graphs are saved in `.edges` files, where one line represents one edge in graph, optional 3rd column can be edge weight.

## Enron

[Data source](http://foreverdata.com/1009/Enron_Dataset_Report.pdf)

`datasets\enron` - input data from Enron divided into timeslots by month. Each person has its unique integer id, mapping id : email can be found in `enron_guys.txt`. In `timeslots` directory there are two types of files:

* `{month}.edges` - All communication from given month. Edge weight is equal to the number of emails send by person.
* `{month}-filtered{k}.edges` - Communication from given month, but nodes which sent emails in less than `k` days are filtered out. 

Communities genereted by CFinder can be found in `communities` directory.

## Hep-Th

[Data source](http://snap.stanford.edu/data/cit-HepTh.html)

Input data dived in yearly timeslots are in `timeslots` dir. Arxiv IDs are used as nodes' label.

In `communities`, CFinder outputs is grouped into seperate directories, while `.communities` files hold groups extracted by Gephi (based on modularity).
Other files:

* `cit-HepTh.txt` - raw file as found on SNAP webpage
* `cit-HepTh-dates.txt` - submission dates of Hep papers
* `cit-HepTh.dates` - submission dates of all papers, after cleaning, removing nodes not existing in network and adding extracted dates.









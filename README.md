# Project 1

## Bayesian Network Scoring
This project is a competition to find Bayesian network structures that best fit some given data.

### Testing: Cooper&Herskovits, 1992
The scoring function is callibrated using the original Bayesian Structure Scoring paper, from which first published the
equations in the Decision Under Uncertainty book (2.80).  The paper provides example input data and values for
two Bayesian networks.

- network1 score=2.22685407871e-09 as in Cooper&Herskovits formula 5 in page 316
- network2 score=2.22685407871e-10
- THUS, network1 is more suitable for the given dataset

The test class is: 
``
graphotest.py
``

The input file: cooperh.csv
The output files:
- network1 graph: cooperh.gph-net1
- network1 plot of the graph: cooperh.gph-net1.png
- network2 graph: cooperh.gph-net2
- network2 plot of the graph: cooperh.gph-net2.png


### Dataset:
These datasets are taken from:
- (small) titanic: https://cran.r-project.org/web/packages/titanic/titanic.pdf
- (medium) wine: https://archive.ics.uci.edu/ml/datasets/Wine+Quality
- (large) secret dungeon

### Dataframes
Data operations are performed by: 

``
graphopanda, which relies on Python's Pandas library
``

### Plotting:
Plotting is performed by:
 
``
graphoshow.py, which relies on Matplot
``

### Graphs:
Graph operations are performed by graphoxnet, which relies on Python's Networkx library

### Scoring:

Scoring is performed by: 

``
graphoscore.py
``

Because Cooper&Herskovits provide a numerical example, their formula (analogous to Decisions Under Uncertainty
2.80) was initially used in scoring.  For reference, the Cooper&Herskovits is included in this repository.

The final Log scoring algorithm matches Decisions Under Uncertainty, page 47, formula 2.83

Both scoring algorithms are defined in graphoscore.py

They are compared to each other in: 

``
graphotest.py
``


### Future work:
Parallelize computation on Spark






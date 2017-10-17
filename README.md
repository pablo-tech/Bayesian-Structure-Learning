# Project 1

## Bayesian Network Scoring
This project is a competition to find Bayesian network structures that best fit some given data.

### Testing: Cooper&Herskovits, 1992
The scoring function is callibrated using the original Bayesian Structure Scoring paper, from which first published the
equations in the Decision Under Uncertainty book (2.80).  The paper provides example input data and values for
two Bayesian networks.
The test class is: graphotest.py
The input file: cooperh.csv
The output files:
- network1 graph: cooperh.gph-net1
- network1 plot of the graph: cooperh.gph-net1.png
- network2 graph: cooperh.gph-net2
- network2 plot of the graph: cooperh.gph-net2.png

To run the test:
``
/path/to/graphotest.py
``

### Dataset:
These datasets are taken from:
- (small) titanic: https://cran.r-project.org/web/packages/titanic/titanic.pdf
- (medium) wine: https://archive.ics.uci.edu/ml/datasets/Wine+Quality
- (large) secret dungeon

### Scoring:








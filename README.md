## Bayesian Network Search
This project finds an optimal Bayesian Network structures that best fit some given data.

### Scoring: Cooper&Herskovits, 1992
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


### System requirements:

Python 2.7.14 with NetworkX 1.9, Pandas 0.20.3, Matplotlib 2.1.0


### How to Run:
``
python project1.py small.csv small.gph
``

``
python project1.py medium.csv medium.gph
``

``
python project1.py large.csv large.gph
``

### Dataframes
Data operations are performed by: 

``
graphopanda, which relies on Python's Pandas library
``

### Querying:
To count occurrance of data patterns, aggregations are performed by:

``
graphocount
``

Queries to filter dataframes are performed by:

``
graphoquery
``


### Plotting:
Plotting is performed by:
 
``
graphoshow.py, which relies on Matplot
``

Note that .png files with images of each graph is also provided.  Example:

![Alt text](medium.gph.jpg?raw=true "Title")


### Graphs:
Graph operations are performed by:
 
``
graphoxnet, which relies on Python's Networkx library
``

### Scoring:

Scoring is performed by: 

``
graphoscore.py
``

Because Cooper&Herskovits provide a numerical example, their formula (analogous to Decisions Under Uncertainty
2.80) was initially used in scoring.  For reference, the Cooper&Herskovits is included in this repository, see page 316, formula 5.

The final Log scoring algorithm matches Decisions Under Uncertainty, page 47, formula 2.83

They are compared to each other in: 

``
graphotest.py
``

### Learning:
The algorithm to find the best representation combines programatic execution with an element of randomness,
to have an opportunity to find a best graph that was not thought of when writing the code.

### Performane:

For high performance, the algorithm developed relies on native filtering methods in Python Pandas Dataframes.

Below is the time it took to run on a personal laptop.  NOTE: the code was run with console logs enabled, which
by itself would likely reduce performance by and order of magnitude.

The algorithm is currently configured to make at most a maximum number of optimization attempts per node
to optimize any one graph.

Initial graph score evaluation:
- (small) titanic: fraction of second
- (medium) wine: 1 second
- (large) secret dungeon: 2 seconds

Run through completion building the highest scoring graph:
- (small) titanic: 35 seconds
- (medium) wine: 2:45 minutes
- (large) secret dungeon: 15 minutes

The biggest performance penalty seems to be to check if the graph is still acyclical in a large network as it takes shape.

NOTE: attention must be paid to preferably use the LOG form of the formula to avoid potential zero, or divide by zero errors

### Sample output:

- (medium) wine:
 
 alcohol,fixedacidity
 
 density,alcohol
 
 alcohol,chlorides
 
 fixedacidity,density
 
 citricacid,sulphates
 
 fixedacidity,citricacid
 
 fixedacidity,residualsugar
 
 fixedacidity,totalsulfurdioxide
 
 alcohol,volatileacidity
 
 fixedacidity,quality
 
 fixedacidity,ph
 
 alcohol,freesulfurdioxide
 

### Plot output

Please find in the folder:
- (small) titanic: small.gph and small.gph.png
- (medium) wine: medium.gph and small.gph.png
- (large) secret dungeon: large.gph and large.gph.png


### Future work:

Use Uniform Dirichlet Prior (all pseudocounts = 1), for any Nijk, so there are no leaps in interpretation if ijk is
 not present in the dataset

Parallelize computation on Spark







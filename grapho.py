# https://networkx.github.io/documentation/networkx-1.9/tutorial/tutorial.html

# NETWORKX
try:
    import networkx as nx
except ImportError:
    raise ImportError("Networkx required for graph()")
except RuntimeError:
    print("Networkx unable to open")
    raise

# SYSTEM
try:
    import sys
except ImportError:
    raise ImportError("SYS required for ARGUMENTS()")
except RuntimeError:
    print("SYS unable to open")
    raise

# CSV
try:
    import csv
except ImportError:
    raise ImportError("CSV required for read()")
except RuntimeError:
    print("CSV unable to open")
    raise

# PANDAS
try:
    import pandas as pd
except ImportError:
    raise ImportError("PANDAS required for read()")
except RuntimeError:
    print("PANDAS unable to open")
    raise


# GRAPHO components
import graphoscore as oscore
import graphoshow as oshow

# GRAPH: that is used to find best
# initialGraph = nx.DiGraph()

# COMPUTE: method called to perform the whole job
# TODO: make sure no self loops
# TODO: output both png and gph files
def compute(infile, outfile):
    graph = getNewGraph("first")
    inputDF = read(infile)
    score = oscore.getScore()
    graph = addRandomVarNodesToGraph(graph, inputDF)
    oshow.plotGraph(graph, outfile)
    oshow.toString(graph)
    oshow.write(outfile, graph)
    pass

# READ: a dataframe from a CSV inputfile
def read(infile):
    inputDF = getInputDF(infile)
    return inputDF

# Graph vs DiGraph
# name=graphName
def getNewGraph(graphName):
    graph = nx.DiGraph(name=graphName)
    return graph

# READ: get dataframe, inferring columns
def getInputDF(infile):
    inputDF = pd.read_csv(infile, header='infer')
    return inputDF

# ADD RANDOM VARIABLE NODES
def addRandomVarNodesToGraph(graph, dataframe):
    for col in list(dataframe):
        # len()
        unique = dataframe[col].unique()
        print"{} \t\t UNIQUE: \t\t {} ".format(col, unique)
        graph.add_node(col)
        # graph.add_edge('age', col)
        #graph.add_nodes_from([2, 3])
        #print(dataframe.col)
    return graph


# FUTURE WORK
#
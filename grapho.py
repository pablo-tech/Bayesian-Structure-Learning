import networkx as nx

# NETWORKX
try:
    import networkx as nx
except ImportError:
    raise ImportError("Networkx required for graph()")
except RuntimeError:
    print("Networkx unable to open")
    raise

# MATPLOTLIB
try:
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError("Matplotlib required for draw()")
except RuntimeError:
    print("Matplotlib unable to open")
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

# GRAPH: that is used to find best
# initialGraph = nx.DiGraph()

# COMPUTE: method called to perform the whole job
def compute(infile, outfile):
    read(infile)
    write(outfile)
    pass

# READ: a dataframe from a CSV inputfile
def read(infile):
    inputDF = getInputDF(infile)
    graph = getNewGraph("first")
    graph = addGraphNodes(graph, inputDF)
    # print(graph.node['fare'])
    # nx.connected_components(graph)
    # graph.adj
    plotGraph(graph)

    #print(inputDF)

    # .values
    # df.head()
    pass

# Graph vs DiGraph
# name=graphName
def getNewGraph(graphName):
    graph = nx.Graph(name=graphName)
    return graph


def query(dataframe):
    #print(inputDF.loc[(inputDF['age']==1) & (inputDF['sex']==2)])
    #print(inputDF.loc[(inputDF['age']==1) & (inputDF['sex']==2)][['age', 'sex']])
    pass

# READ: get dataframe, inferring columns
def getInputDF(infile):
    inputDF = pd.read_csv(infile, header='infer')
    return inputDF

def addGraphNodes(graph, dataframe):
    for col in list(dataframe):
        # len()
        unique = dataframe[col].unique()
        print"{} \t\t UNIQUE: \t\t {} ".format(col, unique)
        graph.add_node(col)
        #graph.add_nodes_from([2, 3])
        #print(dataframe.col)
        # dataframe[col].u
    return graph


# WRITE: a gph output file
def write(outfile):
    with open(outfile, 'wb') as csvfile:
        gph_writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        gph_writer.writerow(['Spam'] * 5 + ['Baked Beans'])
        gph_writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    pass


# COMPUTE
# Directed graphs, that is, graphs with directed edges
G=nx.Graph()
G=nx.DiGraph()

G.add_edge(2,3,weight=0.9)
# G.add_nodes_from([2,3])

# print(G.adj)


def plotGraph(graph):
    print "GRAPH: {} ".format(graph.graph)
    print "NODES: {}".format(graph.nodes())
    print "EDGES: {}".format(graph.edges())
    for node in graph.nodes():
        print "{} NEIGHTBORS: {}".format(node, graph.neighbors(node))
    nx.connected_components
    #nx.draw_networkx(graph)
    graph.adj

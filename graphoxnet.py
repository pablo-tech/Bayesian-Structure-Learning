# Graph operations using Python's NetworkX library


# PANDAS
try:
    import pandas as pd
except ImportError:
    raise ImportError("PANDAS required for read()")
except RuntimeError:
    print("PANDAS unable to open")
    raise

# NETWORKX
try:
    import networkx as nx
except ImportError:
    raise ImportError("Networkx required for graph()")
except RuntimeError:
    print("Networkx unable to open")
    raise


# DIGRAPH: Create a new directional graph
def getNewGraph(graphName):
    graph = nx.DiGraph(name=graphName)
    return graph


# PARENTS for a node
def getRandomVarParents(randomVarName, graph):
    return graph.predecessors(randomVarName)
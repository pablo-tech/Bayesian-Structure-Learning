# Find the best Bayesian network, for a given dataset
# https://networkx.github.io/documentation/networkx-1.9/tutorial/tutorial.html


# # SYSTEM
# try:
#     import sys
# except ImportError:
#     raise ImportError("SYS required for ARGUMENTS()")
# except RuntimeError:
#     print("SYS unable to open")
#     raise


############
# GRAPHO components developed
import graphoscore as oscore
import graphoshow as oshow
import graphopanda as opanda
import graphopanda as oxnet


# COMPUTE: method called to perform the whole job
# TODO: make sure no self loops
# TODO: output both png and gph files
def compute(infile, outfile):
    graph = oxnet.getNewGraph("first")
    inputDF = opanda.read(infile)
    randomVars = opanda.getRandomVarNodeNames(inputDF)
    graph = addRandomVarNodesToGraph(graph, randomVars)
    score = oscore.getScore(graph, inputDF)
    oshow.plotGraph(graph, outfile)
    oshow.toString(graph)
    oshow.write(outfile, graph)
    pass


# ADD RANDOM VARIABLE NODES
# len()
def addRandomVarNodesToGraph(graph, nodeNames):
    for col in nodeNames:
        graph.add_node(col)
    return graph

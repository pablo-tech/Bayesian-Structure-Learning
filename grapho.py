# Find the best Bayesian network, for a given dataset
# https://networkx.github.io/documentation/networkx-1.9/tutorial/tutorial.html


############
# GRAPHO components developed
import graphoscore as oscore
import graphoshow as oshow
import graphopanda as opanda
import graphoxnet as oxnet


# COMPUTE: method called to perform the whole job
# TODO: make sure no self loops
# TODO: output both png and gph files
def compute(infile, outfile):
    label = infile
    graph = oxnet.getNewGraph(label)
    inputDF = opanda.read(infile)
    randomVars = opanda.getRandomVarNodeNames(inputDF)
    graph = addRandomVarNodesToGraph(graph, randomVars)
    score = oscore.getScore(graph, inputDF, label)
    oshow.plotGraph(graph, outfile)
    oshow.toString(graph)
    oshow.write(outfile, graph)
    pass


# ADD RANDOM VARIABLE NODES
# len()
def addRandomVarNodesToGraph(graph, nodeNames):
    for col in nodeNames:
        graph.add_node(col)
        # print "ADDING NODE TO GRAPH: " + col
    return graph

# Find the best Bayesian network, for a given dataset
# https://networkx.github.io/documentation/networkx-1.9/tutorial/tutorial.html


############
# GRAPHO components developed
import graphoscore as oscore
import graphoshow as oshow
import graphopanda as opanda
import graphoxnet as oxnet


# COMPUTE: method called to perform the whole job
def compute(infile, outfile):
    label = infile
    graph = oxnet.getNewGraph(label)
    dataframe = opanda.read(infile)
    randomVars = opanda.getRandomVarNodeNames(dataframe)
    graph = addRandomVarNodesToGraph(graph, randomVars)
    graph = optimizeGraph(graph, dataframe)
    oshow.plotGraph(graph, outfile)
    oshow.toString(graph)
    oshow.write(outfile, graph)
    pass

# OPTIMIZE
# loop a limited number of times morphing graph into higher scoring shape
# TODO: make sure no self loops
def optimizeGraph(graph, dataframe):
    maxTries = 10
    attempt = 0
    score = oscore.getScore(graph, dataframe, attempt)
    for trie in range(0, maxTries):
        attempt = attempt + 1
        tentativeGraph = getHigherScoringGraph(graph, dataframe)
        tentativeScore = oscore.getScore(graph, dataframe, attempt)
        if tentativeScore>score:
            graph = tentativeGraph
            score = tentativeScore
    return graph


# MORPH
# greedy iteration over the graph looking for a better shape than current
def getHigherScoringGraph(graph, dataframe):
    return graph


# ADD RANDOM VARIABLE NODES
# len()
def addRandomVarNodesToGraph(graph, nodeNames):
    for col in nodeNames:
        graph.add_node(col)
        # print "ADDING NODE TO GRAPH: " + col
    return graph

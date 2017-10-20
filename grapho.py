# Find the best Bayesian network, for a given dataset
# https://networkx.github.io/documentation/networkx-1.9/tutorial/tutorial.html

# NETWORKX
try:
    import networkx as nx
except ImportError:
    raise ImportError("Networkx required for graph()")
except RuntimeError:
    print("Networkx unable to open")
    raise

# RANDOM
try:
    from random import choice
except ImportError:
    raise ImportError("Random required for rand()")
except RuntimeError:
    print("Random unable to open")
    raise

# MATH
try:
    import math
except ImportError:
    raise ImportError("Math required for abs()")
except RuntimeError:
    print("Math unable to open")
    raise

############
# GRAPHO components developed
import graphoscore as oscore
import graphoshow as oshow
import graphopanda as opanda
import graphoxnet as oxnet


# COMPUTE: method called to perform the whole job
def compute(infile, outfile):
    label = infile
    newGraph = oxnet.getNewGraph(label)
    dataframe = opanda.read(infile)
    randomVars = opanda.getRandomVarNames(dataframe)
    initGraph = addRandomVarNodesToGraph(newGraph, randomVars)
    optimGraph = optimizeGraph(initGraph, dataframe)
    oshow.plotGraph(optimGraph, outfile) # Disabled for submission
    oshow.write(outfile, optimGraph)
    # oshow.toString(optimGraph)
    print "DONE"
    pass

# OPTIMIZE
# loop a limited number of times morphing graph into higher scoring shape
def optimizeGraph(graph, dataframe):
    # graph = addRandomEdge(graph)
    # graph = addRandomEdge(graph)
    # graph = addRandomEdge(graph)
    initialScore = oscore.getScore(graph, dataframe)
    bestGraph = graph.copy()
    maxAttempts = 5
    attempt = 0
    for node in graph.nodes():
        if attempt < maxAttempts:
            bestGraph = getChangedGraph(bestGraph, node, dataframe).copy()
            attempt = attempt + 1
            print "TOP ATTEMPT: " + str(attempt)
    finalScore = oscore.getScore(bestGraph, dataframe)
    # print "****** INITIAL SCORE: " + str(int(initialScore)) + ", FINAL SCORE: " + str(int(finalScore)) + " ******"
    return bestGraph

# SEED the graph
def addRandomEdge(graph):
    fromNode = choice(graph.nodes())
    toNode = choice(graph.nodes())
    while fromNode==toNode:
        toNode = choice(graph.nodes())
    graph.add_edge(fromNode, toNode)  # seed the graph
    return graph

# MORPH: K2 ALGORITHM
# greedy iteration over the graph looking for a better shape than current
# attempt the modifiaction at the provided node
# try to connect the provided node to a random other node
# a minimum score gain is gauged before deciding to evolve the graph
def getChangedGraph(graph, toNode, dataframe):
    bestMoveGraph = graph.copy()    # greedily find the best graph after maxTries
    maxAttempts = 10
    attempt = 0
    for randomNode in graph.nodes():
        if attempt < maxAttempts:
            if randomNode!=toNode:   # connect only to a different node
                if not graph.has_edge(randomNode, toNode):     # connect only if the nodes are not connected either way
                    if not graph.has_edge(toNode, randomNode):  # connect only if the nodes are not connected either way
                        tentativeGraph1 = graph.copy()
                        tentativeGraph1.add_edge(randomNode, toNode)
                        tentativeGraph2 = graph.copy()
                        tentativeGraph2.add_edge(toNode, randomNode)
                        newBestGaph = compareGraphs(tentativeGraph1, tentativeGraph2, bestMoveGraph, dataframe)
                        bestMoveGraph = switchGraph(newBestGaph, bestMoveGraph).copy()
                        attempt = attempt + 1
                    else: print "Did not tackle because the nodes already shared an edge..."
                else: print "Did not tackle because the nodes already shared an edge..."
            else: print "Did not try to connect same to/from nodes..."
    return bestMoveGraph


# COMPARE: pick the best graph from a comparison set
def compareGraphs(tentativeGraph1, tentativeGraph2, bestMoveGraph, dataframe):
    tentativeScore1 = oscore.getScore(tentativeGraph1, dataframe)
    tentativeScore2 = oscore.getScore(tentativeGraph2, dataframe)
    currentBestScore = oscore.getScore(bestMoveGraph, dataframe)
    print "SCORE COMP: " + str(tentativeScore1) + " " + str(tentativeScore2) + " " + str(currentBestScore)
    # if attempt>10:
    # print "BOTTOM ATTEMPT: " + str(attempt)
    if long(tentativeScore1) > long(tentativeScore2):
        if long(tentativeScore1) > long(currentBestScore):
            return tentativeGraph1
    if long(tentativeScore2) > long(tentativeScore1):
        if long(tentativeScore2) > long(currentBestScore):
            return tentativeGraph2
    # else:   # encourage getting off the status quo; formula appears to not penalize lack of parents
    #     if long(tentativeScore1) > long(tentativeScore2):
    #         return tentativeGraph1
    #     if long(tentativeScore2) > long(tentativeScore1):
    #         return tentativeGraph2
    # print "ATTEMPT " + str(attempt)
    return bestMoveGraph

# SWITCH GRAPH: after verifying the graph is acyclical
def switchGraph(newBestGaph, bestMoveGraph):
    print "considering switch!"
    cycles = list(nx.simple_cycles(newBestGaph))
    if len(cycles) != 0:
        if nx.is_directed_acyclic_graph(newBestGaph):
            print "DAG test failed..."
            return bestMoveGraph
    else:
        print "==> Switching graph candidate!"
        return newBestGaph

# ADD RANDOM VARIABLE NODES
# len()
def addRandomVarNodesToGraph(graph, nodeNames):
    for col in nodeNames:
        graph.add_node(col)
        print "ADDING NODE TO GRAPH: " + col
    return graph

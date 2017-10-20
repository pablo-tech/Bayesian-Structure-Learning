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
    oshow.plotGraph(optimGraph, outfile)
    oshow.write(outfile, optimGraph)
    # oshow.toString(optimGraph)
    pass

# OPTIMIZE
# loop a limited number of times morphing graph into higher scoring shape
def optimizeGraph(graph, dataframe):
    # graph = addRandomEdge(graph)
    # graph = addRandomEdge(graph)
    # graph = addRandomEdge(graph)
    initialScore = oscore.getScore(graph, dataframe, 0)
    bestGraph = graph.copy()
    for node in graph.nodes():
        bestGraph = getChangedGraph(bestGraph, node, dataframe).copy()
    finalScore = oscore.getScore(bestGraph, dataframe, -1)
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
    attempt = 0
    bestMoveGraph = graph.copy()    # greedily find the best graph after maxTries
    for randomNode in graph.nodes():
        if randomNode!=toNode:   # connect only to a different node
            if not graph.has_edge(randomNode, toNode):     # connect only if the nodes are not connected either way
                if not graph.has_edge(toNode, randomNode):  # connect only if the nodes are not connected either way
                    tentativeGraph1 = graph.copy()
                    tentativeGraph1.add_edge(randomNode, toNode)
                    tentativeGraph2 = graph.copy()
                    tentativeGraph2.add_edge(toNode, randomNode)
                    newBestGaph = compareGraphs(tentativeGraph1, tentativeGraph2, bestMoveGraph, dataframe, attempt)
                    bestMoveGraph = switchGraph(newBestGaph, bestMoveGraph).copy()
                    attempt = attempt+1
                else: print "Did not tackle because the nodes already shared an edge..."
            else: print "Did not tackle because the nodes already shared an edge..."
        else: print "Did not try to connect same to/from nodes..."
    return bestMoveGraph


# COMPARE: pick the best graph from a comparison set
def compareGraphs(tentativeGraph1, tentativeGraph2, bestMoveGraph, dataframe, attempt):
    tentativeScore1 = oscore.getScore(tentativeGraph1, dataframe, attempt)
    tentativeScore2 = oscore.getScore(tentativeGraph2, dataframe, attempt)
    currentBestScore = oscore.getScore(bestMoveGraph, dataframe, attempt)
    print "SCORE COMP: " + str(tentativeScore1) + " " + str(tentativeScore2) + " " + str(currentBestScore)
    if attempt>100:
        if tentativeScore1>tentativeScore2:
            if tentativeScore1>currentBestScore:
                return tentativeGraph1
        if tentativeScore2 > tentativeScore1:
            if tentativeScore2>currentBestScore:
                return tentativeGraph2
    else:   # encourage getting off the status quo; formula appears to not penalize lack of parents
        if tentativeScore1>tentativeScore2:
            return tentativeGraph1
        if tentativeScore2 > tentativeScore1:
            return tentativeGraph2
    return bestMoveGraph
            # delta = int(tentativeScore) - int(currentBestScore)
    # print ">Evaluating new graph for better score: from=" + str(int(currentBestScore)) + " to=" + str(
    #     int(tentativeScore)) + \
    #       " GAIN=" + str(delta) + " adding EDGE=" + str(randomNode) + "-" + str(toNode) + \
    #       "TO =>NODES: " + str(tentativeGraph.nodes()) + ", =>EDGES: " + str(tentativeGraph.edges())
    # if int(delta) > int(minScoreGain):
    # else:
    #     print "Did not pursue because the toNode already has a parent..."

# SWITCH GRAPH: after verifying the graph is acyclical
def switchGraph(newBestGaph, bestMoveGraph):
    cycles = list(nx.simple_cycles(newBestGaph))
    print "Potential Graph Cycles: " + str(cycles)
    if len(cycles) == 0:
        # if nx.is_directed_acyclic_graph(tentativeGraph)==False:
        print "==> Switching graph candidate!"
        return newBestGaph
        # else: print "Did not adopt because it would cause a cycle in the graph..."
    else:
        print "Did not enough score gain to make the change..."
        return bestMoveGraph


# ADD RANDOM VARIABLE NODES
# len()
def addRandomVarNodesToGraph(graph, nodeNames):
    for col in nodeNames:
        graph.add_node(col)
        print "ADDING NODE TO GRAPH: " + col
    return graph

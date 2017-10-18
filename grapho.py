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
    randomVars = opanda.getRandomVarNodeNames(dataframe)
    initGraph = addRandomVarNodesToGraph(newGraph, randomVars)
    optimGraph = optimizeGraph(initGraph, dataframe)
    oshow.plotGraph(optimGraph, outfile)
    oshow.toString(optimGraph)
    oshow.write(outfile, optimGraph)
    pass

# OPTIMIZE
# loop a limited number of times morphing graph into higher scoring shape
# a minimum score gain is gauged before deciding to evolve the graph
def optimizeGraph(graph, dataframe):
    maxTries = 10
    attempt = 0
    initialScore = oscore.getScore(graph, dataframe, attempt)
    for trie in range(0, maxTries):
        attempt = attempt + 1
        for node in graph.nodes():
            graph = getChangedGraph(graph, node, dataframe)
    finalScore = oscore.getScore(graph, dataframe, attempt)
    print "****** INITIAL SCORE: " + str(int(initialScore)) + ", FINAL SCORE: " + str(int(finalScore)) + " ******"
    return graph

# MORPH
# greedy iteration over the graph looking for a better shape than current
# attempt the modifiaction at the provided node
# try to connect the provided node to a random other node
def getChangedGraph(graph, fromNode, dataframe):
    maxTries = 100
    attempt = 0
    minScoreGain = 100
    initialGraph = graph
    bestMoveGaph = graph    # greedily find the best graph after maxTries
    while True:
        randomNode = choice(graph.nodes())
        attempt = attempt + 1
        print "Attempt=" + str(attempt) + " at optimizing node=" + str(fromNode)
        if attempt>maxTries:
            if int(oscore.getScore(bestMoveGaph, dataframe, attempt)) > int(oscore.getScore(initialGraph, dataframe, attempt)):
                return bestMoveGaph # after many attempts, return the bestMoveGaph
            else:
                return initialGraph
        if randomNode!=fromNode:   # connect only to a different node
            if not graph.has_edge(fromNode, randomNode):     # connect only if the nodes are not connected either way
                if not graph.has_edge(randomNode, fromNode):  # connect only if the nodes are not connected either way
                    if len(oxnet.getRandomVarParents(randomNode, graph))==0:  # allow one parent for now
                        tentativeGraph = graph
                        tentativeGraph.add_edge(fromNode, randomNode)
                        tentativeScore = oscore.getScore(tentativeGraph, dataframe, attempt)
                        currentBestScore = oscore.getScore(bestMoveGaph, dataframe, attempt)
                        delta = int(tentativeScore) - int(currentBestScore)
                        print ">Evaluating new graph for better score: from=" + str(int(currentBestScore)) + " to=" + str(int(tentativeScore)) + \
                              " GAIN=" + str(delta) + " adding EDGE=" + str(fromNode) +"-"+ str(randomNode)
                        if int(delta) > int(minScoreGain):
                            cycles = list(nx.simple_cycles(tentativeGraph))
                            print "Potential Graph Cycles: " + str(cycles)
                            if len(cycles)==0:
                                if nx.is_directed_acyclic_graph(tentativeGraph)==False:
                                    print "==> Switching graph candidate!"
                                    bestMoveGaph = tentativeGraph

# ADD RANDOM VARIABLE NODES
# len()
def addRandomVarNodesToGraph(graph, nodeNames):
    for col in nodeNames:
        graph.add_node(col)
        print "ADDING NODE TO GRAPH: " + col
    return graph

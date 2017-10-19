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
    oshow.write(outfile, optimGraph)
    # oshow.toString(optimGraph)
    pass

# OPTIMIZE
# loop a limited number of times morphing graph into higher scoring shape
# a minimum score gain is gauged before deciding to evolve the graph
def optimizeGraph(graph, dataframe):
    maxTries = 3
    attempt = 0
    initialScore = oscore.getScore(graph, dataframe, attempt)
    bestGraph = graph.copy()
    for trie in range(0, maxTries):
        attempt = attempt + 1
        for node in graph.nodes():
            bestGraph = getChangedGraph(bestGraph, node, dataframe)
    finalScore = oscore.getScore(bestGraph, dataframe, attempt)
    print "****** INITIAL SCORE: " + str(int(initialScore)) + ", FINAL SCORE: " + str(int(finalScore)) + " ******"
    return bestGraph

# MORPH
# greedy iteration over the graph looking for a better shape than current
# attempt the modifiaction at the provided node
# try to connect the provided node to a random other node
def getChangedGraph(graph, fromNode, dataframe):
    maxTries = 100
    attempt = 0
    minScoreGain = 10
    initialGraph = graph.copy()
    bestMoveGaph = graph.copy()    # greedily find the best graph after maxTries
    while True:
        randomNode = choice(graph.nodes())
        attempt = attempt + 1
        print "Attempt=" + str(attempt) + " at optimizing from node=" + str(fromNode)
        if attempt>maxTries:
            if int(oscore.getScore(bestMoveGaph, dataframe, attempt)) > int(oscore.getScore(initialGraph, dataframe, attempt)):
                print "FOUND a graph optimization from node=" + str(fromNode) + "... " + str(oshow.toEdgesString(bestMoveGaph))
                return bestMoveGaph # after many attempts, return the bestMoveGaph
            else:
                print "NO better graph found from node=" + str(fromNode) + "... " + str(oshow.toEdgesString(initialGraph))
                return initialGraph
        # if randomNode!=fromNode:   # connect only to a different node
        if not graph.has_edge(fromNode, randomNode):     # connect only if the nodes are not connected either way
            if not graph.has_edge(randomNode, fromNode):  # connect only if the nodes are not connected either way
                if len(oxnet.getRandomVarParents(randomNode, graph))==0:  # allow one parent for now
                    tentativeGraph = bestMoveGaph.copy()
                    tentativeGraph.add_edge(fromNode, randomNode)
                    tentativeScore = oscore.getScore(tentativeGraph, dataframe, attempt)
                    currentBestScore = oscore.getScore(bestMoveGaph, dataframe, attempt)
                    delta = int(tentativeScore) - int(currentBestScore)
                    print ">Evaluating new graph for better score: from=" + str(int(currentBestScore)) + " to=" + str(int(tentativeScore)) + \
                          " GAIN=" + str(delta) + " adding EDGE=" + str(fromNode) +"-"+ str(randomNode) + \
                          "TO =>NODES: " + str(tentativeGraph.nodes()) + ", =>EDGES: " + str(tentativeGraph.edges())
                    if int(delta) > int(minScoreGain):
                        cycles = list(nx.simple_cycles(tentativeGraph))
                        print "Potential Graph Cycles: " + str(cycles)
                        if len(cycles)==0:
                            # if nx.is_directed_acyclic_graph(tentativeGraph)==False:
                            print "==> Switching graph candidate!"
                            bestMoveGaph = tentativeGraph.copy()
                            # else: print "Did not adopt because it would cause a cycle in the graph..."
                    else: print "Did not enough score gain to make the change..."
                else: print "Did not pursue because the toNode already has a parent..."
            else: print "Did not tackle because the nodes already shared an edge..."
        else: print "Did not tackle because the nodes already shared an edge..."
        # else: print "Did not try to connect same to/from nodes..."


# ADD RANDOM VARIABLE NODES
# len()
def addRandomVarNodesToGraph(graph, nodeNames):
    for col in nodeNames:
        graph.add_node(col)
        print "ADDING NODE TO GRAPH: " + col
    return graph

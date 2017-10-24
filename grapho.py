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
    optimGraph = optimizeGraph(initGraph, dataframe, outfile)
    print "DONE"
    pass

# OPTIMIZE
# loop a limited number of times morphing graph into higher scoring shape
def optimizeGraph(graph, dataframe, outfile):
    initialScore = oscore.getScore(graph, dataframe)
    bestGraph = graph.copy()
    maxAttempts = 20
    attempt = 0
    for node in graph.nodes():
        if attempt < maxAttempts:
            bestGraph = getChangedGraph(bestGraph, node, dataframe).copy()
            attempt = attempt + 1
            oshow.plotGraph(bestGraph, outfile)  # Disabled for submission
            oshow.write(outfile, bestGraph)
            # oshow.toString(optimGraph)
            print "TOP ATTEMPT: " + str(attempt)

    finalScore = oscore.getScore(bestGraph, dataframe)
    print "****** INITIAL SCORE: " + str(int(initialScore)) + ", FINAL SCORE: " + str(int(finalScore)) + " ******"
    return bestGraph


# MORPH: K2 ALGORITHM
# greedy iteration over the graph looking for a better shape than current
# attempt the modifiaction at the provided node
# try to connect the provided node to a random other node
# a minimum score gain is gauged before deciding to evolve the graph
def getChangedGraph(graph, givenNode, dataframe):
    bestGraph = graph.copy()    # greedily find the best graph after maxTries
    for choiceNode in graph.nodes():
        if choiceNode!=givenNode:   # connect only to a different node
            candidateGraphs = getCandidateGraphs(choiceNode, givenNode, bestGraph)
            newBestGraph = getBestGraph(candidateGraphs, bestGraph, dataframe)
            switched = switchGraph(newBestGraph, bestGraph)
            bestGraph = switched.copy()
        else: print "Did not try to connect same to/from nodes..."
    return bestGraph

# GRADIENT ASCENT: looking for neighboring better scores
def getCandidateGraphs(choiceNode, givenNode, currentGraph):
    candidates = []
    # add edge
    if not currentGraph.has_edge(choiceNode, givenNode):
        if not currentGraph.has_edge(givenNode, choiceNode):
            tentativeGraph1 = currentGraph.copy()
            tentativeGraph1.add_edge(choiceNode, givenNode)
            candidates.append(tentativeGraph1)
    # add opposite edge
    if not currentGraph.has_edge(givenNode, choiceNode):
        if not currentGraph.has_edge(choiceNode, givenNode):
            tentativeGraph2 = currentGraph.copy()
            tentativeGraph2.add_edge(givenNode, choiceNode)
            candidates.append(tentativeGraph2)
    # remove edge
    if currentGraph.has_edge(choiceNode, givenNode):
        tentativeGraph3 = currentGraph.copy()
        tentativeGraph3.remove_edge(choiceNode, givenNode)
        candidates.append(tentativeGraph3)
    # remove opposite edge
    if currentGraph.has_edge(givenNode, choiceNode):
        tentativeGraph4 = currentGraph.copy()
        tentativeGraph4.remove_edge(givenNode, choiceNode)
        candidates.append(tentativeGraph4)
    return candidates

# COMPARE: pick the best graph from a comparison set
def getBestGraph(candidates, currentGraph, dataframe):
    priorGraph = currentGraph
    bestGraph = priorGraph
    priorScore = oscore.getScore(currentGraph, dataframe)
    newBestScore = priorScore
    for graph in candidates:
        score = oscore.getScore(graph, dataframe)
        if score > newBestScore:
            bestGraph = graph.copy()
            newBestScore = score
    if newBestScore > priorScore:
        print "considering switch! Score FROM: priorScore " + str(long(priorScore)) + " TO " + str(long(newBestScore))
    return bestGraph

# SWITCH GRAPH: after verifying the graph is acyclical
def switchGraph(newBestGaph, currentGraph):
    cycles = list(nx.simple_cycles(newBestGaph))
    if len(cycles) != 0:
        if nx.is_directed_acyclic_graph(newBestGaph):
            print "DAG test failed..."
            return currentGraph
    print "==> Switched to graph candidate! " + oshow.toString(newBestGaph)
    return newBestGaph

# ADD RANDOM VARIABLE NODES
# len()
def addRandomVarNodesToGraph(graph, nodeNames):
    for col in nodeNames:
        graph.add_node(col)
        print "ADDING NODE TO GRAPH: " + col
    return graph

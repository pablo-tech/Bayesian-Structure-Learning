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
    maxAttempts = 5
    attempt = 0
    if attempt < maxAttempts:
        for choiceNode in graph.nodes():
            if choiceNode!=givenNode:   # connect only to a different node
                if not graph.has_edge(choiceNode, givenNode):     # connect only if the nodes are not connected either way
                    if not graph.has_edge(givenNode, choiceNode):  # connect only if the nodes are not connected either way
                        candidateGraphs = getCandidateGraphs(choiceNode, givenNode, bestGraph)
                        newBestGraph = getBestGraph(candidateGraphs, bestGraph, dataframe)
                        switched = switchGraph(newBestGraph, bestGraph)
                        bestGraph = switched.copy()
                        attempt = attempt + 1
                    else: print "Did not tackle because the nodes already shared an edge..."
                else: print "Did not tackle because the nodes already shared an edge..."
            else: print "Did not try to connect same to/from nodes..."
    return bestGraph

def getCandidateGraphs(choiceNode, givenNode, currentGraph):
    candidates = []
    # add edge
    tentativeGraph1 = currentGraph.copy()
    tentativeGraph1.add_edge(choiceNode, givenNode)
    candidates.append(tentativeGraph1)
    # add opposite edge
    tentativeGraph2 = currentGraph.copy()
    tentativeGraph2.add_edge(givenNode, choiceNode)
    candidates.append(tentativeGraph2)
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
def switchGraph(newBestGaph, bestMoveGraph):
    cycles = list(nx.simple_cycles(newBestGaph))
    if len(cycles) != 0:
        if nx.is_directed_acyclic_graph(newBestGaph):
            print "DAG test failed..."
            return bestMoveGraph
    print "==> Switching graph candidate!"
    return newBestGaph

# ADD RANDOM VARIABLE NODES
# len()
def addRandomVarNodesToGraph(graph, nodeNames):
    for col in nodeNames:
        graph.add_node(col)
        print "ADDING NODE TO GRAPH: " + col
    return graph

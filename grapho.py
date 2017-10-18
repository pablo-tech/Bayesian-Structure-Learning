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
    minScoreGain = 100
    score = initialScore
    for trie in range(0, maxTries):
        attempt = attempt + 1
        for node in graph.nodes():
            tentativeGraph = getChangedGraph(graph, node)
            tentativeScore = oscore.getScore(tentativeGraph, dataframe, attempt)
            cycles = list(nx.simple_cycles(tentativeGraph))
            if len(cycles)==0:
                print "Graph Cycles: " + str(cycles)
                if nx.is_directed_acyclic_graph(tentativeGraph):    #   make sure it is an acyclical graph
                    delta = int(tentativeScore) - int(score)
                    if int(delta)>int(minScoreGain):
                        print ">modifying graph score from=" + str(score) + " to=" + str(tentativeScore) + " delta=" +str(delta)
                        graph = tentativeGraph
                        score = tentativeScore
    print "****** INITIAL SCORE: " + str(initialScore) + ", FINAL SCORE: " + str(score) + " ******"
    return graph


# MORPH
# greedy iteration over the graph looking for a better shape than current
# attempt the modifiaction at the provided node
# try to connect the provided node to a random other node
def getChangedGraph(graph, node):
    maxTries = 100
    attempt = 0
    while True:
        randomNode = choice(graph.nodes())
        attempt = attempt + 1
        if attempt>maxTries:
            return graph
        if randomNode!=node:   # connect only to a different node
            if not graph.has_edge(node, randomNode):     # connect only if the nodes are not connected
                if len(oxnet.getRandomVarParents(randomNode, graph))==0:  # allow one parent for now
                    graph.add_edge(node, randomNode)
                    # print "trying to switch graphs!!!"
                    return graph
                # else: print "already has parent"
            # else: print "edge already in place"
        # else: print "nodes are the same"

# ADD RANDOM VARIABLE NODES
# len()
def addRandomVarNodesToGraph(graph, nodeNames):
    for col in nodeNames:
        graph.add_node(col)
        print "ADDING NODE TO GRAPH: " + col
    return graph

# NETWORKX
try:
    import networkx as nx
except ImportError:
    raise ImportError("Networkx required for graph()")
except RuntimeError:
    print("Networkx unable to open")
    raise

############
import grapho
import graphoshow as oshow
import graphoscore as oscore
import graphopanda as opanda
import graphoxnet as oxnet

inputFile = "cooperh.csv"
outputFile = "cooperh.gph"

dataframe = opanda.read(inputFile)
randomVarNames = opanda.getRandomVarNodeNames(dataframe)
print "RANDOM VAR NAMES: " + str(randomVarNames)

############
# NETWORK 1: x1 -> x2 -> x3
net1Name = "net1"
net1OutputFile = outputFile + "-" + net1Name

net1Graph = oxnet.getNewGraph(net1Name)
net1Graph = grapho.addRandomVarNodesToGraph(net1Graph, randomVarNames)

net1Graph.add_edge("x1", "x2")
net1Graph.add_edge("x2", "x3")
opanda.getUniqueRandomVarValues(dataframe, "x1")

net1Score = oscore.getScore(net1Graph, dataframe, net1Name)
print net1Name + " SCORE: " + str(net1Score)

oshow.plotGraph(net1Graph, net1OutputFile)
oshow.toString(net1Graph)
oshow.write(net1OutputFile, net1Graph)

############
# NETWORK 2: x1 -> x2, x1 -> x3
net2Name = "net2"
net2OutputFile = outputFile + "-" + net2Name

net2Graph = oxnet.getNewGraph(net2Name)
net2Graph = grapho.addRandomVarNodesToGraph(net2Graph, randomVarNames)

net2Graph.add_edge("x1", "x2")
net2Graph.add_edge("x1", "x3")

net2Score = oscore.getScore(net2Graph, dataframe, net2Name)
print net2Name + " SCORE: " + str(net2Score)

oshow.plotGraph(net2Graph, net2OutputFile)
oshow.toString(net2Graph)
oshow.write(net2OutputFile, net2Graph)


############
# VERIFY NETWORK 1: with Decisions Under Uncertainty, page 47, log formula 2.83
values = [(2, [[5, 5]]), (2, [[1, 4], [4, 1]]), (2, [[4, 1], [0, 5]])]

alphaIJ = oscore.getAlphaijFactors(values)
print "ALPHA: " + str(alphaIJ)

mIJ = oscore.getMijFactors(values)
print "M: " + str(mIJ)

randomVarNames = opanda.getRandomVarNodeNames(dataframe)
n = oscore.getNumRandomVars(randomVarNames)
print "max I: " + str(n)

parents = oxnet.getRandomVarParents("x2", net1Graph)
qi = oscore.getNumRandmVarParents(parents)
print "max J: " + str(qi)

ri = oscore.getNumRandomVarValues(dataframe, "x2")
print "max K: " + str(ri)

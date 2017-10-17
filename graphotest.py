import grapho
import graphoshow as oshow

# NETWORKX
try:
    import networkx as nx
except ImportError:
    raise ImportError("Networkx required for graph()")
except RuntimeError:
    print("Networkx unable to open")
    raise


inputFile = "cooperh.csv"
outputFile = "cooperh.gph"

# grapho.compute("cooperh.csv", "cooperh.gph")

inputDF = grapho.read(inputFile)

# NETWORK 1: x1 -> x2 -> x3
net1OutputFile = outputFile + "-net1"

net1Graph = nx.DiGraph()
net1Graph = grapho.addRandomVarNodesToGraph(net1Graph, inputDF)

oshow.plotGraph(net1Graph, net1OutputFile)
oshow.toString(net1Graph)
oshow.write(net1OutputFile, net1Graph)

# NETWORK 2: x1 -> x2, x1 -> x3
net2OutputFile = outputFile + "-net2"

net2Graph = nx.DiGraph()
net2Graph = grapho.addRandomVarNodesToGraph(net2Graph, inputDF)

oshow.plotGraph(net2Graph, net2OutputFile)
oshow.toString(net2Graph)
oshow.write(net2OutputFile, net2Graph)

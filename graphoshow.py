# NETWORKX
try:
    import networkx as nx
except ImportError:
    raise ImportError("Networkx required for graph()")
except RuntimeError:
    print("Networkx unable to open")
    raise

# MATPLOTLIB
try:
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError("Matplotlib required for draw()")
except RuntimeError:
    print("Matplotlib unable to open")
    raise

# PRINT nodes, graphs, edges, neighbors
def toString(graph):
    print "GRAPH: {} ".format(graph.graph)
    print "NODES: {}".format(graph.nodes())
    print "EDGES: {}".format(graph.edges())
    for node in graph.nodes():
        print "{} EDGES: {}".format(node, graph[node])
        print "{} NEIGHTBORS: {}".format(node, graph.neighbors(node))

# PLOT graph: nodes, edges, labesl
def plotGraph(graph, filename):
    # POSITIONS
    pos = nx.spring_layout(graph)  # positions for all nodes
    # NODES
    nx.draw_networkx_nodes(graph, pos,
                           nodelist=graph.nodes(),
                           node_color='r', node_size=500) # alpha=0.8,
    # EDGES
    nx.draw_networkx_edges(graph, pos,
                           edgelist=graph.edges(),
                           edge_color='b') # alpha=0.5, width=8,
    # LABELS
    labels = {}
    for node in graph.nodes():
        labels[str(node)] = str(node)
    nx.draw_networkx_labels(graph, pos, labels, font_size=10)
    # DRAW ALL
    plt.axis('off')
    plt.savefig(filename)
    # plt.show()

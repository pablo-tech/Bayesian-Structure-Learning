# Plot a graph

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

# CSV
try:
    import csv
except ImportError:
    raise ImportError("CSV required for read()")
except RuntimeError:
    print("CSV unable to open")
    raise

############
# GRAPHO components developed
import graphoxnet as oxnet


# PRINT nodes, graphs, edges, neighbors
def toString(graph):
    print "GRAPH: {} ".format(graph.graph)
    print "NODES: {}".format(graph.nodes())
    print "EDGES: {}".format(graph.edges())
    for node in graph.nodes():
        print "{} EDGES: {}".format(node, graph[node])
        print "{} NEIGHTBORS: {}".format(node, graph.neighbors(node))

# PLOT graph: nodes, edges, labesl
# https://stackoverflow.com/questions/8213522/when-to-use-cla-clf-or-close-for-clearing-a-plot-in-matplotlib
def plotGraph(graph, filename):
    plt.clf()
    # POSITIONS
    pos = nx.spring_layout(graph)  # positions for all nodes
    # NODES
    nx.draw_networkx_nodes(graph, pos,
                           nodelist=graph.nodes(),
                           node_color='r', node_size=500) # alpha=0.8,
    # EDGES
    nx.draw_networkx_edges(graph, pos,
                           edgelist=graph.edges(),
                           edge_color='b',
                           arrows = True) # alpha=0.5, width=8,
    # LABELS
    labels = {}
    for node in graph.nodes():
        labels[str(node)] = str(node)
    nx.draw_networkx_labels(graph, pos, labels, font_size=10)
    # DRAW ALL
    plt.axis('off')
    plt.savefig(filename + ".png")
    # plt.show()


# REPRESENT: save the graph to file
# def represent(graph):

# WRITE: a gph output file
def write(outfile, graph):
    # print "GOT TO WRITE " + str(graph.nodes())
    with open(outfile, 'wb') as csvfile:
        owriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for node in graph.nodes():
            row = node
            parents = oxnet.getRandomVarParents(str(node), graph)
            # print "Parents: " + str(parents)
            for parent in parents:
                row = parent + "," + node
            print "writing row to file: " + str(row)
            owriter.writerow([row])
    pass


def analizeGraph(graph):
    # degree()
    nx.connected_components
    # graph.adj
    # print(graph.node['fare'])
    # nx.connected_components(graph)
    # graph.adj
    # print(inputDF)
    # .values
    # df.head()

import networkx as nx

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

# SYSTEM
try:
    import sys
except ImportError:
    raise ImportError("SYS required for ARGUMENTS()")
except RuntimeError:
    print("SYS unable to open")
    raise

# CSV
try:
    import csv
except ImportError:
    raise ImportError("CSV required for read()")
except RuntimeError:
    print("CSV unable to open")
    raise

# PANDAS
try:
    import pandas as pd
except ImportError:
    raise ImportError("PANDAS required for read()")
except RuntimeError:
    print("PANDAS unable to open")
    raise


# INPUT/OUTPUT files
input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

# READER
# with open('small.csv', 'rb') as csvfile:
#     csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
#     for row in csv_reader:
#         print ', '.join(row)


inputDF = pd.read_csv(input_file_name)
print(inputDF)

# COMPUTE
# Directed graphs, that is, graphs with directed edges
G=nx.Graph()
G=nx.DiGraph()

G.add_edge(2,3,weight=0.9)
G.add_nodes_from([2,3])

print(G.adj)


# WRITER
with open(output_file_name, 'wb') as csvfile:
    gph_writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    gph_writer.writerow(['Spam'] * 5 + ['Baked Beans'])
    gph_writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])




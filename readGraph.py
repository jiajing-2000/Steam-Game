from networkx.readwrite import json_graph
import json

with open("data/graph.json", "r", encoding="latin-1") as json_file:
    graph_data = json.load(json_file)
G = json_graph.node_link_graph(graph_data)

print(G.nodes[1])

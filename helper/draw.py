import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G):
    plt.figure(figsize=(8, 6))  
    pos = nx.spring_layout(G)  
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='black', font_size=10, node_size=500)  
    plt.title("Graph Visualization")  
    plt.show()  

def draw_bigraph(G):
    top = nx.bipartite.sets(G)[0]
    pos = nx.bipartite_layout(G, top)
    edge_labels = nx.get_edge_attributes(G, 'weight') 
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='black', font_size=10, node_size=500)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos = 0.3)  
    plt.title("Bipartite Graph with Edge Weights")
    plt.show()


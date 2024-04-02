from pulp import LpVariable
import networkx as nx
import matplotlib.pyplot as plt
"""
    SUMMARY : This function create bipartite graph from ILP problem

    INPUT   : LpProblem

    OUTPUT  : Bipartite grapj
"""

def Create_bipartite_graph_ILP(problem):


    G = nx.Graph()
    # Add variable in 1st part
    variables = [var for var in problem.variables() if isinstance(var, LpVariable)]
    for var in variables:
        G.add_node(var.name, bipartite=0)

    # Add constraints in 2nd part
    constraints = [const.name for const in problem.constraints.values()]
    for const in constraints:
        G.add_node(const, bipartite=1)

    # Add edge with corespond weight
    coefficients = {x.name: {const: problem.constraints[const].get(x, 0) for const in constraints} for x in variables}
    for var, coeff in coefficients.items():
        for const, weight in coeff.items():
            G.add_edge(var, const, weight=weight)

    return G

# # Sử dụng hàm để tạo đồ thị từ bài toán đã cho
# G = create_bipartite_graph_ILP(problem)

# # Vẽ đồ thị
# top = nx.bipartite.sets(G)[0]
# pos = nx.bipartite_layout(G, top)
# edge_labels = nx.get_edge_attributes(G, 'weight')  # Lấy trọng số của các cạnh
# nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='black', font_size=10, node_size=500)
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos = 0.3)  # Hiển thị trọng số trên các cạnh
# plt.title("Bipartite Graph with Edge Weights")
# plt.show()

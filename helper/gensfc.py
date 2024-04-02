import networkx as nx
import random as rd
import uuid

"""
    SUMMARY: This function generate SFCs

    INPUT: 
        + nodecount : number of node per SFC        - int
        + nodereq   : node capacity requirement     - int
        + linkreq   : link capacity requirement     - int
        + num_sfc   : number of sfcs                - int
    
    OUTPUT: set of SFC

"""

def Generate_linear_sfc_graph(nodecount, nodereq, linkreq, num_sfc):
    def random_int_or_tuple(value):
        if isinstance(value, int):
            return value
        else:
            return rd.randint(value[0], value[1])

    sfc_graphs = []

    # Tạo ngẫu nhiên yêu cầu cho nút và liên kết cho SFC đầu tiên
    node_req = random_int_or_tuple(nodereq)
    link_req = random_int_or_tuple(linkreq)

    for _ in range(num_sfc):
        SFC = nx.DiGraph()
        nodecount = nodecount if isinstance(nodecount, int) else rd.randint(nodecount[0], nodecount[1])

        for i in range(nodecount):
            SFC.add_node(i, req=node_req)

        for n in list(SFC.nodes)[:-1]:
            SFC.add_edge(n, n+1, req=link_req)

        SFC.name = f"linearsfc_{len(list(SFC.nodes))}nodes_{len(list(SFC.edges))}links_{uuid.uuid4().hex[:8]}"
        sfc_graphs.append(SFC)


    return sfc_graphs
# sfc_graphs = generate_linear_sfc_graph(5, 2 , 2, 3)


# Sử dụng hàm để tạo ra số lượng SFC giống nhau và lưu chúng vào một danh sách
# num_sfc = 3  # Số lượng SFC muốn tạo
# nodecount = (5, 10)  # Số lượng nút trong mỗi SFC
# nodereq = (1, 5)  # Yêu cầu cho mỗi nút trong mỗi SFC
# linkreq = (2, 5)  # Yêu cầu cho mỗi liên kết trong mỗi SFC

# sfc_graphs = generate_linear_sfc_graph((5, 5), (1, 5) , (2, 2), 3)

# # In thông tin của các SFC đã tạo
# for idx, sfc in enumerate(sfc_graphs):
#     print(f"SFC {idx + 1}: {sfc.name}, Nodes: {len(list(sfc.nodes))}, Edges: {len(list(sfc.edges))}")

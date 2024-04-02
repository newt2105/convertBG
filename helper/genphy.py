import networkx as nx
import random as rd
import uuid

"""
    SUMMARY: This function generate PHY graph

    INPUT: 
        + nodecap           : node capacity requirement     - int
        + linkcap           : link capacity requirement     - int
        + nodecount         : number of node                - int
        + linkdisconnectrate: the rate of disconnected link - float
    
    OUTPUT: Phy graph

"""

def Generate_random_graph(nodecap, linkcap, nodecount, linkdisconnectrate=0):
    def random_int_or_tuple(value):
        if isinstance(value, int):
            return value
        else:
            return rd.randint(value[0], value[1])

    nodecount = nodecount if isinstance(nodecount, int) else rd.randint(nodecount[0], nodecount[1])
    PHY = nx.DiGraph()

    for i in range(nodecount):
        cap = random_int_or_tuple(nodecap)
        PHY.add_node(i, cap=cap)

    for n in PHY.nodes:
        for nn in PHY.nodes:
            if n == nn:
                continue
            if not PHY.has_edge(n, nn):
                linkcap = random_int_or_tuple(linkcap)
                PHY.add_edge(n, nn, cap=linkcap)
                PHY.add_edge(nn, n, cap=linkcap)

    linkcount = len(list(PHY.edges))
    for i in range(int(linkcount * linkdisconnectrate)):
        link = rd.choice(list(PHY.edges))
        PHY.remove_edge(link[0], link[1])

    PHY.name = f"randomphy_{len(list(PHY.nodes))}nodes_{len(list(PHY.edges))}links_{uuid.uuid4().hex[:8]}"
    return PHY



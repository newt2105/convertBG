from pulp import *
import networkx as nx

"""
    SUMMARY : This function create ILP problem

    INPUT   : Phy graph and SFCs

    OUTPUT  : ILP problem
"""

def Convert_to_ilp(PHY: nx.DiGraph, SFCs: list[nx.DiGraph]) -> LpProblem:
    problem = LpProblem(name="GraphMappingProblem", sense=LpMinimize)

    # Build Node Placement List
    phiNode_S = []
    for sfc in SFCs:
        phiNode_S.append(LpVariable.dicts(
            name=f"xNode_{SFCs.index(sfc)}",
            indices=(sfc.nodes, PHY.nodes),
            cat="Binary"
        ))

    # Build Link Placement List
    phiLink_S = []
    for sfc in SFCs:
        phiLink_S.append(LpVariable.dicts(
            name=f"xEdge_{SFCs.index(sfc)}",
            indices=(sfc.edges, PHY.edges),
            cat="Binary"
        ))

    phiSFC = LpVariable.dicts(
        name="xSFC",
        indices=(range(len(SFCs))),
        cat="Binary"
    )

    # Building Constraints
    problem.constraints.clear()

    ## C1: Node Capacity
    for node in PHY.nodes:
        problem += (
            lpSum(
                lpSum(
                    phiNode_S[SFCs.index(sfc)][node_S][node] * nx.get_node_attributes(sfc, "req")[node_S]
                    for node_S in sfc.nodes
                )
                for sfc in SFCs
            )
            <= nx.get_node_attributes(PHY, "cap")[node],
            f"C1_i{node}"
        )

    ## C2: Edge Capacity
    for edge in PHY.edges:
        problem += (
            lpSum(
                lpSum(
                    phiLink_S[SFCs.index(sfc)][link_S][edge] * nx.get_edge_attributes(sfc, "req")[link_S]
                    for link_S in sfc.edges
                )
                for sfc in SFCs
            )
            <= nx.get_edge_attributes(PHY, "cap")[edge],
            f"C2_ij{edge}"
        )

    ## C3: Map 1 VNF - 1 PHYNODE
    for sfc in SFCs:
        for node in PHY.nodes:
            problem += (
                lpSum(
                    phiNode_S[SFCs.index(sfc)][node_S][node]
                    for node_S in sfc.nodes
                )
                <= 1,
                f"C3_i{node}_s{SFCs.index(sfc)}"
            )

    ## C4.1: Map All VNF
    for sfc in SFCs:
        for node_S in sfc.nodes:
            problem += (
                lpSum(
                    phiNode_S[SFCs.index(sfc)][node_S][node]
                    for node in PHY.nodes
                )
                == phiSFC[SFCs.index(sfc)],
                f"C4_v{node_S}_s{SFCs.index(sfc)}"
            )

    ## C4.2: Map All VLinks
    for sfc in SFCs:
        for edge_S in sfc.edges:
            problem += (
                lpSum(
                    phiLink_S[SFCs.index(sfc)][edge_S][edge]
                    for edge in PHY.edges
                )
                == phiSFC[SFCs.index(sfc)],
                f"C4_v{edge_S}_s{SFCs.index(sfc)}"
            )

    ## C5: Flow-Conservation
    for sfc in SFCs:
        for edge_S in sfc.edges:
            for node in PHY.nodes:
                problem += (
                    lpSum(
                        phiLink_S[SFCs.index(sfc)][edge_S].get((node, nodej))
                        for nodej in PHY.nodes
                    )
                    - 
                    lpSum(
                        phiLink_S[SFCs.index(sfc)][edge_S].get((nodej, node))
                        for nodej in PHY.nodes
                    )
                    == phiNode_S[SFCs.index(sfc)][edge_S[0]][node] - phiNode_S[SFCs.index(sfc)][edge_S[1]][node],
                    f"C5_s{SFCs.index(sfc)}_vw{edge_S}_i{node}"
                )

    # Target function building
    problem += (
        0 - lpSum(
            phiSFC[SFCs.index(sfc)]
            for sfc in SFCs
        )
    )


    return problem

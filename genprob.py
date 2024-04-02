import yaml
import pickle
import gzip

from helper import draw, genphy, ilp, tobigraph, gensfc

"""
    INPUT   : file path
    OUTPUT  : Phy graph and SFCs

    SUMMARY : This file generate graph: PHY and SFCs
"""

def genprob(filepath):
    #read from config file
    with open(filepath, 'r') as file:
        config = yaml.safe_load(file)

    linear_sfc_config = config['linear_sfc_generation']
    network_config = config['network_generation']

    # Generate SFCs graph
    SFCs = gensfc.Generate_linear_sfc_graph(
        linear_sfc_config['node_count'],
        linear_sfc_config['node_requirement'],
        linear_sfc_config['link_requirement'],
        linear_sfc_config['num_sfc']
    )

    # Generate PHY graph
    PHY = genphy.Generate_random_graph(
        network_config['node_capacity'],
        network_config['link_capacity'],
        network_config['node_count'],
        network_config['link_disconnect_rate']
    )

    # save graph
    with gzip.open('data/prob/output_graphs.pkl.gz', 'wb') as outfile:
        pickle.dump({'SFCs': SFCs, 'PHY': PHY}, outfile)
    print(f"prob {PHY} and {SFCs} saved")

if __name__ == "__main__":
    genprob("config/genproconfig.yaml")

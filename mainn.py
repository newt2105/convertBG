from helper import draw, genphy, ilp, tobigraph, gensfc
     
import pickle
import gzip


def main():
    # read file
    with gzip.open('data/prob/output_graphs.pkl.gz', 'rb') as infile:
        data = pickle.load(infile)
    
    # Get graph
    SFCs = data['SFCs']
    PHY = data['PHY']

    
    prob = ilp.Convert_to_ilp(PHY, SFCs)
    G = tobigraph.Create_bipartite_graph_ILP(prob)
    draw.draw_bigraph(G)

if __name__ == "__main__":
    main()

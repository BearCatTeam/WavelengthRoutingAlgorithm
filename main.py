import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
from rwa_adaptive_v2 import rwa_adaptive as rwa_adaptive_v2


def init_graph(G):
    G.add_node(1, name='Hamburg'), G.add_node(2, name='Berlin')
    G.add_node(3, name='Leipzig'), G.add_node(4, name='Nurnberg')
    G.add_node(5, name='Munchen'), G.add_node(6, name='Ulm')
    G.add_node(7, name='Stuttgart'), G.add_node(8, name='Karlsruhe')
    G.add_node(9, name='Mannheim'), G.add_node(10, name='Frankfurt')
    G.add_node(11, name='Koln'), G.add_node(12, name='Dusseldorf')
    G.add_node(13, name='Essen'), G.add_node(14, name='Dortmund')
    G.add_node(15, name='Norden'), G.add_node(16, name='Bremen')
    G.add_node(17, name='Hannover')
    G.add_edges_from([(1, 2, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}), (1, 17, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}),
                      (1, 16, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}), (2, 3, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}),
                      (2, 17, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}), (3, 4, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}),
                      (3, 10, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}), (3, 17, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}),
                      (4, 5, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}), (4, 7, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}),
                      (4, 10, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}), (5, 6, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}),
                      (6, 7, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}), (7, 8, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}),
                      (8, 9, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}), (9, 10, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}),
                      (10, 11, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}), (10, 17, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}),
                      (11, 12, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}), (11, 14, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}),
                      (12, 13, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}), (13, 14, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}),
                      (14, 15, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}), (14, 17, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}),
                      (15, 16, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0}), (16, 17, {'weight': 1, 'usage': 0, 'color': [0], 'centrality': 0})])
    return 17


def init_hop_count(G, hop_count):
    for i in range(1, 17, 1):
        for j in range(i + 1, 17 + 1, 1):
            hop_count[i-1][j-1] = nx.dijkstra_path_length(G, i, j, 'weight')
            hop_count[j-1][i-1] = hop_count[i-1][j-1]

if __name__ == '__main__':
    G = nx.Graph()  # graph matrix
    random.seed(int(input("Enter random-seed: ")))
    alpha = 1
    theta = 249  # before 249
    node_number = init_graph(G)
    iter_num = 1000
    U = np.zeros((iter_num, 1))  # max ultilization of 1000 times run
    hop_count = np.zeros((17, 17))
    init_hop_count(G, hop_count)
    block_count = 0
    wa_block_count = 0
    for i in range(0, iter_num, 1):
        W = random.randint(8, 16)  # number of wavelength/fiber
        N = random.randint(4, 8)  # number of fiber
        demand_list = []
        for k in range(1, node_number, 1):
            for m in range(k+1, node_number+1, 1):
                for l in range(0, random.randint(0, 3)):
                    demand_list.append([hop_count[k-1][m-1], k, m])
        rwa_algorithm = rwa_adaptive_v2(G, alpha, theta)
        demand_list.sort(reverse=True)
        U[i] = rwa_algorithm.run(W, N, demand_list, 1.321, 0.6, 1.0-0.6, i)
        if U[i] >= 1 and rwa_algorithm.wa_block:
            wa_block_count += 1
    S = np.average(U)
    block_count = len(np.where(U >= 1.0)[0])
    print("- blocking probability: ", (float(block_count) / iter_num)*100, "%")
    print("    + block by Wavelength Assignment is: ", wa_block_count)
    print("    + block by Wavelength Routing is   : ", block_count - wa_block_count)
    print("- utilization         : ", S*100, "%")








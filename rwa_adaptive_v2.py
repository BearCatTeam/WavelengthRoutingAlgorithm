import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class rwa_adaptive:
    def __init__(self, G, alpha, theta):
        self.G = nx.Graph(G)
        self.wavelength_number = 0
        self.demand_list = []
        self.beta = 1
        self.wave_color_usage = [0]
        self.W = 0  # number of wavelength - color
        self.N = 0  # number of fiber - maximun usage of one color
        self.wa_block = False  # block cause by wavelength assignment
        self.cal_init_weight(alpha, theta)
        self.trace_path = []

    def cal_init_weight(self, alpha, theta):
        centrality = nx.degree_centrality(self.G)
        for edges in self.G.edges():
            self.G.edge[edges[0]][edges[1]]['centrality'] = theta*(centrality[edges[0]] + centrality[edges[1]])
            self.G.edge[edges[0]][edges[1]]['weight'] = alpha*1 + self.G.edge[edges[0]][edges[1]]['centrality']

    def show(self):
        nx.draw(self.G)
        plt.show()

    def run(self, W, N, demand_list, beta, alpha, theta, trace):  # after many experience Beta = 1.3 giving the best result
        self.wavelength_number = W * N
        self.demand_list = demand_list
        self.beta = beta
        self.wave_color_usage.extend([0]*self.wavelength_number)
        max_usage = 0
        self.W = W
        self.N = N
        for edges in self.G.edges():
            self.G.edge[edges[0]][edges[1]]['color'] = [0]*self.W
        try:
            for i in range(0, len(self.demand_list), 1):
                source = int(self.demand_list[i][1])
                target = int(self.demand_list[i][2])

                path = nx.astar_path(self.G, source, target, rwa_adaptive.dijkstra_heuristic, 'weight')

                # assign wavelength path
                if not self.wavelength_assignment_firstfit(path, source, target, trace):
                    self.wa_block = True
                    return 1


                # update usage and weight
                for j in range(0, len(path)-1, 1):
                    self.G.edge[path[j]][path[j+1]]['usage'] += 1

                    if self.G.edge[path[j]][path[j+1]]['usage'] >= max_usage:
                        max_usage = self.G.edge[path[j]][path[j+1]]['usage']

                    self.G.edge[path[j]][path[j+1]]['weight'] = (alpha*pow(self.beta, self.G.edge[path[j]][path[j+1]]['usage'])
                                                                 + self.G.edge[path[j]][path[j+1]]['centrality'])

                    if self.G.edge[path[j]][path[j + 1]]['usage'] >= self.wavelength_number:
                        self.G.remove_edge(path[j], path[j + 1])

        except nx.NetworkXNoPath:
            return 1

        except RuntimeError, e:
            print e.message

        else:
            return float(max_usage)/self.wavelength_number

    def wavelength_assignment_firstfit(self, demand_path, source, target, trace):
        for choosen_wavelength in range(0, self.W+1, 1):
            if choosen_wavelength == self.W:
                return False
            all_free = True
            for i in range(0, len(demand_path)-1, 1):
                if self.G.edge[demand_path[i]][demand_path[i+1]]['color'][choosen_wavelength] >= self.N:
                    all_free = False
                    break
            if not all_free:
                continue
            else:
                for i in range(0, len(demand_path) - 1, 1):
                    u = demand_path[i]
                    v = demand_path[i+1]
                    self.G.edge[u][v]['color'][choosen_wavelength] += 1
                if trace == 0:
                    print source, " --> ", target, " : ", demand_path, " -- ", choosen_wavelength
                break
        return True

    @staticmethod
    def dijkstra_heuristic(u, v):
        return 0
import networkx as nx
# import plotly.express as px
import warnings
from GA import *
import numpy

# import plotly.graph_objects as go
import numpy as np


def read():
    f = open("fricker26.txt", "r")
    data = f.readlines()
    f.close()

    n = int(data[0])
    tsp = []
    for i in range(1, n + 1):
        tsp.append([int(i) for i in data[i][:-1].split(",")])

    edges = 0
    for i in range(0, n - 1):
        for j in range(i, n):
            if tsp[i][j] != 0:
                edges += 1

    vertices = []
    for i in range(0, n):
        vertices.append(Node(i, tsp[i]))

    net = {'vertices': vertices, 'noV': n, 'mat': tsp, 'noE': edges}
    return net


def afisareGraf(network):
    warnings.simplefilter('ignore')
    A = np.matrix(network["mat"])
    G = nx.from_numpy_matrix(A)
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 8))

    labels = {}
    for node in G.nodes():
        # set the node name as the key and the label as its value
        labels[node] = node

    nx.draw_networkx_labels(G, pos, labels, font_size=16, font_color='black')
    nx.draw_networkx_nodes(G, pos, node_size=300, cmap=plt.cm.RdYlBu)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.show()


def solve(ga, problemParams, bestChrFitness, medChrFitness, worstChrFitness, pathWeights):
    for i in range(problemParams['numberOfIterations']):
        ga.nextGeneration()
        best_chr = ga.best_chromosome()
        worst_chr = ga.worst_chromosome()
        bestChrFitness.append(copy.deepcopy(best_chr.fitness))
        worstChrFitness.append(copy.deepcopy(worst_chr.fitness))
        medChrFitness.append((best_chr.fitness + worst_chr.fitness) / 2)
        path = [y.node_number() for y in best_chr.repres]
        path_distance = 0
        for i in range(0, len(path) - 1):
            path_distance += problemParams['mat'][path[i]][path[i + 1]]
        pathWeights.append(path_distance)


# Node = oras
class Node:
    def __init__(self, node_number, distances):
        self.__node_number = node_number
        self.__distances = distances

    def distance(self, other):
        return self.__distances[other.node_number()]

    def node_number(self):
        return self.__node_number


# fitness = 1/route_distance, deci un fitness mai mare = un drum mai scurt
class Fitness:
    def __init__(self, route):
        self.__route = route
        self.__distance = 0
        self.__fitness = 0.0

    def route_distance(self):
        ruta = [y.node_number() for y in self.__route]
        if self.__distance == 0:
            path_distance = 0
            for i in range(0, len(self.__route)):
                from_node = self.__route[i]
                to_node = None
                if i + 1 < len(self.__route):
                    to_node = self.__route[i + 1]
                else:
                    to_node = self.__route[0]
                path_distance += from_node.distance(to_node)
            self.__distance = path_distance
        return self.__distance

    def get_fitness(self):
        if self.__fitness == 0:
            self.__fitness = 1 / float(self.route_distance())
            # self.__fitness = self.route_distance()
        return self.__fitness

    def set_fitness(self, fitness):
        self.__fitness = fitness


def main():
    np.random.seed(1)
    problemParams = read()
    problemParams['popSize'] = 32
    problemParams['numberOfIterations'] = 200
    problemParams['eliteSize'] = 8
    problemParams['mutationRate'] = 0.05
    problemParams['fitness'] = Fitness

    bestChrFitness = []
    medChrFitness = []
    worstChrFitness = []
    pathWeights = []

    ga = GA(problemParams)

    afisareGraf(problemParams)

    solve(ga, problemParams, bestChrFitness, medChrFitness, worstChrFitness, pathWeights)

    best_chr = ga.best_chromosome()

    print_results(bestChrFitness, best_chr, pathWeights, problemParams)

    x = []
    for i in range(len(bestChrFitness)):
        x.append(i)

    # x = np.linspace(0, 1, problemParams['numberOfIterations'])
    # fig = go.Figure()
    #
    # fig.add_trace(go.Scatter(x=x, y=bestChrFitness,
    #                          mode='lines',
    #                          name='best'))
    #
    # fig.add_trace(go.Scatter(x=x, y=medChrFitness,
    #                          mode='lines',
    #                          name='medium'))
    #
    # fig.add_trace(go.Scatter(x=x, y=worstChrFitness,
    #                          mode='lines',
    #                          name='worst'))
    #
    # fig.show()


def print_results(bestChrFitness, best_chr, pathWeights, problemParams):
    f = open("out.txt", "w")
    f.write(str(problemParams['noV']) + '\n')
    print('Evolutia fitnessului: ')
    for x in bestChrFitness:
        print(x)
    print('Evolutia lungimii drumului: ')
    for x in pathWeights:
        print(x)
    path = [y.node_number() for y in best_chr.repres]
    new_mat = []
    for i in range(0, len(path)):
        new_mat.append([0 for _ in range(len(path))])
    path_distance = 0
    for i in range(0, len(path) - 1):
        path_distance += problemParams['mat'][path[i]][path[i + 1]]
        new_mat[path[i]][path[i + 1]] = new_mat[path[i + 1]][path[i]] = problemParams['mat'][path[i]][path[i + 1]]
    new_mat[path[0]][path[len(path) - 1]] = new_mat[path[len(path) - 1]][path[0]] = problemParams['mat'][path[0]][
        path[len(path) - 1]]
    print(path)
    print(path_distance)
    path_string = ""
    for x in path:
        path_string += str(x) + ", "
    path_string = path_string[:-2]
    f.write(str(path_string) + '\n')
    f.write(str(path_distance) + '\n')
    f.close()
    problemParams['mat'] = new_mat
    afisareGraf(problemParams)


if __name__ == '__main__':
    main()

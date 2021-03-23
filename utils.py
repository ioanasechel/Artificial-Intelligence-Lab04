import warnings
from random import uniform
from GA import *
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import warnings


def generateNewValue(lim1, lim2):
    return uniform(lim1, lim2)


def binToInt(x):
    val = 0
    # x.reverse()
    for bit in x:
        val = val * 2 + bit
    return val


def show_graph(network):
    warnings.simplefilter('ignore')
    A = np.matrix(network["mat"])
    G = nx.from_numpy_matrix(A)
    pos = nx.spring_layout(G)  # compute graph layout
    plt.figure(figsize=(8, 8))  # image is 8 x 8 inches
    nx.draw_networkx_nodes(G, pos, node_size=300, cmap=plt.cm.RdYlBu)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.show()


def show_communities(network, bestChr):
    # plot a particular division in communities
    communities = [1, 2, 1, 2, 1, 1]

    A = np.matrix(network["mat"])
    G = nx.from_numpy_matrix(A)
    pos = nx.spring_layout(G)  # compute graph layout
    plt.figure(figsize=(16, 16))  # image is 8 x 8 inches
    nx.draw_networkx_nodes(G, pos, node_size=300, cmap=plt.cm.RdYlBu, node_color=bestChr.repres)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.show()

import networkx as nx
import random
import numpy as np
import pickle
import matplotlib.pyplot as plt
from numba import jit
import os


@jit(nopython=True)
def rand_pick(probabilities):
    x = random.uniform(0, 1)
    if x <= probabilities:
        return 1
    else:
        return 0


@jit(nopython=True)
def rand_pick_list(pick_list, prob_list):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(pick_list, prob_list):
        cumulative_probability += item_probability
        if x <= cumulative_probability:
            break
    return item


def edge_list_array(edge_list):
    edge_mat = np.zeros([len(edge_list), 2], np.int_)
    for i in range(len(edge_list)):
        edge_mat[i, :] = np.array(edge_list[i])

    return edge_mat


def nbr_dict_mat(nbr_dict):
    """
    turn nbr_dict to mat
    :param nbr_dict:
    :return:
    """
    nodesnum = len(nbr_dict)
    nbr_mat = np.zeros([nodesnum, nodesnum], np.int_)
    deg_array = np.zeros(nodesnum, np.int_)
    for i, nbrs in nbr_dict.items():
        deg_array[i] = len(nbrs)
        if len(nbrs) > 0:
            nbr_mat[i][:len(nbrs)] = np.array(nbrs)
    return nbr_mat, deg_array


def nbrs_edge_mat_dict(tempnet_mat):
    """
    noted: nbr_mat_dict[snap] corresponds a tuple: (nbr_mat, deg_array) for the subgraph in this snapshot
    :param tempnet_mat: 3-dimension matrix: (snap_index, node1, node2)
    :return: edge_mat_dict, nbr_mat_dict
    """

    edge_mat_dict = {}
    nbr_mat_dict = {}

    for snap in range(tempnet_mat.shape[0]):
        sub_mat = tempnet_mat[snap, :, :]
        sub_graph = nx.from_numpy_array(sub_mat)
        nbr_mat_dict[snap] = nbr_dict_mat(nx.to_dict_of_lists(sub_graph))
        edge_mat_dict[snap] = edge_list_array(list(sub_graph.edges()))

    return edge_mat_dict, nbr_mat_dict
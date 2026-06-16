import networkx as nx
import random
import numpy as np
import pickle
import matplotlib.pyplot as plt
from numba import jit
import os
import multiprocessing
from multiprocessing import Process, Manager
import functools
import time
import math
from utils import rand_pick_list, nbr_dict_mat, edge_list_array
# from network_generate_direct import donate2hub, donate2leaf, donateDesign
import scipy.io as scio


@jit(nopython=True)
def single_round(state_array, payoff_array, game_matrix, edge_mat):
    """
    play game on each group
    """

    for i in range(edge_mat.shape[0]):
        nodex = edge_mat[i, 0]
        nodey = edge_mat[i, 1]
        payoff_array[nodex] += game_matrix[state_array[nodex]][state_array[nodey]]
        payoff_array[nodey] += game_matrix[state_array[nodey]][state_array[nodex]]

    return payoff_array


@jit(nopython=True)
def replicate_dynamic(state_array, payoff_array, nbr_mat, deg_array, nodesnum, w):
    """
    replicator dynamic after single round game: DB

    """

    update_node = np.random.choice(np.arange(nodesnum))
    nbrs_num = deg_array[update_node]
    nbrs_array = nbr_mat[update_node][:nbrs_num]

    fitness_group = 1 + w * payoff_array[nbrs_array]
    prob_array = fitness_group / np.sum(fitness_group)
    state_array[update_node] = state_array[rand_pick_list(nbrs_array, prob_array)]

    return state_array


# @jit(nopython=True)
def evolution(game_matrix, edge_mat, nbrs_mat, deg_array, nodesnum, w):
    """
    whole process of evolution for 10000 times of generation
    """

    total_generation = int(1e8)
    payoff_array = np.zeros(nodesnum, dtype=np.float_)
    state_array = np.zeros(nodesnum, dtype=np.int_)
    coop_ini = np.random.choice(nodesnum)
    state_array[coop_ini] = 1

    for time in range(total_generation):
        payoff_array = single_round(state_array, payoff_array, game_matrix, edge_mat)
        state_array = replicate_dynamic(state_array, payoff_array, nbrs_mat, deg_array, nodesnum, w)
        payoff_array[:] = 0
        coord = np.sum(state_array)
        if coord > nodesnum - 1:
            return 1
        if coord == 0:
            return 0
    return coord / nodesnum


def process(core, b, edge_mat, nbrs_mat, deg_array, nodesnum):
    w = 0.01
    game_matrix = np.zeros((2, 2))
    game_matrix[0][0] = 0  # P defect--defect
    game_matrix[0][1] = b  # T d-c
    game_matrix[1][0] = -1  # S
    game_matrix[1][1] = b - 1  # R

    repeat_time = int(1e6)
    repeat_array = np.zeros(repeat_time)
    for rep in range(repeat_time):
        coord_freq = evolution(game_matrix, edge_mat, nbrs_mat, deg_array, nodesnum, w)
        repeat_array[rep] = coord_freq

    return np.sum(repeat_array == 1) / (np.sum(repeat_array == 1) + np.sum(repeat_array == 0))

if __name__ == "__main__":

    with open('result/er_n100_k6_0.pk', 'rb') as f:
        static_matrix = pickle.load(f)  # stack of matrix of snapshot of interaction

    # ---------------------------  graph construction  --------------------------
    graph = nx.from_numpy_matrix(static_matrix)
    nbrs_dict = nx.to_dict_of_lists(graph)
    nbrs_mat, deg_array = nbr_dict_mat(nbrs_dict)
    nodesnum = static_matrix.shape[1]
    edge_array = edge_list_array(list(graph.edges()))


    b_para_list = np.round(np.arange(6.5, 7.5, 0.2), decimals=1)
    fix_prob_b_list = []
    for b_para in b_para_list:
        core_list = np.arange(20)  # 64-cpu core

        pool = multiprocessing.Pool()
        t1 = time.time()

        pt = functools.partial(process, b=b_para, edge_mat=edge_array, nbrs_mat=nbrs_mat, deg_array=deg_array,
                               nodesnum=nodesnum)
        coor_freq_list = pool.map(pt, core_list)
        coor_freq_core = np.mean(np.array(coor_freq_list))
        pool.close()
        pool.join()
        t2 = time.time()
        print("Total time:" + (t2 - t1).__str__())
        print((b_para, coor_freq_core))
        fix_prob_b_list.append(coor_freq_core)

    file = 'result/fix_prob_ER_donate_to_all_neighbors_n' + str(nodesnum) + "_b" \
           + str(min(b_para_list)) + "_" + str(max(b_para_list)) + '.pk'

    with open(file, 'wb') as f:
        pickle.dump(np.array(fix_prob_b_list), f)
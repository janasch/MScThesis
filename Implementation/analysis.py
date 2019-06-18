import numpy as np
import math
import statistics as stat
import preprocessing as pr
import datareader as dr

# =============================================================================
#                     Analysis
# =============================================================================
# Performs analysis on the performance of the algorithms.

class Analysis:
    def __init__(self, user_to_sig, JSim, estJSim):
        """N is true nearest neighbours, M is estimated nearest neighbours.
        Used for approximate recall.
        """
        self.user_to_sig = user_to_sig
        self.data_size = len(user_to_sig.keys())    
        self.JSim = JSim
        self.estJSim = estJSim
        self.N = 20
        self.M = 100


    def MSE(self):
        sq_error = 0
        counter = 0
        for i in range(len(self.JSim)):
            for j in range(i+1, len(self.JSim)):
                counter += 1
                sq_error += (self.JSim[i][j]-self.estJSim[i][j])**2
        return (sq_error/counter)


    def PRF(self):
        """Calculates precision, recall, and F1 score."""
        TP = 0
        FP = 0
        FN = 0
        
        for i in range(self.data_size):

            # Get estimated neighbours
            neigh = np.asarray(self.estJSim[i])
            index_neigh = list(neigh.argsort()[-self.M:][::-1])

            # Get true neighbours
            real_neigh = np.asarray(self.JSim[i])
            real_index_neigh = list(real_neigh.argsort()[-self.N:][::-1])

            for neighbour in index_neigh:
                if neighbour in real_index_neigh:
                    TP += 1
                else:
                    FP += 1
            for n in real_index_neigh:
                if n not in index_neigh:
                    FN += 1

        prec = TP / (FP+TP)
        recall = TP / (TP + FN)
        if prec == 0:
            prec = 1
        if recall == 0:
            recall = 1
        f1 = (2 * prec * recall) / (prec + recall)
        return prec, recall, f1



def set_estJSim(MH_algo, user_to_sig):
    """Generates a matrix of estimated similarities."""

    estJSim = [[0 for x in range(MH_algo.data_size)] for y in range(MH_algo.data_size)]
    id_to_idx = MH_algo.id_to_idx

    for counter, user in enumerate(user_to_sig.keys()):
        id_to_idx[user] = counter
        for other_counter, other_user in enumerate(user_to_sig.keys()):
            if user == other_user:
                continue
            if counter > other_counter:
                estJSim[counter][other_counter] = estJSim[other_counter][counter]
                continue
            id_to_idx[other_user] = other_counter
            estJSim[counter][other_counter] = MH_algo.calc_est_Jacc(user_to_sig[user], user_to_sig[other_user])
    return estJSim


def get_avg_sim(JSim):
    sim = 0
    count = 0
    for i in range(len(JSim)-1):
        for j in range(i+1, len(JSim)):
            sim += JSim[i][j]
            count += 1
    return sim/count

# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 16:15:41 2023

@author: Tanuka
"""
    
import numpy as np
from scipy.sparse import csr_matrix

class Jaccard:
    def __init__(self, mat):
        self.mat = mat
        self.jaccard_index = self.similarity()

    # Jaccard similarity
    def similarity(self):
        A = csr_matrix(self.mat)
        At = csr_matrix(self.mat.T)
        
        # Computing the numerator X.Xt
        intersection = np.dot(A, At)
        
        # Computing the denominator (X.1m,n + (X.1m,n)t - X.Xt)
        ones = np.ones(csr_matrix(self.mat).shape[::-1])
        B = A.dot(ones)
        union = B + B.T - intersection
        
        # Calculated Jaccard's Matrix
        jaccard = np.round((intersection / union), 3)
        return jaccard

    # Jaccard distance
    def distance(self):
        jd = np.ones(self.jaccard_index.shape[::-1]) - self.jaccard_index
        return jd



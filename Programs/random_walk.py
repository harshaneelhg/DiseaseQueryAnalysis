#!/usr/bin/env python

import numpy as np
import scipy.sparse
from sklearn.preprocessing import normalize

def get_ranks(W, q, c):
	"""
		Input:
		W: Sparse adjecency matrix.
		q: Sparse query vector.
		c: Restart probability.

		Output:
		r: Sparse relevancy vector with every other node.
		i: Number of iterations consumed to reach convergence.

		This function implements basic version of RWR to output
		Relevancy of query node with other nodes in a graph represented
		by adjecency matrix W.
	"""

	#Column Normalize Adjecency Matrix.

	W = normalize(W, norm='l1', axis=0)

	#Basic Random Walk with Restarts Algorithm.

	r = q
	r1 = c*(r*W) + (1-c)*q
	i=0

	while (r1-r).dot((r1-r).T) > 1e-5 :
		r = r1
		r1 = c*(r*W) + (1-c)*q
		i= i+1

	return r1,i
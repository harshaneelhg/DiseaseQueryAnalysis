#!/usr/bin/env python

import numpy as np
import scipy.sparse
from sklearn.preprocessing import normalize

__all__ = ['get_rwr_ranks', 'get_k_best']


def get_rwr_ranks(W, q, c):
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

def get_k_best(a,k):
	"""
	Input:
		a: Array conttaining values,
		k: number of best values you want to find out.

	Output:
		k_best : array containing k best elements  from a. (|k_best| = k)

	Example:
		get_k_best([2,6,1,4,9,12,10], 3) = [2,1,4].
	"""
	k_best = list([(a[i],i) for i in range(0,k)])
	min_a = min(k_best,key=lambda item:item[0])
	max_a =max(k_best,key=lambda item:item[0])
	print max_a[0]
	for i in range(k,len(a)):
		if a[i]>max_a[0]:
			
			k_best = [(v,idx) for v,idx in k_best if v != min_a[0]]
			k_best.append((a[i],i))
			max_a = (a[i],i)
			min_a = min(k_best,key=lambda item:item[0])

	return k_best
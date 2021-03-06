#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import scipy.sparse
from sklearn.preprocessing import normalize
import hashlib

__all__ = ['get_rwr_ranks', 'get_k_best', 'get_matching_query', 'get_matching_node']


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
	
	for i in range(k,len(a)):
		if a[i]>min_a[0]:
			k_best = [(v,idx) for v,idx in k_best if v != min_a[0]]
			k_best.append((a[i],i))
			max_a = (a[i],i)
			min_a = min(k_best,key=lambda item:item[0])
	return k_best

def get_matching_query(q,key_id,data_dict):
	"""
	Input: 
		q: Query entered by the user through web application.

	Output:
		index: Index, in string type, of the most matching query from the database.

	Example:
		get_matching_query('牙疼怎么办') = '1000015'

	"""
	if q != '':
		key = hashlib.md5(q.strip()).hexdigest()
		if key in data_dict:
			print "Key found.."
			return str(key_id[key])
		else:
			print "Key not found..."
			return '1000001'

def get_matching_node(n,key_id,data_dict):
	"""
	Input: 
		q: Query entered by the user through web application.

	Output:
		index: Index, in string type, of the most matching query from the database.

	Example:
		get_matching_query('牙疼怎么办') = '1000015'

	"""
	if n != '':
		key = hashlib.md5(n.strip()).hexdigest()
		if key in data_dict:
			print "Key found.."
			return str(key_id[key])
		else:
			print "Key not found..."
			return '1000001'
	else:
		return '0'
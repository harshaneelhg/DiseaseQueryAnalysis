import numpy as np
import scipy.sparse
import scipy.io
from sklearn.preprocessing import normalize
import time

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

data = scipy.io.loadmat('../Data/Baidu/data.mat')
adj = data['adjecency_matrix']

q = np.zeros(1716500)
q[1700000] = 1.0

q = scipy.sparse.csc_matrix(q)
start = time.time()
r1, i = get_ranks(adj, q, 0.5)
end = time.time()
print max(r1.data)
print '\nTotal number of iterations: ' + str(i)
print get_k_best(r1.data,4)
print '\nTotal elapsed time: ' + str(time.time()-start) + ' seconds'
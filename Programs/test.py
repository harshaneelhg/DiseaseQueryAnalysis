import numpy as np
import scipy.sparse
import scipy.io
from sklearn.preprocessing import normalize
import time
import json
import sys

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
	print len(a)
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

reload(sys)
sys.setdefaultencoding('utf8')
data = scipy.io.loadmat('../Data/Baidu/data.mat')
adj = data['adjecency_matrix']
with open('../Data/Baidu/node_data.json', 'rb') as infile:
	data_dict = json.load(infile)
with open('../Data/Baidu/id-key.json', 'rb') as infile:
	id_key = json.load(infile)
q = np.zeros(1716500)
q[1000001] = 1.0

q = scipy.sparse.csc_matrix(q)
start = time.time()
r1, i = get_ranks(adj, q, 0.5)
end = time.time()
print (data_dict[id_key['1000001']])
print 'Best score = ' + str(np.max(r1.data))
print 'Total number of iterations: ' + str(i)
print len(r1.data[1716000:])
#print r1.data[1716000:]
k_best = get_k_best(r1.data[len(r1.data)-500:],10)
#print 'query node = ' + str(data_dict[id_key['100']][1])
print k_best
for t in k_best:
	x =data_dict[id_key[str(1716000+t[1])]]
	print str(x[0]), str(x[1])
print '\nTotal elapsed time: ' + str(time.time()-start) + ' seconds'
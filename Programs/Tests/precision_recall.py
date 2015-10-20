#!/usr/bin/python
# -*- coding: UTF-8 -*-

# This script is used to calculate the precision and recall of RWR algorithm
# ran on Baidu's medical data.

import random
import numpy as np
import scipy.sparse
import scipy.io
from sklearn.preprocessing import normalize
import sys
import pdb
import matplotlib.pyplot as plt

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

def get_precision_recall(adj):
	# Generate candidates for the test
	candidates = []
	while len(candidates) <= 100:
		i = random.randint(0,716000)
		i = i+1000000
		while i in candidates:
			i = random.randint(0,716000)
			i = i+1000000

		candidates.append(i)
	
	results_p=[[],[],[],[],[],[],[],[],[]]
	results_r=[[],[],[],[],[],[],[],[],[]]
	count = 0 
	for c in candidates:
		q = np.zeros(1716500)
		q[int(c)] = 1.0
		q = scipy.sparse.csc_matrix(q)
		possible_result = np.array(adj[c,1716000:].todense()).reshape(-1)
		truth = [i for i in range(0,len(possible_result)) if possible_result[i]==1]
		hide_percent = 0.2
		n_hide = int(len(truth)*hide_percent)
		hide = []
		#pdb.set_trace()
		for num in range(0,9):
			while len(hide)!=n_hide:
				ri = random.randint(0,len(truth)-1)
				hide.append(truth[ri])
				hide = list(set(hide))
			for h in hide:
				adj[c,1716000+h] = 0.0
			r1, i = get_rwr_ranks(adj, q, 0.2)
			for h in hide:
				adj[c,1716000+h] = 1.0
			ranks = r1.todense()
			ranks = np.array(ranks).reshape(-1).tolist()
			
			sorted_ranks = [(i[1],i[0]) for i in sorted(enumerate(ranks[len(ranks)-500:]), key=lambda x:x[1])]
			last_index = 500 - min([i for i in range(len(sorted_ranks)) if sorted_ranks[i][1] in truth])
			width = last_index
			sorted_ranks = sorted_ranks[::-1]
			k_idx = [j for i,j in k_best]
			precision = 0
			for k in k_idx:
				if k in truth:
					precision += 1
			recall = precision*1.0/width
			precision = precision/(10.0)
			#print precision, recall
			results_r[num].append(recall)
			results_p[num].append(precision)
			hide_percent+=0.1
			hide_percent = round(hide_percent,2)
			n_hide = int(len(truth)*hide_percent)
			#pdb.set_trace()
		count +=1
		if count%1 == 0:
			x = '-'*int(count*50.0/100.0) + '>' + '_'*int((count-100.0)*50.0/100.0) + '| ' + str(int(count*100.0/100.0)) + '%'
			sys.stdout.flush()
			sys.stdout.write('%s\r' % x)
	print '-'*int(100.0*50.0/100.0) + '>' + '| ' + str(100) + '%'
	return results_p,results_r

# Read data
print 'Reading data...'
data = scipy.io.loadmat('../../Data/Baidu/data_1.mat')
adj = data['adjecency_matrix']
PERCENT_CHAR = '%'
p = [20,30,40,50,60,70,80,90,100]
pr = [[],[],[],[],[],[],[],[],[]]
rec = [[],[],[],[],[],[],[],[],[]]

for i in range(0,10):
	print "Set "+str(i+1)+" :"
	r1,r2 = get_precision_recall(adj)
	print "[ 20"+PERCENT_CHAR+" HIDDEEN EDGES ]  Precision = "+ str("%0.4f"%np.mean(r1[0]))+ ", Recall = "+ str("%0.4f"%np.mean(r2[0]))
	pr[0].append(np.mean(r1[0]))
	rec[0].append(np.mean(r2[0]))
	print "[ 30"+PERCENT_CHAR+" HIDDEEN EDGES ]  Precision = "+ str("%0.4f"%np.mean(r1[1]))+ ", Recall = "+ str("%0.4f"%np.mean(r2[1]))
	pr[1].append(np.mean(r1[1]))
	rec[1].append(np.mean(r2[1]))
	print "[ 40"+PERCENT_CHAR+" HIDDEEN EDGES ]  Precision = "+ str("%0.4f"%np.mean(r1[2]))+ ", Recall = "+ str("%0.4f"%np.mean(r2[2]))
	pr[2].append(np.mean(r1[2]))
	rec[2].append(np.mean(r2[2]))
	print "[ 50"+PERCENT_CHAR+" HIDDEEN EDGES ]  Precision = "+ str("%0.4f"%np.mean(r1[3]))+ ", Recall = "+ str("%0.4f"%np.mean(r2[3]))
	pr[3].append(np.mean(r1[3]))
	rec[3].append(np.mean(r2[3]))
	print "[ 60"+PERCENT_CHAR+" HIDDEEN EDGES ]  Precision = "+ str("%0.4f"%np.mean(r1[4]))+ ", Recall = "+ str("%0.4f"%np.mean(r2[4]))
	pr[4].append(np.mean(r1[4]))
	rec[4].append(np.mean(r2[4]))
	print "[ 70"+PERCENT_CHAR+" HIDDEEN EDGES ]  Precision = "+ str("%0.4f"%np.mean(r1[5]))+ ", Recall = "+ str("%0.4f"%np.mean(r2[5]))
	pr[5].append(np.mean(r1[5]))
	rec[5].append(np.mean(r2[5]))
	print "[ 80"+PERCENT_CHAR+" HIDDEEN EDGES ]  Precision = "+ str("%0.4f"%np.mean(r1[6]))+ ", Recall = "+ str("%0.4f"%np.mean(r2[6]))
	pr[6].append(np.mean(r1[6]))
	rec[6].append(np.mean(r2[6]))
	print "[ 90"+PERCENT_CHAR+" HIDDEEN EDGES ]  Precision = "+ str("%0.4f"%np.mean(r1[7]))+ ", Recall = "+ str("%0.4f"%np.mean(r2[7]))
	pr[7].append(np.mean(r1[7]))
	rec[7].append(np.mean(r2[7]))
	print "[ 100"+PERCENT_CHAR+" HIDDEEN EDGES ] Precision = "+ str("%0.4f"%np.mean(r1[8]))+ ", Recall = "+ str("%0.4f"%np.mean(r2[8]))
	pr[8].append(np.mean(r1[8]))
	rec[8].append(np.mean(r2[8]))
	print ""

err_1 = []
err_2 = []

for i in range(0, len(pr)):
	e = max(pr[i]) - min(pr[i])
	err_1.append(e/2.0)

for i in range(0, len(rec)):
	e = max(rec[i]) - min(rec[i])
	err_2.append(e/2.0)

plt.errorbar(p, [np.mean(pr[0]),np.mean(pr[1]),np.mean(pr[2]),np.mean(pr[3]),np.mean(pr[4]),np.mean(pr[5]),np.mean(pr[6]),np.mean(pr[7]),np.mean(pr[8])],color ='b',yerr=err_1)
plt.xlabel('Percentage edge hiding')
plt.ylabel('Precision')
plt.title('Precision v/s edge hiding')
plt.grid()
plt.show()

plt.errorbar(p, [np.mean(rec[0]),np.mean(rec[1]),np.mean(rec[2]),np.mean(rec[3]),np.mean(rec[4]),np.mean(rec[5]),np.mean(rec[6]),np.mean(rec[7]),np.mean(rec[8])],color ='r',yerr=err_2)
plt.xlabel('Percentage edge hiding')
plt.ylabel('Recall')
plt.title('Recall v/s edge hiding')
plt.grid()
plt.show()	

fig, ax1 = plt.subplots()
fig.suptitle('Precision and recall with edge hiding')
ax1.errorbar(p, [np.mean(pr[0]),np.mean(pr[1]),np.mean(pr[2]),np.mean(pr[3]),np.mean(pr[4]),np.mean(pr[5]),np.mean(pr[6]),np.mean(pr[7]),np.mean(pr[8])],yerr=err_1,color ='b')
ax1.set_xlabel('Percentage edge hiding')
ax1.set_ylabel('Precision', color='b')

ax2 = ax1.twinx()
ax2.errorbar(p, [np.mean(rec[0]),np.mean(rec[1]),np.mean(rec[2]),np.mean(rec[3]),np.mean(rec[4]),np.mean(rec[5]),np.mean(rec[6]),np.mean(rec[7]),np.mean(rec[8])],color ='r',yerr=err_2)
ax2.set_ylabel('Recall', color = 'r')

plt.grid()
plt.show()
		
#scipy.io.savemat('../../Data/Baidu/precision_recall.mat', {'results':final})

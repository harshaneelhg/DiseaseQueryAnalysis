#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import scipy.sparse
import scipy.io
import random
import string
import hashlib
import pdb
import sys
import json
import codecs
import snap

__all__ = ['preprocess']

def preprocess():
	"""
	Output: Sparse adjecency matrix with structure like-

			Block matrix structure for Disease-Chemical-Genes association:
			(0 indicates block of zeros in block matrix)

					U 		Q 		D 
				-------------------------
			    |	 	|		|		|
			U	|	0	|		|	0	|
				|		|		|		|
				-------------------------
			 	|		|		|		|
			Q	|		|	0	|		|
				|		|		|		|
				-------------------------
			 	|		|		|		|
			D	|	0	|		|	0	|
				|		|		|		|
				-------------------------

			id-key lookup dictionary like-

			{
				<id_1>: <key_1>,
				<id_2>: <key_2>,
				<id_2>: <key_2>,
				.
				.
				.
				<id_n>: <key_n>
			}

			and id-name dictionary of like-

			{
				'<key_1>': [
					'<some_description>',
					'<user/query/disease>'
				],
				'<key_2>': [
					'<some_description>',
					'<user/query/disease>'
				],
				.
				.
				.
				.
				'<key_n>': [
					'<some_description>',
					'<user/query/disease>'
				[
			}
	"""
	# Read data.
	data = scipy.io.loadmat('../Data/Baidu/baidu_medical.mat')
	# Separate individual sparse matrices.
	uq = data['adj_user_query']
	qd = data['adj_query_disease']

	# Number of Users
	n1 = uq.shape[0]
	# Number of queries
	n2 = uq.shape[1]
	# Number of diseases
	n3 = qd.shape[1]

	n = n1 + n2 + n3
	# Load overall adjecency matrix.
	data = scipy.io.loadmat('../Data/Baidu/adj_matrix_2.mat')
	adj = data['adj_matrix']
	save = {
		'adjecency_matrix': adj,
		'n': n,
		'n1': n1,
		'n2': n2,
		'n3': n3,
		}
	scipy.io.savemat('../Data/Baidu/data_2.mat', save)

	G = snap.TUNGraph.New()
	for i in range(n):
		G.AddNode(i)

	f = open('../Data/Baidu/user_query.txt', 'rb')
	line = f.readline()
	while line!='':
		xy = line.split(' ')
		x = int(xy[0])
		y = int(xy[1])+n1
		G.AddEdge(x,y)
		line = f.readline()
	f = open('../Data/Baidu/query_disease.txt', 'rb')
	line = f.readline()
	while line!='':
		xy = line.split(' ')
		x = int(xy[0])+n1
		y = int(xy[1])+n1+n2
		G.AddEdge(x,y)
		line = f.readline()

	FOut = snap.TFOut('../Data/Baidu/connections.graph')
	G.Save(FOut)

	print 'constructing dictionary'
	data_dict = {}
	id_key_lookup = {}
	key_id_lookup = {}
	print 'processing users...'
	#print n
	f = open('../Data/Baidu/user_dict.txt', 'rb')
	line = f.readline()
	idx = 0
	while line!='':
		key = hashlib.md5(str(line)).hexdigest()
		id_key_lookup[str(idx)] = str(key)
		key_id_lookup[str(key)] = str(idx)
		d = ['user',str(line).strip()]
		data_dict[str(key)]= d
		idx = idx + 1
		if idx%10000 == 0:
			#print idx, n, line
			x = '-'*int(idx*50.0/n) + '>' + '_'*int((idx-n)*50.0/n) + '| ' + str(int(idx*100.0/n)) + '%'
			sys.stdout.flush()
			sys.stdout.write('%s\r' % x)
		line = f.readline()
	print 'processing queries...'
	f = open('../Data/Baidu/query_dict.txt', 'rb')
	line = f.readline()
	while line!='':
		key = hashlib.md5(line.strip()).hexdigest()
		id_key_lookup[str(idx)] = str(key)
		key_id_lookup[str(key)] = str(idx)
		#print line.strip().encode('UTF-8')
		d = ['query',line]
		data_dict[str(key)]= d
		idx = idx + 1
		if idx%10000 == 0:
			#print idx, n
			x = '-'*int(idx*50.0/n) + '>' + '_'*int((idx-n)*50.0/n) + '| ' + str(int(idx*100.0/n)) + '%'
			sys.stdout.flush()
			sys.stdout.write('%s\r' % x)
		line = f.readline()
	print 'processing diseases...'
	f = open('../Data/Baidu/disease_dict.txt', 'rb')
	line = f.readline()
	while line!='':
		key = hashlib.md5(line.strip()).hexdigest()
		id_key_lookup[str(idx)] = str(key)
		key_id_lookup[str(key)] = str(idx)
		d = ['disease',line]
		#print d[1]
		data_dict[str(key)]= d
		idx = idx + 1
		if idx%10000 == 0:
			x = '-'*int(idx*50.0/n) + '>' + '_'*int((idx-n)*50.0/n) + '| ' + str(int(idx*100.0/n)) + '%'
			sys.stdout.flush()
			sys.stdout.write('%s\r' % x)
		line = f.readline()
	
	print '\nSaving dictionaries'
	with open('../Data/Baidu/id-key.json', 'w') as outfile:
		json.dump(id_key_lookup, outfile)
	with open('../Data/Baidu/key-id.json', 'w') as outfile:
		json.dump(key_id_lookup, outfile)
	with open('../Data/Baidu/node_data.json', 'w') as outfile:
		json.dump(data_dict, outfile)


preprocess()

"""
Sample output:

constructing dictionary
--------------------------------------------------------------------------------------------------->| 99%
Saving dictionaries

"""
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import flask, flask.views
import scipy.io
import scipy.sparse
import sys
import json
import numpy as np
import time
import pdb
import snap
import networkx as nx
from modules.modules import get_rwr_ranks, get_k_best, get_matching_query, get_matching_node

app = flask.Flask(__name__)

# Create secret key for POST responses. This key must be random and must be secret.
app.secret_key= 'dsrtyuioklmnbvcdfgtyh'
reload(sys)
sys.setdefaultencoding('utf-8')

data = scipy.io.loadmat('../../Data/Baidu/data.mat')
adj = data['adjecency_matrix']
with open('../../Data/Baidu/node_data.json', 'rb') as infile:
	data_dict = json.load(infile)
with open('../../Data/Baidu/id-key.json', 'rb') as infile:
	id_key = json.load(infile)
with open('../../Data/Baidu/key-id.json', 'rb') as infile:
	key_id = json.load(infile)
#FIn = snap.TFIn("connections.graph")
#G = snap.TNGraph.Load(FIn)

n1 = 1000000
n2 = 716000
el = []

G = snap.TUNGraph.New()
for i in range(adj.shape[0]):
	G.AddNode(i)

f = open('../../Data/Baidu/user_query.txt', 'rb')
line = f.readline()
while line!='':
	xy = line.split(' ')
	x = int(xy[0])
	y = int(xy[1])+n1
	el.append((x,y))
	G.AddEdge(x,y)
	line = f.readline()
f = open('../../Data/Baidu/query_disease.txt', 'rb')
line = f.readline()
while line!='':
	xy = line.split(' ')
	x = int(xy[0])+n1
	y = int(xy[1])+n1+n2
	el.append((x,y))
	G.AddEdge(x,y)
	line = f.readline()

print "Data loaded..."

G1 = nx.from_edgelist(el)
el = None
print "graph formed..."

def bfs(start, end):
    queue = [[start]]
    visited = set()

    while queue:
        # Gets the first path in the queue
        path = queue.pop(0)

        # Gets the last node in the path
        vertex = path[-1]

        # Checks if we got to the end
        if vertex == end:
            return path
        # We check if the current node is already in the visited nodes set in order not to recheck it
        elif vertex not in visited:
			# enumerate all adjacent nodes, construct a new path and push it into the queue
			NodeVec = snap.TIntV()
			n_nodes = snap.GetNodesAtHop(G,vertex,1,NodeVec,False)
			nodes = [item for item in NodeVec]
			for current_neighbour in nodes:
			    new_path = list(path)
			    new_path.append(current_neighbour)
			    queue.append(new_path)

			# Mark the vertex as visited
			visited.add(vertex)

def get_links(g, link_type):
	if link_type == 'path':
		edges = nx.edges(g)
		l = []
		for edge in edges:
			x1 =  data_dict[str(id_key[str(edge[0])])]
			x2 =  data_dict[str(id_key[str(edge[1])])]
			l.append({'source': x1[1]+'('+str(x1[0])+')', 'target':x2[1]+'('+str(x2[0])+')'})
		return l
	else:
		edges = nx.edges(st_links)
		l = []
		for edge in edges:
			l.append({'source': str(get_name(edge[0])), 'target':str(get_name(edge[1]))})
		return l

class Home(flask.views.MethodView):

	def get(self):
		r = flask.Response()
		r.headers['Content-Type'] = 'text/html; charset=utf-8'
		r.data = flask.render_template('index.html').encode('utf-8')
		return r

	def post(self):
		r = flask.Response()
		r.headers['Content-Type'] = 'text/html; charset=utf-8'
		r.data = flask.render_template('index.html').encode('utf-8')
		return r


app.add_url_rule(
				 '/home',
				 view_func=Home.as_view('index'),
				 methods=['GET', 'POST']
				)

@app.route('/get_ranks', methods=['GET'])
def get_ranks():
	start = time.time()
	print flask.request.args
	query = flask.request.args['search']
	index = get_matching_query(query,key_id,data_dict)
	q = np.zeros(1716500)
	q[int(index)] = 1.0
	q = scipy.sparse.csc_matrix(q)
	r1, i = get_rwr_ranks(adj, q, 0.7)
	scores = np.array(r1.todense()).flatten()
	k_best_diseases = get_k_best(scores[1716000:1716500],5)
	k_best_users = get_k_best(scores[0:1000000],5)
	k_best_queries = get_k_best(scores[1000000:1716000],5)
	end = time.time()
	r = {'t':[],
		 'diseases':[],
		 'users':[],
		 'queries':[]
		}
	r['t'] = str(end-start)
	for k in k_best_diseases:
		r['diseases'].append([k[0], data_dict[id_key[str(1716000+k[1])]][1]])
	for k in k_best_users:
		r['users'].append([k[0], data_dict[id_key[str(k[1])]][1]])
	for k in k_best_queries:
		r['queries'].append([k[0], data_dict[id_key[str(1000000+k[1])]][1]])
	return json.dumps(r)

@app.route('/get_path', methods=['GET'])
def get_path():
	start = time.time()
	src = flask.request.args['source']
	tgt = flask.request.args['target']
	s = get_matching_node(src,key_id,data_dict)
	t = get_matching_node(tgt,key_id,data_dict)
	path = nx.shortest_path(G1,int(s),int(t))
	g = nx.Graph()
	g.add_path(path)
	links = get_links(g,'path')
	r = {'data':links}
	return json.dumps(r)

@app.route('/get_neighbors', methods=['GET'])
def get_neighbors():
	start = time.time()
	node = flask.request.args['node']
	node = get_matching_node(node,key_id,data_dict)
	NodeVec = snap.TIntV()
	n_nodes = snap.GetNodesAtHop(G,int(node),1,NodeVec,False)
	nodes = [item for item in NodeVec]
	l = []
	for n in nodes:
		x1 =  data_dict[str(id_key[str(node)])]
		x2 =  data_dict[str(id_key[str(n)])]
		l.append({'source': x1[1]+'('+str(x1[0])+')', 'target':x2[1]+'('+str(x2[0])+')'})
	r = {'data':l}
	return json.dumps(r)

@app.route('/get_connections', methods=['GET'])
def get_connections():
	x = [1000000, 1000100, 1716100, 1000500, 1716227]
	G_temp = nx.Graph()
	paths = {}
	for i in x:
		for j in x:
			if i!=j:
				path = nx.shortest_path(G1,i,j)
				G_temp.add_edge(i,j,weight=len(path))
				paths[str(i)+','+str(j)] = path
				paths[str(j)+','+str(i)] = path[::-1]
	tree = nx.minimum_spanning_tree(G_temp)
	G_temp = nx.Graph()
	for e in tree.edges():
		G_temp.add_path(paths[str(e[0])+','+str(e[1])])
	links = get_links(G_temp,'path')
	selected = [data_dict[str(id_key[str(ele)])][1] for ele in x]
	r = {'data':links, 'selected': selected}
	return json.dumps(r)

app.debug = True
app.run(port=8086)
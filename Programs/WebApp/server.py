#!/usr/bin/python
# -*- coding: UTF-8 -*-

import flask, flask.views
import scipy.io
import scipy.sparse
import sys
import json
import numpy as np
import time
from modules.modules import get_rwr_ranks, get_k_best, get_matching_query

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
	r1, i = get_rwr_ranks(adj, q, 0.2)
	k_best = get_k_best(r1.data[len(r1.data)-500:],5)
	end = time.time()
	r = {}
	r['t'] = str(end-start)
	idx = 1
	for k in k_best:
		r[str(idx)] = [k[0], data_dict[id_key[str(1716000+k[1])]][1]]
		idx = idx+1
	return json.dumps(r)

app.debug = True
app.run(port=8088)
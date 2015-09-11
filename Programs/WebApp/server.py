#!/usr/bin/python
# -*- coding: UTF-8 -*-

import flask, flask.views
import scipy.io
import scipy.sparse
import sys
import json
import numpy as np
from modules.modules import get_rwr_ranks, get_k_best, get_matching_query

app = flask.Flask(__name__)
data = scipy.io.loadmat('../../Data/Baidu/data.mat')
adj = data['adjecency_matrix']
with open('../../Data/Baidu/node_data.json', 'rb') as infile:
	data_dict = json.load(infile)
with open('../../Data/Baidu/id-key.json', 'rb') as infile:
	id_key = json.load(infile)


# Create secret key for POST responses. This key must be random and must be secret.
app.secret_key= 'dsrtyuioklmnbvcdfgtyh'
reload(sys)
sys.setdefaultencoding('utf-8')

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
	print flask.request.args
	query = flask.request.args['search']
	index = get_matching_query(query)
	q = np.zeros(1716500)
	q[int(index)] = 1.0
	r1, i = get_rwr_ranks(adj, q, 0.5)
	k_best = get_k_best(r1.data[len(r1.data)-500:],5)
	#print (k_best[2][0]).encode('hex')
	return json.dumps({'1':k_best[2][0]})

app.debug = True
app.run(port=8088)
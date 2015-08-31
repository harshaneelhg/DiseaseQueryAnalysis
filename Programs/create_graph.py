#!/usr/bin/env python

# This program reads raw data in .mat format and converts it into 
# a sparse matrix structure.

def preprocess(path):
	"""
	Input:
		path: path to the CSV file containing data in .mat format.
	Output:
		n : Size of adjecency matrix.
		n_user : Number of unique users.
		n_query : Number of unique queries.
		n_disease : Number of unique diseases.
		A : Adjecency matrix of user-query-disease association.
		user_dict : Dictionary of disease names and their DOIDs.
		query_dict : Dictionary of chemical names and their CHIDs.
		user_id : Dictionary of column/row numbers of diseases and their DOID.
		query_id : Dictionary of column/row numbers of chemicals and their CHID.
		gene_id : Dictionary of column/row numbers of genes and gene names.

	Block matrix structure for Disease-Chemical-Genes association:
	(0 indicates block of zeros in block matrix)

			U 		Q 		D 
		-------------------------
	    |	 	|		|		|
	U	|	0	|		|		|
		|		|		|		|
		-------------------------
	 	|		|		|		|
	Q	|		|	0	|	0	|
		|		|		|		|
		-------------------------
	 	|		|		|		|
	D	|		|	0	|	0	|
		|		|		|		|
		-------------------------
	
	"""
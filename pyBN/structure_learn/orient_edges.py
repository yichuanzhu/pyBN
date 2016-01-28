"""
******************
Orient Edges from
Structure Learning
******************

[1] Chickering. "Learning Equivalence Classes of Bayesian
Network Structues"
http://www.jmlr.org/papers/volume2/chickering02a/chickering02a.pdf
"""

__author__ = """Nicholas Cullen <ncullen.th@dartmouth.edu>"""

from pyBN.independence.constraint_tests import mi_test

import itertools
from copy import copy

def orient_edges_gs(edge_dict, blanket, data, alpha):
	"""
	Orient edges for GrowShrink based on the rules presented
	in Margaritis' Thesis pg. 35. This method requires a
	markov blanket, so may not be useful for other Structure
	learning methods.

	# if there exists a variable Z in N(X)-N(Y)-{Y}
	# such that Y and Z are dependent given S+{X} for
	# all S subset of T, where
	# T is smaller of B(Y)-{X,Z} and B(Z)-{X,Y}

	Arguments
	---------
	*edge_dict* : a dictionary, where
		key = node and value = list
		of neighbors for key. Note: there
		MUST BE duplicates in edge_dict ->
		i.e. each edge should be in edge_dict
		twice since Y in edge_dict[X] and
		X in edge_dict[Y]

	*blanket* : a dictionary, where
		key = node and value = list of
		nodes in the markov blanket of node

	*data* : a nested numpy array

	*alpha* : a float
		Probability of Type II error.

	Returns
	-------
	*d_edge_dict* : a dictionary
		Dictionary of directed edges, so
		there are no duplicates

	Effects
	-------
	None

	Notes
	-----

	"""
	for X in edge_dict.keys():
		for Y in edge_dict[X]:
			nxy = set(edge_dict[X]) - set(edge_dict[Y]) - {Y}

			for Z in nxy:
				by = set(blanket[Y]) - {X} - {Z}
				bz = set(blanket[Z]) - {X} - {Y}
				T = min(by,bz)
				if len(T)>0:
					for i in range(len(T)):
						for S in itertools.combinations(T,i):
							cols = (Y,Z,X) + tuple(S)
							pval = mi_test(data[:,cols])
							if pval < alpha:
								if Y in edge_dict[X]:
									edge_dict[X].remove(Y)
							else:
								if Y in edge_dict[X]:
									edge_dict[Y].remove(X)
				else:
					cols = (Y,Z,X)
					pval = mi_test(data[:,cols])
					if pval < alpha:
						if Y in edge_dict[X]:
							edge_dict[X].remove(Y)
					else:
						if X in edge_dict[Y]:
							edge_dict[Y].remove(X)
	return edge_dict


def orient_edges_pc(edge_dict, block_dict):
	"""
	Orient edges produced from the Path Condition algorithm

	The orientation step will proceed by looking
	for sets of three variables {X, Y,Z} such that
	edges X - Z, Y - Z are in the graph by not the
	edge X - Y . Then, if Z not in block_dict[x][y] , it orients the
	edges from X to Z and from Y to Z creating a
	v-structure: X -> Z <- Y

	Arguments
	---------
	*edge_dict* : a dictionary, where
		key = vertex and value = list of its neighbors.
		NOTE: this is undirected, so the edges are duplicated.

	*block_dict* : a dictionary, where
		key = X, value = another dictionary where
		key = Y, value = set S such that I(X,Y|S)

	Returns
	-------
	*d_edge_dict* : an directed version of original edge_dict

	Effects
	-------
	None

	Notes
	-----
	"""
	d_edge_dict = dict([(rv,[]) for rv in edge_dict.keys()])
	for x in edge_dict.keys():
		for z in edge_dict[x]:
			for y in edge_dict[z]:
				if y!=x and x not in edge_dict[y] and y not in edge_dict[x]:
					if y in block_dict[x]:
						if z not in block_dict[x][y]:
							if z not in d_edge_dict[x]:
								d_edge_dict[x].append(z)
							if z not in d_edge_dict[y]:
								d_edge_dict[y].append(z)
						else:
							if x not in d_edge_dict[z]:
								d_edge_dict[z].append(x)
							if y not in d_edge_dict[z]:
								d_edge_dict[z].append(y)

	return d_edge_dict















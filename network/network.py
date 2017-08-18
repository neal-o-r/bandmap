import numpy as np
import pandas as pd


def get_table(filename):
	# read in a file, group the customers by 
	# author and give it back

	df = pd.read_csv(filename, delimiter='\t', usecols=['User', 'Artist'])
	cn = df.User.value_counts()

	df = df.groupby('Artist').User.apply(set).to_frame()
	df = df[df.index.isin(df.User.apply(len).nlargest(1000).index)]
	
	df['Artist'] = df.index
	df.index = range(len(df))

	return df, cn


def jaccard_distance(set1, set2):
	# compute jaccard similarity of 2 sets
	return float(len(set1 & set2)) / len(set1 | set2)


def set_weight(set1, set2, cn):
	
	intersection = set1 & set2
	union = set1 | set2

	weight1 = mu(intersection, cn)
	weight2 = mu(union, cn)

	return weight1 / weight2
	

def mu(set1, cn):
	
	return (1 / cn[set1] + 20).sum()


def dist_matrix(df, cn):
	# create n x n distance matrix

	customer_sets = df.User.values
	n = len(customer_sets)

	f = open('edges.csv', 'w')

	dists = np.zeros((n, n))
	for i, s1 in enumerate(customer_sets):
		for j, s2 in enumerate(customer_sets[i:]):
			j += i	
			#w = jaccard_distance(s1, s2)
			w = set_weight(s1, s2, cn)

			if (w != 0) and (w != 1):
				f.write('{};{};Undirected;{}\n'.format(
					 i, j, w))
		
			dists[i, j] = w

		if i % 100 == 0: print('{} / {}'.format(i, n))	
 
	dists += dists.T

	f.close()

	return dists


if __name__ == '__main__':

	df, cn = get_table('../data/data_1M.tsv')
	dists = dist_matrix(df, cn)
 
	df.Artist.to_csv('node.csv', sep=';', header=['Label'])

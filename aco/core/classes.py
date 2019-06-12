import random
from scipy.spatial import distance
import numpy as np
import math
import pandas as pd



class Space():
	def __init__(self, Q, ALPHA, BETA, RHO):
		self.min_lenght = float('inf') 
		self.min_path = float('inf')
		self.min_visited_nodes = []
		self.Q = Q
		self.alpha = ALPHA
		self.beta = BETA
		self.rho = RHO



class Ant():
	def __init__(self, graph):
		self.position = random.choice(graph.nodes)
		self.visited_nodes = [self.position]
		self.path = []
		self.has_visited_all_nodes = False



class Edge():
	def __init__(self, nodes, lenght, Q):
		self.pheromone = 1.0
		self.sum_delta_pheromone = 0.0
		self.desirability = 1/lenght
		self.nodes = nodes
		self.lenght = lenght



class Graph():
	def __init__(self, NODES, edges):
		self.nodes = NODES
		self.edges = edges
		self.structure = {}

	def set_connections(self, EDGES):
		for node in self.nodes:
			self.structure[node]=set()

		for edge in EDGES:
			self.structure[edge[0]].add(edge[1])
			self.structure[edge[1]].add(edge[0])

	def get_edge(self, one_node, other_node):
		for edge in self.edges:
			if one_node in edge.nodes and other_node in edge.nodes:
				return edge

	def get_path_lenght(self, path):
		l=0
		for edge in path:
			l = l + edge.lenght
		return l

	def update_delta_pheromone(self, path, space):
		for edge in path:
			edge.sum_delta_pheromone = edge.sum_delta_pheromone + space.Q/edge.lenght 

	def update_pheromone(self, rho):
		for edge in self.edges:
			#evaporate
			edge.pheromone = (1-rho)*edge.pheromone + edge.sum_delta_pheromone
			edge.sum_delta_pheromone=0



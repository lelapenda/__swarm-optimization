import random
from scipy.spatial import distance
import numpy as np
import math
import pandas as pd



class Space():
	def __init__(self, Q, Q0, BETA, RHO, EPSILON, N_CITIES):
		self.min_lenght = float('inf') 
		self.min_path = float('inf')
		self.min_visited_nodes = []
		self.Q0 = Q0
		self.Q = Q
		self.beta = BETA
		self.rho = RHO
		self.epsilon = EPSILON
		self.best_ant = None
		self.n_cities = N_CITIES



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
		self.nearest_neighbor = {}

	def set_connections(self, EDGES):
		for node in self.nodes:
			self.structure[node]=set()

		for edge in EDGES:
			self.structure[edge[0]].add(edge[1])
			self.structure[edge[1]].add(edge[0])

	def set_nearest_neighbor(self):
		node = random.choice(self.nodes)
		visited_nodes = [node]
		initial_node = node
		
		while set(visited_nodes)!=set(self.nodes):
			possible_edges = []
			for id_, to_node in enumerate(self.structure[node]):
				if to_node not in visited_nodes: 
					possible_edges.append(self.get_edge(one_node=node, other_node=to_node))

			if possible_edges==[]: #no edge to follow
				self.set_nearest_neighbor()

			min_edge_lenght = float('inf')
			for edge in possible_edges:
				if edge.lenght<min_edge_lenght:
					min_edge_lenght = edge.lenght
					to_node = list(filter(lambda x: x!=node, edge.nodes))
					self.nearest_neighbor[node] = to_node[0]

			visited_nodes.append(self.nearest_neighbor[node])
			node = self.nearest_neighbor[node]

		self.nearest_neighbor[node]=initial_node


	def get_edge(self, one_node, other_node):
		for edge in self.edges:
			if one_node in edge.nodes and other_node in edge.nodes:
				return edge

	def get_path_lenght(self, path):
		l = sum([edge.lenght for edge in path])
		return l

	def update_delta_pheromone(self, space):
		for edge in space.best_ant.path:
			edge.sum_delta_pheromone = edge.sum_delta_pheromone + 1/space.min_lenght 

	def update_pheromone(self, rho):
		for edge in self.edges:
			#evaporate
			edge.pheromone = (1-rho)*edge.pheromone + rho*edge.sum_delta_pheromone
			edge.sum_delta_pheromone=0

	def local_pheromone_update(self, edge, ant_previous_position, space):
		#lnn heuristic used is the shortest edge lenght from actual node **
		lnn = self.get_edge(ant_previous_position, self.nearest_neighbor[ant_previous_position]).lenght
		delta_pheromone = 1/(space.n_cities*lnn)
		edge.pheromone = (1-space.epsilon)*edge.pheromone + space.epsilon*delta_pheromone



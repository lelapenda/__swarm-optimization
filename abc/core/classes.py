import random
from scipy.spatial import distance
import numpy as np
import math
import pandas as pd



#---- Class Food ------------------


class Food():
	def __init__(self, space):
		self.source = space.lower_boundary + np.random.uniform(0,1,space.dimensions)*(space.upper_boundary-space.lower_boundary)
		self.fitness = float('inf')
		self.countlimit = 0
		self.p = 0

	def set_fitness(self, space):
		self.fitness = space.fitness_function(self.source)

	def probability(self, sumfitness):
		self.p = 1-(self.fitness/float(sumfitness))

	def new_position(self, space, foodn):
		d = random.randint(0,space.dimensions-1)
		newp = self.source.copy()
		newp[d] = self.source[d] + np.random.uniform(-1,1)*(self.source[d]-foodn.source[d])
		return newp

	def greedy_search(self, food, space, idx):
		randomb=random.randint(0,space.n_food-1)
		while(randomb==idx):
			randomb=random.randint(0,space.n_food-1)

		newp = self.new_position(space, food[randomb])
		if space.fitness_function(newp)<self.fitness:
			self.source = newp
			self.set_fitness(space)
			self.countlimit = 0
		else:
			self.countlimit += 1



class Space():
	def __init__(self, D, N_FOOD, func):
		self.dimensions = D
		self.function_name = func
		self.n_food = N_FOOD

		self.boundaries()

	def boundaries(self):
		if self.function_name=='sphere':
			self.lower_boundary = -100
			self.upper_boundary = 100
		elif self.function_name=='rastrigin':
			self.lower_boundary = -5.12
			self.upper_boundary = 5.12
		elif self.function_name=='rosenbrock':
			self.lower_boundary = -30
			self.upper_boundary = 30
	
	def fitness_function(self, x):
		if self.function_name=='sphere':
			return sum(x**2)
		elif self.function_name=='rastrigin':
			return sum((x**2)-(10*np.cos(2*np.pi*x))+10)
		elif self.function_name=='rosenbrock':
			return np.sum(100.0 * (x[1:] - x[:-1] ** 2) ** 2 + (x[:-1] - 1) ** 2)

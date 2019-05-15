import random
from scipy.spatial import distance
import numpy as np
import math
import pandas as pd



#-- Class Fish ---------------

class Fish():
	def __init__(self, space):
		self.position = np.random.uniform(space.lower_boundary,space.upper_boundary,space.dimensions)
		self.weight = random.random() + space.min_weight 
		self.old_weight = self.weight
		self.old_position = self.position
		self.n_position = self.position
		self.delta_fitness = 0

	def info(self):
		print ("position: " + str(self.position) + \
				"\nweight: " + str(self.weight) + \
				"\nold_weight: " + str(self.old_weight) + \
				"\nn_position: " + str(self.n_position) + \
				"\ndelta_fitness: " + str(self.delta_fitness))

	def individual_movement(self, space):
		r = np.random.uniform(-1,1)
		#r = np.random.uniform(-1,1,space.dimensions)
		self.n_position = self.position + space.step_ind*r
		for i in range (0,len(self.n_position)):
			self.n_position[i]=space.lower_boundary if self.n_position[i]<space.lower_boundary else self.n_position[i]
			self.n_position[i]=space.upper_boundary if self.n_position[i]>space.upper_boundary else self.n_position[i]

		self.old_position = self.position.copy()
		self.delta_fitness = float(space.fitness_function(self.n_position)-space.fitness_function(self.position))

		if self.delta_fitness<0:
			self.position = self.n_position.copy()

	def set_weight(self, space):
		if space.max_delta_fitness!=0:
			self.old_weight = self.weight
			self.weight = self.weight + self.delta_fitness/float(space.max_delta_fitness)

	def collective_instictive_movement(self, space):
		self.position = self.position + space.drift

	def collective_volitive_movement(self, space, equation):
		r = np.random.uniform(0,1)
		#r = np.random.uniform(0,1,space.dimensions)
		d=distance.euclidean(self.position, space.baricenter)

		if d!=0:
			if equation == 1:
				self.position = self.position - space.step_vol*r*(self.position-space.baricenter)/d
			else:
				self.position = self.position + space.step_vol*r*(self.position-space.baricenter)/d


#-- Class Search Space ---------------

class Space():
	def __init__(self, STEP_IND_INI, STEP_VOL_INI, MIN_WEIGHT, D, func):
		self.step_ind = STEP_IND_INI 
		self.step_vol = STEP_VOL_INI
		self.min_weight = MIN_WEIGHT
		self.dimensions = D
		self.function_name = func

		self.boundaries()

		self.max_delta_fitness = float('-inf')
		self.drift = []
		self.baricenter = []
		self.overall_weight = 0
		self.old_overall_weight = self.overall_weight

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

	def find_max_delta_fitness(self, fishes):
		self.max_delta_fitness = max([np.abs(p.delta_fitness) for p in fishes]) 

	def compute_drift(self, fishes):
		a = []
		b = []
		for fish in fishes:
			delta_position = [x1-x2 for x1,x2 in zip(fish.position, fish.old_position)]
			a.append([p*fish.delta_fitness for p in delta_position])
			b.append(fish.delta_fitness)
		m = sum(np.array(a))/float(sum(np.array(b)))
		self.drift = m

	def compute_baricenter(self, fishes):
		a = []
		b = []
		for fish in fishes:
			a.append([p*fish.weight for p in fish.position])
			b.append(fish.weight)
		num = np.array(a)
		fishes_weight = np.array(b)
		self.baricenter = sum(num)/float(sum(fishes_weight))

	def compute_overall_weight(self, fishes):
		self.old_overall_weight = self.overall_weight
		self.overall_weight = sum([f.weight for f in fishes])

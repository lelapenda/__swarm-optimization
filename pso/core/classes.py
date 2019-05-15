import random
from scipy.spatial import distance
import numpy as np
import math
import pandas as pd


class Particle():
	def __init__(self, space):
		self.position = np.random.uniform(space.lower_boundary,space.upper_boundary,space.dimensions)
		self.pbest_position = self.position
		self.pbest_value = float('inf')
		self.velocity = np.random.uniform(space.lower_boundary,space.upper_boundary,space.dimensions)
		#para local
		self.lbest_position=self.position
		self.lbest_value=float('inf')

	def informe_posicao(self):
		print("minha posicao atual: " , str(self.position) , "\nminha melhor posicao: " , str(self.pbest_position) , "\nmeu melhor valor: " , str(self.pbest_value) , "\nminha velocidade: ", str(self.velocity))



class Space():
	def __init__(self, D, c1, c2, func, w_variation, topology):
		self.gbest_value = float('inf')
		self.dimensions = D
		self.c1 = c1
		self.c2 = c2
		self.function_name = func
		self.w_variation = w_variation
		self.w = 0
		self.topology = topology

		self.boundaries()

		self.gbest_position = np.random.uniform(self.lower_boundary,self.upper_boundary,self.dimensions)

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

	def set_pbest(self, particle):
		if self.fitness_function(particle.position) < particle.pbest_value:
			particle.pbest_value = self.fitness_function(particle.position)
			particle.pbest_position = particle.position

	def set_gbest(self, particle):
		if particle.pbest_value < self.gbest_value:
			self.gbest_value = particle.pbest_value
			self.gbest_position = particle.pbest_position

	def move_particles(self, particles, particle, focal, ite, indices, N_INTERATIONS):

		if self.topology=='local':
			#dst = [distance.euclidean(particle.position, particle2.position) if distance.euclidean(particle.position, particle2.position)!=0 else float('inf') for particle2 in particles]
			#indices = np.argpartition(dst, number_neighboors)[:number_neighboors]
			particle.lbest_value=float('inf') #o lbest deve ser reinicalizado para toda iteracao com os vizinhos para n manter valores de vizinhos antigos
			for i in range(0, len(indices)):
				if particles[indices[i]].pbest_value<=particle.lbest_value:
					particle.lbest_value=particles[indices[i]].pbest_value
					higher_neighboor_indice=indices[i]
			particle.lbest_position=particles[higher_neighboor_indice].pbest_position

		if self.topology=='global':
			X_POSITION=self.gbest_position
		elif self.topology=='local':
			X_POSITION=particle.lbest_position
		elif self.topology=='focal':
			X_POSITION=focal.pbest_position

		r1=np.array([random.random() for i in range(0,self.dimensions)])
		r2=np.array([random.random() for i in range(0,self.dimensions)])

		if self.w_variation=='constant':
			self.w=0.8
			particle.velocity = self.w*particle.velocity+self.c1*r1*(particle.pbest_position-particle.position)+self.c2*r2*(X_POSITION-particle.position)
		elif self.w_variation=='linear':
			self.w = 0.9-ite*(0.9-0.4)/N_INTERATIONS
			particle.velocity = self.w*particle.velocity+self.c1*r1*(particle.pbest_position-particle.position)+self.c2*r2*(X_POSITION-particle.position)
		elif self.w_variation=='clerc':
			self.w = 2/(math.fabs(2-(self.c1+self.c2)-math.sqrt((self.c1+self.c2)**2-4*(self.c1+self.c2))))
			particle.velocity = self.w*(particle.velocity+self.c1*r1*(particle.pbest_position-particle.position)+self.c2*r2*(X_POSITION-particle.position))
			
		for i in range (0,len(particle.velocity)):
			particle.velocity[i] = self.lower_boundary if particle.velocity[i]<self.lower_boundary else particle.velocity[i]
			particle.velocity[i] = self.upper_boundary if particle.velocity[i]>self.upper_boundary else particle.velocity[i]

		particle.position = particle.position + particle.velocity

	def move_focal(self, particle, ite, N_INTERATIONS):
		
		r1=np.array([random.random() for i in range(0,self.dimensions)])
		r2=np.array([random.random() for i in range(0,self.dimensions)])

		if self.w_variation=='constant':
			self.w=0.8
			particle.velocity = self.w*particle.velocity+self.c1*r1*(particle.pbest_position-particle.position)+self.c2*r2*(self.gbest_position-particle.position)
		elif self.w_variation=='linear':
			self.w = 0.9-ite*(0.9-0.4)/N_INTERATIONS
			particle.velocity = self.w*particle.velocity+self.c1*r1*(particle.pbest_position-particle.position)+self.c2*r2*(self.gbest_position-particle.position)
		elif self.w_variation=='clerc':
			self.w = 2/(math.fabs(2-(self.c1+self.c2)-math.sqrt((self.c1+self.c2)**2-4*(self.c1+self.c2))))
			particle.velocity = self.w*(particle.velocity+self.c1*r1*(particle.pbest_position-particle.position)+self.c2*r2*(self.gbest_position-particle.position))
			
		for i in range (0,len(particle.velocity)):
			particle.velocity[i] = self.lower_boundary if particle.velocity[i]<self.lower_boundary else particle.velocity[i]
			particle.velocity[i] = self.upper_boundary if particle.velocity[i]>self.upper_boundary else particle.velocity[i]

		particle.position = particle.position + particle.velocity

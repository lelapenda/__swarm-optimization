import numpy as np
import os
import classes


FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"



#--- CONSTANTS --------------------
FUNCTIONS=['sphere', 'rastrigin', 'rosenbrock']
FITNESS_SIMULACOES_ITE={'sphere':[], 'rastrigin':[], 'rosenbrock':[]}
AVERAGE_FITNESS_SIMULACOES_ITE = {'sphere':[], 'rastrigin':[], 'rosenbrock':[]}
FITNESS_SIMULACOES_FUNC = {'sphere':[], 'rastrigin':[], 'rosenbrock':[]}


#---PROBLEM SETUP
D = 30 #number of dimensions
N_COLONIA = 30
N_FOOD = N_EMPLOYER = N_ONLOOKER = N_COLONIA/2


N_INTERATIONS = 500000
N_SIMULATIONS = 30



#-- Main ----------------------


for func in FUNCTIONS:

	for simulacoes in range(0,N_SIMULATIONS):
		print(simulacoes, func)

		space = classes.Space(D, N_FOOD, func)
		food = [classes.Food(space) for i in range (0,N_FOOD)]
		FITNESS_VALUES=[]
		BEST_FITNESS = float('inf')


		for ite in range(0, N_INTERATIONS):

			#evaluate fitness for food sources
			for f in food:
				f.set_fitness(space)

			#---EMPLOYERS

			#find new neighbour and perform greedy search
			for idx, f in enumerate(food):
				f.greedy_search(food, space, idx)


			#compute probability
			sumfitness = sum([f.fitness for f in food])
			for f in food:
				f.probability(sumfitness)

			#---ONLOOKERS
			for i in range(0,N_ONLOOKER):
				for idx, f in enumerate(food):
					r = np.random.uniform(0,1)
					if r < f.p:
						f.greedy_search(food, space, idx)
		
			#---SCOUT
			for i in range(0,N_FOOD):
				if food[i].countlimit>=100:
					food[i] = Food() #scouts look for new food
		
			for f in food:
				if f.fitness < BEST_FITNESS:
					BEST_FITNESS = f.fitness

			print(BEST_FITNESS, func)
			FITNESS_VALUES.append(BEST_FITNESS)
				
		FITNESS_SIMULACOES_ITE[func].append(np.array(FITNESS_VALUES))
		FITNESS_SIMULACOES_FUNC[func].append(BEST_FITNESS)

	AVERAGE_FITNESS_SIMULACOES_ITE[func] = np.sum(FITNESS_SIMULACOES_ITE[func], axis=0)/N_SIMULATIONS
		
	np.save(FILE_PATH + "../data/" + func +  "/fitness_simulacoes_ite", FITNESS_SIMULACOES_ITE[func])
	np.save(FILE_PATH + "../data/" + func +  "/average_fitness_ite", AVERAGE_FITNESS_SIMULACOES_ITE[func])
	np.save(FILE_PATH + "../data/" + func +  "/fitness_simulacoes_func", FITNESS_SIMULACOES_FUNC[func])


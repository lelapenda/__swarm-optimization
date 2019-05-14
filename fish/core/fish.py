import numpy as np
import os
import classes


FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"



#--- CONSTANTS --------------------
FUNCTIONS=['sphere', 'rastrigin', 'rosenbrock']
FITNESS_SIMULACOES_ITE={'sphere':[], 'rastrigin':[], 'rosenbrock':[]}
AVERAGE_FITNESS_SIMULACOES_ITE = {'sphere':[], 'rastrigin':[], 'rosenbrock':[]}
FITNESS_SIMULACOES_FUNC = {'sphere':[], 'rastrigin':[], 'rosenbrock':[]}


#--- PROBLEM SETUP
D = 30 #number of dimensions
N = 30 #number of fishes
STEP_IND_INI = 0.1
STEP_IND_FIN = 0.001
STEP_VOL_INI = 0.01
STEP_VOL_FIN = 0.001
MIN_WEIGHT = 1


N_INTERATIONS = 500000
N_SIMULATIONS = 30


#-- Main ----------------------


for func in FUNCTIONS:

	for simulacoes in range(0,N_SIMULATIONS):
		print(simulacoes, func)

		space = classes.Space(STEP_IND_INI, STEP_VOL_INI, MIN_WEIGHT, D, func)
		fishes = [classes.Fish(space) for i in range (0,N)]
		FITNESS_VALUES=[]
		BEST_FITNESS = float('inf')


		for ite in range(0, N_INTERATIONS):

			for fish in fishes:
				fish.individual_movement(space)

			space.find_max_delta_fitness(fishes)

			for fish in fishes:
				fish.set_weight(space)
			
			space.compute_drift(fishes)

			for fish in fishes:
				fish.collective_instictive_movement(space)


			space.compute_baricenter(fishes)
			space.compute_overall_weight(fishes)

			for fish in fishes:
				if space.overall_weight > space.old_overall_weight:
					fish.collective_volitive_movement(space, 1)
				else:
					fish.collective_volitive_movement(space, 2)


			space.step_ind = space.step_ind - (STEP_IND_INI-STEP_IND_FIN)/(ite+1)
			space.step_vol = space.step_vol - (STEP_VOL_INI-STEP_VOL_FIN)/(ite+1)

			for fish in fishes:
				if space.fitness_function(fish.position)<BEST_FITNESS:
					BEST_FITNESS = space.fitness_function(fish.position)
			
			#print(BEST_FITNESS)
			FITNESS_VALUES.append(BEST_FITNESS)
				
		FITNESS_SIMULACOES_ITE[func].append(np.array(FITNESS_VALUES))
		FITNESS_SIMULACOES_FUNC[func].append(BEST_FITNESS)

	AVERAGE_FITNESS_SIMULACOES_ITE[func] = np.sum(FITNESS_SIMULACOES_ITE[func], axis=0)/N_SIMULATIONS
		
	np.save(FILE_PATH + "../data/" + func +  "/fitness_simulacoes_ite", FITNESS_SIMULACOES_ITE[func])
	np.save(FILE_PATH + "../data/" + func +  "/average_fitness_ite", AVERAGE_FITNESS_SIMULACOES_ITE[func])
	np.save(FILE_PATH + "../data/" + func +  "/fitness_simulacoes_func", FITNESS_SIMULACOES_FUNC[func])


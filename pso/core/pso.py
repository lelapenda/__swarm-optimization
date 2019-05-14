import numpy as np
import os
import classes


FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"



#-- CONSTANTS ---------------------
TOPOLOGIES=['global','local', 'focal']
FUNCTIONS=['sphere', 'rastrigin', 'rosenbrock']
FITNESS_SIMULACOES_ITE={'global':{'sphere':[], 'rastrigin':[], 'rosenbrock':[]}, 'local':{'sphere':[], 'rastrigin':[], 'rosenbrock':[]}, 'focal':{'sphere':[], 'rastrigin':[], 'rosenbrock':[]}}
AVERAGE_FITNESS_SIMULACOES_ITE = {'global':{'sphere':[], 'rastrigin':[], 'rosenbrock':[]}, 'local':{'sphere':[], 'rastrigin':[], 'rosenbrock':[]}, 'focal':{'sphere':[], 'rastrigin':[], 'rosenbrock':[]}}
FITNESS_SIMULACOES_FUNC = {'global':{'sphere':[], 'rastrigin':[], 'rosenbrock':[]}, 'local':{'sphere':[], 'rastrigin':[], 'rosenbrock':[]}, 'focal':{'sphere':[], 'rastrigin':[], 'rosenbrock':[]}}
W_VARIATION='linear'

#--- PROBLEM SETUP ----------------
D = 30 #number of dimensions
N = 30 #number of particles
c1 = 2.05
c2 = 2.05
NUMBER_NEIGHBOORS=2 #for local topology


N_INTERATIONS = 10000
N_SIMULATIONS = 30


#-- Main ----------------------


for func in FUNCTIONS:

	for topology in TOPOLOGIES:

			for simulacoes in range(0,N_SIMULATIONS):
				print(topology, simulacoes, func)

				space = classes.Space(D, c1, c2, func, W_VARIATION, topology)
				particles = [classes.Particle(space) for i in range (0,N)]
				focal = classes.Particle(space)
				
				FITNESS_VALUES=[]

				for ite in range(0, N_INTERATIONS):
					
					for particle in particles:

						space.set_pbest(particle)
						space.set_gbest(particle)

						if topology=='focal':
							space.set_pbest(focal)
							space.move_focal(focal, ite, N_INTERATIONS)

						space.move_particles(particles, particle, focal, ite, [particles.index(particle)-1,particles.index(particle)-len(particles)+1], N_INTERATIONS)

					FITNESS_VALUES.append(space.gbest_value)
					#print space.gbest_value

				FITNESS_SIMULACOES_ITE[topology][func].append(np.array(FITNESS_VALUES))
				FITNESS_SIMULACOES_FUNC[topology][func].append(space.gbest_value)

			AVERAGE_FITNESS_SIMULACOES_ITE[topology][func] = np.sum(FITNESS_SIMULACOES_ITE[topology][func], axis=0)/N_SIMULATIONS
		
			np.save(FILE_PATH + "../data/" + topology + "-" + func + "-" + W_VARIATION + "/fitness_simulacoes_ite", FITNESS_SIMULACOES_ITE[topology][func])
			np.save(FILE_PATH + "../data/" + topology + "-" + func + "-" + W_VARIATION + "/average_fitness_ite", AVERAGE_FITNESS_SIMULACOES_ITE[topology][func])
			np.save(FILE_PATH + "../data/" + topology + "-" + func + "-" + W_VARIATION + "/fitness_simulacoes_func", FITNESS_SIMULACOES_FUNC[topology][func])


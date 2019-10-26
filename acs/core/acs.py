import numpy as np
import os
import classes
import graph

FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"



#--- CONSTANTS --------------------
NODES = graph.NODES
EDGES = graph.EDGES 
INITIAL_NODE = '1'

#--- PROBLEM SETUP --------------------
N_CITIES = len(NODES)
N_ANTS = 10
EPSILON = 0.1 #paper rho
BETA = 2
RHO = 0.1 #paper alpha
Q0 = 0.9

N_ITERATIONS = 2500
N_SIMULATIONS = 1


#-- Main ----------------------
def main(space, ant, graph):

	r = ant.choose_edge(space, graph)
	to_edge = r[0]
	to_node = r[1]

	#local pheromone update
	graph.local_pheromone_update(to_edge, ant.position, space) #old position (not updated yet)

	#move ant to new position
	ant.position = to_node #update ant's position
	ant.path.append(to_edge)
	ant.visited_nodes.append(ant.position) #update ant's visited nodes

	if set(ant.visited_nodes)==set(graph.nodes): #ant has visited all nodes
		ant.has_visited_all_nodes = True
		#return to original city -- comment two lines below if not necessary
		ant.path.append(graph.get_edge(ant.visited_nodes[-1], space.initial_node))
		ant.visited_nodes.append(space.initial_node)
		return True

	return False
	


#--- Loop ----------------------
for simulacoes in range(0,N_SIMULATIONS):

	space = classes.Space(Q0, BETA, RHO, EPSILON, N_CITIES, INITIAL_NODE)
	edges = [classes.Edge({x,y},lenght) for x,y,lenght in EDGES]
	graph = classes.Graph(NODES, edges)
	graph.set_connections(EDGES)
	#---nearest neighbor heuristic (uncomment two lines below) 
	#graph.set_nearest_neighbor()
	#graph.set_initial_pheromone(space)

	ants = [classes.Ant(space) for i in range(0, N_ANTS)]

	for ite in range (0,N_ITERATIONS):

		for i in range(0,N_ANTS):

			if ants[i].has_visited_all_nodes==False:

				renew_ant = main(space, ants[i], graph)

				if renew_ant==True and ants[i].has_visited_all_nodes==False: #ant cannot move: reinitialize ant
					ants[i] = classes.Ant(space)
				if renew_ant==True and ants[i].has_visited_all_nodes==True: #ant has completed graph
					l = graph.get_path_lenght(ants[i].path)
					if l<space.min_lenght:
						space.min_lenght=l 
						space.min_path=ants[i].path
						space.min_visited_nodes = ants[i].visited_nodes


		n_ants_completed_path = len((list(filter(lambda x: x.has_visited_all_nodes==True, ants))))
		if n_ants_completed_path==N_ANTS: #if all ants have ended
			graph.update_pheromone(space) #adjust edge's pheromone
			ants = [classes.Ant(space) for i in range(0, N_ANTS)] # ant has completed and n_iterations has not finished yet, reinitialize ant

	print(space.min_visited_nodes)
	print(space.min_lenght)

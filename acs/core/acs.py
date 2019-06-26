import numpy as np
import os
import classes
import graph

FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"



#--- CONSTANTS --------------------
NODES = graph.NODES
EDGES = graph.EDGES 


#--- PROBLEM SETUP --------------------
N_ANTS = 5
N_CITIES = 17
Q = 100
EPSILON = 0.1 #paper rho
BETA = 2
RHO = 0.1 #paper alpha
Q0 = 0.9

N_ITERATIONS = 2500
N_SIMULATIONS = 1


#-- Main ----------------------
def main(space, ant, graph):

	#find the edges connected to an ant
	ant_possible_edges = []
	for id_, to_node in enumerate(graph.structure[ant.position]):
		if to_node not in ant.visited_nodes: #avoids ant to go back to already visited position
			ant_possible_edges.append(graph.get_edge(one_node=ant.position, other_node=to_node))
			
	#e.g.: A -> B or C -> C but C only connects to A (already visited), therefore ant cannot continue exploring this path and has to be reinitialized
	if ant_possible_edges==[]:
		return True
		
	l=[edge.pheromone*edge.desirability**(space.beta) for edge in ant_possible_edges]
	q = np.random.uniform(0,1)

	#acs transition
	if q<space.Q0: #exploitation
		edge_index = l.index(max(l))
	else: #biased exploration - ant system transition rule
		probability=[]
		sum_pheromone_desirability = sum([v for v in l])
		probability = [v/sum_pheromone_desirability for v in l]

		indexes=[i for i, x in enumerate(probability)] 
		edge_index = np.random.choice(indexes, 1, p=probability)[0] #get index of edge chosen by ant 


	#local pheromone update
	graph.local_pheromone_update(ant_possible_edges[edge_index], ant.position, space) #old position (not updated yet)

	#move ant to new position
	to_node = list(filter(lambda x: x!=ant.position, ant_possible_edges[edge_index].nodes)) #get ant's next node
	ant.position = to_node[0] #update ant's position
	ant.visited_nodes.append(ant.position) #update ant's visited nodes

	if set(ant.visited_nodes)==set(graph.nodes):
		#ant has visited all nodes: set ant path
		for i in range(1,len(ant.visited_nodes)):
			ant.path.append(graph.get_edge(one_node=ant.visited_nodes[i-1], other_node=ant.visited_nodes[i]))
			ant.has_visited_all_nodes = True
		return True

	return False
	


#--- Loop ----------------------
for simulacoes in range(0,N_SIMULATIONS):

	space = classes.Space(Q, Q0, BETA, RHO, EPSILON, N_CITIES)
	edges = [classes.Edge({x,y},lenght, space.Q) for x,y,lenght in EDGES]
	graph = classes.Graph(NODES, edges)
	graph.set_connections(EDGES)
	graph.set_nearest_neighbor()
	graph.set_initial_pheromone(space)
	ants = [classes.Ant(graph) for i in range(0, N_ANTS)]

	for ite in range (0,N_ITERATIONS):

		for i in range(0,N_ANTS):

			if ants[i].has_visited_all_nodes==False:

				renew_ant = main(space, ants[i], graph)

				if renew_ant==True and ants[i].has_visited_all_nodes==False: #ant cannot move: reinitialize ant
					ants[i] = classes.Ant(graph)
				if renew_ant==True and ants[i].has_visited_all_nodes==True: #ant has completed graph
					l = graph.get_path_lenght(ants[i].path)
					if l<space.min_lenght:
						space.min_lenght=l 
						space.min_path=ants[i].path
						space.min_visited_nodes = ants[i].visited_nodes
						space.best_ant = ants[i]


		n_ants_completed_path = len((list(filter(lambda x: x.has_visited_all_nodes==True, ants))))
		if n_ants_completed_path==N_ANTS: #if all ants have ended
			graph.update_delta_pheromone(space) #adjust edge's delta pheromone (for each ant)
			graph.update_pheromone(space.rho) #adjust edge's pheromone
			
			ants = [classes.Ant(graph) for i in range(0, N_ANTS)] # ant has completed and n_iterations has not finished yet, reinitialize ant
			n_ants_completed_path=0

	print(space.min_visited_nodes)
	print(space.min_lenght)
import numpy as np
import os
import classes
import graph

FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"



#--- CONSTANTS --------------------
NODES = graph.NODES
EDGES = graph.EDGES #undirected graph


#--- PROBLEM SETUP --------------------
N_ANTS = 5
Q = 100
ALFA = 1
BETA = 5
RHO = 0.5

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

	#compute probability of each edge
	probability=[]
	sum_pheromone_desirability = sum([edge.pheromone**(space.alpha)*edge.desirability**(space.beta) for edge in ant_possible_edges])
	for edge in ant_possible_edges:
		p = (edge.pheromone**(space.alpha)*edge.desirability**(space.beta))/sum_pheromone_desirability
		probability.append(p)

	#ant chooses edge to follow
	l=[i for i, x in enumerate(probability)] 
	edge_index = np.random.choice(l, 1, p=probability)[0] #get index of edge chosen by ant 
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

	space = classes.Space(Q, ALFA, BETA, RHO)
	edges = [classes.Edge({x,y},lenght, space.Q) for x,y,lenght in EDGES]
	graph = classes.Graph(NODES, edges)
	graph.set_connections(EDGES)
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


		n_ants_completed_path = len((list(filter(lambda x: x.has_visited_all_nodes==True, ants))))
		if n_ants_completed_path==N_ANTS: #if all ants have ended
			for ant in ants:
				graph.update_delta_pheromone(ant.path, space) #adjust edge's delta pheromone (for each ant)
			graph.update_pheromone(space.rho) #adjust edge's pheromone
			
			ants = [classes.Ant(graph) for i in range(0, N_ANTS)] # ant has completed and n_iterations has not finished yet, reinitialize ant

	print(space.min_visited_nodes)
	print(space.min_lenght)

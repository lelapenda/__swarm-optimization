import numpy as np
import os
import classes
import graph

FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"



#--- CONSTANTS --------------------
NODES = graph.NODES
EDGES = graph.EDGES 


#--- PROBLEM SETUP --------------------
N_TEAMS = 1
N_ANTS = 5 #number of ants per team
N_CITIES = 17
EPSILON = 0.1 #paper rho
BETA = 2
RHO = 0.1 #paper alpha
Q0 = 0.9

N_ITERATIONS = 3000
N_SIMULATIONS = 1




#-- Auxiliary --------------
def compare_ants(ant, index, team, space, graph):

		r = ant.choose_edge(team, space, graph)
		if r!=False:

			to_edge = r[0]
			to_node = r[1]

			#verify if this ant is the best possible ant to move to chosen city
			ants2=[]
			ant_distance=ant.partial_path_lenght + to_edge.lenght
			for ant2 in team.ants:
				if ant2 != ant:
					if graph.get_edge(ant2.position, to_node)!=None:
						ant2_distance=ant2.partial_path_lenght + graph.get_edge(ant2.position, to_node).lenght
						if ant2_distance<ant_distance:
							ants2.append((ant2, ant2_distance))

			if ants2==[]:
				return ant, to_node, to_edge
			else: #there are better ants
				d = [x[1] for x in ants2]
				ants2_index = d.index(min(d)) #get min distance
				ant2 = ants2[ants2_index][0]
				ant, to_node, to_edge = compare_ants(ant2, team.ants.index(ant2), team, space, graph)
				return ant, to_node, to_edge
		else: #ant cant move - reinitialize team
			team.reinitialize = True
			team.update_visited_nodes(ant.path)
			team.ants[index] = classes.Ant(space)
			ant, to_node, to_edge = compare_ants(team.ants[index], index, team, space, graph)
			return ant, to_node, to_edge

#-- Main ----------------------
def main(space, team, graph):

	a=[ant.partial_path_lenght for ant in team.ants]
	index = a.index(min(a))
	ant = team.ants[index]

	ant, to_node, to_edge = compare_ants(ant, index, team, space, graph)

	#local pheromone update
	graph.local_pheromone_update(to_edge, ant.position, space) #old position (not updated yet)

	#move ant to new position
	ant.position = to_node #update ant's position
	ant.path.append(to_edge)
	ant.visited_nodes.append(to_node)
	ant.partial_path_lenght = graph.get_path_lenght(ant.path)

	team.visited_nodes.append(ant.position) #update ant's visited nodes

	if set(team.visited_nodes)==set(graph.nodes):
		team.has_visited_all_nodes = True
	

#--- Loop ----------------------
for simulacoes in range(0,N_SIMULATIONS):

	space = classes.Space(Q0, BETA, RHO, EPSILON, N_CITIES, N_ANTS, NODES)
	edges = [classes.Edge({x,y},lenght) for x,y,lenght in EDGES]
	graph = classes.Graph(NODES, edges)
	graph.set_connections(EDGES)
	graph.set_nearest_neighbor()
	graph.set_initial_pheromone(space)

	teams = []
	for team in range(N_TEAMS):
		teams.append(classes.Team(space, N_ANTS))

	for ite in range (0,N_ITERATIONS):

		for i in range(0,N_TEAMS):

			if teams[i].has_visited_all_nodes==False:

				main(space, teams[i], graph)

				if teams[i].has_visited_all_nodes==True: #ant has completed graph
					r = teams[i].square_sum()
					if r<space.best_team_square_sum:
						space.best_team=teams[i]
						space.best_team_square_sum = space.best_team.square_sum()
				elif teams[i].reinitialize==True:
					teams[i] = classes.Team(space, N_ANTS)

		n_teams_completed_path = len((list(filter(lambda x: x.has_visited_all_nodes==True, teams))))
		if n_teams_completed_path==N_TEAMS: #if all teams have completed
			
			graph.update_delta_pheromone(space) #adjust edge's delta pheromone (for each ant)
			graph.update_pheromone(space.rho) #adjust edge's pheromone
			
			teams = [classes.Team(space, N_ANTS) for i in range(0, N_TEAMS)] # team has completed and n_iterations has not finished yet, reinitialize team
			n_teams_completed_path=0


	for ant in space.best_team.ants:
		print(ant.visited_nodes)
	print(space.best_team_square_sum)

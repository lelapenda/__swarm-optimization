import numpy as np
import os
import time
import classes
import graph

start_time = time.time()


FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"

#--- CONSTANTS --------------------
NODES = graph.NODES
EDGES = graph.EDGES 
INITIAL_NODE = '1'
RETURN_INITIAL_NODE = True

#--- PROBLEM SETUP --------------------
N_CITIES = len(NODES)
N_TEAMS = 10
N_ANTS = 2 #number of ants per team
EPSILON = 0.1 #paper rho
BETA = 2
RHO = 0.1 #paper alpha
Q0 = 0.9

N_ITERATIONS = 200*N_TEAMS
N_SIMULATIONS = 1
RECURSION_DEPTH=0
EVALUATOR = 'minmax'


#-- Auxiliary --------------
def compare_ants(ant, index, team, space, graph):

		global RECURSION_DEPTH 
		RECURSION_DEPTH = RECURSION_DEPTH + 1

		r = ant.choose_edge(team, space, graph)

		if r!=False:

			to_edge = r[0]
			to_node = r[1]

			#verify if this ant is the best possible ant to move to chosen city
			ants2=[]
			ant_distance=ant.partial_path_lenght + to_edge.lenght + graph.get_edge(to_node, space.initial_node).lenght
			for ant2 in team.ants:
				if ant2 != ant:
					if graph.get_edge(ant2.position, to_node)!=None:
						ant2_distance=ant2.partial_path_lenght + graph.get_edge(ant2.position, to_node).lenght + graph.get_edge(to_node, space.initial_node).lenght
						if ant2_distance<ant_distance:
							ants2.append((ant2, ant2_distance))

			if ants2==[] or RECURSION_DEPTH>5:
				return ant, to_node, to_edge
			else: #there are better ants
				d = [x[1] for x in ants2]
				ants2_index = d.index(min(d)) #get min distance
				ant2 = ants2[ants2_index][0]
				ant, to_node, to_edge = compare_ants(ant2, team.ants.index(ant2), team, space, graph)
				return ant, to_node, to_edge
		else: #ant cant move - reinitialize ant and team
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

	global RECURSION_DEPTH
	RECURSION_DEPTH=0
	ant, to_node, to_edge = compare_ants(ant, index, team, space, graph)

	#local pheromone update
	graph.local_pheromone_update(to_edge, ant.position, space) #old position (not updated yet)

	#move ant to new position
	ant.position = to_node #update ant's position
	ant.path.append(to_edge)
	ant.visited_nodes.append(to_node)
	ant.partial_path_lenght = graph.get_path_lenght(ant.path)

	team.visited_nodes.append(ant.position) #update ant's visited nodes
	team.visited_edges.append(to_edge)

	if set(team.visited_nodes)==set(graph.nodes):
		team.has_visited_all_nodes = True
		for ant in team.ants:
			if graph.get_edge(ant.visited_nodes[-1], space.initial_node)!=None: #if there is an edge between last city and original city, TO DO: treat if there isnt
				if space.return_initial_node==True:
					ant.path.append(graph.get_edge(ant.visited_nodes[-1], space.initial_node))
					ant.visited_nodes.append(space.initial_node)
					ant.partial_path_lenght = graph.get_path_lenght(ant.path)
	

#--- Loop ----------------------
for simulacoes in range(0,N_SIMULATIONS):

	space = classes.Space(Q0, BETA, RHO, EPSILON, N_CITIES, N_ANTS, NODES, INITIAL_NODE, RETURN_INITIAL_NODE)
	edges = [classes.Edge({x,y},lenght) for x,y,lenght in EDGES]
	graph = classes.Graph(NODES, edges)
	graph.set_connections(EDGES)
	#---nearest neighbor heuristic (uncomment two lines below) 
	#graph.set_nearest_neighbor()
	#graph.set_initial_pheromone(space)

	teams = []
	for team in range(N_TEAMS):
		teams.append(classes.Team(space, N_ANTS))

	for ite in range (0,N_ITERATIONS):

		for i in range(0,N_TEAMS):

			if teams[i].has_visited_all_nodes==False:

				main(space, teams[i], graph)

				if teams[i].has_visited_all_nodes==True: #ant has completed graph
					r = teams[i].evaluation(EVALUATOR)
					if r<space.best_team_metric:
						space.best_team = teams[i]
						space.best_team_metric = r
				elif teams[i].reinitialize==True:
					teams[i] = classes.Team(space, N_ANTS)

		n_teams_completed_path = len((list(filter(lambda x: x.has_visited_all_nodes==True, teams))))
		if n_teams_completed_path==N_TEAMS: #if all teams have completed

			# 2-opt local search
			'''
			for team in teams:
				for ant in team.ants:
					ant.visited_nodes = graph.two_opt(ant.visited_nodes)
					ant.path=[]
					ant.partial_path_lenght=0
					for n in range(1,len(ant.visited_nodes)):
						edge = graph.get_edge(ant.visited_nodes[n-1], ant.visited_nodes[n])
						ant.path.append(edge)
					ant.partial_path_lenght = graph.get_path_lenght(ant.path)
				r = team.evaluation(EVALUATOR)
				if r<space.best_team_metric:
					space.best_team = team
					space.best_team_metric = r
			'''
			graph.update_pheromone(space) #adjust edge's pheromone
			teams = [classes.Team(space, N_ANTS) for i in range(0, N_TEAMS)] # team has completed and n_iterations has not finished yet, reinitialize team


# 2-opt local search for best team
for ant in space.best_team.ants:
	ant.visited_nodes = graph.two_opt(ant.visited_nodes)
	ant.path=[]
	ant.partial_path_lenght=0
	for n in range(1,len(ant.visited_nodes)):
		edge = graph.get_edge(ant.visited_nodes[n-1], ant.visited_nodes[n])
		ant.path.append(edge)
	ant.partial_path_lenght = graph.get_path_lenght(ant.path)
	print(ant.visited_nodes)

space.best_team_metric = space.best_team.evaluation(EVALUATOR)
print(space.best_team_metric)


print("--- %s seconds ---" % (time.time() - start_time))
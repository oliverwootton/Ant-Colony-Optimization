import numpy as np
import random

from file_reader import file_read

# Function to multiply each value in D with its 
# counter part in F    
def cost_function(D, F):
    return [[ D[i][j] * F[i][j] for j in range(50)] for i in range(50)]

# Function to initialise the Pheromone Matrix with random values
def pheromone(n):
    T = [[ random.random() if (i != j) else 0  for j in range(n)] for i in range(n)]
    return T

# Function to set one column of a Matrix H to 0
def set_zeros(column, n, H):
    for i in range(n):
        for j in range(n):
            if (i != j) and (j in column):
                H[i][j] = 0
    return H

# Function to caculate the transition probabilities of 
# the next node to traverse to
def transition_prob(i, n, T, route):
    den = 0 
    N = [None] * n
    for j in range(n):
        if (i != j) and (j not in route):
            N[j] = T[i][j]
            den += N[j]
        else:
            N[j] = 0 
    for j in range(n):
        if den > 0 and N[j] != 0:
            N[j] = N[j]/den
        else:
            N[j] = 0
    return N

# Function to randomly select the next node to visit using 
# the probabilities provided by N
def cumulative_prop(num_cities, N):
    CP = 0
    ran = random.random()
    
    for i in range(num_cities):
        CP += N[i]
        if CP > ran:
            return i+1

# Function to calculate the fitness of each path 
# taken by the ants
def fitness(routes, H, m):
    fitness = []
    for i in range(m):
        x = 0
        delta = 0
        for y in routes[i]:
            if x == y:
                continue
            delta += H[x][y]
            x = y
        fitness.append(delta)
    return fitness

# Function to add pheromone to the pheromone matrix
# for each path traversed by the ants
def ant_pheromone(ant, delta, T, n):
    for i in range(n):
        T[ant[i]][ant[i+1]] += delta
    return T

# Function to evaporate the pheromone by e for each #
# value in the matrix
def evaportation(rho, T, n):
    for i in range(n):
        for j in range(n):
            T[i][j] = (rho)*T[i][j]
    return T

# Function to find the lowest value in and array of values
def best_fitness(delta):
    min = delta[0]
    for fitness in delta:
        if fitness < min:
            min = fitness
    return min

# Function to find the route that one ant takes
def one_ant(n, H, T):
    buildingNo = 0
    route = []
    route.append(buildingNo)
    
    for i in range(n-1):
        H = set_zeros(route, n, H)
        # Calculates the probability of moving to the next building
        N = transition_prob(route[-1], n, T, route)
        # Randomly goes to the next building
        buildingNo = cumulative_prop(n, N)
        route.append(buildingNo-1)
    route.append(0)
    return route  

# Function to run 1 trail of 10,000 fitness evaluations
def main(n, D, F, m, rho):
    fitness_eval = 10000
    T = pheromone(n)
    minimum_fitness = []
    for i in range((int) (fitness_eval/m)):
        ant_paths = []
        
        for j in range(m):
            # Generates a list of m ant paths
            H = cost_function(D, F)
            ant_paths.append(one_ant(n, H, T))
        
        H = cost_function(D, F)
        delta = fitness(ant_paths, H, m) 
        
        j = 0
        for route in ant_paths:
            T = ant_pheromone(route, 1/delta[j], T, n)
            j += 1
        
        T = evaportation(rho, T, n)
        
        minimum_fitness.append(best_fitness(delta))
    return best_fitness(minimum_fitness)
        
random.seed(0)
m = 10
e = 0.9

n, D, F = file_read('data.txt')

trial_fitness = []

for i in range(5):
    trial_fitness.append(main(n, D, F, m, e))

print(trial_fitness)

# m = 100, e = 0.9 [74302, 68609, 68557, 68344, 63906]
# m = 100, e = 0.5 [57167, 52777, 53563, 56038, 54639]
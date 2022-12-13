import numpy as np
import random

from file_reader import file_read

def pheromone(n):
    T = [[ random.random() if (i != j) else 0  for j in range(n)] for i in range(n)]
    return T

def set_zeros(column, n, H):
    for i in range(n):
        for j in range(n):
            if (i != j) and (j in column):
                H[i][j] = 0
    return H

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

def cumulative_prop(num_cities, N):
    CP = 0
    ran = random.random()
    
    for i in range(num_cities):
        CP += N[i]
        if CP > ran:
            return i+1

def evaportation(rho, T, n):
    for i in range(n):
        for j in range(n):
            T[i][j] = (rho)*T[i][j]
    return T
            
def ant_pheromone(ant, delta, T, n):
    for i in range(n):
        T[ant[i]][ant[i+1]] += delta
    return T
        
def cost_function(D, F):
    return [[ D[i][j] * F[i][j] for j in range(50)] for i in range(50)]

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

def best_fitness(delta):
    min = delta[0]
    for fitness in delta:
        if fitness < min:
            min = fitness
    return min
  
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

def main(n, D, F, m, rho):
    fitness_eval = 10000
    T = pheromone(n)
    fitness = []
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
        
        fitness.append(delta)
    print(best_fitness(fitness))

random.seed(0)
m = 100
e = 0.9

n, D, F = file_read('data.txt')

main(n, D, F, m, e)

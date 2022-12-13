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

def transition_prob(i, n, T, H):
    den = 0 
    N = [None] * n
    for j in range(n):
        N[j] = T[i][j] * H[i][j]
        print("n")
        print(T[i][j])
        print(H[i])
        print(T[i][j] * H[i][j])
        den += N[j]
    print(den)
    for j in range(n):
        if den > 0:
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
            # print(f"City number --> {i+1}")
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
    min = delta[0]*3
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
        if i == 48:
            print('\n'.join([''.join(['{:20}'.format(item) for item in row]) for row in H]))
        # Calculates the probability of moving to the next building
        N = transition_prob(route[-1], n, T, H)
        print(route[-1])
        # print(N)
        # Randomly goes to the next building
        buildingNo = cumulative_prop(n, N)
        route.append(buildingNo-1)
    route.append(0)
    return route  

def main(n, D, F, m, rho):
    T = pheromone(n)
    fitness_eval = 10000
    
    for i in range((int) (fitness_eval/m)):
        ant_paths = []
        # Generates a list of m ant paths
        k = 0 
        for _ in range(m):
            H = cost_function(D, F)
            ant_paths.append(one_ant(n, H, T))
            print(k)
            k += 1
        
        H = cost_function(D, F)
        delta = fitness(ant_paths, H, m)
        
        j = 0
        for route in ant_paths:
            T = ant_pheromone(route, 1/delta[i], T, n)
            j += 1
        
        T = evaportation(rho, T, n)
        
        minimum_fitness = best_fitness(delta)
        print(minimum_fitness)
        
    
random.seed(0)
m = 100
e = 0.9

n, D, F = file_read('data.txt')

main(n, D, F, m, e)

# for i in range(1):
#     T = ant_colony(D, F, n, num_ants, alpha, beta)
#     # print('\n'.join([''.join(['{:20}'.format(item) for item in row]) for row in T]))
#     print(route_finder(T))

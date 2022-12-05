import numpy as np
import random

from file_reader import file_read

def heuristic(num_cities, D):
    H = [[ round(1/D[i][j],4) if (i != j and D[i][j] !=0) else 0 for j in range(50)] for i in range(50)]
    return H

def pheromone(num_cities):
    T = [[ 1 for j in range(num_cities)] for i in range(num_cities)]
    return T

def set_zeros(column, num_cities, H, D):
    for i in range(num_cities):
        for j in range(num_cities):
            if (i != j) and (j not in column) and (D[i][j] != 0):
                H[i][j] = round(1/D[i][j],4)
            else:
                H[i][j] = 0
    return H

def transition_prob(alpha, beta, i, num_cities, T, H):
    den = 0 
    N = [None] * num_cities
    for j in range(num_cities):
        N[j] = T[i][j] ** alpha * H[i][j] ** beta
        den += N[j]
    
    for j in range(num_cities):
        N[j] = N[j]/den
    return N
    
def cumulative_prop(num_cities, N):
    CP = 0
    ran = random.random()
    
    for i in range(num_cities):
        CP += N[i]
        if CP > ran:
            # print(f"City number --> {i+1}")
            return i+1

def iteration(H, D, num_cities, alpha, beta, T):
    city_number = 1
    routes = []
    routes.append(city_number-1)
    for i in range(num_cities-1):
        H = set_zeros(routes, num_cities, H, D)
        N = transition_prob(alpha, beta, routes[-1], num_cities, T, H)
        city_number = cumulative_prop(num_cities, N)
        routes.append(city_number-1)
    routes.append(0)
    return routes
    
def evaportation(rho, T, num_cities):
    for i in range(num_cities):
        for j in range(num_cities):
            T[i][j] = (1-rho)*T[i][j]
    return T
            
def ant_pheromone(ant, delta, T, num_cities):
    for i in range(num_cities):
        T[ant[i]][ant[i+1]] += delta
    return T

def ant_colony(D, num_cities, num_ants, alpha, beta):
    H = heuristic(num_cities, D)
    T = pheromone(num_cities)
    
    ants = []
    for i in range(num_ants):
        routes = iteration(H, D, num_cities, alpha, beta, T)
        H = heuristic(num_cities, D)
        ants.append(routes)
    
    rho = 0.5
    T = evaportation(rho, T, num_cities)
    
    for i in range(num_ants):
        x = ants[i][0]
        delta = 0
        for y in ants[i]:
            if x == y:
                continue
            delta += D[x][y]
            x = y
        
        delta = 1/delta
        T = ant_pheromone(ants[i], delta, T, num_cities)
    return T

def route_finder(T):
    route = [1]
    nodes = [i for i in range(1, 51, 1)]
    
    for i in range(len(nodes)):
        max = [0, 0]
        y = 0
        for x in T[route[-1]-1]:
            if x > max[0] and y+1 not in route:
                max = [x, y]
            y += 1
        route.append(max[1]+1)
    return route
        

def cost_function(D, F):
    return None

num_ants = 3
alpha = 1
beta  = 2
random.seed(0)

n, D, F = file_read('data.txt')

for i in range(1):
    T = ant_colony(F, n, num_ants, alpha, beta)
    # print('\n'.join([''.join(['{:20}'.format(item) for item in row]) for row in T]))
    print(route_finder(T))

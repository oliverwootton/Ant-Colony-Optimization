import numpy as np
import random

from file_reader import file_read

# def heuristic(num_cities, D):
#     H = [[ round(1/D[i][j],4) if (i != j and D[i][j] !=0) else 0 for j in range(50)] for i in range(50)]
#     return H

def pheromone(num_cities):
    T = [[ random.random() if (i != j) else 0  for j in range(num_cities)] for i in range(num_cities)]
    return T

def set_zeros(column, num_cities, H):
    for i in range(num_cities):
        for j in range(num_cities):
            if (i == j) and (j in column):
                H[i][j] = 0
    return H

def transition_prob(alpha, beta, i, num_cities, T, H):
    den = 0 
    N = [None] * num_cities
    for j in range(num_cities):
        N[j] = T[i][j] ** alpha * H[i][j] ** beta
        den += N[j]
    
    for j in range(num_cities):
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

def iteration(H, num_cities, alpha, beta, T):
    city_number = 1
    routes = []
    routes.append(city_number-1)
    for i in range(num_cities-1):
        H = set_zeros(routes, num_cities, H)
        N = transition_prob(alpha, beta, routes[-1], num_cities, T, H)
        city_number = cumulative_prop(num_cities, N)
        routes.append(city_number-1)
    routes.append(0)
    return routes
    
def evaportation(rho, T, num_cities):
    for i in range(num_cities):
        for j in range(num_cities):
            T[i][j] = (rho)*T[i][j]
    return T
            
def ant_pheromone(ant, delta, T, num_cities):
    for i in range(num_cities):
        T[ant[i]][ant[i+1]] += delta
    return T

def ant_colony(D, F, num_cities, num_ants, alpha, beta):
    # H = heuristic(num_cities, D)
    H = cost_function(D, F)
    T = pheromone(num_cities)
    
    ants = []
    for i in range(num_ants):
        H = cost_function(D, F)
        routes = iteration(H, num_cities, alpha, beta, T)
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
    return [[ D[i][j] * F[i][j] for j in range(50)] for i in range(50)]

def fitness(route, H):
    x = route[0]
    delta = 0
    for y in route:
        if x == y:
            continue
        delta += H[x][y]
        x = y
    return delta

def ant(n):
    buildingNo = 0
    routes = []
    routes.append(buildingNo)
    
    for i in range(n-1):
        H = set_zeros(routes, n, H)
        N = transition_prob(alpha, beta, routes[-1], n, T, H)
        buildingNo = cumulative_prop(n, N)
        routes.append(buildingNo-1)
    routes.append(0)
    

def main(n):
    T = pheromone(n)
    
    
    

num_ants = 3
alpha = 1
beta  = 2
random.seed(0)

n, D, F = file_read('data.txt')

main(n)

# for i in range(1):
#     T = ant_colony(D, F, n, num_ants, alpha, beta)
#     # print('\n'.join([''.join(['{:20}'.format(item) for item in row]) for row in T]))
#     print(route_finder(T))

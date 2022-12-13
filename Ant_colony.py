import numpy as np
import random
import matplotlib.pyplot as plt

from file_reader import file_read

# Function to multiply each value in D with its 
# counter part in F    
def cost_function(D, F):
    return [[ D[i][j] * F[i][j] for j in range(50)] for i in range(50)]

# Function to initialise the Pheromone Matrix with random values
def pheromone(n):
    return [[ random.random() if (i != j) else 0  for j in range(n)] for i in range(n)]

# Function to set one column of a Matrix H to 0
def set_zeros(column, n, H):
    for i in range(n):
        H[i][column] = 0
    return H

# Function to caculate the transition probabilities of 
# the next node to traverse to
def transition_prob(i, n, T, route):
    # Denominator
    den = 0 
    N = [None] * n
    
    # Loop sets N values and adds each value to den
    for j in range(n):
        if (i != j) and (j not in route):
            N[j] = T[i][j]
            den += N[j]
        else:
            N[j] = 0 
    # Loop converts values in N to probabilities
    for j in range(n):
        if den > 0 and N[j] != 0:
            N[j] = N[j]/den
        else:
            N[j] = 0
    return N

# Function to randomly select the next node to visit using 
# the probabilities provided by N
def cumulative_prop(n, N):
    CP = 0
    ran = random.random()
    for i in range(n):
        CP += N[i]
        if CP > ran:
            return i

# Function to calculate the fitness of each path 
# taken by the ants
def fitness(routes, H, m):
    fitness = []
    # Finds the value at each point that the ant traversed
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
    # for i in range(n):
    #     for j in range(n):
    #         T[i][j] = (rho)*T[i][j]
    # return T
    return [[(rho)*T[i][j] for j in range(n)] for i in range(n)]

# Function to find the lowest value in and array of values
def best_fitness(delta):
    min = delta[0]
    for fitness in delta:
        if fitness < min:
            min = fitness
    return min

# Function to find the route that one ant takes
def one_ant(n, H, T):
    # Start Node
    node = 0
    route = []
    route.append(node)
    # Loop finds the path from the start node through each other node
    for _ in range(n-1):
        H = set_zeros(route[-1], n, H)
        # Calculates the probability of moving to the next building
        N = transition_prob(route[-1], n, T, route)
        # Randomly goes to the next building
        node = cumulative_prop(n, N)
        route.append(node)
    # Adds the start node to the end to return to the first building
    route.append(0)
    return route  

# Function to run 1 trail of 10,000 fitness evaluations
def main(n, D, F, m, rho):
    fitness_eval = 10000
    # Initialise the pheromone matrix
    T = pheromone(n)
    # List to keep track of all the fitness scores of each path
    minimum_fitness = []
    for _ in range((int) (fitness_eval/m)):
        # List of paths taken by the ants
        ant_paths = []
        
        # Generates a list of m ant paths
        for j in range(m):
            H = cost_function(D, F)
            ant_paths.append(one_ant(n, H, T))
        
        H = cost_function(D, F)
        # Finds the fitness of each path taken 
        delta = fitness(ant_paths, H, m) 
        
        j = 0
        for route in ant_paths:
            T = ant_pheromone(route, 1/delta[j], T, n)
            j += 1
        
        T = evaportation(rho, T, n)
        
        minimum_fitness.append(best_fitness(delta))
    return best_fitness(minimum_fitness)

# Function to plot a graph of the average fitness of each trial
def plotGraph(y, y1):
    x = [1, 2, 3, 4, 5]
    if y == 0:
        plt.plot(x, y1, marker = 'o', label = "m = 100, e = 0.9")
    if y == 1:
        plt.plot(x, y1, marker = 'o', label = "m = 100, e = 0.5")
    if y == 2:
        plt.plot(x, y1, marker = 'o', label = "m = 10, e = 0.9")
    if y == 3:
        plt.plot(x, y1, marker = 'o', label = "m = 10, e = 0.5")

# Function runs 5 trial for one experiment
def run(m, e):
    trial_fitness = []
    for _ in range(5):
        trial_fitness.append(main(n, D, F, m, e))
    return trial_fitness

# Function sets the parameters for each trial and displace 
# the formatted graph with results
def run_trials():
    m = 100
    e = 0.9
    trials = []
    
    trials.append(run(m, e))
    e = 0.5
    trials.append(run(m, e))
    m = 10
    e = 0.9
    trials.append(run(m, e))
    e = 0.5
    trials.append(run(m, e))
    
    for x in trials:
        print(x)
        z = 0
        for y in x:
            z += y
        print(z/5)
    
    for i in range(len(trials)):
        plotGraph(i, trials[i])
    
    plt.title("Experiment Results")
    plt.xlabel("Trial Number")
    plt.ylabel("Average Fitness Score")
    plt.legend(loc="upper right")
    plt.show()

random.seed(0)
n, D, F = file_read('Uni50a.dat')
run_trials()

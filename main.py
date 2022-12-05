import numpy as np

from Ant_colony import AntColony

from file_reader import file_read

n, d, f = file_read('data.txt')

D = np.array(d)

print(d)

ant_colony = AntColony(D, 1, 1, 100, 0.95, alpha=1, beta=1)
shortest_path = ant_colony.run()
print ("shorted_path: {}".format(shortest_path))

import matplotlib.pyplot as plt

# Function to display a before and after gra
def plotGraph(y1, y2, y3, y4):
    x = [1, 2, 3, 4, 5]

    plt.plot(x, y1, marker = 'o', label = "m = 100, e = 0.9")
    plt.plot(x, y2, marker = 'o', label = "m = 100, e = 0.5")
    plt.plot(x, y3, marker = 'o', label = "m = 10, e = 0.9")
    plt.plot(x, y4, marker = 'o', label = "m = 10, e = 0.5")
    plt.title("Experiment Results")
    plt.xlabel("Trial Number")
    plt.ylabel("Average Fitness Score")
    plt.legend(loc="upper right")
    plt.show()

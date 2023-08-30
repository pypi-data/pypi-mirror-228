import matplotlib.pyplot as plt
import numpy as np

def logistic_map(a, u_initial, iterations):
    values = []
    u = u_initial
    for _ in range(iterations):
        u = a * u * (1 - u)
        values.append(u)
    return values[-100:]  # 只返回最后100个值，以减少收敛的影响

def plot_bifurcation_diagram():
    a_values = np.linspace(0, 4, 10000)
    initial_value = 0.5
    iterations = 1000

    x = []
    y = []

    for a in a_values:
        u_values = logistic_map(a, initial_value, iterations)
        x.extend([a] * len(u_values))
        y.extend(u_values)

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, s=0.1)
    plt.xlabel("a")
    plt.ylabel("$u_n$")
    plt.title("Bifurcation Diagram")
    plt.show()



if __name__ == "__main__":
    plot_bifurcation_diagram()


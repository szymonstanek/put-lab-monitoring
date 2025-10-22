import numpy as np
import matplotlib.pyplot as plt
from z21 import calculate_traffic_per_class, calculate_distribution, calculate_blocking_probability

def run_task_22():
    C = 20
    t = np.array([1, 3])
    amin = 0.2
    amax = 1.3
    astep = 0.1

    a_values = np.arange(amin, amax + astep/2, astep)

    results = []

    for a in a_values:
        a_i = calculate_traffic_per_class(a, C, t)
        p = calculate_distribution(C, a_i, t)
        E = calculate_blocking_probability(p, t, C)
        results.append([a, *E])

    filename = 'task_22_blocking_probabilities.txt'
    with open(filename, 'w') as f:
        f.write(f"# C = {C}\n")
        f.write("#\n")
        for i in range(len(t)):
            f.write(f"#\tt[{i+1}]= {t[i]}\n")
        f.write("#\n")

        for row in results:
            line = f"{row[0]:.1f}"
            for val in row[1:]:
                line += f"\t{val:.8f}"
            f.write(line + "\n")

    results = np.array(results)

    plt.figure(figsize=(10, 6))

    for i in range(len(t)):
        plt.semilogy(results[:, 0], results[:, i+1], marker='o', label=f't{i+1} = {t[i]} AU')

    plt.xlabel('Offered traffic per capacity unit (a) [Erl]')
    plt.ylabel('Blocking probability (log scale)')
    plt.title(f'Task 2.2: Blocking Probability (C={C} AUs)')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.3)
    plt.tight_layout()

    plot_filename = 'task_22_plot.png'
    plt.savefig(plot_filename, dpi=300)
    plt.close()

    print(f"Task 2.2 completed successfully")
    print(f"  Data saved to: {filename}")
    print(f"  Plot saved to: {plot_filename}")

import numpy as np
from z21 import *

amin = float(input("amin: "))
amax = float(input("amax: "))
astep = float(input("astep: "))
C = int(input("C (pojemność): "))
m = int(input("m (liczba klas): "))

t = []
for i in range(m):
    ti = int(input(f"Podaj t[{i}]: "))
    t.append(ti)

t = np.array(t)

a_values = np.arange(amin, amax + astep, astep)

results = []

for a in a_values:
    a_i = calculate_traffic_per_class(a, C, t)
    p = calculate_distribution(C, a_i, t)
    E = calculate_blocking_probability(p, t, C)
    results.append([a, *E])

with open('blocking_probabilities.txt', 'w') as f:
    f.write(f"# C = {C}\n")
    f.write(f"# t[1]= {t[0]}\n")
    for i in range(1, len(t)):
        f.write(f"# t[{i + 1}]= {t[i]}\n")
    f.write("#\n")

    for row in results:
        line = f"{row[0]:.1f}"
        for val in row[1:]:
            line += f"\t{val:.8f}"
        f.write(line + "\n")

print("Zapisano do blocking_probabilities.txt")
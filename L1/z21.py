import numpy as np

def calculate_distribution(C, a, t):
    s = np.zeros(C+1)
    s[0] = 1
    for n in range(1, C+1):
        sum_value = 0
        for i in range(len(a)):
            if n >= t[i] :
                sum_value += a[i] * t[i] * s[n - t[i]]
        s[n] = sum_value / n

    total_sum = np.sum(s)
    p = s/total_sum
    return p

def calculate_blocking_probability(p, t, C):
    E = np.zeros(len(t))
    for i in range(len(t)):
        start = C - t[i] + 1
        E[i] = np.sum(p[start:C+1])
    return E

def calculate_traffic_per_class(a, C, t):
    m = len(t)
    a_i = np.zeros(m)

    for i in range(m):
        a_i[i] = (a *C) / (m * t[i])
    return a_i
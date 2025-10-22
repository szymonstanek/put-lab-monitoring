import numpy as np

def calculate_distribution(C, a, t):
    s = np.zeros(C+1)
    s[0] = 1

    # Rekurencyjne obliczanie stanów 1, 2, ..., C
    for n in range(1, C+1):
        sum_value = 0
        for i in range(len(a)):  #
            if n >= t[i]:
                sum_value += a[i] * t[i] * s[n - t[i]]  # Rekursywne wyrażenie: poprzedni stan * waga ruchu
        s[n] = sum_value / n  # Wzór Kaufmana-Robertsa: suma podzielona przez n

    # Normalizacja - zamiana s[n] na prawdziwe prawdopodobieństwa p[n]
    total_sum = np.sum(s)
    p = s/total_sum
    return p

def calculate_blocking_probability(p, t, C):
    # Obliczanie prawdopodobieństwa blokady dla każdej klasy (wzór 5)
    E = np.zeros(len(t))  # Tablica prawdopodobieństw blokady dla każdej klasy
    for i in range(len(t)):  # Dla każdej klasy strumienia
        start = C - t[i] + 1  # Pierwszy stan gdzie następuje blokada (za mało miejsca)
        E[i] = np.sum(p[start:C+1])  # Suma prawdopodobieństw stanów blokujących
    return E

def calculate_traffic_per_class(a, C, t):
    # Obliczanie natężenia ruchu dla każdej klasy (wzór 7)
    m = len(t)  # Liczba klas strumieni
    a_i = np.zeros(m)  # Tablica natężeń ruchu dla poszczególnych klas

    for i in range(m):
        a_i[i] = (a * C) / (m * t[i])  # Rozkład ruchu proporcjonalny do zapotrzebowania
    return a_i

def calculate_average_occupancy(p, a_i, t, C):
    # Obliczanie średniej liczby zajętych zasobów w każdym stanie (wzór 6)
    m = len(t)  # Liczba klas strumieni
    y = np.zeros((C+1, m))  # Macierz: wiersze = stany (0..C), kolumny = klasy

    for n in range(C+1):  # Dla każdego stanu zajętości systemu
        if p[n] > 0:  # Unikaj dzielenia przez zero
            for i in range(m):
                if n >= t[i]:
                    # Wzór: y_i(n) = (a_i * t_i * p[n-t_i]) / p[n]
                    y[n][i] = (a_i[i] * t[i] * p[n - t[i]]) / p[n]

    return y
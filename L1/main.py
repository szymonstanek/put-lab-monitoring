import numpy as np
from z21 import *
from z22 import run_task_22
from z23 import run_task_23

def run_task_21():
    amin = float(input("amin: ")) #Dolny zakres
    amax = float(input("amax: ")) #Górny zakres oferowanego ruchu przypadający na jedną jednostkę pojemności
    astep = float(input("astep: ")) #Ile wynosi krok miedzy a_min a a_max np. a_step=0.1 to krok o 0.1 od a_min do a_max
    C = int(input("C (pojemność): ")) #Liczba wszystkich dostępnych AU (ostatnia *[n])
    m = int(input("m (liczba klas): ")) #Liczba strumieni ruchu prowadzących do zasobów (ostatnia *[i])

    t = []
    for i in range(m):
        ti = int(input(f"Podaj t[{i}]: "))
        t.append(ti)

    t = np.array(t)

    # Generowanie wartości ruchu oferowanego w zadanym zakresie
    a_values = np.arange(amin, amax + astep, astep)

    results = []  # Lista wyników: [a, E[0], E[1], ...]
    occupancy_data = []  # Lista danych zajętości: [(a, macierz_y), ...]

    # Główna pętla - obliczenia dla każdej wartości ruchu
    for a in a_values:
        a_i = calculate_traffic_per_class(a, C, t)  # Ruch per klasa (wzór 7)
        p = calculate_distribution(C, a_i, t)  # Rozkład zajętości (Kaufman-Roberts)
        E = calculate_blocking_probability(p, t, C)  # Prawdopodobieństwo blokady (wzór 5)
        results.append([a, *E])  # Zapisz: ruch + blokady dla każdej klasy

        y = calculate_average_occupancy(p, a_i, t, C)  # Średnia zajętość (wzór 6)
        occupancy_data.append((a, y))  # Zapisz parę: (ruch, macierz zajętości)

    # Zapis wyników prawdopodobieństw blokady do pliku
    with open('blocking_probabilities.txt', 'w') as f:
        # Nagłówek: informacje o systemie
        f.write(f"# C = {C}\n")
        f.write("#\n")
        for i in range(len(t)):
            f.write(f"#\tt[{i+1}]= {t[i]}\n")
        f.write("#\n")

        # Dane: ruch + prawdopodobieństwa blokady dla każdej klasy
        for row in results:
            line = f"{row[0]:.1f}"  # Pierwsza kolumna: wartość ruchu
            for val in row[1:]:  # Kolejne kolumny: E[i] dla każdej klasy
                line += f"\t{val:.8f}"
            f.write(line + "\n")

    # Zapis wyników średniej zajętości zasobów do pliku
    with open('average_occupancy.txt', 'w') as f:
        # Nagłówek: informacje o systemie
        f.write(f"# C = {C}\n")
        f.write("#\n")
        for i in range(len(t)):
            f.write(f"#\tt[{i+1}]= {t[i]}\n")
        f.write("#\n")

        # Dane dla każdej wartości ruchu
        for a, y_matrix in occupancy_data:
            f.write(f"{a:.1f}\n")  # Wartość ruchu

            # Nagłówek tabeli: stan | t1 | t2 | ... | suma
            header = "0"
            for i in range(len(t)):
                header += f"\tt{i+1}"
            header += "\t:\tsum"
            f.write(header + "\n")

            # Dane: dla każdego stanu n wypisz zajętość każdej klasy
            for n in range(C+1):
                line = f"{n}"  # Pierwsza kolumna: stan (liczba zajętych AU)
                total = 0
                for i in range(len(t)):  # Dla każdej klasy
                    val = y_matrix[n][i]  # Średnia zajętość klasy i w stanie n
                    if abs(val - round(val)) < 1e-9:  # Zaokrąglij jeśli blisko liczby całkowitej
                        line += f"\t{int(round(val))}"
                    else:
                        line += f"\t{val:.6g}"
                    total += val
                # Ostatnia kolumna: suma (powinna być równa n)
                if abs(total - round(total)) < 1e-9:
                    line += f"\t:\t{int(round(total))}"
                else:
                    line += f"\t:\t{total:.6g}"
                f.write(line + "\n")

            f.write("\n")  # Pusta linia między wartościami ruchu

    print("Task 2.1 completed successfully")
    print("  Data saved to: blocking_probabilities.txt")
    print("  Data saved to: average_occupancy.txt")

if __name__ == "__main__":
    print("=" * 50)
    print("Network Monitoring Lab 1")
    print("=" * 50)
    print("Available tasks:")
    print("  2.1 - Calculate blocking probabilities (custom parameters)")
    print("  2.2 - Generate plots for C=20, t=[1,3]")
    print("  2.3 - Generate plots for C=40, t=[1,3,4]")
    print("=" * 50)

    task = input("Select task (2.1 / 2.2 / 2.3): ").strip()

    if task == "2.1":
        run_task_21()
    elif task == "2.2":
        run_task_22()
    elif task == "2.3":
        run_task_23()
    else:
        print(f"Invalid task selection: {task}")
        print("Please run the program again and select 2.1, 2.2, or 2.3")
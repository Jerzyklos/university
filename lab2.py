import matplotlib.pyplot as plt
import numpy as np

def stworzMacierz_warunki_1():
    t_grzalki = 80
    t_brzeg_blaszki = 10
    t_blaszki = 20
    A = round(n / 3)
    B = round(n / 3)
    C = round(n / 6)

    # Pierwszy wymiar ma wartość 0 gdy próżnia, 1 gdy blaszka i 2 gdy blaszka ale o stałej temp.
    # Drugi wymiar to temperatura
    matrix = np.zeros((n, n, 2), dtype='double')

    # inicjalizacja blaszki
    for x in range(n):
        for y in range(n):
            # rogi gdzie jest próżnia. Rogi: lewy górny, lewy dolny, prawy górny, lewy górny.
            if (x < A and y < B) or (x < A and y > (A + B)) or (x > (A + B) and y < B) or (x > (A + B) and y > (A + B)):
                matrix[x, y, 0] = 0
            # blaszka
            else:
                matrix[x, y, 0] = 1
    # inicjalizacja temperatur
    for x in range(n):
        for y in range(n):
            # grzałka
            if x > (A + (B - C) / 2) and x < (A + (B - C) / 2 + C) and y > (B + (A - C) / 2) and y < (
                    B + (A - C) / 2 + C):
                matrix[x, y, 1] = t_grzalki
            elif matrix[x, y, 0]:
                matrix[x, y, 1] = t_blaszki
            else:
                matrix[x, y, 1] = 0
    # brzegi blaszki
    for i in range(A):
        matrix[i, B, 1] = t_brzeg_blaszki
        matrix[A+B+i, B, 1] = t_brzeg_blaszki
        matrix[i, B+A, 1] = t_brzeg_blaszki
        matrix[A+B+i, B+A, 1] = t_brzeg_blaszki
        matrix[0, B+i, 1] = t_brzeg_blaszki
        matrix[n-1, B+i] = t_brzeg_blaszki
    for i in range(B):
        matrix[A+i, 0, 1] = t_brzeg_blaszki
        matrix[A+i+1, n-1, 1] = t_brzeg_blaszki
        matrix[A, i, 1] = t_brzeg_blaszki
        matrix[A, B+A+i, 1] = t_brzeg_blaszki
        matrix[A+B, i, 1] = t_brzeg_blaszki
        matrix[A+B, B+A+i] = t_brzeg_blaszki

    # ustawienie wartości 2 w miejscach, których temp. się nie zmienia
    for x in range(n):
        for y in range(n):
            if matrix[x, y, 1] != t_blaszki and matrix[x, y, 1] != 0:
                matrix[x, y, 0] = 2

    return matrix

def pokazWykres(matrix):
    Z = matrix[:, :, 1]
    plt.imshow(Z, origin='lower', interpolation='bilinear')
    plt.colorbar()
    plt.title("Rozkład temperatury")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

def warunki1(dt, n, t_max, K, c, p):
    dx = 1/n
    dy = 1/n

    matrix = stworzMacierz_warunki_1()

    for i in range(t_max):
        matrix_nowy = matrix[:,:,:]
        for x in range(1, n-1):
            for y in range(1, n-1):
                if matrix[x, y, 0] == 1:
                    matrix_nowy[x, y, 1] = matrix[x, y, 1] + K*dt*(matrix[x+1, y, 1] - 2*matrix[x, y, 1] + matrix[x-1, y, 1])/(c*p*dx**2) + K*dt*(matrix[x, y+1, 1] - 2*matrix[x, y, 1] + matrix[x, y-1, 1])/(c*p*dy**2)
        matrix = matrix_nowy[:,:,:]
        if i*dt == 10:
            print("wyłączam grzałkę")
            pokazWykres(matrix)
            for x in range(n):
                for y in range(n):
                    # grzałka
                    A = round(n / 3)
                    B = round(n / 3)
                    C = round(n / 6)
                    if x > (A + (B - C) / 2) and x < (A + (B - C) / 2 + C) and y > (B + (A - C) / 2) and y < (
                            B + (A - C) / 2 + C):
                        matrix[x, y, 0] = 1
            pokazWykres(matrix)
    pokazWykres(matrix)

# aluminium
dt = 0.5
n = 100 # rozdzielczość siatki
t_max = 50
K = 237
c = 900
p = 2700

warunki1(dt, n, t_max, K, c, p)
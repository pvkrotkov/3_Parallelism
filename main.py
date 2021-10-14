# -*- coding: utf-8 -*-
from multiprocessing import Pool # импорт

def element(index, A, B): #нахождение элемента
    i, j = index
    res = 0
    # get a middle dimension
    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]
    with open("log.txt", "a") as file:
        file.write(res)
    return res

matrix1 = []
with open("matrix1.txt", "r") as file:    
    for i in file:
        matrix1.append(list(map(int, i.split()))) #чтение первой матрицы
matrix2 = []
with open("matrix2.txt", "r") as file:  # чтение второй матрицы  
    for i in file:
        matrix2.append(list(map(int, i.split())))
matrix3 = []
if __name__ == "__main__":
    with Pool(processes=4) as p: #пул с 4 процессами
        for i in range(len(matrix1)): #каждачя строка матрицы будет рассчитываться синхронно
            line = [p.apply_async(element, ((i,j), matrix1, matrix2)) for j in range(len(matrix2))]
            matrix3.append(line)
        for i in range(len(matrix1)): # распаковываеи результаты вычислений
            for j in range(len(matrix2)):
                matrix3[i][j]=matrix3[i][j].get()
print(matrix3)

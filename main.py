from multiprocessing import Process, Pool
import csv


def print_matr(matrix):
    """
    Функция для печати матрицы в консоли
    """
    max_len = 0
    for row in matrix:
        len_list = list(map(str, row))
        if len(len_list) > 0:
            max_len_local = len(max(len_list, key=len))
            if max_len_local > max_len:
                max_len = max_len_local
    print('-'*((max_len+1)*len(matrix[0])+1))
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print('|', end='')
            print(str(matrix[i][j]).center(max_len), end='')
        if len(matrix[i]) != 0:
            print('|')
            print('-'*((max_len+1)*len(matrix[0])+1))


def read_matrix(path):
    """
    Функция чтения матрицы. Принимает на вход путь до файла.
    """
    with open(path, 'r') as matrix_csv:
        matrix = list(csv.reader(matrix_csv, delimiter=';'))
        matrix_list = list(map(lambda row: list(map(float, row)), matrix))
    return matrix_list


def element(element):
    """
       Функция, расчитывающая элемент. Позаимствована из методички.
       """
    index = element[0]
    A = element[1]
    B = element[2]
    i, j = index
    res = 0
    N = len(A[0]) or len(B)
    for k in range(N):
        num = round(A[i][k] * B[k][j], 2)
        res += num
    return res


def main():
    matrix_1 = read_matrix("matrix_1.csv")
    matrix_2 = read_matrix("matrix_2.csv")
    # Количество процессов равно количеству элементов в конечной матрице, что равно произведению количества
    # столбцов и строк в конечной матрице.
    num_of_processes = Pool(processes=len(matrix_1) * len(matrix_2[0])) # программа сама определяет необходимое число потоков
    # Для удобного вызова пула процессов представим элемент в виде списка из трёх элементов: список с его координатами
    # и две матрицы
    elements = [[[i, j], matrix_1, matrix_2] for i in range(len(matrix_1)) for j in range(len(matrix_2[0]))]
    result = num_of_processes.map(element, elements)

    # Запись результирущей матрицы в файл. Сохранится в текущей директории.
    with open('result.csv', 'w') as res:
        writer = csv.writer(res, delimiter=';')
        for row in range(0, len(result), len(matrix_2[0])):
            writer.writerow(result[row:row + len(matrix_2[0])])

    matrix = read_matrix("result.csv")
    print('Matrix 1')
    print_matr(matrix_1)
    print('Matrix 2')
    print_matr(matrix_2)
    print('Result matrix')
    print_matr(matrix)


if __name__ == '__main__':
    main()

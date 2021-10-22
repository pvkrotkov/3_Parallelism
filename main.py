from multiprocessing import *
from itertools import product
from random import randint
from time import sleep
import keyboard

LOG_FILE = "log.txt"
STOP = "q"


def read_matrix(file_name):
    with open(file_name, "r") as file:
        matrix = [list(map(int, line.split(" "))) for line in file]
        return matrix


def write_settings(size, element_range, file_name):
    with open(file_name, "a") as file:
        file.write(f"Размер матрицы: {size}*{size}\n")
        file.write(f"Диапазон данных: [{element_range[0]}; {element_range[1]}]\n")


def write_log(first_matrix, second_matrix, result, size, file_name):
    with open(file_name, "a") as file:
        file.write("Матрица A:\n" + matrix_to_str(first_matrix, size))
        file.write("Матрица B:\n" + matrix_to_str(second_matrix, size))
        file.write("Результат:\n" + matrix_to_str(result, size) + "\n")


def matrix_to_str(matrix, size):
    line = ""
    for row in range(size):
        for column in range(size):
            line += " " * (get_length(matrix, size, column) - len(str(matrix[row * size + column]))) + str(
                matrix[row * size + column]) + " "
        line += "\n"
    else:
        line += "\n"
    return line


def get_length(matrix, size, column):
    return max([len(str(matrix[index * size + column])) for index in range(size)])


def check_matrices(first_matrix, second_matrix):
    return len(first_matrix[0]) == len(second_matrix)


def generate_matrix(size=3, element_range=(-100, 100)):
    return [randint(*element_range) for _ in range(size ** 2)]


def calculate_element(args):
    (first_matrix, second_matrix, size, (i, j)) = args
    result = float(0)
    for k in range(size):
        result += first_matrix[i * size + k] * second_matrix[k * size + j]
    return str(int(result))


def loop(size, element_range, stop_event):
    while not stop_event.is_set():
        first_matrix = generate_matrix(size, element_range)
        second_matrix = generate_matrix(size, element_range)
        indexes = list(product(range(size), repeat=2))
        pool = Pool(processes=max(size ** 2, 6))
        result = pool.map(calculate_element,
                          list(map(lambda x: (first_matrix, second_matrix, size, x), indexes)))
        write_log(first_matrix, second_matrix, result, size, LOG_FILE)
        sleep(1)


def main():
    stop_event = Event()
    size = int(input("Введите размер квадратной матрицы: "))
    element_range = [int(i) for i in
                     input("Введите минимальный и максимальный возможный элемент через пробел: ").split(" ")]
    print("Чтобы выйти, нажмите клавишу q")
    main_process = Process(target=loop, args=(size, element_range, stop_event))
    main_process.start()
    write_settings(size, element_range, LOG_FILE)
    while True:
        if keyboard.is_pressed(STOP):
            stop_event.set()
            break
    main_process.join()


if __name__ == '__main__':
    main()

import csv
import numpy as np
import time


def read_from_csv(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            matrix.append([int(element) for element in row])
    return matrix


def convert_to_edge_matrix(graph):
    nodes_count = len(graph)
    edge_matrix = np.full((nodes_count, nodes_count), np.inf, dtype=float)
    np.fill_diagonal(edge_matrix, 0)
    for i in range(nodes_count):
        for j in range(len(graph[i])):
            if j % 2 == 0:
                node = graph[i][j]
                weight = graph[i][j+1]
                element = edge_matrix[i, node - 1]
                if element != 0:
                    edge_matrix[i][node - 1] = weight

    return [[int(element) if element.is_integer() else element for element in row] for row in edge_matrix]


def floyd_warshall(T):
    n = T.shape[0]
    H = np.zeros_like(T, dtype=int)

    # Инициализация матрицы H
    for i in range(n):
        for j in range(n):
            if T[i, j] != 0 or not np.isinf(T[i, j]):
                H[i, j] = j + 1

    n = len(T[0])

    for n in range(n):
        mask = np.ones_like(T, dtype=bool)
        mask[n, :] = False
        mask[:, n] = False

        # Проверяем нулевые и бесконечные значения в строке и столбце
        zero_or_inf = np.where(np.logical_or(T[n] == 0, np.isinf(T[n])))
        if zero_or_inf[0].size > 0:
            mask[:, zero_or_inf] = False

        zero_or_inf = np.where(np.logical_or(T[:, n] == 0, np.isinf(T[:, n])))
        if zero_or_inf[0].size > 0:
            mask[zero_or_inf, :] = False

        i, j = np.where(mask)

        # Проверяем условие, при котором необходимо обновить значения матрицы T
        mask_condition = T[i, j] > T[n, j] + T[i, n]

        # Получаем отфильтрованные индексы i и j
        i_masked = i[mask_condition]
        j_masked = j[mask_condition]

        # Обновляем значения матрицы T и H
        T[i_masked, j_masked] = T[n, j_masked] + T[i_masked, n]
        H[i_masked, j_masked] = H[i_masked, n]
    return T, H


def path(T, i, j, H):
    ret = {'path': [], 'length': T[i-1, j-1]}
    current = i
    ret['path'].append(current)
    while current != j:
        current = H[current-1, j-1]
        ret['path'].append(current)
    return ret


if __name__ == '__main__':
    print('Введите начальную вершину: ')
    start_v = int(input())
    print('Введите конечную вершину: ')
    finish_v = int(input())
    startTime = time.time()
    file_path = 'result.csv'
    graph = read_from_csv(file_path)
    x = convert_to_edge_matrix(graph)
    x = np.array(x)

    T, H = floyd_warshall(x)
    path = path(T, start_v, finish_v, H)
    print("Кратчайший путь:")
    print(path)
    print(f"Completed in {time.time() - startTime} seconds.")
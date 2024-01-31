import random
import time
import csv


def generate_graph(num_vertices_left, num_vertices_right, max_weight):
    graph = []
    for i in range(num_vertices_left):
        for j in range(num_vertices_left, num_vertices_left + num_vertices_right):
            graph.append([i, j, random.randint(1, max_weight)])
    print(graph)
    return graph


def graph_to_file(graph, filename):
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        for row in graph:
            writer.writerow(row)


def bipartite_to_matrix(bipartite_graph, num_vertices_left, num_vertices_right):
    matrix = [[0] * num_vertices_right for _ in range(num_vertices_left)]
    for row in bipartite_graph:
        i, j, weight = row
        matrix[i][j - num_vertices_left] = weight
    print(matrix)
    return matrix


def write_matrix_to_csv(matrix, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        for row in matrix:
            writer.writerow(row)


start = time.time()

num_vertices_left = 2500
num_vertices_right = 4500
max_weight = 100

graph = generate_graph(num_vertices_left, num_vertices_right, max_weight)
graph_to_file(graph, "bipartite graph.txt")

matrix = bipartite_to_matrix(graph, num_vertices_left, num_vertices_right)
write_matrix_to_csv(matrix, "matrix.csv")

print(time.time()-start)
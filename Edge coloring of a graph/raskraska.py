import csv
import time
import math


def read_graph_from_csv(file_name):
    graph = {}
    colors = {}
    hrom_index = 0

    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';', skipinitialspace=True)
        counter = 1
        for row in csv_reader:
            temp_graph = []
            for value in row:
                temp_graph.append(int(value))
            graph[counter] = temp_graph
            colors[counter] = []
            len_temp_graph = len(temp_graph)

            if len_temp_graph > hrom_index:
                hrom_index = len_temp_graph

            counter += 1

    return graph, colors, hrom_index


def initialize_matrix(len_graph, hrom_index):
    matrix_graph = []
    for _ in range(len_graph + 1):
        row = []
        for _ in range(len_graph + 1):
            row.append(math.inf)
        matrix_graph.append(row)

    color = []
    for i in range(1, hrom_index + 1):
        color.append(i)

    return matrix_graph, color


def color_edges(graph, colors, matrix_graph):
    max_color = 0
    # print('Изначальный граф:')
    # print(graph)

    edges = set()
    for vertex in graph:
        for neighbor in graph[vertex]:
            if (vertex, neighbor) not in edges and (neighbor, vertex) not in edges:
                edges.add((vertex, neighbor))


    for vertex, vertex_n in edges:
        if matrix_graph[vertex][vertex_n] == math.inf:
            available_colors = set(range(1, len(graph) + 1)) - set(colors[vertex]) - set(colors[vertex_n])
            if available_colors:
                selected_color = min(available_colors)
            matrix_graph[vertex][vertex_n] = selected_color
            matrix_graph[vertex_n][vertex] = selected_color
            if max_color < selected_color:
                max_color = selected_color - 1
            colors[vertex].append(selected_color)
            colors[vertex_n].append(selected_color)
            colors[vertex].sort()
            colors[vertex_n].sort()
            print(f"Ребро {vertex}-{vertex_n}: Цвет {selected_color}")

    return max_color


if __name__ == '__main__':
    start = time.time()
    graph, colors, hrom_index = read_graph_from_csv('output_graph.csv')
    matrix_graph, color = initialize_matrix(len(graph), hrom_index)
    max_color = color_edges(graph, colors, matrix_graph)
    stop = time.time()

    # print(colors)
    print('Максимальный цвет:', max_color)
    print('Индекс хроматичности:', hrom_index)
    print('Время выполнения:', stop - start)



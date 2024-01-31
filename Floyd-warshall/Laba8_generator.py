import random
import networkx as nx
import matplotlib.pyplot as plt
import configparser
import csv
import time
import numpy as np

config = configparser.ConfigParser()
config.read('config.ini')


nodes_count = config.getint('parameters', 'nodes_count')
max_edges = config.getint('parameters', 'max_edges')
max_capacity = config.getint('parameters', 'max_capacity')
filename = config.get('parameters', 'filename')


# def oriented_weight_graph(nodes_count, max_edges, max_capacity):
#     nodes = list(range(1, nodes_count + 1))
#     result = []
#     for i in range(nodes_count):
#         # Определяем максимальное количество исходящих ребер для текущей вершины
#         max_edges_for_node = min(max_edges, len(nodes) - 1)
#         # Выбираем случайный набор вершин для исходящих ребер
#         available_nodes = nodes[:i] + nodes[i + 1:]
#         edges_count = min(max_edges_for_node, len(available_nodes))
#         edges = random.sample(available_nodes, edges_count)
#         # Создаем список ребер для текущей вершины
#         node_edges = [(v, random.randint(1, max_capacity)) for v in edges]
#         # Добавляем список ребер текущей вершины в результат
#         result.append(node_edges)
#     return result
def esli_pusto(result):
    nodes = [i for i in range(1, nodes_count + 1)]
    random_edge = random.choice(nodes)
    count_random_edge = 0
    for i in range(len(result)):
        for j in range(0, len(result[i]), 2):
            if result[i][j] == []:
                break
            elif result[i][j] == random_edge:
                count_random_edge += 1
        if count_random_edge == max_edges:
            nodes.remove(random_edge)
            return number_of_occurrences(result, nodes)
    return random_edge


def number_of_occurrences(result, nodes):
    random_edge = random.choice(nodes)
    count_random_edge = 0
    for i in range(len(result)):
        for j in range(0, len(result[i]), 2):
            if result[i][j] == []:
                break
            elif result[i][j] == random_edge:
                count_random_edge += 1
        if count_random_edge == max_edges:
            nodes.remove(random_edge)
            return number_of_occurrences(result, nodes)
    return random_edge


def oriented_weight_graph(nodes_count, max_edges, max_capacity):
    result = [[] for _ in range(nodes_count)]
    count = 0
    while count < nodes_count:
        nodes = [i for i in range(1, nodes_count + 1)]
        current_node = nodes[count]
        nodes.remove(current_node)
        edges_count = random.randint(1, max_edges)
        edges = []
        while len(edges) < edges_count + edges_count:
            random_edgik = number_of_occurrences(result, nodes)
            random_ves = random.randint(1, max_capacity)
            if random_edgik not in edges and current_node not in result[random_edgik-1]:
                edges.append(random_edgik)
                edges.append(random_ves)
            nodes.remove(random_edgik)
        result[count] = edges
        count += 1
    for i in range(len(result)):
        if result[i] == []:
            result[i].append(esli_pusto(result))
            result[i].append(random.randint(1, max_capacity))
    return result

def draw_graph(graph_edges):
    G = nx.DiGraph()
    for i in range(1, len(graph_edges) + 1):
        G.add_node(i)
    for i in range(len(graph_edges)):
        for j in range(0, len(graph_edges[i]), 2):
            if graph_edges[i][j] != []:
                G.add_edge(i+1, graph_edges[i][j], weight=graph_edges[i][j+1])
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()


def flatten_list(lst):
    return [[elem for tpl in inner_lst for elem in tpl] for inner_lst in lst]


# def convert_to_edge_matrix(graph):
#     nodes_count = len(graph)
#     edge_matrix = np.full((nodes_count, nodes_count), np.inf, dtype=float)
#     np.fill_diagonal(edge_matrix, 0)
#     for i in range(nodes_count):
#         for j in range(len(graph[i])):
#             if j % 2 == 0:
#                 node = graph[i][j]
#                 weight = graph[i][j+1]
#                 element = edge_matrix[i, node - 1]
#                 if element != 0:
#                     edge_matrix[i][node - 1] = weight
#
#     return [[int(element) if element.is_integer() else element for element in row] for row in edge_matrix]


def write_matrix_to_csv(matrix, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for row in matrix:
            writer.writerow(row)


def printfile(file, res):
    outfile = open('{}.csv'.format(file), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    for line in res:
        writer.writerow(line)
    outfile.close()

startTime = time.time()
graph_edges = oriented_weight_graph(nodes_count, max_edges, max_capacity)
# x = flatten_list(graph_edges)
# edge_matrix = convert_to_edge_matrix(graph_edges)


# Запись матрицы в CSV файл
write_matrix_to_csv(graph_edges, "result.csv")
print(graph_edges)
# print(x)
print(f"Completed in {time.time() - startTime} seconds.")
printfile(filename, graph_edges)
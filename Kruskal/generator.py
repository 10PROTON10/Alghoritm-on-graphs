import csv
import random
import configparser
#import sys
#import threading
import time
import networkx as nx
import matplotlib.pyplot as plt


#sys.setrecursionlimit(1000000000)
#threading.stack_size(200000000)


startTime = time.time()
config = configparser.ConfigParser()
config.read("config_kruskal.ini")
filename = config.get('parameters', 'filename')
nodes_count = config.getint('parameters', 'nodes_count')
max_edges = config.getint('parameters', 'max_edges')
max_weight = config.getint('parameters', 'max_weight')
start_node = config.getint('parameters', 'start_node')


def bfs(graph, start_node):
    visited = []
    queue = [start_node]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
            neighbors = graph[node - 1][::2]
            queue += neighbors
    return visited


def not_oriented_weighted_graph(nodes_count, max_edges, max_weight):
    result = [[] for _ in range(nodes_count)]
    graph_connected = False
    while not graph_connected:
        for i in range(1, nodes_count + 1):
            nodes = [j for j in range(1, nodes_count + 1) if j != i]
            edges_count = random.randint(1, max_edges)
            # Удаление уже существующих связей из списка доступных вершин
            for j in result[i - 1]:
                if j in nodes:
                    nodes.remove(j)
            # Проверка на то, что количество связей для выбранной вершины меньше максимального
            while len(result[i - 1]) < edges_count:
                if nodes == []:
                    break
                random_edge = random.choice(nodes)
                random_ves = random.randint(1, max_weight)
                if len(result[random_edge - 1]) < max_edges:
                    result[i - 1].append(random_edge)
                    result[i - 1].append(random_ves)
                    result[random_edge - 1].append(i)
                    result[random_edge - 1].append(random_ves)
                nodes.remove(random_edge)

        start_node = random.randint(1, nodes_count)
        visited = bfs(result, start_node)
        if len(visited) == nodes_count:
            graph_connected = True
        else:
            result = [[] for _ in range(nodes_count)]

    return result


def draw_graph(graph):
    G = nx.Graph()
    for i in range(len(graph)):
        for j in range(0, len(graph[i]), 2):
            G.add_edge(i+1, graph[i][j], weight=graph[i][j+1])
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_nodes(G, pos, node_color='b', node_size=500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.axis('off')
    plt.show()


def printfile(file, res):
    outfile = open('{}.csv'.format(file), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    for line in res:
        writer.writerow(line)
    outfile.close()


graph = not_oriented_weighted_graph(nodes_count, max_edges, max_weight)
print(graph)
draw_graph(graph)
print(f"Completed in {time.time() - startTime} seconds.")
printfile(filename, graph)

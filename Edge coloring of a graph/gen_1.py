import csv
import random
import configparser
import time
import networkx as nx
import matplotlib.pyplot as plt

startTime = time.time()
config = configparser.ConfigParser()
config.read("config.ini")
filename = config.get('parameters', 'filename')
nodes_count = config.getint('parameters', 'nodes_count')
max_edges = config.getint('parameters', 'max_edges')

def not_oriented_graph(nodes_count, max_edges):
    result = [[] for _ in range(nodes_count)]
    for i in range(1, nodes_count + 1):
        nodes = [i for i in range(1, nodes_count + 1)]
        nodes.remove(i)
        edges_count = random.randint(1, max_edges)
        # Удаление уже существующих связей из списка доступных вершин
        for j in result[i - 1]:
            if j in nodes:
                nodes.remove(j)
        # Проверка на то, что количество связей для выбранной вершины меньше максимального
        while len(result[i - 1]) < edges_count:
            random_edge = random.choice(nodes)
            if len(result[random_edge - 1]) < max_edges:
                result[i - 1].append(random_edge)
                result[random_edge - 1].append(i)
            nodes.remove(random_edge)
    return result

def draw_graph(graph):
    G = nx.Graph()
    for i in range(1, len(graph)+1):
        for j in range(len(graph[i-1])):
            G.add_edge(i, graph[i-1][j])
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='b', node_size=500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos)
    plt.axis('off')
    plt.show()

def printfile(file, res):
    outfile = open('{}.csv'.format(file), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    for i in range(1, len(res)+1):
        writer.writerow(res[i-1])
    outfile.close()

graph = not_oriented_graph(nodes_count, max_edges)
print(graph)
print(f"Completed in {time.time() - startTime} seconds.")
# draw_graph(graph)
printfile(filename, graph)

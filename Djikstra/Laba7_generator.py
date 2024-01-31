import random
import networkx as nx
import matplotlib.pyplot as plt
import configparser
import csv
import time


config = configparser.ConfigParser()
config.read('config.ini')


nodes_count = config.getint('parameters', 'nodes_count')
max_edges = config.getint('parameters', 'max_edges')
max_capacity = config.getint('parameters', 'max_capacity')
filename = config.get('parameters', 'filename')


def oriented_weight_graph(nodes_count, max_edges, max_capacity):
    nodes = list(range(1, nodes_count + 1))
    result = []
    for i in range(nodes_count):
        # Определяем максимальное количество исходящих ребер для текущей вершины
        max_edges_for_node = min(max_edges, len(nodes) - 1)
        # Выбираем случайный набор вершин для исходящих ребер
        available_nodes = nodes[:i] + nodes[i + 1:]
        edges_count = min(max_edges_for_node, len(available_nodes))
        edges = random.sample(available_nodes, edges_count)
        # Создаем список ребер для текущей вершины
        node_edges = [(v, random.randint(1, max_capacity)) for v in edges]
        # Добавляем список ребер текущей вершины в результат
        result.append(node_edges)
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


def printfile(file, res):
    outfile = open('{}.csv'.format(file), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    for line in res:
        writer.writerow(line)
    outfile.close()

startTime = time.time()
graph_edges = oriented_weight_graph(nodes_count, max_edges, max_capacity)
x = flatten_list(graph_edges)
print(graph_edges)
print(x)
print(f"Completed in {time.time() - startTime} seconds.")
printfile(filename, x)
# draw_graph(x)
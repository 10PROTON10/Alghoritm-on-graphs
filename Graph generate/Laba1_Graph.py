import random
import csv
import matplotlib.pyplot as plt
import networkx as nx
import configparser
import time


startTime = time.time()


def oriented_graph(nodes_count, max_edges):
    result = [[] for _ in range(nodes_count)]
    count = 0
    while count < nodes_count:
        nodes = [i for i in range(1, nodes_count + 1)]
        current_node = nodes[count]
        nodes.remove(current_node)
        edges_count = random.randint(1, max_edges)
        edges = []
        while len(edges) < edges_count:
            random_edge = random.choice(nodes)
            edges.append(random_edge)
            nodes.remove(random_edge)
        result[count] = edges
        count += 1
    return result


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


def draw_graph(res, oriented=False):
    if oriented == True:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    edges = []
    for i in range(len(res)):
        for j in res[i]:
            edges.append((i + 1, j))
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()


def printfile(file, res):
    outfile = open('{}.csv'.format(file), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    for line in res:
        writer.writerow(line)
    outfile.close()


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    oriented = config.getboolean('parameters', 'oriented')
    nodes_count = config.getint('parameters', 'nodes_count')
    max_edges = config.getint('parameters', 'max_edges')
    filename = config.get('parameters', 'filename')

    if oriented:
        graph = oriented_graph(nodes_count, max_edges)
        print(graph)
        printfile(filename, graph)
        # draw_graph(graph, oriented=True)
    else:
        graph = not_oriented_graph(nodes_count, max_edges)
        print(graph)
        printfile(filename, graph)
        draw_graph(graph)

    print(f"Completed in {time.time() - startTime} seconds.")


main()
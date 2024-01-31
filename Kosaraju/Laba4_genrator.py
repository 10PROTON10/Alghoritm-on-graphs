import random
import csv
import matplotlib.pyplot as plt
import networkx as nx
import configparser
import time


startTime = time.time()


def esli_pusto(result):
    nodes = [i for i in range(1, nodes_count + 1)]
    random_edge = random.choice(nodes)
    count_random_edge = 0
    for i in range(len(result)):
        for j in range(len(result[i])):
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
        for j in range(len(result[i])):
            if result[i][j] == []:
                break
            elif result[i][j] == random_edge:
                count_random_edge += 1
        if count_random_edge == max_edges:
            nodes.remove(random_edge)
            return number_of_occurrences(result, nodes)
    return random_edge


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
            random_edgik = number_of_occurrences(result, nodes)
            if random_edgik not in edges and current_node not in result[random_edgik-1]:
                edges.append(random_edgik)
            nodes.remove(random_edgik)
        result[count] = edges
        count += 1
    for i in range(len(result)):
        if result[i] == []:
            result[i].append(esli_pusto(result))
    return result


def draw_graph(res):
    G = nx.DiGraph()
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


config = configparser.ConfigParser()
config.read('config.ini')


nodes_count = config.getint('parameters', 'nodes_count')
max_edges = config.getint('parameters', 'max_edges')
filename = config.get('parameters', 'filename')


graph = oriented_graph(nodes_count, max_edges)
# draw_graph(graph)
print(graph)
printfile(filename, graph)

print(f"Completed in {time.time() - startTime} seconds.")


import random
import networkx as nx
import matplotlib.pyplot as plt
import configparser
import csv


config = configparser.ConfigParser()
config.read('config.ini')


nodes_count = config.getint('parameters', 'nodes_count')
max_edges = config.getint('parameters', 'max_edges')
max_capacity = config.getint('parameters', 'max_capacity')
filename = config.get('parameters', 'filename')


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


def oriented_graph(nodes_count, max_edges, max_capacity):
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


def printfile(file, res):
    outfile = open('{}.csv'.format(file), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    for line in res:
        writer.writerow(line)
    outfile.close()


graph_edges = oriented_graph(nodes_count, max_edges, max_capacity)
print(graph_edges)
printfile(filename, graph_edges)
draw_graph(graph_edges)

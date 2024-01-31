import csv
import configparser
import time
import sys

sys.setrecursionlimit(10 ** 6)
startTime = time.time()
config = configparser.ConfigParser()
config.read("config2.ini")
start_node = config.getint('parameters', 'start_search')
filename = config.get('parameters', 'filename')


with open('output_graph.csv') as f:
    reader = csv.reader(f)
    graph = []
    for row in reader:
        for i in row:
            graph.append(list(map(int, i.split(';'))))
print(graph)


# graph = [[4],[1],[2],[3,5,6],[6],[7],[5]]

def dfs(graph, start_node, visited, stack, path, cycles):
    if start_node > len(visited):
        visited += [False] * (start_node - len(visited))
    visited[start_node-1] = True
    path.append(start_node)
    for neighbor in graph[start_node-1]:
        if neighbor > len(visited):
            visited += [False] * (neighbor - len(visited))
        if neighbor in path:
            cycle = path[path.index(neighbor):]
            cycles.append(cycle)
        if not visited[neighbor-1]:
            dfs(graph, neighbor, visited, stack, path, cycles)
    path.pop()
    stack.append(start_node)


def reverse_graph(graph):
    n = len(graph)
    reversed_graph = [[] for _ in range(n)]
    for i in range(n):
        for j in graph[i]:
            reversed_graph[j-1].append(i+1)
    return reversed_graph


def kosaraju_algorithm(graph):
    n = len(graph)
    visited = [False] * n
    stack = []
    cycles = []
    path = []
    for i in range(n):
        if not visited[i]:
            dfs(graph, i+1, visited, stack, path, cycles)
    reversed_graph = reverse_graph(graph)
    visited = [False] * n
    scc = []
    while stack:
        node = stack.pop()
        if not visited[node-1]:
            component = []
            dfs(reversed_graph, node, visited, component, [], cycles)
            scc.append(component)
    return scc, cycles


def printfile(file, res):
    outfile = open('{}.csv'.format(file), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    for line in res:
        writer.writerow(line)
    outfile.close()


scc, cycles = kosaraju_algorithm(graph)
scc.sort(key=lambda x: len(x), reverse=True)
printfile(filename, scc)
print("Циклы:")
print(cycles)
print("Компоненты сильной связности:")
print(scc)


endTime = time.time()
print("Execution time: ", endTime-startTime)

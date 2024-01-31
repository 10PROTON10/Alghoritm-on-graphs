import csv
import configparser
import time
from collections import deque


startTime = time.time()
config = configparser.ConfigParser()
config.read('config_dinica_csv.ini')

filename = config.get('parameters', 'filename')


with open('output_graph.csv') as f:
    reader = csv.reader(f)
    graph = []
    for row in reader:
        for i in row:
            if i:
                graph.append(list(i.split(';')))

for row in graph:
    for i in range(len(row)):
        try:
            row[i] = int(row[i])
        except ValueError:
            row[i] = 0

result = []
for j in range(len(graph)):
    for i in range(0, len(graph[j])-1, 2):
        if i+1 < len(graph[j]):
            node2 = graph[j][i]
            weight = graph[j][i+1]
            result.append((j+1, node2, weight))
print('Рёбра графа: ')
print(result)


# функция поиска кратчайшего увеличивающего пути методом BFS
def bfs(graph, s, t):
    queue = deque([s])
    dist = {s: 0}  # расстояние от источника до вершины
    blocking_flow = {s: float('inf')}  # блокирующий поток
    path = {s: []}

    while queue:
        u = queue.popleft()
        for v, capacity in graph[u].items(): # проход по соседним вершинам
            if v not in dist and capacity > 0:
                dist[v] = dist[u] + 1 # обновление расстояния от источника до вершины
                blocking_flow[v] = min(blocking_flow[u], capacity) # обновление блокирующего потока для вершины
                path[v] = path[u] + [(u, v)] # обновление пути от источника до вершины
                queue.append(v)

    if t not in dist:
        return None, None
    else:
        return path[t], blocking_flow[t] # возвращаем путь от источника до стока и блокирующий поток на этом пути


def dinic(graph, s, t):
    flow = 0
    paths = []
    # пока существует путь из источника в сток
    while True:
        # поиск кратчайшего увеличивающего пути методом BFS
        path, blocking_flow = bfs(graph, s, t)
        if path is None:
            break

        flow += blocking_flow
        u = t # обновляем веса ребер на найденном пути и на обратных ребрах
        while u != s:
            for edge in path:
                graph[edge[0]][edge[1]] -= blocking_flow # уменьшаем пропускную способность на прямом ребре
                graph[edge[1]][edge[0]] += blocking_flow # увеличиваем пропускную способность на обратном ребре
            u = path[0][0]
        paths.append((path, blocking_flow))
        print("Путь: ", path, '=', blocking_flow)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for path, blocking_flow in paths:
            writer.writerow([path, blocking_flow])

    return flow


graph = {}
for u, v, capacity in result:
    if u not in graph:
        graph[u] = {}
    if v not in graph:
        graph[v] = {}
    graph[u][v] = capacity # Добавляем ребро от u к v с пропускной способностью capacity
    graph[v][u] = 0 # Добавляем обратное ребро от v к u со значением пропускной способности равным нулю
s = 1
t = max(graph.keys()) - 1
max_flow = dinic(graph, s, t)

print("Сумма значений максимального потока: ", max_flow)
print(f"Completed in {time.time() - startTime} seconds.")

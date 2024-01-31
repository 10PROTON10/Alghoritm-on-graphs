import csv
import configparser
import time
import heapq


def dijkstra(G, start, end):
    n = len(G)
    distance = {i+1: float('inf') for i in range(1, n + 1)}  # словарь кратчайших расстояний от начальной вершины
    distance[start] = 0  # расстояние от начальной вершины до самой себя
    heap = [(0, start)]  # куча для хранения вершин
    previous = {}

    while heap:
        cost, u = heapq.heappop(heap)  # извлекаем вершину с наименьшим расстоянием
        if u == end:
            break
        for v, weight in zip(G[u - 1][::2], G[u - 1][1::2]):
            if v not in distance or cost + weight < distance[v]: # Если новый путь короче предыдущего, то обновляем кратчайшее расстояние
                distance[v] = cost + weight
                heapq.heappush(heap, (distance[v], v)) # добавляем соседа в кучу
                previous[v] = u

    if end not in previous: # Если конечная вершина не имеет предыдущей вершины
        return "Граф содержит отрицательный цикл"

    sum = distance[end]
    path = []  # кратчайший путь
    current = end
    while current != start:  # пока не дойдем до начальной вершины
        for i in range(n):  # перебираем все вершины графа
            for j in range(1, len(G[i]), 2):  # перебираем всех соседей текущей вершины
                if G[i][j-1] == current and distance[i+1] + G[i][j] == distance[current]:  # если найден путь до текущей вершины, то добавляем ее в путь и переходим к предыдущей вершине
                    path.append(current)
                    current = previous[current]
                    break
    path.append(start)
    path.reverse()
    return (sum, path)


if __name__ == '__main__':
    startTime = time.time()
    config = configparser.ConfigParser()
    config.read('config.ini')

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
    G = graph
    start_vertex = 1
    end_vertex = len(graph)
    result = dijkstra(G, start_vertex, end_vertex)
    print("Кратчайший путь из вершины", start_vertex, "в вершину", end_vertex, ":", result[1])
    print("Суммарный вес кратчайшего пути:", result[0])
    print(f"Completed in {time.time() - startTime} seconds.")
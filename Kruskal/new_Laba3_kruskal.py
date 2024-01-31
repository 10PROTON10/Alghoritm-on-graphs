import csv
import configparser
import time
import itertools


startTime = time.time()
config = configparser.ConfigParser()
config.read('config_kruskal_csv.ini')

nodes_count = config.getint('parameters', 'nodes_count')
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


def kruskal(graph, nodes_count):
    graph.sort(key=lambda x: x[2])
    parents = [i for i in range(nodes_count)]
    si = [1] * nodes_count
    result = [[] for _ in range(nodes_count)]
    for u, v, weight in graph:
        u -= 1  # уменьшаем на 1, чтобы обходить с 1 вершины
        v -= 1
        root_u = u
        while root_u != parents[root_u]:
            root_u = parents[root_u]
        root_v = v
        while root_v != parents[root_v]:
            root_v = parents[root_v]
        if root_u != root_v:
            if si[root_u] < si[root_v]:
                root_u, root_v = root_v, root_u
            parents[root_v] = root_u
            si[root_u] += si[root_v]
            result[u].append((v+1, weight))
            result[v].append((u+1, weight))

    return result


massiv = kruskal(result, nodes_count)

otvet = []
node1 = 1
for i, sub_arr in enumerate(massiv):
    for elem in sub_arr:
        otvet.append((i+1,) + elem)

summa = 0
new_otvet = []
for i in otvet:
    if (i[0], i[1]) not in [(x[1], x[0]) for x in new_otvet]:
        new_otvet.append(i)
summa = 0
for i in range (len(new_otvet)):
    summa += otvet[i][2]

data = sorted(otvet, key=lambda x: x[0])

with open('output_graphik.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for key, group in itertools.groupby(data, key=lambda x: x[0]):
        row = [key] + [x[1:] for x in group]
        writer.writerow(row)

# summa = 0
# for i in range (len(otvet)):
#     summa += otvet[i][2]


# with open("output_graph.csv", "w", newline="") as f:
#     write = csv.writer(f)
#     for i in range(len(new_otvet)):
#         x = new_otvet[i][0]
#         y = new_otvet[i][1]
#         weight = new_otvet[i][2]
#         for x, y, weight in new_otvet[i]:
#             row.append(str(x) + "," + str(y) + "," + str(weight))
#         write.writerow(row)
print(otvet)
print(summa)
print(f"Completed in {time.time() - startTime} seconds.")
# print("Время выполнения: ", end-start, "с")

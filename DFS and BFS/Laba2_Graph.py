import csv
import configparser
import time

startTime = time.time()
config = configparser.ConfigParser()
config.read("config2.ini")
file = config["traversal"]['filename']
start_node = int(config["traversal"]['start_search'])
choosing_a_graph_traversal = int(config["traversal"]['choosing_a_graph_traversal'])


with open('output_graph.csv') as f:
    reader=csv.reader(f)
    graph = []
    for row in reader:
        for i in row:
            graph.append(list(map(int, i.split(';'))))


def bfs(graph, start_node):
    graphy = graph
    visited = [start_node]
    queue = graphy[start_node - 1]
    while len(visited) < len(graphy):
        first_element = queue[0]
        if first_element not in visited:
            visited.append(first_element)
            queue.remove(first_element)
            for i in range(len(graphy[first_element - 1])):
                if graphy[first_element - 1][i] not in visited and graphy[first_element - 1][i] not in queue:
                    queue.append(graphy[first_element - 1][i])
        else:
            queue.remove(first_element)

        if queue == [] and len(visited) < len(all_nodes):
            for i in range(1, len(all_nodes) + 1):
                if len(queue) < 1 and all_nodes[i] not in visited:
                    queue.append(all_nodes[i])
                    break

    return visited


def dfs(graph, start_node):
    graphx = graph
    visited = [start_node]
    stack = graphx[start_node - 1]
    while len(visited) < len(graphx):
        last_element = stack[-1]
        if last_element not in visited:
            visited.append(last_element)
            stack.remove(last_element)
            for i in range(len(graphx[last_element - 1])):
                if graphx[last_element - 1][i] not in visited and graphx[last_element - 1][i] not in stack:
                    stack.append(graphx[last_element - 1][i])
        else:
            stack.remove(last_element)

        if stack == [] and len(visited) < len(all_nodes):
            for i in range(1, len(all_nodes) + 1):
                if len(stack) < 1 and all_nodes[i] not in visited:
                    stack.append(all_nodes[i])
                    break

    return visited

all_nodes = list(range(1, len(graph) + 1))
print(all_nodes)

if choosing_a_graph_traversal == 1:
    print('Обход графа в ширину', bfs(graph, start_node))
elif choosing_a_graph_traversal == 2:
    print('Обход графа в глубину: ', dfs(graph, start_node))
print(f"Completed in {time.time() - startTime} seconds.")




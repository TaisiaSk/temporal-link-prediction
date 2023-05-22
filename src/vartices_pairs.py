from collections import deque
from graph import Graph
from logger import Logger
import basic_properties as bp
import os
import random

def find_double_neighbors(graph : Graph, src : int, filter : int, logger : Logger, 
                          found_0 : int = 0, found_1 : int = 0, max_amount : int = 10000) -> tuple:
    
    visited = [False for _ in range(graph.number_of_vertices())]
    prev = [-1 for _ in range(graph.number_of_vertices())]
    
    queue = deque()  
    queue.append(src)
    visited[src] = True

    while (queue):
        current = queue.popleft()
        for child in graph.adj(current, timestamp_filter=filter):
            if not (visited[child]):
                visited[child] = True
                prev[child] = current
                queue.append(child)

            parent = prev[current]
            if (parent == -1) or (logger.contains(parent, child)):
                continue
           
            if (graph.has_edges_between(parent, child)):
                if (found_1 >= max_amount):
                    continue
                logger.log(parent, child, [1])
                found_1 += 1
            else:
                if (found_0 >= max_amount):
                    continue
                logger.log(parent, child, [0])
                found_0 += 1
    
    return found_0, found_1    


def find_pairs(graph : Graph, filter : int, logger : Logger) -> None:
    logs = logger.get_logs()
    found_0 = len([key for key, value in logs.items() if value[0] == 0])
    found_1 = len([key for key, value in logs.items() if value[0] == 1])
    max_amount = 10000

    for _ in range(500):
        found_0, found_1 = find_double_neighbors(graph, random.randint(1, graph.number_of_vertices() - 1), 
                                                 filter, logger, found_0, found_1)
        print(found_0, found_1)
        if (found_0 >= max_amount) and (found_1 >= max_amount):
            return
    

datasets = [{'file_name' : 'email.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 1, 'filter' : 69}, 
            {'file_name' : 'bitcoinotc.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 1, 'filter' : 52}, 
            {'file_name' : 'bitcoinalpha.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 1, 'filter' : 47}, 
            {'file_name' : 'ucsocial.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 2, 'filter' : 23}]


for current_dataset in datasets: 
    logger = Logger(logs_file_name=current_dataset['file_name'] + '.json')
    file_path = '../data/' + current_dataset['file_name']
    timestamp_col = current_dataset['timestamp_col']
    number_of_lines_to_skip = current_dataset['number_of_lines_to_skip']
    filter = current_dataset['filter']

    g = Graph(file_path, timestamp_col, number_of_lines_to_skip)
    find_pairs(g, filter, logger)
    logger.dump()



    



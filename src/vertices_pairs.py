from collections import deque
from graph import Graph
from logger import Logger
from main import datasets
import random

def find_double_neighbors(graph_full : Graph, graph_cut : Graph, src : int, logger : Logger, 
                          found_0 : int = 0, found_1 : int = 0, max_amount : int = 10000) -> tuple:
    
    visited = [False for _ in range(graph_full.number_of_vertices())]
    prev = [-1 for _ in range(graph_full.number_of_vertices())]
    
    queue = deque()  
    queue.append(src)
    visited[src] = True

    while (queue):
        current = queue.popleft()

        for child in graph_cut.adj(current):
            if not (visited[child]):
                visited[child] = True
                prev[child] = current
                queue.append(child)

            parent = prev[current]
            if (parent == -1) or (parent == child):
                continue
            if (logger.contains(parent, child)) or (graph_cut.has_edges_between(child, parent)):
                continue
           
            if (graph_full.has_edges_between(parent, child)):
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


def find_pairs(graph_full : Graph, graph_cut : Graph, logger : Logger) -> None:
    logs = logger.get_pairs()
    found_0 = len([pair for pair in logs if pair[2] == 0])
    found_1 = len([pair for pair in logs if pair[2] == 1])
    max_amount = 10000

    for _ in range(1000):
        src = random.randint(1, graph_full.number_of_vertices() - 1)
        found_0, found_1 = find_double_neighbors(graph_full, graph_cut, src, logger, found_0, found_1)
        print(found_0, found_1)
        if (found_0 >= max_amount) and (found_1 >= max_amount):
            return
    
    logger.dump()

def add_pairs_wich_will_appear(graph_cut : Graph, logger : Logger, filter : int) -> None:
    dct = dict()
    for edge in graph_cut.edges_that_will_appear(filter):
        v1 = edge[0]
        v2 = edge[1]
        if graph_cut.has_edges_between(v1, v2):
            continue

        v1_neighbors = graph_cut.adj(v1)
        v2_neighbors = graph_cut.adj(v2)

        if len(v1_neighbors.intersection(v2_neighbors)) > 0:
            if (logger.contains(v1, v2)):
                key = f'{min(v1, v2)}-{max(v1, v2)}'
                if (key not in dct):
                    dct[key] = 0
                dct[key] += 1

            if (not logger.contains(v1, v2)):
                print(v1, v2)
                logger.log(v1, v2, [1])

    logger.dump()


def check(graph_full : Graph, graph_cut : Graph, logger : Logger) -> None:
    pairs = logger.get_pairs()
    for pair in pairs:
        v1 = pair[0]
        v2 = pair[1]
        appearance = pair[2]

        if (graph_cut.has_edges_between(v1, v2)):
            print('Has edge between:', v1, v2, appearance)
        if (appearance == 0) and (graph_full.has_edges_between(v1, v2)):
            print('Edge will appear:', v1, v2, appearance)
        if (appearance == 1) and not (graph_full.has_edges_between(v1, v2)):
            print('Edge will not appear:', v1, v2, appearance)


def count_appearance(logger : Logger) -> list:
    pairs = logger.get_pairs()
    cnt = [0, 0]
    for pair in pairs:
        appearance = pair[2]
        cnt[appearance] += 1

    return cnt


# current_dataset = datasets[0]
# logger = Logger(dir='../pairs/', logs_file_name=current_dataset['file_name'] + '.json', saving_step=100, dump_before_del=False)

# file_path = '../data/' + current_dataset['file_name']
# timestamp_col = current_dataset['timestamp_col']
# number_of_lines_to_skip = current_dataset['number_of_lines_to_skip']
# filter = current_dataset['filter']

# graph_full = Graph(file_path, timestamp_col, number_of_lines_to_skip)
# graph_cut = Graph(file_path, timestamp_col, number_of_lines_to_skip, filter)

# print(graph_cut.cut_proportion(), len(graph_full.edges_that_will_appear(filter)))

# find_pairs(graph_full, graph_cut, logger)
# add_pairs_wich_will_appear(graph_cut, logger, filter)
# check(graph_full, graph_cut, logger)
# print(count_appearance(logger))

   
        
   



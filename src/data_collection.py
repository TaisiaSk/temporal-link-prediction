import numpy as np
import random
from logger import Logger
from graph import Graph
from collections import deque
from temporal_features import get_temporal_features as get_temporal
from static_features import get_static_properties as get_static

##########################################################__FEATURES__##########################################################

def get_features_as_matrix(dataset : dict, static : bool) -> tuple:
    subdir = 'static/' if (static) else 'temporal/'
    features_logger = Logger(dir='../features/' + subdir, logs_file_name=dataset['file_name'] + '.json', safe_mode=True)
    if (features_logger.is_empty()):
        return None

    features = features_logger.get_features()

    vector = []
    matrix = []
    for feature in features:
        vector.append(feature[0])
        feature.pop(0)
        matrix.append(feature)

    return np.array(vector), np.nan_to_num(np.array(matrix), posinf=0, neginf=0)


def collect_features_into_files(dataset : dict, static : bool):

    graph = Graph(file_path = '../data/' + dataset['file_name'], 
                  timestamp_col = dataset['timestamp_col'], 
                  number_of_lines_to_skip = dataset['number_of_lines_to_skip'],  
                  timestamp_filter = 100 if (static) else dataset['filter'])
    features_logger = Logger(dir = '../features/' + ('static/' if (static) else 'temporal/'), 
                             logs_file_name = dataset['file_name'] + '.json', 
                             saving_step = 1000)
    pairs_logger = Logger(dir = '../pairs/', 
                          logs_file_name = dataset['file_name'] + '.json', 
                          safe_mode = True)

    pairs_list = pairs_logger.get_pairs()
    max_amount = min(len([pair for pair in pairs_list if pair[2] == 0]), 
                     len([pair for pair in pairs_list if pair[2] == 1]))

    features_list = features_logger.get_features()
    features_counter = [len([feature for feature in features_list if feature[0] == 0]), 
                        len([feature for feature in features_list if feature[0] == 1])]

    for pair in pairs_list:
        v1 = pair[0]
        v2 = pair[1]
        appearance = pair[2]

        if (features_counter[appearance] == max_amount) or (features_logger.contains(v1, v2)):
            continue

        print(v1, v2, features_counter)
        features = [appearance] + (get_static(v1, v2, graph) if (static) else get_temporal(v1, v2, graph).tolist()) 
     
        features_logger.log(v1, v2, features)
        features_counter[appearance] += 1

    features_logger.dump()

##########################################################__PAIRS__##########################################################

def collect_pairs_into_files(dataset : dict):
    logger = Logger(dir='../pairs/', logs_file_name=dataset['file_name'] + '.json', saving_step=100)

    file_path = '../data/' + dataset['file_name']
    timestamp_col = dataset['timestamp_col']
    number_of_lines_to_skip = dataset['number_of_lines_to_skip']
    filter = dataset['filter']

    graph_full = Graph(file_path, timestamp_col, number_of_lines_to_skip)
    graph_cut = Graph(file_path, timestamp_col, number_of_lines_to_skip, filter)

    __approximate_pairs_collection(graph_full, graph_cut, logger)
    __add_pairs_wich_will_appear(graph_cut, logger, filter)
    __check_correctness(graph_full, graph_cut, logger)
    print(__count_appearance(logger))

def __check_correctness(graph_full : Graph, graph_cut : Graph, logger : Logger) -> None:
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

def __count_appearance(logger : Logger) -> list:
    pairs = logger.get_pairs()
    cnt = [0, 0]
    for pair in pairs:
        appearance = pair[2]
        cnt[appearance] += 1

    return cnt

def __find_double_neighbors(graph_full : Graph, graph_cut : Graph, src : int, logger : Logger, 
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

def __approximate_pairs_collection(graph_full : Graph, graph_cut : Graph, logger : Logger) -> None:
    logs = logger.get_pairs()
    found_0 = len([pair for pair in logs if pair[2] == 0])
    found_1 = len([pair for pair in logs if pair[2] == 1])
    max_amount = 10000

    for _ in range(1000):
        src = random.randint(1, graph_full.number_of_vertices() - 1)
        found_0, found_1 = __find_double_neighbors(graph_full, graph_cut, src, logger, found_0, found_1)
        print(found_0, found_1)
        if (found_0 >= max_amount) and (found_1 >= max_amount):
            return
    
    logger.dump()

def __add_pairs_wich_will_appear(graph_cut : Graph, logger : Logger, filter : int) -> None:
    for edge in graph_cut.edges_that_will_appear(filter):
        v1 = edge[0]
        v2 = edge[1]
        if graph_cut.has_edges_between(v1, v2):
            continue

        v1_neighbors = graph_cut.adj(v1)
        v2_neighbors = graph_cut.adj(v2)

        if (len(v1_neighbors.intersection(v2_neighbors)) > 0) and (not logger.contains(v1, v2)):
            print(v1, v2)
            logger.log(v1, v2, [1])

    logger.dump()
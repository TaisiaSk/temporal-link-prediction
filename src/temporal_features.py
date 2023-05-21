from math import exp, sqrt, log
import numpy as np
from typing import Callable
from functools import lru_cache
import time


from graph import Graph

# buffer = {f'{i}{j}': {} for i in range(3) for j in range(9)}

# def __get_buffer_key0(time_strategy: Callable[[float, float, float], float], \
#                       agg_strategy: Callable[[list], float] | None = None) -> str:
#     i = get_weightings().index(time_strategy)
#     j = 8
    
#     if (agg_strategy != None):
#         j = get_aggregations().index(agg_strategy)

#     return f'{i}{j}'

# def __get_buffer_key1(u: int, v: int) -> str:
#     return f'{min(u, v)}-{max(u, v)}'
    

# Temporal topological features

# Temporal weighting
# Utility functions
def _normalize(value: float, l_bound: float = 0.2) -> float:
    return l_bound + (1 - l_bound) * value

def _get_lin(t: float, t_min: float, t_max: float) -> float:
    return (t - t_min) / (t_max - t_min)


# Time strategies
def lin_w(t: float, t_min: float, t_max: float) -> float:
    return _normalize(_get_lin(t, t_min, t_max))

def exp_w(t: float, t_min: float, t_max: float) -> float:
    return _normalize((exp(3 * _get_lin(t, t_min, t_max)) - 1) / (exp(3) - 1))

def sqrt_w(t: float, t_min: float, t_max: float) -> float:
    return _normalize(sqrt(_get_lin(t, t_min, t_max)))


# All weighting strategies
def get_weightings() -> tuple:
    return (lin_w, exp_w, sqrt_w)


# def __q1(x):
#     return np.quantile(x, 0.25)

# def __q4(x):
#     return np.quantile(x, 0.75)

# All past event aggregation strategies
def get_aggregations() -> tuple:
    # q0, q1, q2, q3, q4, sum, mean, variance
    strategies = (min, \
                  lambda x: np.quantile(x, 0.25), \
                #   __q1, \
                  np.median, \
                  lambda x: np.quantile(x, 0.75), \
                #   __q4, \
                  max, \
                  sum, \
                  np.mean, \
                  np.var)
    
    return strategies


# The edge weight depending on the strategies
@lru_cache
def get_weight(u: int, \
               v: int, \
               graph: Graph, \
               timestamp: int, \
               time_strategy: Callable[[float, float, float], float], \
               agg_strategy: Callable[[list], float] | None, \
               is_multiedge: bool = False) -> float:
    
    # key0 = __get_buffer_key0(time_strategy, agg_strategy)
    # key1 = __get_buffer_key1(u, v)

    # if (key1 in buffer[key0]):
    #     return buffer[key0][key1]

    edges = graph.get_edges_between(u, v, timestamp)
    t_min = graph.min_timestamp()
    t_max = graph.max_timestamp()

    if (is_multiedge):
        timestamps = []

        for edgeId in edges:
            timestamps.append(graph.get_edge_info(edgeId)[0])

        weightings = [time_strategy(t, t_min, t_max) for t in timestamps]
        weight = agg_strategy(weightings)
        # buffer[key0][key1] = weight

        return weight
    
    edgeId = edges.pop()
    t = graph.get_edge_info(edgeId)[0]
    weight = time_strategy(t, t_min, t_max)
    # buffer[key0][key1] = weight

    return weight

    
# Weighted topological features
# Adamic-Adar (AA)
def _aa(u: int, \
        v: int, \
        graph: Graph, \
        timestamp: int, \
        time_strategy: Callable[[float, float, float], float], \
        agg_strategy: Callable[[list], float] | None = None, \
        is_multiedge: bool = False) -> float:
    
    aa = 0
    neighbors_u = graph.adj(u, timestamp)
    neighbors_v = graph.adj(v, timestamp)
    common_neighbors = neighbors_u.intersection(neighbors_v)

    for neighbor in common_neighbors:
        curr_neighbors = graph.adj(neighbor, timestamp)
        curr_sum = 0

        for vertex in curr_neighbors:
            curr_sum += get_weight(neighbor, vertex, graph, timestamp, time_strategy, agg_strategy, is_multiedge)

        weight_to_u = get_weight(neighbor, u, graph, timestamp, time_strategy, agg_strategy, is_multiedge)
        weight_to_v = get_weight(neighbor, v, graph, timestamp, time_strategy, agg_strategy, is_multiedge)

        aa += (weight_to_u + weight_to_v) / (log(1 + curr_sum))

    return aa


# Common Neighbours (CN)
def _cn(u: int, \
        v: int, \
        graph: Graph, \
        timestamp: int, \
        time_strategy: Callable[[float, float, float], float], \
        agg_strategy: Callable[[list], float] | None = None, \
        is_multiedge: bool = False) -> float:
    
    cn = 0
    neighbors_u = graph.adj(u, timestamp)
    neighbors_v = graph.adj(v, timestamp)
    common_neighbors = neighbors_u.intersection(neighbors_v)

    for neighbor in common_neighbors:
        weight_to_u = get_weight(neighbor, u, graph, timestamp, time_strategy, agg_strategy, is_multiedge)
        weight_to_v = get_weight(neighbor, v, graph, timestamp, time_strategy, agg_strategy, is_multiedge)

        cn += weight_to_u + weight_to_v

    return cn

# Jaccard Coefficient (JC) 
def _jc(u: int, \
        v: int, \
        graph: Graph, \
        timestamp: int, \
        time_strategy: Callable[[float, float, float], float], \
        agg_strategy: Callable[[list], float] | None = None, \
        is_multiedge: bool = False) -> float:
    
    jc = 0
    neighbors_u = graph.adj(u, timestamp)
    neighbors_v = graph.adj(v, timestamp)
    common_neighbors = neighbors_u.intersection(neighbors_v)

    sum_u = 0
    for neighbor in neighbors_u:
        sum_u += get_weight(neighbor, u, graph, timestamp, time_strategy, agg_strategy, is_multiedge)

    sum_v = 0
    for neighbor in neighbors_v:
        sum_v += get_weight(neighbor, v, graph, timestamp, time_strategy, agg_strategy, is_multiedge)

    if (sum_u == 0 and sum_v == 0):
        return 0

    for neighbor in common_neighbors:
        weight_to_u = get_weight(neighbor, u, graph, timestamp, time_strategy, agg_strategy, is_multiedge)
        weight_to_v = get_weight(neighbor, v, graph, timestamp, time_strategy, agg_strategy, is_multiedge)

        jc += weight_to_u + weight_to_v

    return jc / (sum_u + sum_v)

# Preferential Attachment (PA)
def _pa(u: int, \
        v: int, \
        graph: Graph, \
        timestamp: int, \
        time_strategy: Callable[[float, float, float], float], \
        agg_strategy: Callable[[list], float] | None = None, \
        is_multiedge: bool = False) -> float:
    
    neighbors_u = graph.adj(u, timestamp)
    neighbors_v = graph.adj(v, timestamp)

    sum_u = 0
    for neighbor in neighbors_u:
        sum_u += get_weight(neighbor, u, graph, timestamp, time_strategy, agg_strategy, is_multiedge)

    sum_v = 0
    for neighbor in neighbors_v:
        sum_v += get_weight(neighbor, v, graph, timestamp, time_strategy, agg_strategy, is_multiedge)

    pa = sum_u * sum_v

    return pa


# Get final topological features
def get_topological_feature(u: int, v: int, graph: Graph, timestamp: int) -> list:
    result = []
    features = (_aa, _cn, _jc, _pa)
    
    is_multigraph = graph.is_multigraph()
    time_strategies = get_weightings()

    if (is_multigraph):
        agg_strategies = get_aggregations()

        for feature in features:
            for weight in time_strategies:
                for agg in agg_strategies:
                    result.append(feature(u, v, graph, timestamp, weight, agg, is_multiedge=True))

    else:  
        for feature in features:  
            for weight in time_strategies:
                result.append(feature(u, v, graph, timestamp, weight, is_multiedge=False))

    return result


# a = Graph(file_path='./data/opsahl-ucsocial.tsv', timestamp_col=3, number_of_lines_to_skip=2)

# start_time = time.time()
# features = get_topological_feature(105, 8, a, 100)
# print("--- %s seconds ---" % (time.time() - start_time))

# print(a.is_multigraph())
# print(features)
# print(len(features))
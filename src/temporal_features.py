from math import exp, sqrt, log
import numpy as np
from typing import Callable

from Graph import Graph

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
def get_weightings() -> dict:
    strategies = {'lin': lin_w, \
                  'exp': exp_w, \
                  'sqrt': sqrt_w}
    
    return strategies


# All past event aggregation strategies
def get_aggregations() -> dict:
    strategies = {'q0': min, \
                  'q1': lambda x: np.quantile(x, 0.25), \
                  'q2': np.median, \
                  'q3': lambda x: np.quantile(x, 0.75), \
                  'q4': max, \
                  'sum': sum, \
                  'mean': np.mean, \
                  'variance': np.var}
    
    return strategies


# The edge weight depending on the strategies
def get_weight(u: int, \
               v: int, \
               graph: Graph, \
               timestamp: int, \
               time_strategy: Callable[[float, float, float], float], \
               agg_strategy: Callable[[list], float] | None, \
               is_multiedge: bool = False) -> float:
    
    edges = graph.get_edges_between(u, v, timestamp)
    t_min = graph.min_timestamp()
    t_max = graph.max_timestamp()

    if (len(edges) < 1):
        return 0

    if (is_multiedge):
        timestamps = []

        for edgeId in edges:
            timestamps.append(graph.get_edge_info(edgeId)[0])

        weightings = [time_strategy(t, t_min, t_max) for t in timestamps]

        return agg_strategy(weightings)
    
    edgeId = edges.pop()
    t = graph.get_edge_info(edgeId)[0]

    return time_strategy(t, t_min, t_max)

    
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
    features = {'AA': _aa, 'CN': _cn, 'JC': _jc, 'PA': _pa}
    
    # is_multigraph = graph.is_multigraph()
    is_multigraph = True
    time_strategies = get_weightings()

    if (is_multigraph):
        agg_strategies = get_aggregations()

        for feature in features.values():
            for weight in time_strategies.values():
                for agg in agg_strategies.values():
                    result.append(feature(u, v, graph, timestamp, weight, agg, is_multiedge=True))

    else:  
        for feature in features.values():  
            for weight in time_strategies.values():
                result.append(feature(u, v, graph, timestamp, weight, is_multiedge=False))

    return result

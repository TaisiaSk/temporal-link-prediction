from math import exp, sqrt, log
import numpy as np
from typing import Callable
import time

from graph import Graph

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



# All past event aggregation strategies
def get_aggregations() -> tuple:
    # q0, q1, q2, q3, q4, sum, mean, variance
    strategies = (min, \
                  lambda x: np.quantile(x, 0.25), \
                  np.median, \
                  lambda x: np.quantile(x, 0.75), \
                  max, \
                  sum, \
                  np.mean, \
                  np.var)
    
    return strategies

# Get weigth of edge(s)
def wtf(times: list, \
        graph: Graph, \
        time_strategy: Callable[[float, float, float], float], \
        agg_strategy: Callable[[list], float] | None, \
        is_multiedge: bool = False) -> float:

    t_min = graph.min_timestamp()
    t_max = graph.max_timestamp()

    if (is_multiedge):
        weightings = [time_strategy(t, t_min, t_max) for t in times]

        return agg_strategy(weightings)
    
    return time_strategy(times[0], t_min, t_max)

# Get final vector
def feature(u: int, v: int, graph: Graph, timestamp: int) -> list:
    cn = []
    jc = []
    aa = []
    pa = []

    is_multigraph = graph.is_multigraph()
    
    neighbors_u = graph.adj(u, timestamp)
    neighbors_v = graph.adj(v, timestamp)
    common_neighbors = neighbors_u.intersection(neighbors_v)

    time_strategies = get_weightings()

    if (is_multigraph):
        agg_strategies = get_aggregations()

        for time in time_strategies:
            for agg in agg_strategies:
                cn_curr = jc_curr = aa_curr = 0

                edges_from_u = [graph.get_edges_between(u, z, timestamp) for z in neighbors_u]
                edges_from_v = [graph.get_edges_between(u, z, timestamp) for z in neighbors_v]

                sum_from_u = 0
                sum_from_v = 0 

                for edge_u in edges_from_u:
                    times = [graph.get_edge_info(edge)[0] for edge in edge_u]
                    if (not times):
                        continue
                    sum_from_u += wtf(times, graph, time, agg, is_multiedge=True)

                for edge_v in edges_from_v:
                    times = [graph.get_edge_info(edge)[0] for edge in edge_v]
                    if (not times):
                        continue
                    sum_from_v += wtf(times, graph, time, agg, is_multiedge=True)

                pa_curr = sum_from_u * sum_from_v

                for neighbor in common_neighbors:
                    wtf_u = wtf_v = 0

                    nb_to_u = graph.get_edges_between(u, neighbor, timestamp)
                    nb_to_v = graph.get_edges_between(v, neighbor, timestamp)

                    if (nb_to_u):
                        times = [graph.get_edge_info(edge)[0] for edge in nb_to_u]
                        wtf_u += wtf(times, graph, time, agg, is_multiedge=True)

                    if (nb_to_v):
                        times = [graph.get_edge_info(edge)[0] for edge in nb_to_v]
                        wtf_u += wtf(times, graph, time, agg, is_multiedge=True)

                    cn_curr += wtf_u + wtf_v
                    jc_curr += wtf_u + wtf_v 

                    from_neighbor = graph.adj(neighbor, timestamp)                    
                    nb_to_node = [graph.get_edges_between(neighbor, node, timestamp) for node in from_neighbor]
                    sum_from_nb = 0

                    for edge_nb in nb_to_node:
                        times = [graph.get_edge_info(edge)[0] for edge in edge_nb]
                        if (not times):
                            continue
                        sum_from_nb += wtf(times, graph, time, agg, is_multiedge=True)

                    aa_curr += (wtf_u + wtf_v) / log(1 + sum_from_nb)

                jc_curr /=  (sum_from_u + sum_from_v)

                cn.append(cn_curr)
                jc.append(jc_curr)
                aa.append(aa_curr)
                pa.append(pa_curr)        
    else:
        for time in time_strategies:
            cn_curr = jc_curr = aa_curr = 0

            edges_from_u = [graph.get_edges_between(u, z, timestamp).pop() for z in neighbors_u]
            edges_from_v = [graph.get_edges_between(u, z, timestamp).pop() for z in neighbors_v]

            sum_from_u = 0
            sum_from_v = 0 

            for edge_u in edges_from_u:
                time_u = [graph.get_edge_info(edge_u)[0]]
                sum_from_u += wtf(time_u, graph, time, is_multiedge=False)

            for edge_v in edges_from_v:
                time_v = [graph.get_edge_info(edge_v)[0]]
                sum_from_v += wtf(time_v, graph, time, is_multiedge=False)

            pa_curr = sum_from_u * sum_from_v

            for neighbor in common_neighbors:
                wtf_u = wtf_v = 0
                nb_to_u = graph.get_edges_between(u, neighbor, timestamp)
                nb_to_v = graph.get_edges_between(v, neighbor, timestamp)

                if (nb_to_u):
                    time_nb_to_u = [graph.get_edge_info(nb_to_u.pop())[0]]
                    wtf_u = wtf(time_nb_to_u, graph, time, is_multiedge=False)

                if (nb_to_v):
                    time_nb_to_v = [graph.get_edge_info(nb_to_v.pop())[0]]
                    wtf_v = wtf(time_nb_to_v, graph, time, is_multiedge=False)

                cn_curr += nb_to_u + nb_to_v
                jc_curr += nb_to_u + nb_to_v 

                from_neighbor = graph.adj(neighbor, timestamp)                    
                nb_to_node = [graph.get_edges_between(neighbor, node, timestamp).pop() for node in from_neighbor]
                sum_from_nb = 0

                for edge_nb in nb_to_node:
                    times = [graph.get_edge_info(edge_nb)[0]]
                    sum_from_nb += wtf(times, graph, time, is_multiedge=False)

                aa_curr += (nb_to_u + nb_to_v) / log(1 + sum_from_nb)

            jc_curr /=  (sum_from_u + sum_from_v)

            cn.append(cn_curr)
            jc.append(jc_curr)
            aa.append(aa_curr)
            pa.append(pa_curr)

    return cn + jc + aa + pa 


a = Graph(file_path='./data/opsahl-ucsocial.tsv', timestamp_col=3, number_of_lines_to_skip=2)

# start_time = time.time()
# features0 = get_topological_feature(105, 8, a, 100)
# print("--- %s seconds ---" % (time.time() - start_time))
# print(features0)

start_time = time.time()
features1 = feature(105, 8, a, 100)
print("--- %s seconds ---" % (time.time() - start_time))
print(features1)

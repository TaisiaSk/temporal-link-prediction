from Graph import Graph
from collections import deque
import random
import math

# count of vertices
# => Graph

# count of edges
# => Graph

# dencity
# WARNING: not for multigraph!
# TODO: multigraph?
def get_dencity(graph: Graph) -> float:
    n = graph.number_of_vertices()
    return 1.0 * graph.number_of_edges() / ( n * (n - 1) / 2)

# BFS for searching component from v
# returns size of component and removes visited vertices from set of not_visited
# WARNING: changes (not_visited)
def bfs_search_component(graph: Graph, v: int, not_visited: set) -> int:
    count = 0
    q = deque()
    q.append(v)
    while (len(q) != 0):
        v = q.popleft()
        count += 1
        adj = graph.adj(v)
        for node in adj:
            if (node in not_visited):
                not_visited.remove(node)
                q.append(node)

    return count

# info about components:
# list of tuples [root, size] for each component
def get_components(graph: Graph) -> list:
    not_visited = set(graph.vertices())
    components = list()
    while(len(not_visited) != 0):
        v = not_visited.pop()
        component_size = bfs_search_component(graph, v, not_visited)
        components.append((v, component_size))
    return components

# components: list of tuples [root, size]
# returns tuple [root, size] with max component
def find_max_component(components: list) -> tuple:
    components_sorted = sorted(components, key=lambda a: a[1], reverse=True)
    return components_sorted[0]

# components: list of tuples [root, size]
# returns percentage of vertices in max component
def percent_of_vertices_in_max_component(components: list, graph: Graph) -> float:
    root, size = find_max_component(components)
    return 1.0 * size / graph.number_of_vertices()

############################################################################################

# this function add count to list of distances to d - 1 position
# distances = list (array), i-th element represents count of vertices on i+1 distance
# WARNING: this function assumes that new distance d, that is not in list yet, is +1 then
# maximum in list because d comes from BFS, where each level is +1 then previous.
# thus new distance comes to the end of list.
def add_to_distances_list(d: int, count: int, distances: list):
    if (len(distances) < d):
        distances.append(count)
    else:
        distances[d - 1] += count

# this function collect count of vertices on each possible distance (level) to special list: distances
# distances = list (array), i-th element represents count of vertices on i+1 distance
# returns eccentricity of given vertex
# WARNING: changes (distances)
# TODO: possible to check (while) with len(visited) == size, not len(q). Less loops
def bfs_get_counts_of_vertices_on_distance(v: int, distances: list, graph: Graph) -> int:
    visited = set()
    visited.add(v)
    q = deque()
    d = 0
    q.append((v, d))
    while (len(q) != 0):
        v, d = q.popleft()
        adj = graph.adj(v)
        count_adj = len(adj)
        if (count_adj == 0):
            return d
        count_new = 0
        for node in adj:
            if (node not in visited):
                visited.add(node)
                q.append((node, d + 1))
                count_new += 1
        if (count_new != 0):
            d += 1
            add_to_distances_list(d, count_new, distances)

    return d

# returns set of vertices in given component with root = v
def get_component_vertices(v: int, graph: Graph) -> set:
    visited = set()
    visited.add(v)
    q = deque()
    q.append(v)
    while (len(q) != 0):
        v = q.popleft()
        adj = graph.adj(v)
        for node in adj:
            if (node not in visited):
                visited.add(node)
                q.append(node)

    return visited

# radius, diameter and 90-th percentile
# distances = list (array), i-th element represents count of vertices on i+1 distance
# max_distances = not sorted list of eccentricities
# returns d_metrics = {'radius', 'diameter', 'perc90'}
def get_metrics_from_distances_list(distances: list, max_distances: list) -> dict:
    d_metrics = {'radius': 0, 'diameter': 0, 'perc90': '0'}

    max_distances.sort()
    d_metrics['radius'] = max_distances[0]
    d_metrics['diameter'] = max_distances[-1]

    selection_size = sum(distances)
    idx_proc90 = math.ceil(selection_size * 0.9)
    idx = 0
    for d, count in enumerate(distances):
        if (count + idx < idx_proc90):
            idx += count
            continue
        else:
            d_metrics['perc90'] = d + 1
            return d_metrics

# returns subgraph made by snowball method with root = v and size ~max_count
def snowball_BFS(v: int, graph: Graph, max_count: int) -> set:
    visited = set()
    visited.add(v)
    q = deque()
    q.append(v)
    while (len(q) != 0):
        v = q.popleft()
        adj = graph.adj(v)
        count_adj = len(adj)
        for node in adj:
            if (node not in visited):
                visited.add(node)
                q.append(node)
        if (count_adj + len(visited) > max_count):
            return visited
    return visited

# returns list of randomly picked v from vertices
# сделать сравнение с наличием в выбранных и не удалять!
def pick_vertexes(vertices: set, count: int) -> list:
    vertexes_copy = list(vertices)
    chosen = list()
    for i in range(0, count):
        random_idx = random.randint(0, len(vertexes_copy) - 1)
        random_v = vertexes_copy[random_idx]
        chosen.append(random_v)
        vertexes_copy.remove(random_v)
    return chosen

# estimate radius, diameter and 90-th percentile not by snow method
# it takes 500 random vertices and counts distances for them to all other vertices in component
# returns d_metrics = {'radius', 'diameter', 'perc90'}
def estimate_metrics_not_snow(vertices: set, graph: Graph) -> dict:
    random_count = 500  # count of v for random picking
    loop_count = 3  # count of times for estimation

    distances = list()
    max_distances = list()
    radius = 0
    diameter = 0
    perc90 = 0
    for i in range(0, loop_count):
        chosen = pick_vertexes(vertices, random_count)
        for v in chosen:
            max_distances.append(bfs_get_counts_of_vertices_on_distance(v, distances, graph))
        metrix = get_metrics_from_distances_list(distances, max_distances)
        radius += metrix['radius']
        diameter += metrix['diameter']
        perc90 += metrix['perc90']
    # count arithmetical mean
    return {'radius': radius * 1.0 / loop_count, 'diameter': diameter * 1.0 / loop_count,
            'perc90': perc90 * 1.0 / loop_count}

# estimate radius, diameter and 90-th percentile by snow method
# it takes 2 random vertices, makes subgraph with 500 vertices by snowball method
# and counts distances for them to all other vertices in component
# returns d_metrics = {'radius', 'diameter', 'perc90'}
def estimate_metrics_snow(vertexes, graph):
    snowball_count = 3  # count of roots for snowball
    random_count = 500  # max count of v in snowball subgraph

    distances = list()
    max_distances = list()
    radius = 0
    diameter = 0
    perc90 = 0
    for i in range(0, snowball_count):
        chosen = pick_vertexes(vertexes, 1)
        vertexes_in_snowboll = (snowball_BFS(chosen[0], graph, random_count))
        for v in vertexes_in_snowboll:
            max_distances.append(bfs_get_counts_of_vertices_on_distance(v, distances, graph))
        metrix = get_metrics_from_distances_list(distances, max_distances)
        radius += metrix['radius']
        diameter += metrix['diameter']
        perc90 += metrix['perc90']
    # count arithmetical mean
    return {'radius': radius * 1.0 / snowball_count, 'diameter': diameter * 1.0 / snowball_count,
            'perc90': perc90 * 1.0 / snowball_count}

# component = [root, size] of max component (requires to be found outside from this function)
# counts distance properties: for small / big graphs
# returns:
# d_metrics = {'radius', 'diameter', 'perc90'} for SMALL
# d_metrics = {'snow': {'radius', 'diameter', 'perc90'}, 'not_snow': {'radius', 'diameter', 'perc90'}} for BIG
def get_distance_properties(component, graph):
    small_graph_size = 500
    root, size = component
    vertices = get_component_vertices(root, graph)
    # small graph
    if (size < small_graph_size):
        distances = list()
        max_distances = list()
        for v in vertices:
            max_distances.append(bfs_get_counts_of_vertices_on_distance(v, distances, graph))
        return get_metrics_from_distances_list(distances, max_distances)
    # big graph
    else:
        metrics_not_snow = estimate_metrics_not_snow(vertices, graph)
        metric_snow = estimate_metrics_snow(vertices, graph)
        return {'not_stow': metrics_not_snow, 'snow': metric_snow}

#small
#graph = Graph(file_path="out .soc-sign-test", timestamp_col=2, skip_first_line=True)

#big
#graph = Graph(file_path="out.sx-superuser", timestamp_col=2, skip_first_line=True)
#comps = get_components(graph)
#max_comp = find_max_component(comps)
#print(get_distance_properties(max_comp, graph))

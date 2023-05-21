from graph.Graph import Graph


# Degree assortativity
def degree_assortativity(graph: Graph) -> float:
    edges_count = 0
    vertices = graph.vertices()
    visited = set()
    sum_mult = 0
    sum_sum = 0
    sum_sumsquares = 0

    for vertex in vertices:
        neighbors = graph.adj(vertex)
        degree = len(neighbors)

        for neighbor in neighbors:
            if (neighbor in visited):
                continue

            curr_degree = len(graph.adj(neighbor))

            sum_mult += degree * curr_degree
            sum_sum += degree + curr_degree
            sum_sumsquares += degree ** 2 + curr_degree ** 2

            edges_count += 1

        visited.add(vertex)

    M = 1 / edges_count
    arg = M * ((0.5 * sum_sum) ** 2)
    r = (sum_mult - arg) / (0.5 * sum_sumsquares - arg)

    return r

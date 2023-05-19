from Graph import Graph
import math

# common neighbours
def get_CN(common_neighbours: set) -> int:
    return len(common_neighbours)

# adamic adar
def get_AA(common_neighbours: set, graph: Graph) -> int:
    result = 0
    for v in common_neighbours:
        result += 1.0 / math.log(len(graph.adj(v)))
    return result

# jaccard coefficient
def get_JC(common_neighbours: set, union: set) -> int:
    return 1.0 * len(common_neighbours) / len(union)

# preferential attachment
def get_PA(adj_u: int, adj_v:int) -> int:
    return len(adj_u) * len(adj_v)

# this function counts all static properties for (u, v) and returns
# dict = { 'CN', 'AA', 'JC', 'PA' }
# assuming that given graph is temporal slice
def get_static_properties(u: int, v: int, graph: Graph):
    adj_u: set = graph.adj(u)
    adj_v: set = graph.adj(v)
#    adj_u: set = set(graph.adj(u)) # use if graph version is old and return list instead of set
#    adj_v: set = set(graph.adj(v))
    common_neighbours = adj_u.intersection(adj_v)
    union = adj_u.union(adj_v)
    d_static_properties = { 'CN': get_CN(common_neighbours), 'AA': get_AA(common_neighbours, graph), 'JC': get_JC(common_neighbours, union), 'PA': get_PA(adj_u, adj_v) }
    return d_static_properties

graph = Graph(file_path="out .soc-sign-test", timestamp_col=2, skip_first_line=True)
print(get_static_properties(1, 2, graph))
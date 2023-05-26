from graph import Graph
import basic_properties
import networkx as nx

test_datasets = [
    {'file_name' : 'testgraph_1.txt', 'weight_col' : None, 'timestamp_col' : None, 'number_of_lines_to_skip' : 0, 'filter' : None, 'is_multigraph' : True},
    {'file_name' : 'testgraph_2.txt', 'weight_col' : None, 'timestamp_col' : None, 'number_of_lines_to_skip' : 0, 'filter' : None, 'is_multigraph' : True},
    {'file_name' : 'testgraph_3.txt', 'weight_col' : None, 'timestamp_col' : None, 'number_of_lines_to_skip' : 0, 'filter' : None, 'is_multigraph' : True},
    {'file_name' : 'testgraph_4.txt', 'weight_col' : None, 'timestamp_col' : None, 'number_of_lines_to_skip' : 0, 'filter' : None, 'is_multigraph' : True},
    {'file_name' : 'testgraph_5.txt', 'weight_col' : None, 'timestamp_col' : None, 'number_of_lines_to_skip' : 0, 'filter' : None, 'is_multigraph' : True},
    #{'file_name' : 'testgraph_6.txt', 'weight_col' : None, 'timestamp_col' : None, 'number_of_lines_to_skip' : 0, 'filter' : None, 'is_multigraph' : True},
    #{'file_name' : 'testgraph_7.txt', 'weight_col' : None, 'timestamp_col' : None, 'number_of_lines_to_skip' : 0, 'filter' : None, 'is_multigraph' : True},
    {'file_name' : 'team_5.txt', 'weight_col' : None, 'timestamp_col' : None, 'number_of_lines_to_skip' : 0, 'filter' : None, 'is_multigraph' : True},
]

def make_nx(file_path):
    graph = nx.Graph()
    with open(file_path, "r") as file:
        for line in file:
            tokens = line.split()
            v1 = int(tokens[0])
            v2 = int(tokens[1])
            graph.add_edge(v1, v2)
    return graph

def count_nx(graph: nx.Graph):
    print(f'- counting basics')
    number_vertices = graph.number_of_nodes()
    number_edges = graph.number_of_edges()
    density = nx.density(graph)

    print(f'- counting component\nvertices={number_vertices}, edges={number_edges}, density={density}')
    components_count = nx.number_connected_components(graph)

    print(
        f'- counting metrics\ncomponents_count={components_count}')
    radius = nx.radius(graph)
    diameter = nx.diameter(graph)

    print(f'- counting coeffs\nradius={radius}, diameter={diameter}')
    avg_coeff = nx.average_clustering(graph)
    assort = nx.degree_assortativity_coefficient(graph)
    print(f'avg={avg_coeff}, assort={assort}')
    print(
        f'RESULT NETWORX:\nvertices={number_vertices}, edges={number_edges}, density={density}\ncomponents_count={components_count}\nradius={radius}, diameter={diameter}\n avg={avg_coeff}, assort={assort}')


for data in test_datasets:
    file_path = '../data/' + data['file_name']
    print(f'------------ start read graph {file_path}')

    count_nx(make_nx(file_path))
    continue

    graph = Graph(file_path, data['timestamp_col'], data['weight_col'], data['number_of_lines_to_skip'], data['filter'], data['is_multigraph'])

    print(f'- counting basics')
    number_vertices = basic_properties.get_vertices_count(graph)
    number_edges = basic_properties.get_edges_count(graph)
    density = basic_properties.get_dencity(graph)

    print(f'- counting component\nvertices={number_vertices}, edges={number_edges}, density={density}')
    components_count = basic_properties.get_components_count(graph)
    percentage = basic_properties.get_percentage(graph)
    #max_comp_size = basic_properties.get_max_component_size(graph)
    #print(f'max_comp_size={max_comp_size}')

    #print(f'- counting metrics\ncomponents_count={components_count}, percentage={percentage}, max_comp_size={max_comp_size}')
    print(
        f'- counting metrics\ncomponents_count={components_count}, percentage={percentage}')
    small_graph_size = 1000
    metrics = basic_properties.get_metrics(graph, small_graph_size)

    print(f'- counting coeffs\nmetrix: {metrics}')
    #avg_coeff = basic_properties.get_avg_coeff(graph)
    #assort = basic_properties.get_dg_assortativity(graph)
    #print(f'avg={avg_coeff}, assort={assort}')

    #print(f'RESULT:\nvertices={number_vertices}, edges={number_edges}, density={density}\ncomponents_count={components_count}, percentage={percentage}, max_comp_size={max_comp_size}\nmetrix: {metrics}\navg={avg_coeff}, assort={assort}')
    print(f'RESULT:\nvertices={number_vertices}, edges={number_edges}, density={density}\ncomponents_count={components_count}, percentage={percentage}\nmetrix: {metrics}')


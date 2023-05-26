from graph import Graph
import basic_properties


for data in dataset:
    print(f'--- start read graph {}')
    graph = Graph(file_path, timestamp_col, current_dataset['weight_col'], number_of_lines_to_skip)

    print(f'- counting basics')
    number_vertices = basic_properties.get_vertices_count(graph)
    number_edges = basic_properties.get_edges_count(graph)
    density = basic_properties.get_dencity(graph)

    print(f'- counting component\nvertices={number_vertices}, edges={number_edges}, density={density}')
    components_count = basic_properties.get_components_count(graph)
    percentage = basic_properties.get_percentage(graph)

    print(f'- counting metrics\ncomponents_count={components_count}, percentage={percentage}')
    small_graph_size = 500
    metrics = basic_properties.get_metrics(graph, small_graph_size)

    print(f'metrix: {metrics}')


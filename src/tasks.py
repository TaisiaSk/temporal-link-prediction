from graph import Graph
from data_collection import get_features_as_matrix
from prediction import prediction
import basic_properties as bp

def task_1(graph : Graph) -> tuple:
    vertices = bp.get_vertices_count(graph)
    edges = bp.get_edges_count(graph)
    dencity = bp.get_dencity(graph)
    components = bp.get_components_count(graph)
    percentage = bp.get_percentage(graph)

    heading = ('Vertices', 'Edges', 'Dencity', 'Components', 'Percentage')
    values = (vertices, edges, dencity, components, percentage)

    return heading, values

def task_2(graph : Graph) -> tuple:
    metrics = bp.get_metrics(graph) 

    if ('snow' in metrics):
        heading = ('Radius (snow)', 'Diameter (snow)', '90-th (snow)', 
                   'Radius (rand)', 'Diameter (rand)', '90-th (rand)')
        values = (metrics['snow']['radius'], metrics['snow']['diameter'], metrics['snow']['perc90'], 
                  metrics['not_snow']['radius'], metrics['not_snow']['diameter'], metrics['not_snow']['perc90'])
    else:
        heading = ('Radius', 'Diameter', '90-th percentile')
        values = (metrics['radius'], metrics['diameter'], metrics['perc90'])
    
    return heading, values

def task_3(graph : Graph) -> tuple:
    coefficient = bp.get_avg_coeff(graph)
    
    heading = ('Average clustering coefficient',)
    values = (coefficient,)

    return heading, values

def task_4(graph : Graph) -> tuple:
    coefficient = bp.get_dg_assortativity(graph)

    heading = ('Degree assortativity',)
    values = (coefficient,)

    return heading, values

def task_5(dataset : dict, static : bool) -> tuple:
    data = get_features_as_matrix(dataset, static)
    feture_set = 'I' if static else 'II-A'

    if (data is None):
        return None
    
    heading = ('Precision',)
    values = (prediction(data, dataset['file_name'].split('.')[0], feture_set),)

    return heading, values 

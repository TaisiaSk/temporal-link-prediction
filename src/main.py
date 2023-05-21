from graph import Graph
from table_maker import table_str
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

# !!!!!!!!!!!!!!!!!!!!!!!
# ЕСТЬ 2 ВАРИАНТА ВЫВОДА:
# 
# 1) Для большого графа (мощность самой большой компоненты >= 500)
#  две строки вывода: снежный ком и рандом
#  
# 2) Маленький граф
#  одна строка вывода
# НАДО РАЗБИТЬ НА ДВА СЛУЧАЯ
# !!!!!!!!!!!!!!!!!!!!!!!!
def task_2(graph : Graph) -> tuple:
    # bp.get_metrics(graph) returns:
    # d_metrics = {'radius', 'diameter', 'perc90'} for SMALL
    # d_metrics = {'snow': {'radius', 'diameter', 'perc90'}, 
    #              'not_snow': {'radius', 'diameter', 'perc90'}} for BIG
    # metrics = bp.get_metrics(graph) 
    radius = None       #ВСТАВИТЬ СВОЁ ЗНАЧЕНИЕ
    diameter = None     #ВСТАВИТЬ СВОЁ ЗНАЧЕНИЕ
    snowball90 = None   #ВСТАВИТЬ СВОЁ ЗНАЧЕНИЕ
    random90 = None     #ВСТАВИТЬ СВОЁ ЗНАЧЕНИЕ
    
    heading = ('Radius', 'Diameter', '90-th (snowball)', '90-th (random 500)')
    values = (radius, diameter, snowball90, random90)
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

def results_to_console(graph : Graph, function : callable, table_len : int = 100) -> None:
    heading, values = function(graph)
    print(table_str(heading, values, table_len))


def main() -> None:
    graph = Graph(file_path='./data/soc-sign-bitcoinotc.tsv', timestamp_col=3, number_of_lines_to_skip=2)

    tasks_to_output = {task_1, task_2, task_3, task_4}
    for task in tasks_to_output:
        results_to_console(graph, task, table_len=100)


main()
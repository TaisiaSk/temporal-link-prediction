
from graph.graph import Graph
from output.table_maker import table_str

def task_1(graph : Graph) -> tuple:
    vertices = graph.number_of_vertices()
    edges = graph.number_of_edges(without_multiplicity=True)
    dencity = None      #ВСТАВИТЬ СВОЁ ЗНАЧЕНИЕ
    components = None   #ВСТАВИТЬ СВОЁ ЗНАЧЕНИЕ - количество компонент связности
    percentage = None   #ВСТАВИТЬ СВОЁ ЗНАЧЕНИЕ - доля вершин в максимальной по мощности компоненте

    heading = ('Vertices', 'Edges', 'Dencity', 'Components', 'Percentage')
    values = (vertices, edges, dencity, components, percentage)
    return heading, values

def task_2(graph : Graph) -> tuple:
    radius = None       #ВСТАВИТЬ СВОЁ ЗНАЧЕНИЕ
    diameter = None     #ВСТАВИТЬ СВОЁ ЗНАЧЕНИЕ
    snowball90 = None   #ВСТАВИТЬ СВОЁ ЗНАЧЕНИЕ
    random90 = None     #ВСТАВИТЬ СВОЁ ЗНАЧЕНИЕ
    
    heading = ('Radius', 'Diameter', '90-th (snowball)', '90-th (random 500)')
    values = (radius, diameter, snowball90, random90)
    return heading, values

def task_3(graph : Graph) -> tuple:
    coefficient = None     #ВСТАВИТЬ СВОЁ ЗНАЧЕНИЕ
    
    heading = ('Average cluster coefficient',)
    values = (coefficient,)
    return heading, values

def task_4(graph : Graph) -> tuple:
    coefficient = None     #ВСТАВИТЬ СВОЁ ЗНАЧЕНИЕ

    heading = ('Coefficient of assortativity',)
    values = (coefficient,)
    return heading, values

def results_to_console(graph : Graph, task_number : int, table_len : int = 100) -> None:
    function_name = f'task_{task_number}'
    heading, values = eval(function_name)(graph)
    print(table_str(heading, values, table_len))


def main() -> None:
    graph = Graph(file_path='../data/soc-sign-bitcoinotc.tsv', timestamp_col=3, number_of_lines_to_skip=2)

    tasks_to_output = {1, 2, 3, 4}
    for task_number in tasks_to_output:
        results_to_console(graph, task_number, table_len=90)


main()
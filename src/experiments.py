from graph import Graph
from logger import Logger

datasets = [{'file_name' : 'email.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 1, 'filter' : 69}, 
            {'file_name' : 'bitcoinotc.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 1, 'filter' : 52}, 
            {'file_name' : 'bitcoinalpha.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 1, 'filter' : 47}, 
            {'file_name' : 'ucsocial.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 2, 'filter' : 23}]

current_dataset = datasets[2] 
logger = Logger(logs_file_name=current_dataset['file_name'] + '.json')
file_path = '../data/' + current_dataset['file_name']
timestamp_col = current_dataset['timestamp_col']
number_of_lines_to_skip = current_dataset['number_of_lines_to_skip']
filter = current_dataset['filter']

g = Graph(file_path, timestamp_col, number_of_lines_to_skip)

print(g.number_of_vertices(), g.number_of_edges(), g.number_of_edges(without_multiplicity=True))
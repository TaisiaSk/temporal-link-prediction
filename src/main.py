from graph import Graph
from table_maker import table_str
from tasks import *
import os


datasets = [{'file_name' : 'diggfriends.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 0, 'filter' : 50}, 
            {'file_name' : 'bitcoinotc.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 1, 'filter' : 42}, 
            {'file_name' : 'bitcoinalpha.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 1, 'filter' : 34}, 
            {'file_name' : 'email.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 1, 'filter' : 26}, 
            {'file_name' : 'ucsocial.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 2, 'filter' : 18}]

tasks_to_output = [{'name' : 'Number of vertices, number of edges, density...', 'func' : task_1}, 
                   {'name' : 'Radius, network diameter, 90 percentile...', 'func' : task_2}, 
                   {'name' : 'Average cluster coefficient', 'func' : task_3}, 
                   {'name' : 'The coefficient of assortativity', 'func' : task_4}]

if os.name == 'nt':
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')


def results_as_table(graph : Graph, function : callable, table_len : int = 100) -> str:
    heading, values = function(graph)
    return table_str(heading, values, table_len)


def results_section(idx : int, output : str = '') -> str:
    current_dataset = datasets[idx]
    file_path = '../data/' + current_dataset['file_name']
    timestamp_col = current_dataset['timestamp_col']
    number_of_lines_to_skip = current_dataset['number_of_lines_to_skip']

    g = Graph(file_path, timestamp_col, number_of_lines_to_skip)

    while True:
        output += 'You have chosen: ' + str(datasets[idx]['file_name']) + '\n\n'
        output += 'Select a task to output:\n\n'
        for task_idx in range(len(tasks_to_output)):
            output += ' ' + str(task_idx) + ' : ' + str(tasks_to_output[task_idx]['name']) + '\n'
        output += '\n-1 : Exit\n'
        output += '\nEnter the number: '

        clear()
        print(output, end='')
        task_idx = input()

        if (task_idx == '-1'):
            return int(task_idx), datasets_section

        if not (task_idx.isdigit()):
            output = f'Incorrect output: {task_idx}\n\n'
            continue
        
        task_idx = int(task_idx)
        if (task_idx < 0) or (task_idx >= len(tasks_to_output)):
            output = f'Your number is out of range: [-1, {len(tasks_to_output) - 1}]\n\n'
            continue

        clear()
        table = results_as_table(g, tasks_to_output[task_idx]['func'], table_len=100) + '\n\n'
        output = 'You have chosen: ' + str(tasks_to_output[task_idx]['name']) + '\n\n' + table + '\n\n'
        output += 'Press any button to exit\n'
        clear()
        print(output, end='')
        
        input()


def datasets_section(idx : int, output : str = '') -> tuple:
    while True:
        output += 'Select a dataset:\n\n'
        for idx in range(len(datasets)):
            output += ' ' + str(idx) + ' : ' + datasets[idx]['file_name'] + '\n'
        output += '\n-1 : Exit\n'
        output += '\nEnter the number: '

        clear()
        print(output, end='')
        idx = input()

        if (idx == '-1'):
            return int(idx), None

        if not (idx.isdigit()):
            output = f'Incorrect output: {idx}\n\n'
            continue
        
        idx = int(idx)
        if (idx < 0) or (idx >= len(datasets)):
            output = f'Your number is out of range: [-1, {len(datasets) - 1}]\n\n'
            continue
        
        return idx, results_section


def main() -> None:
    console_state = datasets_section
    idx = 0

    while (True):
        idx, console_state = console_state(idx=idx) 
        if (console_state is None):
            return

# main()
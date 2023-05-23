from properties.graph import Graph
from interface.table_maker import table_str
from interface.tasks import *
from config import datasets
import os

tasks_to_output = [{'name' : 'Number of vertices, number of edges, density...', 'func' : task_1}, 
                   {'name' : 'Radius, network diameter, 90 percentile...', 'func' : task_2}, 
                   {'name' : 'Average cluster coefficient', 'func' : task_3}, 
                   {'name' : 'The coefficient of assortativity', 'func' : task_4}, 
                   {'name' : 'Prediction model', 'func' : None}]

if os.name == 'nt':
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')


def __results_as_table(graph : Graph, function : callable, table_len : int = 100) -> str:
    heading, values = function(graph)
    if (heading is None) or (values is None):
        return ''
    return table_str(heading, values, table_len)


def __results_section(dataset_idx : int, output : str = '', graph : Graph = None) -> str:
    current_dataset = datasets[dataset_idx]
    file_path = './data/' + current_dataset['file_name']
    timestamp_col = current_dataset['timestamp_col']
    number_of_lines_to_skip = current_dataset['number_of_lines_to_skip']

    if (graph is None):
        graph = Graph(file_path, timestamp_col, number_of_lines_to_skip)

    while True:
        output += 'You have chosen: ' + str(current_dataset['file_name']) + '\n\n'
        output += 'Select a task to output:\n\n'
        for task_idx in range(len(tasks_to_output)):
            output += ' ' + str(task_idx) + ' : ' + str(tasks_to_output[task_idx]['name']) + '\n'
        output += '\n-1 : Exit\n'
        output += '\nEnter the number: '

        clear()
        print(output, end='')
        task_idx = input()

        if (task_idx == '-1'):
            return None, __datasets_section, None

        if not (task_idx.isdigit()):
            output = f'Input must be a number of range [-1, {len(tasks_to_output) - 1}]\n\n'
            output += 'Press any button to continue'
            clear()
            print(output)
            input()
            output = ''
            continue
        
        task_idx = int(task_idx)
        if (task_idx == len(tasks_to_output) - 1):
            return dataset_idx, __prediction_section, graph


        if (task_idx < 0) or (task_idx >= len(tasks_to_output)):
            output = f'Input must be a number of range [-1, {len(tasks_to_output) - 1}]\n\n'
            output += 'Press any button to continue'
            clear()
            print(output)
            input()
            output = ''
            continue

        clear()
        print('Wait a moment...')
        table = __results_as_table(graph, tasks_to_output[task_idx]['func'], table_len=100) + '\n\n'
        output = 'You have chosen: ' + str(tasks_to_output[task_idx]['name']) + '\n\n' + table
        output += 'Press any button to continue'
        clear()
        print(output)
        input()
        output = ''


def __prediction_section(dataset_idx : int, output : str = '', graph : Graph = None) -> tuple:
    while True:
        output += 'Select a type of prediction model:\n\n'
        output += ' 0 : Static\n'
        output += ' 1 : Temporal\n\n'
        output += '-1 : Exit\n'
        output += '\nEnter the number: '

        clear()
        print(output, end='')
        task_idx = input()

        if (task_idx == '-1'):
            return dataset_idx, __results_section, graph

        if not (task_idx.isdigit()):
            output = f'Input must be a number of range [-1, 1]\n\n'
            output += 'Press any button to continue'
            clear()
            print(output)
            input()
            output = ''
            continue
        
        task_idx = int(task_idx)
        if (task_idx == 0) or (task_idx == 1):
            clear()
            print('Close the window to continue')
            ans = task_5(datasets[dataset_idx], static=(task_idx == 0))
            if (ans is None):
                output = 'No data has been collected for this graph\n\n'
                output += 'Press any button to continue'
                clear()
                print(output)
                input()
                return dataset_idx, __results_section, graph
            else:
                output = 'You have chosen: ' + str(datasets[dataset_idx]['file_name'])
                output +=(' (static model)' if (task_idx == 0) else ' (temporal model)') + '\n\n'
                output += table_str(ans[0], ans[1], 100) + '\n\n'
                output += 'Press any button to continue'
                clear()
                print(output)
                input()
            output = ''
        else:
            output = f'Input must be a number of range [-1, 1]\n\n'
            output += 'Press any button to continue'
            clear()
            print(output)
            input()
            output = ''


def __datasets_section(dataset_idx : int, output : str = '', graph : Graph = None) -> tuple:
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
            return int(idx), None, None

        if not (idx.isdigit()):
            output = f'Input must be a number of range [-1, {len(datasets) - 1}]\n\n'
            output += 'Press any button to continue'
            clear()
            print(output)
            input()
            output = ''
            continue
        
        idx = int(idx)
        if (idx < 0) or (idx >= len(datasets)):
            output = f'Input must be a number of range [-1, {len(datasets) - 1}]\n\n'
            output += 'Press any button to continue'
            clear()
            print(output)
            input()
            output = ''
            continue
        
        clear()
        print('Wait a moment...')
        return idx, __results_section, None


def launch() -> None:
    console_state = __datasets_section
    graph = None
    dataset_idx = 0

    while (True):
        dataset_idx, console_state, graph = console_state(dataset_idx=dataset_idx, graph=graph) 
        if (console_state is None):
            return

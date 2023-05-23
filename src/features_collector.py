from graph import Graph
from logger import Logger
from main import datasets
from temporal_features import get_temporal_features as get_features
import numpy as np

def features_to_matrix(dataset : dict) -> tuple:
    features_logger = Logger(dir='../features/', logs_file_name=dataset['file_name'] + '.json', dump_before_del=False)
    features = features_logger.get_features()

    vector = []
    matrix = []
    for feature in features:
        vector.append(feature[0])
        feature.pop(0)
        matrix.append(feature)

    return np.array(vector), np.array(matrix)


def find_features(current_dataset : dict):
    file_path = '../data/' + current_dataset['file_name']
    timestamp_col = current_dataset['timestamp_col']
    number_of_lines_to_skip = current_dataset['number_of_lines_to_skip']
    filter = current_dataset['filter']

    graph = Graph(file_path, timestamp_col, number_of_lines_to_skip, filter)
    pairs_logger = Logger(dir='../pairs/', logs_file_name=current_dataset['file_name'] + '.json', dump_before_del=False)
    features_logger = Logger(dir='../features/', logs_file_name=current_dataset['file_name'] + '.json', saving_step=30)

    pairs = pairs_logger.get_pairs()
    max_amount = min(len([pair for pair in pairs if pair[2] == 0]), len([pair for pair in pairs if pair[2] == 1]))
    logs = features_logger.get_features()
    counter = [len([feature for feature in logs if feature[0] == 0]), len([feature for feature in logs if feature[0] == 1])]

    for pair in pairs:
        v1 = pair[0]
        v2 = pair[1]
        appearance = pair[2]

        if (counter[appearance] == max_amount) or (features_logger.contains(v1, v2)):
            continue
        print(v1, v2, counter)
        features = [appearance] + get_features(v1, v2, graph).tolist()
        features_logger.log(v1, v2, features)
        counter[appearance] += 1

    features_logger.dump()


# current_dataset = datasets[0] 
# find_features(current_dataset)
# print(len(vector), len(matrix))
# print(len(matrix[0]))
        






    

   
        
   



from graph import Graph
from logger import Logger
from temporal_features import get_temporal_features as get_features

datasets = [{'file_name' : 'bitcoinotc.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 1, 'filter' : 42}, 
            {'file_name' : 'bitcoinalpha.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 1, 'filter' : 34}, 
            {'file_name' : 'email.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 1, 'filter' : 26}, 
            {'file_name' : 'ucsocial.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 2, 'filter' : 18}]

for current_dataset in datasets: 
    file_path = '../data/' + current_dataset['file_name']
    timestamp_col = current_dataset['timestamp_col']
    number_of_lines_to_skip = current_dataset['number_of_lines_to_skip']
    filter = current_dataset['filter']

    graph = Graph(file_path, timestamp_col, number_of_lines_to_skip, filter)
    pairs_logger = Logger(dir='../pairs/', logs_file_name=current_dataset['file_name'] + '.json')
    features_logger = Logger(dir='../features/', logs_file_name=current_dataset['file_name'] + '.json', saving_step=30)

    pairs = pairs_logger.get_pairs()
    max_amount = min(len([pair for pair in pairs if pair[2] == 0]), len([pair for pair in pairs if pair[2] == 1]))
    counter = [0, 0]

    for pair in pairs:
        v1 = pair[0]
        v2 = pair[1]
        appearance = pair[2]

        if (counter[appearance] == max_amount) or (features_logger.contains(v1, v2)):
            continue
        print(v1, v2)
        features = [appearance] + get_features(v1, v2, graph).tolist()
        features_logger.log(v1, v2, features)
        counter[appearance] += 1

    features_logger.dump()
        






    

   
        
   



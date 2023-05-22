import json
import os

class Logger(object):
    def __init__(self, dir : str = './', logs_file_name : str = 'logs.json', saving_step : int = 1000):
        if (saving_step <= 0):
            raise Exception("Saving step value is negative: " + str(saving_step))

        self.__counter = 0
        self.__saving_step = saving_step
        self.__file_path = dir + '/' + logs_file_name

        if os.path.isfile(self.__file_path):
            self.__logs = self.__parse_from_file()
        else:
            self.__logs = {}


    def dump(self):
        with open(self.__file_path, 'w+') as file:
            json.dump(self.__logs, file)


    def get_logs(self) -> dict:
        return self.__logs
    

    def log(self, vertex_id_1 : int, vertex_id_2 : int, features : list):
        key = self.__key(vertex_id_1, vertex_id_2)

        if (key in self.__logs):
            raise Exception("Such data is already stored:\n " + key + " : " + str(self.__logs[key]))

        self.__logs[key] = features
        self.__counter += 1

        if (self.__counter % self.__saving_step == 0):
            self.dump()

    
    def contains(self, vertex_id_1 : int, vertex_id_2 : int):
        return self.__key(vertex_id_1, vertex_id_2) in self.__logs


    def __parse_from_file(self) -> dict:
        try:
            with open(self.__file_path, 'r') as file:
                return json.load(file)
        except OSError:
            print("Could not open/read file: ", self.__file_path)
        except Exception:
            print("Could not parse json: ", self.__file_path)


    def __key(self, vertex_id_1 : int, vertex_id_2 : int) -> str:
        return str(min(vertex_id_1, vertex_id_2)) + '-' + str(max(vertex_id_1, vertex_id_2))
    
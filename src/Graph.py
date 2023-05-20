class Graph(object):
    def __init__(self, file_path : str, timestamp_col : int = 2, number_of_lines_to_skip : int = 0):        
        try:
            self.__adjacent_vertices = dict()
            self.__edges_info = dict()
            self.__timestamps = set()

            with open(file_path, "r") as file:
                for _ in range(0, number_of_lines_to_skip):
                    next(file)

                edge_id = 0
                for line in file:
                    tokens = line.split()
                    v1 = int(tokens[0])
                    v2 = int(tokens[1])
                    timestamp = float(tokens[timestamp_col])

                    self.__timestamps.add(timestamp)
                    self.add_edge(v1, v2, edge_id, timestamp)
                    edge_id += 1

        except OSError:
            print("Could not open/read file: ", file_path)


    def number_of_edges(self, timestamp_filter : int = 100) -> int:
        if (timestamp_filter == 100):
            return len(self.__edges_info)
        filter = self.__filter(timestamp_filter)
        return len([id for id, props in self.__edges_info.items() if props[0] <= filter])


    def max_timestamp(self) -> float:
        return max(self.__timestamps)
    

    def min_timestamp(self) -> float:
        return min(self.__timestamps)


    def number_of_vertices(self) -> int:
        return len(self.__adjacent_vertices)


    def edges_ids(self, timestamp_filter : int = 100) -> set:
        if (timestamp_filter == 100):
            return set(self.__edges_info.keys())
        filter = self.__filter(timestamp_filter)
        return set(id for id, props in self.__edges_info.items() if props[0] <= filter)


    def vertices(self) -> set:
        return set(self.__adjacent_vertices.keys())


    def splitting_by_filter(self, timestamp_filter : int) -> float:
        return self.number_of_edges(timestamp_filter) / self.number_of_edges()


    def get_edge_info(self, edge_id : int) -> list:
        if (edge_id in self.__edges_info):
            return self.__edges_info[edge_id]
        return None


    def adj(self, vertex_id : int, timestamp_filter : int = 100) -> set:
        if not (vertex_id in self.__adjacent_vertices):
            return set()
        if (timestamp_filter == 100):
            return set(self.__adjacent_vertices[vertex_id].keys())
        return set(id for id in self.__adjacent_vertices[vertex_id] if self.has_edges_between(vertex_id, id, timestamp_filter))


    def has_edges_between(self, vertex_id_1 : int, vertex_id_2 : int, timestamp_filter : int = 100) -> bool:
        return len(self.get_edges_between(vertex_id_1, vertex_id_2, timestamp_filter)) > 0


    def get_edges_between(self, vertex_id_1 : int, vertex_id_2 : int, timestamp_filter : int = 100) -> set:
        if not ((vertex_id_1 in self.__adjacent_vertices) and (vertex_id_2 in self.__adjacent_vertices[vertex_id_1])):
            return set()
        
        edges = self.__adjacent_vertices[vertex_id_1][vertex_id_2]
        if (timestamp_filter == 100):
            return edges
        
        filter = self.__filter(timestamp_filter)
        return set(id for id in edges if self.__edges_info[id][0] <= filter)


    def add_vertex(self, vertex_id : int):
        if (vertex_id is None) or (vertex_id < 0):
            raise Exception(f"Vertex id is invalid: " + str(vertex_id))
        if not (vertex_id in self.__adjacent_vertices):
            self.__adjacent_vertices[vertex_id] = dict() 


    def remove_vertex(self, vertex_id : int):
        if (vertex_id is None) or (vertex_id < 0):
            raise Exception(f"Vertex id is invalid: " + str(vertex_id))
        if not (vertex_id in self.__adjacent_vertices):
            return

        edges_to_delete = set()
        for edges_list in self.__adjacent_vertices[vertex_id].values():
            edges_to_delete.update(edges_list)

        for edge_id in edges_to_delete:
            self.remove_edge(edge_id)
        del self.__adjacent_vertices[vertex_id]
        

    def add_edge(self, vertex_id_1 : int, vertex_id_2 : int, edge_id : int, timestamp : float = None):
        if (edge_id in self.__edges_info):
            raise Exception(f"Such edge id already exists: " + str(edge_id))

        self.add_vertex(vertex_id_1)
        self.add_vertex(vertex_id_2)

        self.__add_edge_to_list(vertex_id_1, vertex_id_2, edge_id)
        self.__add_edge_to_list(vertex_id_2, vertex_id_1, edge_id)

        self.__edges_info[edge_id] = [timestamp, vertex_id_1, vertex_id_2]


    def remove_edge(self, edge_id : int):
        if (edge_id is None) or (edge_id < 0):
            raise Exception(f"Edge id is invalid: " + str(edge_id))
        
        if (edge_id in self.__edges_info):
            vertex_id_1 = self.__edges_info[edge_id][1]
            vertex_id_2 = self.__edges_info[edge_id][2]

            self.__remove_edge_from_list(vertex_id_1, vertex_id_2, edge_id)
            self.__remove_edge_from_list(vertex_id_2, vertex_id_1, edge_id)

            del self.__edges_info[edge_id]
         

    def __str__(self) -> str:
        format_str = '%6s %6s %6s %16s\n'
        graph_str = format_str % ('e', 'v1', 'v2', 'time')
        for edge_id, edge in self.__edges_info.items():
            graph_str += format_str % (edge_id, edge[1], edge[2], edge[0])
        return graph_str


    def __add_edge_to_list(self, vertex_from : int, vertex_to : int, edge_id : int):
        if not (vertex_to in self.__adjacent_vertices[vertex_from]):
            self.__adjacent_vertices[vertex_from][vertex_to] = set()
        self.__adjacent_vertices[vertex_from][vertex_to].add(edge_id)


    def __remove_edge_from_list(self, vertex_from : int, vertex_to : int, edge_id : int):
        self.__adjacent_vertices[vertex_from][vertex_to].remove(edge_id)
        if (len(self.__adjacent_vertices[vertex_from][vertex_to]) == 0):
            del self.__adjacent_vertices[vertex_from][vertex_to]


    def __filter(self, timestamp_filter : int):
        if (timestamp_filter < 0 or timestamp_filter > 100):
            raise Exception(f"Required filter value is out of range: " + str(timestamp_filter))
        
        max = self.max_timestamp()
        min = self.min_timestamp()
        return (max - min) * timestamp_filter / 100 + min

        

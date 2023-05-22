class Graph(object):
    def __init__(self, file_path : str, timestamp_col : int = 2, number_of_lines_to_skip : int = 0, timestamp_filter : int = 100):        
        try:
            with open(file_path, "r") as file:
                self.__init_data_structures(file, timestamp_col, number_of_lines_to_skip)
                for _ in range(0, number_of_lines_to_skip):
                    next(file)

                edge_id = 0
                filter = self.__filter(timestamp_filter)

                for line in file:
                    tokens = line.split()
                    v1 = int(tokens[0])
                    v2 = int(tokens[1])
                    timestamp = float(tokens[timestamp_col])

                    if (timestamp > filter):
                        continue

                    self.add_edge(v1, v2, edge_id, timestamp)
                    edge_id += 1

        except OSError:
            print("Could not open/read file: ", file_path)

    
    def edges_that_will_appear(self, timestamp_filter : int) -> list:
        filter = self.__filter(timestamp_filter)
        edges = []
        for key in self.__timestamps: 
            if (key <= filter):
                continue
            edges.extend(self.__timestamps[key])

        return edges

    
    def cut_proportion(self, timestamp_filter : int) -> float:
        total_len = 0
        for value in self.__timestamps.values():
            total_len += len(value)
        return self.number_of_edges() / total_len


    def __init_data_structures(self, file, timestamp_col : int, number_of_lines_to_skip : int):
        self.__is_multigraph = False
        self.__number_of_edges_without_multiplicity = 0
        self.__number_of_vertices = 0
      
        self.__edges_info = dict()
        self.__timestamps = dict()
        vertices_num = self.__numer_of_vertices_from_file(file, timestamp_col, number_of_lines_to_skip)
        self.__adjacent_vertices = [None for _ in range(vertices_num + 1)]


    def __numer_of_vertices_from_file(self, file, timestamp_col : int, number_of_lines_to_skip : int) -> int:
        file.seek(0)
        for _ in range(0, number_of_lines_to_skip):
            next(file)

        vertices = set()

        for line in file:
            tokens = line.split()
            v1 = int(tokens[0])
            v2 = int(tokens[1])
            timestamp = float(tokens[timestamp_col])

            vertices.add(v1)
            vertices.add(v2)
    
            if (timestamp not in self.__timestamps):
                self.__timestamps[timestamp] = []
            self.__timestamps[timestamp].append([v1, v2])

        file.seek(0)
        return len(vertices)


    def number_of_edges(self, without_multiplicity : bool = False) -> int:
        if (without_multiplicity):
            return int(self.__number_of_edges_without_multiplicity / 2)
        return len(self.__edges_info)
       

    def max_timestamp(self) -> float:
        return max(self.__timestamps)
    

    def min_timestamp(self) -> float:
        return min(self.__timestamps)


    def number_of_vertices(self) -> int:
        return self.__number_of_vertices


    def edges_ids(self) -> set:
        return set(self.__edges_info.keys())


    def vertices(self) -> set:
        return set(i for i in range(1, len(self.__adjacent_vertices)))


    def get_edge_info(self, edge_id : int) -> list:
        if (edge_id in self.__edges_info):
            return self.__edges_info[edge_id]
        return None


    def adj(self, vertex_id : int) -> set:
        if (self.__adjacent_vertices[vertex_id] is None):
            return set()
        return set(self.__adjacent_vertices[vertex_id].keys())
        

    def has_edges_between(self, vertex_id_1 : int, vertex_id_2 : int) -> bool:
        return len(self.get_edges_between(vertex_id_1, vertex_id_2)) > 0


    def get_edges_between(self, vertex_id_1 : int, vertex_id_2 : int) -> set:
        if (self.__adjacent_vertices[vertex_id_1] is None) or (vertex_id_2 not in self.__adjacent_vertices[vertex_id_1]):
            return set()
        return self.__adjacent_vertices[vertex_id_1][vertex_id_2]
        

    def is_multigraph(self) -> bool:
        return self.__is_multigraph


    def remove_vertex(self, vertex_id : int) -> None:
        if (vertex_id is None) or (vertex_id < 0):
            raise Exception(f"Vertex id is invalid: " + str(vertex_id))
        if (self.__adjacent_vertices[vertex_id] is None):
            return

        edges_to_delete = set()
        for edges_list in self.__adjacent_vertices[vertex_id].values():
            edges_to_delete.update(edges_list)

        for edge_id in edges_to_delete:
            self.remove_edge(edge_id)
        self.__adjacent_vertices[vertex_id] = None
        self.__number_of_vertices -= 1

    
    def remove_edge(self, edge_id : int) -> None:
        if (edge_id is None) or (edge_id < 0):
            raise Exception(f"Edge id is invalid: " + str(edge_id))
        
        if (edge_id in self.__edges_info):
            vertex_id_1 = self.__edges_info[edge_id][1]
            vertex_id_2 = self.__edges_info[edge_id][2]

            self.__remove_edge_from_list(vertex_id_1, vertex_id_2, edge_id)
            self.__remove_edge_from_list(vertex_id_2, vertex_id_1, edge_id)

            del self.__edges_info[edge_id]
        

    def add_edge(self, vertex_id_1 : int, vertex_id_2 : int, edge_id : int, timestamp : float = None) -> None:
        if (edge_id in self.__edges_info):
            raise Exception(f"Such edge id already exists: " + str(edge_id))

        self.__add_vertex(vertex_id_1)
        self.__add_vertex(vertex_id_2)

        self.__add_edge_to_list(vertex_id_1, vertex_id_2, edge_id)
        self.__add_edge_to_list(vertex_id_2, vertex_id_1, edge_id)

        self.__edges_info[edge_id] = [timestamp, vertex_id_1, vertex_id_2]
         

    def __add_vertex(self, vertex_id : int) -> None:
        if (vertex_id is None) or (vertex_id < 0):
            raise Exception(f"Vertex id is invalid: " + str(vertex_id))
        if (self.__adjacent_vertices[vertex_id] is None):
            self.__adjacent_vertices[vertex_id] = dict() 
            self.__number_of_vertices += 1


    def __str__(self) -> str:
        format_str = '%6s %6s %6s %16s\n'
        graph_str = format_str % ('e', 'v1', 'v2', 'time')
        for edge_id, edge in self.__edges_info.items():
            graph_str += format_str % (edge_id, edge[1], edge[2], edge[0])
        return graph_str


    def __add_edge_to_list(self, vertex_from : int, vertex_to : int, edge_id : int) -> None:
        if (vertex_to not in self.__adjacent_vertices[vertex_from]):
            self.__adjacent_vertices[vertex_from][vertex_to] = set()
            self.__number_of_edges_without_multiplicity += 1

        if (self.__is_multigraph == False) and (len(self.__adjacent_vertices[vertex_from][vertex_to]) > 0):
            self.__is_multigraph = True

        self.__adjacent_vertices[vertex_from][vertex_to].add(edge_id)


    def __remove_edge_from_list(self, vertex_from : int, vertex_to : int, edge_id : int) -> None:
        self.__adjacent_vertices[vertex_from][vertex_to].remove(edge_id)
        if (len(self.__adjacent_vertices[vertex_from][vertex_to]) == 0):
            del self.__adjacent_vertices[vertex_from][vertex_to]
            self.__number_of_edges_without_multiplicity -= 1


    def __filter(self, timestamp_filter : int) -> float:
        if (timestamp_filter < 0 or timestamp_filter > 100):
            raise Exception(f"Required filter value is out of range: " + str(timestamp_filter))
        max = self.max_timestamp()
        min = self.min_timestamp()
        return (max - min) * timestamp_filter / 100 + min

import numpy as np


class Graph:

    def __init__(self):
        self._outgoing = {}
        self._incoming = {}

    def vertex_count(self):
        return len(self._outgoing)

    def vertices(self):
        return self._outgoing.keys()

    def edge_count(self):
        total = sum(len(self._outgoing[vertice]) for vertice in self._outgoing)
        return total

    def edges(self):
        result = set()
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())
        return result

    def get_edge(self, origin, destination):
        return self._outgoing[origin].get(destination)

    def incident_edges(self, vertice, outgoing=True):
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[vertice].values():
            yield edge

    def insert_vertex(self, index, value=None):  # x=None
        vertice = self.Vertex(index)
        self._outgoing[vertice] = {}
        self._incoming[vertice] = {}
        return vertice

    def insert_edge(self, u, v, x=None):  # edge = (u,v)
        edge = self.Edge(u, v, x)
        self._outgoing[u][v] = edge
        self._incoming[v][u] = edge

    class Vertex:

        def __init__(self, index, value=None):
            self._value = value
            self._index = index
            self._predecessor = None

        def get_value(self):
            return self._value

        def set_value(self, value):
            self._value = value

        def get_index(self):
            return self._index

        def set_index(self, index):
            self._index = index

        def get_predecessor(self):
            return self._predecessor

        def set_predecessor(self, predecessor):
            self._predecessor = predecessor

    class Edge:

        def __init__(self, origin, destination, distance):
            self._origin = origin
            self._destination = destination
            self._distance = distance

        def get_distance(self):
            return self._distance

        def set_distance(self, distance):
            self._distance = distance

        def get_origin(self):
            return self._origin

        def set_origin(self, origin):
            self._origin = origin

        def get_destination(self):
            return self._destination

        def set_destination(self, destination):
            self._destination = destination

        def endpoints(self):
            return (self._origin, self._destination)

        def opposite(self, vertice):
            return self._destination if vertice is self._origin else self._origin


class PriorityQueueBase:

    class _Item:

        def __init__(self, key, value):
            self._key = key
            self._value = value

        def __It__(self, other):
            return self._key < other._key

    def is_empty(self):
        return len(self) == 0


class HeapPriorityQueue(PriorityQueueBase):

    def _parent(self, j):
        return (j - 1) // 2

    def _left(self, j):
        return 2 * j + 1

    def _right(self, j):
        return 2 * j + 2

    def _has_left(self, j):
        return self._left(j) < len(self._data)

    def _has_right(self, j):
        return self._right(j) < len(self._data)

    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j]._key < self._data[parent]._key:
            self._swap(j, parent)
            self._upheap(parent)

    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            small_child = left
            if self._has_right(j):
                right = self._right(j)
                if self._data[right]._key < self._data[left]._key:
                    small_child = right
            if self._data[small_child]._key < self._data[j]._key:
                self._swap(j, small_child)
                self._downheap(small_child)

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def add(self, key, value):
        self._data.append(self._Item(key, value))
        self._upheap(len(self._data) - 1)

    def min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty')
        item = self._data[0]
        return (item._key, item._value)

    def remove_min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty')
        self._swap(0, len(self._data) - 1)
        item = self._data.pop()
        self._downheap(0)
        return (item._key, item._value)


class AdaptableHeapPriorityQueue(HeapPriorityQueue):

    class Item(HeapPriorityQueue._Item):

        def __init__(self, key, value, index):
            super().__init__(key, value)
            self._index = index

    def _swap(self, i, j):
        super()._swap(i, j)
        self._data[i]._index = i
        self._data[j]._index = j

    def _bubble(self, j):
        if j > 0 and self._data[j]._key < self._data[self._parent(j)]._key:
            self._upheap(j)
        else:
            self._downheap(j)

    def add(self, key, value):
        token = self.Item(key, value, len(self._data))
        self._data.append(token)
        self._upheap(len(self._data) - 1)
        return token

    def update(self, item, newkey, newval):
        j = item._index
        if not (0 <= j < len(self) and self._data[j] is item):
            raise ValueError('Invalid Locator')
        item._key = newkey
        item._value = newval
        self._bubble(j)

    def remove(self, item):
        j = item._index
        if not (0 <= j < len(self) and self._data[j] is item):
            raise ValueError('Invalid Locator')
        if j == len(self) - 1:
            self._data.pop()
        else:
            self._swap(j, len(self) - 1)
            self._data.pop()
            self._bubble(j)
        return (item._key, item._value)


def get_values_from_matrix(filename):

    values = []

    with open(filename, 'r') as r:
        for line in r:
            line = line.replace('\t', ' ')
            line = line.replace('\n', ' ')
            for i in line.split(' '):
                if i != '':
                    values.append(int(i))

    return values


def fill_matrix_with_values(values):

    n_vertices = values.pop(0)                                  # extract number of vertices
    matrix_of_vertices = np.zeros((n_vertices, n_vertices))     # create matrix with zeros

    # Fill matrix with entry .txt
    x = 0
    for i in range(0, n_vertices, +1):

        for j in range(i, n_vertices, +1):

            if j == i:
                matrix_of_vertices[i][i] = 0
                continue

            matrix_of_vertices[i][j] = values[x]
            matrix_of_vertices[j][i] = values[x]

            x = x + 1

    return n_vertices, matrix_of_vertices


def initialize_vertices_and_edges(graph, matrix, n_vertices):

    vert = []
    for i in range(n_vertices):
        vert.append(graph.insert_vertex(index=i))

    for i in range(n_vertices):
        for j in range(n_vertices):
            if j == i:
                continue
            else:
                graph.insert_edge(vert[i], vert[j], matrix[i, j])

    return vert


def shortest_path_lenghts(graph, initial_vertice):
    distance = {}                       # distance[v] is upper bound s to v
    cloud = {}                          # map reachable vertice to its distance[vertice] value
    pq = AdaptableHeapPriorityQueue()   # vertex vertice will have key distance[vertice]
    pq_item = {}                        # map from vertex to its pq item
    vertices = {}

    for vertice in graph.vertices():
        if vertice is initial_vertice:
            distance[vertice] = 0
        else:
            distance[vertice] = float('inf')                    # systax for positive  infinity
        pq_item[vertice] = pq.add(distance[vertice], vertice)   # save item for future updates

    while not pq.is_empty():
        key, u = pq.remove_min()
        cloud[u.get_index()] = key              # its correct d[u] value
        vertices[u.get_index()] = u
        del pq_item[u]                          # u is no longer in pq
        for edge in graph.incident_edges(u):    # outgoing edges (u,v)
            v = edge.opposite(u)
            if v not in cloud:
                # perform relaxation step on edge (u,v)
                edge_distance = edge.get_distance()
                if distance[u] + edge_distance < distance[v]:       # better path to v?
                    distance[v] = distance[u] + edge_distance       # update the distance
                    v.set_predecessor(u.get_index())
                    # print(v.get_index(), v.get_predecessor(), u.get_index())                          # update the pred
                    pq.update(pq_item[v], distance[v], v)           # update the pq entry

    return cloud, vertices                                              # only includes reachable vertices


def predecessor_list(vertices):
    i = len(vertices) - 1
    pilha = []
    pilha.append(vertices[i].get_index())
    while vertices[i].get_index() != 0:
        pilha.append(vertices[i].get_predecessor())
        i = vertices[i].get_predecessor()

    pilha.reverse()

    return pilha


def shortest_path(filename):

    values = get_values_from_matrix(filename)

    n_vertices, matrix = fill_matrix_with_values(values)

    graph = Graph()                                       # initialize graph

    vert = initialize_vertices_and_edges(graph, matrix, n_vertices)

    cloud, vertices = shortest_path_lenghts(graph, vert[0])

    print(filename, 'Value of Shortest Path from Origin to Vertice', (n_vertices - 1), ':', cloud[n_vertices - 1])
    print('Path from Vertice 0 to', (n_vertices - 1), '=>', predecessor_list(vertices), end='\n\n')


def main():

    shortest_path('dij10.txt')

    shortest_path('dij20.txt')

    shortest_path('dij40.txt')

    shortest_path('dij50.txt')


if __name__ == '__main__':
    main()

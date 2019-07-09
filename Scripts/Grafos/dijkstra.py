import numpy as np


class Graph:

    def __init__(self, directed=False):
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing

    def is_directed(self):
        return self._incoming is not self._outgoing

    def vertex_count(self):
        return len(self._outgoing)

    def vertices(self):
        return self._outgoing.keys()

    def edge_count(self):
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        return total if self.is_directed() else total // 2

    def edges(self):
        result = set()
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())
        return result

    def get_edge(self, u, v):
        return self._outgoing[u].get(v)

    def degree(self, v, _outgoing=True):
        adj = self._outgoing if _outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None):  # x=None
        v = self.Vertex(x)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}
        return v

    def insert_edge(self, u, v, x=None):  # x=None
        e = self.Edge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e

    class Vertex:

        def __init__(self, x):
            self._element = x
            self.pred = []

        def element(self):
            return self._element

        def __hash__(self):
            return hash(id(self))

        def att_pred(self, vector):
            self.pred.clear()
            self.pred = [vector.pred, vector.element()]

    class Edge:

        def __init__(self, u, v, x):
            self._origin = u
            self._destination = v
            self._element = x

        def endpoints(self):
            return (self._origin, self._destination)

        def opposite(self, v):
            return self._destination if v is self._origin else self._origin

        def element(self):
            return self._element

        def __hash__(self):
            return hash((self._origin, self._destination))


class PriorityQueueBase:

    class _Item:

        def __init__(self, k, v):
            self._key = k
            self._value = v

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
        # print('j', j)
        # print('parent', parent)
        # print('data[j] key', self._data[j]._key)
        # print('data[parent]', self._data[parent]._key)
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

    class Locator(HeapPriorityQueue._Item):

        def __init__(self, k, v, j):
            super().__init__(k, v)
            self._index = j

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
        token = self.Locator(key, value, len(self._data))
        self._data.append(token)
        self._upheap(len(self._data) - 1)
        return token

    def update(self, loc, newkey, newval):
        j = loc._index
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError('Invalid Locator')
        loc._key = newkey
        loc._value = newval
        self._bubble(j)

    def remove(self, loc):
        j = loc._index
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError('Invalid Locator')
        if j == len(self) - 1:
            self._data.pop()
        else:
            self._swap(j, len(self) - 1)
            self._data.pop()
            self._bubble(j)
        return (loc._key, loc._value)


def shortest_path_lenghts(g, src):
    vert = {}
    d = {}                              # d[v] is upper bound s to v
    cloud = {}                          # map reachable v to its d[v] value
    pq = AdaptableHeapPriorityQueue()   # vertex v will have key d[v]
    pqlocator = {}                      # map from vertex to its pq locator

    for v in g.vertices():
        if v is src:
            d[v] = 0
        else:
            d[v] = float('inf')         # systax for positive  infinity
        pqlocator[v] = pq.add(d[v], v)  # save locator for future updates

    while not pq.is_empty():
        key, u = pq.remove_min()
        cloud[u.element()] = key        # its correct d[u] value
        vert[u.element()] = u
        del pqlocator[u]                # u is no longer in pq
        for e in g.incident_edges(u):   # outgoing edges (u,v)
            v = e.opposite(u)

            if v not in cloud:
                # perform relaxation step on edge (u,v)
                wgt = e.element()
                if d[u] + wgt < d[v]:                       # better path to v?
                    d[v] = d[u] + wgt                       # update the distance
                    v.att_pred(u)                           # update the pred
                    pq.update(pqlocator[v], d[v], v)        # update the pq entry

    return cloud, vert                     # only includes reachable vertices


def shortest_path_tree(g, s, d):
    tree = {}
    for v in d:
        if v is not s:
            for e in g.incident_edges(v, False):
                u = e.opposite(v)
                wgt = e.element()
                if d[v] == d[u] + wgt:
                    print(e)
                    tree[v] = e
    return tree


def shortest_path(filename):

    values = get_values_from_matrix(filename)

    n_vertices, matrix = fill_matrix_with_values(values)

    graph = Graph(directed=True)                                       # initialize graph

    vert = initialize_vertices_and_edges(graph, matrix, n_vertices)

    cloud, d = shortest_path_lenghts(graph, vert[0])
    #print(filename, ' -->  Shortest path from origin to vertice', (n_vertices - 1), ':', cloud)

    print(n_vertices - 1, cloud[n_vertices - 1], d[n_vertices - 1].pred)


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
        vert.append(graph.insert_vertex(x=i))

    for i in range(n_vertices):
        for j in range(n_vertices):
            if j == i:
                continue
            else:
                graph.insert_edge(vert[i], vert[j], matrix[i, j])

    return vert


def main():

    shortest_path('dij10.txt')

    shortest_path('dij20.txt')

    shortest_path('dij40.txt')

    shortest_path('dij50.txt')


if __name__ == '__main__':
    main()

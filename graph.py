from ds2.deque import DoublyLinkedList as Deque


class Graph:
    # V - Vertex
    # E - Edge
    def __init__(self, V, E):
        self.V = set(V)
        self.E = set(frozenset((u, v)) for u, v in E)
        self._neighbors = {}
        for v in V:
            self._neighbors[v] = set()
        for u, v in self.E:
            self._neighbors[u].add(v)
            self._neighbors[v].add(u)

    # Returns the degree of the specified vertex
    def deg(self, v):
        return len(self._neighbors[v])

    # Returns an iterator object with all the neighbors of the given vertex v
    def neighbors(self, v):
        return iter(self._neighbors[v])

    # Returns vertex u if it is in self.V. Also removes all the edges containing the given vertex u
    def remove_vertex(self, u):
        if u in self.V:
            todelete = list(self.neighbors(u))
            for v in todelete:
                self.remove_edge(u, v)
            del self._neighbors[u]
            self.V.remove(u)
        else:
            print("No such vertex exists!")

    # Adds vertex v if it already doesn't exist
    def add_vertex(self, v):
        if v not in self.V:
            self.V.add(v)
            self._neighbors[v] = set()

    # Removes an edge connecting two vertices
    def remove_edge(self, u, v):
        if u in self.V and v in self.V:
            e = frozenset((u, v))
            # Checks to see if such an edge exists
            if e in self.E:
                self.E.remove(e)
                self._neighbors[u].remove(v)
                self._neighbors[v].remove(u)
            else:
                print(f"There is no such edge connecting vertices {u} and {v}!")
        else:
            print("One or all of the vertices are not part of this graph!")

    # Adds an edge connecting two vertices
    def add_edge(self, u, v):
        if u not in self.V:
            self.add_vertex(u)
        if v not in self.V:
            self.add_vertex(v)
        self.E.add(frozenset([u, v]))
        self._neighbors[u].add(v)
        self._neighbors[v].add(u)

    def breadth_first_search(self, v):
        tree = {}
        tovisit = [(None, v)]
        while tovisit:
            a, b = tovisit.pop()
            if b not in tree:
                tree[b] = a
                for c in self.neighbors(b):
                    tovisit.insert(0, (b, c))
        return tree

    def depth_first_search(self, v):
        tree = {}
        tovisit = [(None, v)]
        while tovisit:
            a, b = tovisit.pop()
            if b not in tree:
                tree[b] = a
                for c in self.neighbors(b):
                    tovisit.append((b, c))
        return tree

    def path(self, u, v):
        tree = self.breadth_first_search(v)
        if u in tree:
            path = []
            while u is not None:
                path.append(u)
                u = tree[u]
            return path

    def deque_to_tour(self, deque):
        path = []
        while deque:
            path.append(deque.removefirst())
        return path

    def euler_tour(self, v):
        if self.is_eulerian():
            path = Deque()
            H = Graph(self.V, self.E)
            current_vertex = v
            while len(H.E) > 0:
                if H.deg(current_vertex) > 0:
                    next_vertex = next(H.neighbors(current_vertex))
                    path.addlast(next_vertex)
                    H.remove_edge(current_vertex, next_vertex)
                    current_vertex = next_vertex
                else:
                    current_vertex = path.removefirst()
                    path.addlast(current_vertex)
            dtt = self.deque_to_tour(path)
            return dtt
        else:
            print("The specified graph is not eulerian!")

    def get_any_vertex(self):
        return next(iter(self._neighbors))

    # Checks if the degree of every vertex is greater than 0
    def is_connected(self):
        v = self.get_any_vertex()
        return len(self.depth_first_search(v)) == len(self.V)

    # Checks if there's a possible path between given vertices u and v
    def are_connected(self, u, v):
        return v in self.depth_first_search(u)

    # Check if the current graph is eulerian
    def is_eulerian(self):
        return self.is_connected() and all(self.deg(v) % 2 == 0 for v in self.V)

from random import randint

# ----------------- Graph Class ----------------- #
class Graph:
    """
    Represents a graph using an adjacency list.

    Attributes:
        nv (int): Number of vertices.
        Vertices (list): Adjacency list representation of the graph.
        directed (bool): Indicates if the graph is directed.
        weighted (bool): Indicates if the edges have weights.
    """
    def __init__(self, nv, directed=False, weighted=False):
        self.nv = nv
        self.Vertices = [[] for _ in range(nv)]
        self.directed = directed
        self.weighted = weighted

    def add_edge(self, u, v, weight=0):
        """
        Adds an edge between vertices u and v.

        Args:
            u (int): Starting vertex (1-indexed).
            v (int): Ending vertex (1-indexed).
            weight (float): Edge weight (default is 0).
        """
        u -= 1
        v -= 1
        if self.directed:
            if not self.weighted:
                self.Vertices[u].append(v)
            else:
                self.Vertices[u].append((weight, v))
        else:
            if not self.weighted:
                self.Vertices[u].append(v)
                self.Vertices[v].append(u)
            else:
                self.Vertices[u].append((weight, v))
                self.Vertices[v].append((weight, u))

    def neighbors(self, u):
        """
        Returns the neighbors of vertex u.

        Args:
            u (int): Vertex (1-indexed).

        Returns:
            set: Set of neighbors.
        """
        return set(self.Vertices[u - 1])


# ----------------- Disjoint Set for Kruskal ----------------- #
class DisjointSet:
    """
    Represents a disjoint set used in Kruskal's algorithm.

    Attributes:
        id (int): Set identifier.
        size (int): Number of elements in the set.
        set (list): Elements in the set.
    """
    def __init__(self):
        self.id = -1
        self.size = 0
        self.set = []


# ----------------- EdgeStore (Min Heap-like) ----------------- #
class EdgeStore:
    """
    A custom structure to store and extract the minimum edge efficiently.

    Attributes:
        store (dict): Maps vertex to edge weight.
        size (int): Number of edges in the store.
        in_heap (dict): Tracks if a vertex is in the heap.
    """
    def __init__(self, n):
        self.store = {}
        self.size = 0
        self.in_heap = {i: False for i in range(n)}

    def add(self, edge):
        """
        Adds an edge to the store.

        Args:
            edge (tuple): (vertex, weight)
        """
        self.store[edge[0]] = edge[1]
        self.size += 1
        self.in_heap[edge[0]] = True

    def extract_min(self):
        """
        Extracts the edge with the minimum weight.

        Returns:
            tuple: (weight, vertex)
        """
        items = list(self.store.items())
        min_edge = (-1, float('inf'))
        for e in items:
            if e[1] < min_edge[1]:
                min_edge = e
        weight, vertex = min_edge[1], min_edge[0]
        del self.store[vertex]
        self.size -= 1
        self.in_heap[vertex] = False
        return weight, vertex


# ----------------- Kruskal's Minimum Spanning Tree ----------------- #
def kruskal_mst(G):
    """
    Computes the Minimum Spanning Tree using Kruskal's algorithm.

    Args:
        G (Graph): Input undirected weighted graph.

    Returns:
        float: Total weight of the MST.
    """
    T = Graph(G.nv, False, True)
    sets = [DisjointSet() for _ in range(G.nv)]

    for i in range(G.nv):
        sets[i].id = i
        sets[i].size = 1
        sets[i].set.append(i)

    edges = []
    for i in range(G.nv):
        for v in G.Vertices[i]:
            if i < v[1]:
                edges.append([i, v[1], v[0]])

    edges.sort(key=lambda x: x[2])
    m = 0
    total_weight = 0

    while m < G.nv - 1 and edges:
        u, v, w = edges.pop(0)
        if sets[u].id != sets[v].id:
            T.add_edge(u + 1, v + 1, w)
            total_weight += w
            m += 1

            big = sets[sets[u].id] if sets[sets[u].id].size >= sets[sets[v].id].size else sets[sets[v].id]
            small = sets[u] if big == sets[v] else sets[v]
            big.size += small.size
            big.set += small.set
            for x in small.set:
                sets[x].id = big.id
            small.size = 0
            small.set = []

    return round(total_weight, 2)


# ----------------- Dijkstra's Shortest Path ----------------- #
def dijkstra(G, source):
    """
    Computes shortest paths from the source vertex using Dijkstra's algorithm.

    Args:
        G (Graph): Directed weighted graph.
        source (int): Source vertex (1-indexed).

    Returns:
        list: Distances from source to all vertices.
    """
    parent = [-2] * G.nv
    visited = [False] * G.nv
    dist = [float("inf")] * G.nv

    source -= 1
    visited[source] = True
    dist[source] = 0
    parent[source] = -1

    heap = EdgeStore(G.nv)
    for v in G.Vertices[source]:
        visited[v[1]] = True
        parent[v[1]] = source
        heap.add((v[1], v[0]))

    while heap.size != 0:
        weight, vtx = heap.extract_min()
        dist[vtx] = weight
        for v in G.Vertices[vtx]:
            if not visited[v[1]]:
                visited[v[1]] = True
                parent[v[1]] = vtx
                heap.add((v[1], dist[vtx] + v[0]))
            else:
                in_heap = heap.in_heap.get(v[1], False)
                current = -1 if not in_heap else heap.store[v[1]]
                if current != -1 and dist[vtx] + v[0] < current:
                    parent[v[1]] = vtx
                    heap.store[v[1]] = dist[vtx] + v[0]

    return dist


# ----------------- Connected Components (BFS) ----------------- #
def connected_components(G):
    """
    Finds and prints all connected components of an undirected graph.

    Args:
        G (Graph): Undirected graph.
    """
    visited = [False] * G.nv
    for i in range(G.nv):
        if not visited[i]:
            visited[i] = True
            result = [i + 1]
            queue = [i]
            while queue:
                current = queue.pop(0)
                for v in G.Vertices[current]:
                    if not visited[v]:
                        visited[v] = True
                        queue.append(v)
                        result.append(v + 1)
            result.sort()
            print(" ".join(map(str, result)))


# ----------------- Graph File Generator (.dl format) ----------------- #
def generate_graph(V, E, filename, directed=False, weighted=False):
    """
    Generates a random graph and writes it to a .dl file.

    Args:
        V (int): Number of vertices.
        E (int): Number of edges.
        filename (str): Output filename.
        directed (bool): Whether the graph is directed.
        weighted (bool): Whether the edges are weighted.

    Returns:
        Graph: The generated graph instance.
    """
    g = Graph(V, directed, weighted)
    lines = ["dl\n", "format=edgelist1\n", f"n={V}\n", "data:\n"]
    for _ in range(E):
        u = v = -1
        while v == u or v in g.Vertices[u]:
            u = randint(0, V - 1)
            v = randint(0, V - 1)
        w = round(randint(0, 100000) / 1000, 3)
        if weighted:
            lines.append(f"{u+1} {v+1} {w}\n")
        else:
            lines.append(f"{u+1} {v+1}\n")
        g.add_edge(u + 1, v + 1, w)
    with open(filename, 'w') as f:
        f.writelines(lines)
    return g


# ----------------- Graph Test Runner (from file) ----------------- #
def test_graph(filepath):
    """
    Loads a graph from file and runs Dijkstra's algorithm on it.

    Args:
        filepath (str): Path prefix of the input graph (.dl) and solution file.
    """
    with open(filepath + "_grafo.dl", 'r') as f:
        lines = f.readlines()

    n = int(lines[2].split('=')[1])
    G = Graph(n, True, True)
    for line in lines[4:]:
        u, v, w = line.split()
        G.add_edge(int(u), int(v), float(w))

    with open(filepath + "_solucao.txt", 'r') as f:
        correct = float(f.readline().split()[0])

    dists = dijkstra(G, 1)
    for i, d in enumerate(dists):
        if d == float('inf'):
            print(f"{i+1} INFINITE")
        else:
            print(f"{i+1} {d:.3f}")


# ----------------- CLI Entry Point ----------------- #
if __name__ == "__main__":
    """
    Command-line interface for graph operations.
    """
    print("Graph Suite - Python 🧠")
    print("1. Run Connected Components")
    print("2. Run Kruskal MST")
    print("3. Run Dijkstra")
    print("4. Generate Random Graph")
    print("5. Test Graph from File")
    opt = int(input("Choose option: "))

    if opt == 1:
        print("Enter .dl graph manually (edgelist1 format):")
        input()
        input()
        n = int(input().split('=')[1])
        input()
        G = Graph(n, False, False)
        while True:
            try:
                u, v = map(int, input().split())
                G.add_edge(u, v)
            except EOFError:
                break
        connected_components(G)

    elif opt == 2:
        V = int(input("Vertices: "))
        E = int(input("Edges: "))
        G = generate_graph(V, E, "kruskal_test.dl", False, True)
        weight = kruskal_mst(G)
        print(f"\nMinimum Spanning Tree Weight: {weight:.3f}")

    elif opt == 3:
        V = int(input("Vertices: "))
        E = int(input("Edges: "))
        G = generate_graph(V, E, "dijkstra_test.dl", True, True)
        source = int(input("Source vertex: "))
        dist = dijkstra(G, source)
        for i, d in enumerate(dist):
            print(f"{i+1} {d if d != float('inf') else 'INFINITE'}")

    elif opt == 4:
        V = int(input("Vertices: "))
        E = int(input("Edges: "))
        filename = input("Filename (.dl): ")
        generate_graph(V, E, filename, False, True)
        print(f"Graph written to {filename}")

    elif opt == 5:
        prefix = input("Graph file prefix (without _grafo.dl): ")
        test_graph(prefix)

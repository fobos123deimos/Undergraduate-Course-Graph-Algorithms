from random import randint

# ----------------- Graph Class ----------------- #
class Graph:
    def __init__(self, nv, directed=False, weighted=False):
        self.nv = nv  # Number of vertices
        self.Vertices = [[] for _ in range(nv)]  # Adjacency list
        self.directed = directed  # Whether graph is directed
        self.weighted = weighted  # Whether edges have weights

    # Adds an edge from u to v (1-indexed)
    def add_edge(self, u, v, weight=0):
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

    # Returns neighbors of vertex u (1-indexed)
    def neighbors(self, u):
        return set(self.Vertices[u - 1])


# ----------------- Disjoint Set for Kruskal ----------------- #
class DisjointSet:
    def __init__(self):
        self.id = -1     # Unique set ID
        self.size = 0    # Size of the set
        self.set = []    # Vertices in the set


# ----------------- EdgeStore (Min Heap-like) ----------------- #
class EdgeStore:
    def __init__(self, n):
        self.store = {}            # Maps vertex to its edge weight
        self.size = 0              # Number of elements
        self.in_heap = {i: False for i in range(n)}  # Boolean heap membership

    # Add edge to heap
    def add(self, edge):
        self.store[edge[0]] = edge[1]
        self.size += 1
        self.in_heap[edge[0]] = True

    # Extract edge with minimum weight
    def extract_min(self):
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
    T = Graph(G.nv, False, True)  # Resulting MST
    sets = [DisjointSet() for _ in range(G.nv)]

    # Initialize disjoint sets
    for i in range(G.nv):
        sets[i].id = i
        sets[i].size = 1
        sets[i].set.append(i)

    # Collect all edges
    edges = []
    for i in range(G.nv):
        for v in G.Vertices[i]:
            if i < v[1]:  # Prevent duplicates in undirected graph
                edges.append([i, v[1], v[0]])

    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    m = 0
    total_weight = 0

    # Kruskal’s main loop
    while m < G.nv - 1 and edges:
        u, v, w = edges.pop(0)
        if sets[u].id != sets[v].id:
            T.add_edge(u + 1, v + 1, w)
            total_weight += w
            m += 1

            # Merge sets (union by size)
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
    parent = [-2] * G.nv       # Stores path parent
    visited = [False] * G.nv   # Tracks visited vertices
    dist = [float("inf")] * G.nv  # Shortest distance estimates

    source -= 1
    visited[source] = True
    dist[source] = 0
    parent[source] = -1

    heap = EdgeStore(G.nv)
    for v in G.Vertices[source]:
        visited[v[1]] = True
        parent[v[1]] = source
        heap.add((v[1], v[0]))

    # Main loop of Dijkstra
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

    # You can add comparison logic here if needed


# ----------------- CLI Entry Point ----------------- #
if __name__ == "__main__":
    print("Graph Suite - Python 🧠")
    print("1. Run Connected Components")
    print("2. Run Kruskal MST")
    print("3. Run Dijkstra")
    print("4. Generate Random Graph")
    print("5. Test Graph from File")
    opt = int(input("Choose option: "))

    if opt == 1:
        print("Enter .dl graph manually (edgelist1 format):")
        input()  # "dl"
        input()  # "format=edgelist1"
        n = int(input().split('=')[1])
        input()  # "data:"
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

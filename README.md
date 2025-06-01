# 🎓 Undergraduate Course: Graph Algorithms

This repository contains a set of **Python and C++ implementations** of classical graph algorithms studied in an undergraduate Computer Science course.

> 👨‍🏫 **Professor**: [Prof. Dr. Pablo Mayckon Silva Farias](http://lattes.cnpq.br/7678130748412873)

---

## 🧠 Dependencies & Libraries

The following **standard libraries** were used across the Python and C++ implementations in this repository:

[![C++](https://img.shields.io/badge/C++17-supported-00599C?style=flat-square&logo=c%2B%2B&logoColor=white)](https://en.cppreference.com/) [![g++](https://img.shields.io/badge/g++-14.2.0-00599C?style=flat-square&logo=c%2B%2B&logoColor=white)](https://gcc.gnu.org/) [![gcc](https://img.shields.io/badge/gcc-14.2.0-F34B7D?style=flat-square&logo=gnu&logoColor=white)](https://gcc.gnu.org/) [![Python](https://img.shields.io/badge/Python-3.11.5-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3115/) [![C++ STL](https://img.shields.io/badge/C++-STL-00599C?style=flat-square&logo=cplusplus&logoColor=white)](https://en.cppreference.com/w/cpp) [![C++ IOStream](https://img.shields.io/badge/C++-IOStream-00599C?style=flat-square&logo=cplusplus&logoColor=white)](https://en.cppreference.com/w/cpp/io) [![C++ Vector](https://img.shields.io/badge/C++-Vector-00599C?style=flat-square&logo=cplusplus&logoColor=white)](https://en.cppreference.com/w/cpp/container/vector) [![C++ List](https://img.shields.io/badge/C++-List-00599C?style=flat-square&logo=cplusplus&logoColor=white)](https://en.cppreference.com/w/cpp/container/list) [![Python Random](https://img.shields.io/badge/Python-Random-3776AB?style=flat-square&logo=python&logoColor=white)](https://docs.python.org/3/library/random.html)


### ✅ Main Usage per File:

| File                                | Libraries                                                       |
| ------------------------------------ | ---------------------------------------------------------------- |
| `graph_suite.py`                    | Python Random (Standard Library)                                 |
| `AdjacencyGraph.hpp`                | C++ STL, IOStream                                                |
| `ConnectedComponents.cpp`           | C++ STL, IOStream, Vector, List                                  |

---

## 📘 Mathematical Background

### 📐 Graph Definitions

A **graph** is defined as a pair:

$$G = (V, E)$$

- $V$: a finite set of **vertices** or **nodes**
- $E \subseteq V \times V$: a set of **edges** (can be directed or undirected)

A graph may be:
- **Directed**: edges are ordered pairs $(u, v)$
- **Undirected**: edges are unordered pairs $\{u, v\}$
- **Weighted**: edges have associated values $w(u, v) \in \mathbb{R}$

---

## 🚀 Algorithms

### 🔍 Connected Components

- **Description**: Finds all maximal sets of connected nodes in an undirected graph.
- **Complexity**:
  - BFS/DFS: $O(V + E)$
  - Union-Find: near $O(E \cdot \alpha(V))$ where $\alpha$ is the inverse Ackermann function.
- **Applications**:
  - Image segmentation
  - Social network analysis
  - Cluster detection
- **References**:
  - Cormen et al., *Introduction to Algorithms*, 3rd Ed., Chapter 22
  - Tarjan, *Efficiency of a Good But Not Linear Set Union Algorithm* (1975)

---

### 🧮 Dijkstra’s Algorithm

- **Description**: Computes shortest paths from a source to all vertices in a graph with non-negative weights.
- **Complexity**:
  - With binary heap: $O((V + E) \cdot \log V)$
  - With Fibonacci heap: $O(E + V \cdot \log V)$
- **Applications**:
  - GPS navigation
  - Network routing
  - Game AI pathfinding
- **References**:
  - Dijkstra, *A Note on Two Problems in Connexion with Graphs* (1959)
  - Cormen et al., *Introduction to Algorithms*, 3rd Ed., Chapter 24

---

### 🌲 Kruskal’s Algorithm (MST)

- **Description**: Finds the minimum spanning tree of a connected, undirected, weighted graph.
- **Complexity**:
  - $O(E \cdot \log E)$, dominated by edge sorting.
- **Applications**:
  - Network design (e.g., telecom, electric grids)
  - Cluster analysis
  - Image segmentation
- **References**:
  - Kruskal, *On the Shortest Spanning Subtree of a Graph and the Traveling Salesman Problem* (1956)
  - Cormen et al., *Introduction to Algorithms*, 3rd Ed., Chapter 23

---

## 📦 Repository Structure

This repository provides **implementations**, **generators**, and **test routines** for several classic graph algorithms, coded with an educational perspective in mind.

---

### 🔧 `graph_suite.py`

> 🐍 A complete all-in-one Python script containing:

- Graph creation (directed/undirected, weighted/unweighted)
- Connected components (BFS)
- Kruskal’s MST
- Dijkstra’s shortest path
- Graph generator to `.dl` format
- CLI for educational testing

---

### 🧱 `AdjacencyGraph.hpp`

> 🧩 A C++ header file defining a **template-based graph structure** using **adjacency lists**.

**Features:**
- Struct-based `Graph` and `Node` definitions
- Graph initialization with dynamic memory
- Edge insertion for **directed graphs**
- Memory cleanup function (`Destroy_Graph`)

**Mathematical Insight:**

A graph $G = (V, E)$ is stored as an **array of linked lists**:

$$\text{Adj}[u] = \{ v \in V \mid (u, v) \in E \}$$

This structure supports:
- Fast iteration over neighbors $O(\deg(v))$
- Efficient edge insertions $O(1)$
- Memory-efficient representation for **sparse graphs**

**Reference to Adjacency Representation:**
- Sedgewick, *Algorithms in C, Part 5: Graph Algorithms*

---

### 💻 `ConnectedComponents.cpp`

> 🧱 C++ implementation of:
- Adjacency list using raw pointers
- Manual component merging for finding connected components
- Memory allocation and deallocation routines

Ideal for practicing **low-level data structure handling**.

---

### 📂 `.dl File Format`

Most examples use the Pajek-compatible `.dl` format:

```
dl
format=edgelist1
n=5
data:
1 2
1 3
2 4
3 5
```

---

## 📎 Test Examples

Below are small test cases to validate the main algorithms implemented in the repository.

---

### 🧪 Connected Components (C++)

**Input (`stdin`) in `.dl` format:**

```
dl
format=edgelist1
n=6
data:
1 2
2 3
4 5
```

**Expected Output (`stdout`):**

```
1 2 3 
4 5 
6
```

**How to run:**

```bash
g++ ConnectedComponents.cpp -o cc
./cc  input_file.dl
```

---

### 🧪 Kruskal’s MST (Python)

**Example Python usage:**

```python
from graph_suite import generate_graph, kruskal_mst

G = generate_graph(5, 6, "kruskal_test.dl", directed=False, weighted=True)
mst_weight = kruskal_mst(G)
print(f"MST weight: {mst_weight}")
```

**Expected output (varies due to randomness):**

```
MST weight: 8.732
```

To test with a fixed graph, manually define the edges instead of using `generate_graph()`.

---

### 🧪 Dijkstra’s Algorithm (Python)

**Input graph:**

```python
from graph_suite import Graph, dijkstra

G = Graph(5, directed=True, weighted=True)
G.add_edge(1, 2, 2.0)
G.add_edge(1, 3, 5.0)
G.add_edge(2, 3, 1.0)
G.add_edge(2, 4, 2.5)
G.add_edge(4, 5, 1.5)

distances = dijkstra(G, source=1)
print(distances)
```

**Expected Output:**

```
[0, 2.0, 3.0, 4.5, 6.0]
```

---

### 🧪 Graph Generation (`.dl`)

Generate a random graph and inspect its structure:

```python
generate_graph(4, 4, "example_graph.dl", directed=False, weighted=True)
```

**Example `.dl` Output:**

```
dl
format=edgelist1
n=4
data:
1 3 7.421
1 2 3.057
2 4 5.111
3 4 6.228
```

You can then use this file with `ConnectedComponents.cpp` or other compatible readers.

---

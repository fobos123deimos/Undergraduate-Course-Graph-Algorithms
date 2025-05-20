# 🎓 Undergraduate Course: Graph Algorithms

This repository contains a set of **Python and C++ implementations** of classical graph algorithms studied in an undergraduate Computer Science course.

> 👨‍🏫 **Professor**: [Prof. Dr. Pablo Mayckon Silva Farias]( http://lattes.cnpq.br/7678130748412873)

---

## 📘 Mathematical Background

### 📐 Graph Definitions

A **graph** is defined as a pair:

\[
G = (V, E)
\]

- \( V \): a finite set of **vertices** or **nodes**
- \( E \subseteq V \times V \): a set of **edges** (can be directed or undirected)

A graph may be:
- **Directed**: edges are ordered pairs \((u, v)\)
- **Undirected**: edges are unordered pairs \(\{u, v\}\)
- **Weighted**: edges have associated values \( w(u, v) \in \mathbb{R} \)

### 🧩 Connected Components

A **connected component** in an undirected graph is a maximal set \( C \subseteq V \) such that:

\[
\forall u, v \in C,\quad \exists \text{ a path from } u \text{ to } v
\]

Implemented using:
- **Breadth-First Search (BFS)**
- **Disjoint-set merging**

### 🧮 Dijkstra’s Algorithm

Solves the **single-source shortest path problem** for graphs with non-negative edge weights.

**Goal**: Given a graph \( G = (V, E) \) and source node \( s \), compute:

\[
\forall v \in V, \quad d(s, v) = \min_{\text{paths } P} \sum_{(u,v) \in P} w(u,v)
\]

Implemented with:
- Greedy selection of the next node via **custom heap**
- Edge relaxation

### 🌲 Kruskal’s Algorithm (MST)

Finds a **minimum spanning tree** of a connected, undirected, weighted graph.

Given:

\[
G = (V, E), \quad w: E \rightarrow \mathbb{R}
\]

Kruskal constructs a subgraph \( T = (V, E_T) \) such that:
- \( T \) is connected
- \( T \) is acyclic
- \( |E_T| = |V| - 1 \)
- Total weight is minimized:

\[
\sum_{(u,v) \in E_T} w(u,v) = \min
\]

Uses **Union-Find (Disjoint Set)** to avoid cycles.

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

A graph \( G = (V, E) \) is stored as an **array of linked lists**:

\[
\text{Adj}[u] = \{ v \in V \mid (u, v) \in E \}
\]

This structure supports:
- Fast iteration over neighbors \( O(\deg(v)) \)
- Efficient edge insertions \( O(1) \)
- Memory-efficient representation for **sparse graphs**

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

```text
dl
format=edgelist1
n=5
data:
1 2
1 3
2 4

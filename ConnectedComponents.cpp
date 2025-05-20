#include <iostream>
#include <stdio.h>
#include <vector>
#include <list>

using std::nothrow;
using std::cout;
using std::cin;
using std::list;
using std::vector;

// Node structure for adjacency list
template<typename>
struct Node {
	int index;
	Node<int>* next;
};

// Graph structure using adjacency list representation
struct Graph { 
	int nVertices;           // Number of vertices
	Node<int>** Vertices;    // Array of adjacency lists
};

// Function to initialize a graph with a given number of vertices
bool Initialize_Graph(Graph& G, int nVertices)
{
	if (nVertices >= 1) {
		G.nVertices = nVertices;
		G.Vertices = new(nothrow) Node<int>*[nVertices - 1]; // ⚠️ Bug: should be [nVertices]

		if (G.Vertices) {
			for (int i = 0; i < nVertices; ++i)
				G.Vertices[i] = NULL;
			return false; // false = success
		}
		return true; // Allocation failed
	}
	return true; // Invalid number of vertices
}

// Function to add a directed edge from u to v
bool Add_Edge(Graph& G, int u, int v)
{
	Node<int>* n = new(nothrow) Node<int>;
	if (n) {
		n->index = v - 1;               // Adjust index to 0-based
		n->next = G.Vertices[u - 1];    // Insert at beginning of list
		G.Vertices[u - 1] = n;
		return false; // Edge added successfully
	}
	return true; // Memory allocation failed
}

// Function to release all memory used by the graph
void Destroy_Graph(Graph& G)
{
	for (int i = 0; i < G.nVertices; ++i) {
		Node<int>* n = G.Vertices[i];
		while (n) {
			Node<int>* temp = n;
			n = n->next;
			delete temp;
		}
	}
	delete[] G.Vertices;
}

// Structure representing a set/component of vertices
struct Component {
	list<int> elements; // Vertices in the component
	int pos;            // Position identifier (acts like parent ID)
};

int main() {

	// Step 1: Read number of vertices
	int n = -1;
	do {
		cout << "dl\n";
		cout << "format=edgelist1\n";
		cout << "n=";
		scanf("%d", &n);
	} while (n < 0);

	// Step 2: Initialize the graph
	Graph G;
	int MAX_EDGES = (n * (n - 1) / 2); // Maximum possible edges in undirected graph
	bool result = Initialize_Graph(G, n);
	
	if (!result) {

		// Step 3: Read edges until EOF or max edges reached
		cout << "data:\n";
		int edge_count = 0;
		while (edge_count < MAX_EDGES) {
			int u, v;
			cin >> u >> v;
			if (cin.eof()) break;

			if ((u <= n && v <= n) && (u > 0 && v > 0)) {
				Add_Edge(G, u, v);
				++edge_count;
			}
		}

		// Step 4: Initialize one component per vertex
		vector<Component> Components(G.nVertices);
		for (int i = 0; i < G.nVertices; ++i) {
			Component C;
			C.elements.push_back(i + 1);
			C.pos = i;
			Components[i] = C;
		}

		// Step 5: Merge components based on graph edges
		Node<int>* p;
		for (int i = 0; i < G.nVertices; ++i) {
			for (p = G.Vertices[i]; p; p = p->next) {
				// Skip if both are already in the same component
				if (Components[p->index].pos == i || Components[p->index].pos == Components[i].pos) {
					continue;
				} else {
					// Merge if both are isolated (initial components)
					if (Components[i].elements.size() == 1 && Components[p->index].elements.size() == 1) {
						int greater = i >= p->index ? i : p->index;
						int lesser = (greater == i) ? p->index : i;
						Components[lesser].elements.merge(Components[greater].elements);
						Components[greater].pos = Components[lesser].pos;
					} else {
						// Merge based on size - like union by size heuristic
						if (!Components[Components[i].pos].elements.empty() && !Components[Components[p->index].pos].elements.empty()) {
							int greater = Components[Components[i].pos].elements.size() >= Components[Components[p->index].pos].elements.size() ? Components[i].pos : Components[p->index].pos;
							int lesser = (greater == Components[i].pos) ? Components[p->index].pos : Components[i].pos;
							Components[greater].elements.merge(Components[lesser].elements);
							Components[lesser].pos = Components[greater].pos;
						}
					}
				}
			}
		}

		// Step 6: Output all components (connected components of the graph)
		cout << "\n";
		for (int i = 0; i < G.nVertices; ++i) {
			if (!Components[i].elements.empty()) {
				for (list<int>::iterator it = Components[i].elements.begin(); it != Components[i].elements.end(); ++it) {
					cout << *it << " ";
				}
				cout << "\n";
			}
		}
	}

	return 0;
	// To solve using shortest paths algorithms in the future
};

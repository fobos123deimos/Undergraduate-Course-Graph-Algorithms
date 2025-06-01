#include <iostream>
#include <stdio.h>
#include <vector>
#include <list>

using std::nothrow;
using std::cout;
using std::cin;
using std::list;
using std::vector;

/**
 * @brief Template for a generic node used in adjacency lists.
 * 
 * @tparam T Unused template type (provided for generality).
 */
template<typename>
struct Node {
	int index;           ///< Index of the adjacent vertex (0-based)
	Node<int>* next;     ///< Pointer to the next node in the adjacency list
};

/**
 * @brief Structure representing a graph using adjacency list representation.
 */
struct Graph { 
	int nVertices;           ///< Total number of vertices
	Node<int>** Vertices;    ///< Array of adjacency list heads (one per vertex)
};

/**
 * @brief Initializes a graph with a given number of vertices.
 * 
 * Allocates memory for the adjacency list structure and sets all heads to NULL.
 * 
 * @param G Reference to the graph to be initialized.
 * @param nVertices Number of vertices in the graph.
 * @return true if memory allocation fails or the number of vertices is invalid; false on success.
 * 
 */
bool Initialize_Graph(Graph& G, int nVertices)
{
	if (nVertices >= 1) {
		G.nVertices = nVertices;
		G.Vertices = new(nothrow) Node<int>*[nVertices - 1];

		if (G.Vertices) {
			for (int i = 0; i < nVertices; ++i)
				G.Vertices[i] = NULL;
			return false; // false = success
		}
		return true; // allocation failed
	}
	return true; // invalid number of vertices
}

/**
 * @brief Adds a directed edge from vertex u to vertex v.
 * 
 * @param G Reference to the graph.
 * @param u Source vertex (1-based index).
 * @param v Destination vertex (1-based index).
 * @return true if memory allocation fails; false if the edge is added successfully.
 */
bool Add_Edge(Graph& G, int u, int v)
{
	Node<int>* n = new(nothrow) Node<int>;
	if (n) {
		n->index = v - 1;
		n->next = G.Vertices[u - 1];
		G.Vertices[u - 1] = n;
		return false; // edge added successfully
	}
	return true; // memory allocation failed
}

/**
 * @brief Releases all memory used by the graph.
 * 
 * Deallocates all adjacency lists and the array of list heads.
 * 
 * @param G Reference to the graph to destroy.
 */
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

/**
 * @brief Structure representing a connected component of the graph.
 * 
 * Stores a list of vertices and a representative position (similar to a parent pointer in disjoint sets).
 */
struct Component {
	list<int> elements; ///< Vertices in the component
	int pos;            ///< Representative position (component ID)
};

/**
 * @brief Main function for reading a graph and printing its connected components.
 * 
 * Workflow:
 * 1. Read number of vertices (in .dl format)
 * 2. Initialize graph structure
 * 3. Read edges until EOF
 * 4. Build disjoint components
 * 5. Merge components using adjacency list information
 * 6. Output each connected component
 * 
 * @return int Exit code.
 */
int main() {

	// Step 1: Read number of vertices from input
	int n = -1;
	do {
		cout << "dl\n";
		cout << "format=edgelist1\n";
		cout << "n=";
		scanf("%d", &n);
	} while (n < 0);

	// Step 2: Initialize graph structure
	Graph G;
	int MAX_EDGES = (n * (n - 1) / 2); // Max edges for undirected graph
	bool result = Initialize_Graph(G, n);
	
	if (!result) {

		// Step 3: Read edges from input (edgelist1 format)
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

		// Step 4: Initialize components (one per vertex)
		vector<Component> Components(G.nVertices);
		for (int i = 0; i < G.nVertices; ++i) {
			Component C;
			C.elements.push_back(i + 1);
			C.pos = i;
			Components[i] = C;
		}

		// Step 5: Merge components based on graph connectivity
		Node<int>* p;
		for (int i = 0; i < G.nVertices; ++i) {
			for (p = G.Vertices[i]; p; p = p->next) {
				if (Components[p->index].pos == i || Components[p->index].pos == Components[i].pos) {
					continue;
				} else {
					if (Components[i].elements.size() == 1 && Components[p->index].elements.size() == 1) {
						int greater = i >= p->index ? i : p->index;
						int lesser = (greater == i) ? p->index : i;
						Components[lesser].elements.merge(Components[greater].elements);
						Components[greater].pos = Components[lesser].pos;
					} else {
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

		// Step 6: Output all non-empty components
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
}

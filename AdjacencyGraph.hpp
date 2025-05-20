#include <iostream>
using std::nothrow;

// Template for a generic node, specialized below as int
template<typename>
struct Node {
	int index;
	Node<int>* next;
};

// Structure representing a graph using adjacency lists
struct Graph {
	int nVertices;       // Number of vertices in the graph
	Node<int>** Vertices; // Array of pointers to adjacency lists
};

// Function to initialize the graph with a given number of vertices
bool Initialize_Graph(Graph& G, int nVertices)
{
	if (nVertices >= 1) {
		G.nVertices = nVertices;
		// Allocate an array of pointers for each vertex
		G.Vertices = new(nothrow) Node<int>*[nVertices - 1];
		
		if (G.Vertices) {
			// Initialize all adjacency list heads to NULL
			for (int i = 0; i < nVertices; ++i) {
				G.Vertices[i] = NULL;
			}
			return false; // Return false to indicate success (strange convention!)
		}
		return true; // Allocation failed
	}
	return true; // Invalid number of vertices
}

// Function to add an edge from vertex u to vertex v
bool Add_Edge(Graph& G, int u, int v)
{
	Node<int>* n = new(nothrow) Node<int>;
	if (n) {
		n->index = v - 1;
		n->next = G.Vertices[u - 1];
		G.Vertices[u - 1] = n;
		return false; // Edge added successfully
	}
	return true; // Memory allocation failed
}

// Function to deallocate all memory used by the graph
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

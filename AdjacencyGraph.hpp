#include <iostream>
using std::nothrow;

/**
 * @brief Template for a generic linked list node.
 * 
 * Specialized below as Node<int> to be used in graph adjacency lists.
 * 
 * @tparam T Data type for the node (not used here).
 */
template<typename>
struct Node {
	int index;             ///< Index of the adjacent vertex
	Node<int>* next;       ///< Pointer to the next node in the list
};

/**
 * @brief Structure representing a graph using adjacency lists.
 */
struct Graph {
	int nVertices;           ///< Number of vertices in the graph
	Node<int>** Vertices;    ///< Array of adjacency list heads (one per vertex)
};

/**
 * @brief Initializes a graph with a given number of vertices.
 * 
 * Allocates memory for the adjacency list array and sets all pointers to NULL.
 * 
 * @param G Reference to the Graph to initialize.
 * @param nVertices Number of vertices to allocate.
 * @return true if there was an error (e.g., invalid size or allocation failure), false otherwise.
 * 
 * @note Returns false to indicate success, which is an unusual but consistent convention in this code.
 */
bool Initialize_Graph(Graph& G, int nVertices)
{
	if (nVertices >= 1) {
		G.nVertices = nVertices;
		G.Vertices = new(nothrow) Node<int>*[nVertices - 1];

		if (G.Vertices) {
			for (int i = 0; i < nVertices; ++i) {
				G.Vertices[i] = NULL;
			}
			return false; // Initialization successful
		}
		return true; // Allocation failed
	}
	return true; // Invalid number of vertices
}

/**
 * @brief Adds a directed edge from vertex u to vertex v.
 * 
 * Creates a new node in the adjacency list of vertex u pointing to vertex v.
 * 
 * @param G Reference to the graph.
 * @param u Starting vertex (1-indexed).
 * @param v Ending vertex (1-indexed).
 * @return true if memory allocation failed, false if edge was added successfully.
 */
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

/**
 * @brief Frees all memory associated with the graph.
 * 
 * Iterates through each adjacency list and deallocates all nodes,
 * then deallocates the array of adjacency lists itself.
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

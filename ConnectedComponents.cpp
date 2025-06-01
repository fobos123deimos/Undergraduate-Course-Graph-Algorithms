#include <iostream>
#include <fstream>
#include <sstream>
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
 * @return int Exit code.
 */
int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: ./cc <filename.dl>\n";
        return 1;
    }

    std::ifstream file(argv[1]);
    if (!file) {
        std::cerr << "Could not open file: " << argv[1] << "\n";
        return 1;
    }

    // Step 1: Read header
    std::string line, header, format, n_line;
    std::getline(file, header);       // "dl"
    std::getline(file, format);       // "format=edgelist1"
    std::getline(file, n_line);       // "n=6"

    int n = -1;
    if (n_line.rfind("n=", 0) == 0) {
        n = std::stoi(n_line.substr(2));
    }

    if (n < 0) {
        std::cerr << "Invalid number of vertices.\n";
        return 1;
    }

    std::getline(file, line); // skip "data:"

    // Step 2: Initialize graph
    Graph G;
    int MAX_EDGES = (n * (n - 1) / 2);
    bool result = Initialize_Graph(G, n);

    if (!result) {
        // Step 3: Read edges
        int edge_count = 0;
        while (std::getline(file, line) && edge_count < MAX_EDGES) {
            if (line.empty()) continue;
            std::istringstream iss(line);
            int u, v;
            iss >> u >> v;
            if ((u <= n && v <= n) && (u > 0 && v > 0)) {
                Add_Edge(G, u, v);
                ++edge_count;
            }
        }

        // Step 4: Initialize components
        std::vector<Component> Components(G.nVertices);
        for (int i = 0; i < G.nVertices; ++i) {
            Component C;
            C.elements.push_back(i + 1);
            C.pos = i;
            Components[i] = C;
        }

        // Step 5: Merge components
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
                        if (!Components[Components[i].pos].elements.empty() &&
                            !Components[Components[p->index].pos].elements.empty()) {
                            int greater = Components[Components[i].pos].elements.size() >=
                                          Components[Components[p->index].pos].elements.size()
                                              ? Components[i].pos
                                              : Components[p->index].pos;
                            int lesser = (greater == Components[i].pos) ? Components[p->index].pos
                                                                        : Components[i].pos;
                            Components[greater].elements.merge(Components[lesser].elements);
                            Components[lesser].pos = Components[greater].pos;
                        }
                    }
                }
            }
        }

        // Step 6: Output components
        std::cout << "\n";
        for (int i = 0; i < G.nVertices; ++i) {
            if (!Components[i].elements.empty()) {
                for (std::list<int>::iterator it = Components[i].elements.begin();
                     it != Components[i].elements.end(); ++it) {
                    std::cout << *it << " ";
                }
                std::cout << "\n";
            }
        }
    }

    return 0;
}
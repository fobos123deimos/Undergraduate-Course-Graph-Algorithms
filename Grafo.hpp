#include <iostream>
using std::nothrow;

template<typename>
struct No{
	int indice;
	No<int> *prox;
};


struct Grafo { 
	int nvertices;  
	No<int> **Vertices; 
};


bool Inicializar_Grafo (Grafo &G, int nvertices)
{
    if(nvertices>=1){
	   G.nvertices = nvertices;
       G.Vertices = new(nothrow) No<int>* [nvertices-1];
       if (G.Vertices){
           int i; 
   	       for(i = 0; i < nvertices; ++i) G.Vertices[i] = NULL;
	       return false;
       }return true;
    }return true;
}

bool Adicionar_Aresta (Grafo &G, int u, int v)
{
   No<int> *n = new(nothrow) No<int>;
   if (n){   
   	   n->indice = v-1;n->prox = G.Vertices[u-1];  
	   G.Vertices[u-1] = n;  return false; 
	}return true;
} 

void Terminar_Grafo (Grafo &G)
{
	for (int i = 0; i < G.nvertices; ++i){  
		No<int> *n = G.Vertices[i];  
		while (n){ 
			No<int> *a = n; 
			n = n->prox; 
			delete a; 
		}  
	}delete[] G.Vertices;
}

//Remoção de Arestas
//Grafo_Vazio1: Sem Vertices; Grafo_Vazio2: Sem Arestas    
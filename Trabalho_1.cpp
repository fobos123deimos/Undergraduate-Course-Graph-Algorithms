#include <iostream>
#include <stdio.h>
#include <vector>
#include <list>

using std::nothrow;
using std::cout;
using std::cin;
using std::list;
using std::vector;

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

struct Conjunto{
    list<int> Conj;
    int pos;
};

int main(){
	
	//Vértices
	int n = -1;
	do{
  	    cout << "dl\n";
	    cout << "format=edgelist1\n";
	    cout << "n=";
	    scanf("%d",&n);
	}while(n<0);
	
	//Cria Grafo
	Grafo G;
	int MAX_AR = (n*(n-1)/2);
	bool VALOR = Inicializar_Grafo(G,n);
	if(!VALOR){
	//Arestas
	cout << "data:\n";
	int n_aresta = 0;
	while(n_aresta<MAX_AR){
		int u,v;
		cin >> u >> v;
		if(cin.eof()) break;
		if((u<=n && v<=n)&&(u>0 && v>0)){
		    Adicionar_Aresta(G,u,v);
		    ++n_aresta;
		}
	}
	//Inicializo as Componentes Elementares em Cpts
	vector<Conjunto> Cpts(G.nvertices);
	int i;
	for(i=0;i<G.nvertices;++i){
		Conjunto Comp; Comp.Conj.push_back(i+1);Comp.pos = i;
		Cpts[i] = Comp;
	}


     No<int> *p;
	//Montagem das Componentes a partir das arestas do Grafo
	for(i=0;i<G.nvertices;++i){
		for(p=G.Vertices[i];p;p=p->prox){
			if(Cpts[p->indice].pos==i||Cpts[p->indice].pos==Cpts[i].pos){continue;}
                        else{
			    if(Cpts[i].Conj.size()==1 && Cpts[p->indice].Conj.size()==1){
				        int MAIOR = i>=p->indice?i:p->indice;
				        int MENOR = MAIOR==i?p->indice:i;
				        Cpts[MENOR].Conj.merge(Cpts[MAIOR].Conj);
				        Cpts[MAIOR].pos = Cpts[MENOR].pos;

	    		    }else{
	    			if(Cpts[Cpts[i].pos].Conj.size()!=0 && Cpts[Cpts[p->indice].pos].Conj.size()!=0){
					    int MAIOR = Cpts[Cpts[i].pos].Conj.size()>=Cpts[Cpts[p->indice].pos].Conj.size()?Cpts[i].pos:Cpts[p->indice].pos;
                                            int MENOR = MAIOR==Cpts[i].pos?Cpts[p->indice].pos:Cpts[i].pos;
                                            Cpts[MAIOR].Conj.merge(Cpts[MENOR].Conj);
                                            Cpts[MENOR].pos = Cpts[MAIOR].pos;

					}
				}
			}
			
		}
	}	
	cout << "\n";
	for(i=0;i<G.nvertices;++i){
	     if(!Cpts[i].Conj.empty()){
              for (list<int>::iterator it=Cpts[i].Conj.begin(); it!=Cpts[i].Conj.end();++it){
                   cout <<*it<<" ";
              }cout << "\n";
            }
       }
    }   
    return 0;
    //Resolver utilizando caminhos minimos
} 

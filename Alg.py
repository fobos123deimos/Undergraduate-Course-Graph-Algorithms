from random import randint

class Grafo(object):

    def __init__(self,nv,D=False,Pond=False):
        self.nv = nv
        self.Vertices = [[] for _ in range(self.nv)]
        self.D = D
        self.Pond = Pond

    def aresta(self,u,v,peso=0):
        if(self.D):
            if(not(self.Pond)): self.Vertices[u-1].append(v-1)
            else: self.Vertices[u-1].append((peso,v-1))
        else:
            if(not(self.Pond)):
                self.Vertices[u-1].append(v-1)
                self.Vertices[v-1].append(u-1)
            else:
                self.Vertices[u-1].append((peso,v-1))
                self.Vertices[v-1].append((peso,u-1))

    def Vizinhos(self,u):
        viz = []
        for i in range(len(self.Vertices[u-1])):
            viz.append(self.Vertices[u-1][i])
        return set(viz)


class Conjunto(object):

    def __init__(self):
        self.id = -1
        self.Tam = 0
        self.Conj = []


class Armz_Edg(object):
    
    def __init__(self,n):
        self.Armz = {}
        self.Tam =0 
        self.Table = {0:False}
    def Adc(self,edg):
        self.Armz[edg[0]] = edg[1]
        self.Tam+=1
        self.Table[edg[0]] = True
        
    def Men(self):
        aux = list(self.Armz.items())
        val = (-1,float('inf'))
        for ar in aux:
            if(val[1]>ar[1]):
                val = ar
                
        peso = val[1]
        vt = val[0]
        del(self.Armz[vt])
        self.Tam-=1
        self.Table[vt] = False
        return peso,vt


#Precisa de Revisões
def Gerar_Grafo(Vert,Art,nome,Dirig=False,pond=False,variante=1,G=Grafo(0)):
    arquivo = open(nome, 'w+')
    arquivo.close()
    g = 0
    if(variante==1):
        if(Dirig and pond):
            g = Grafo(Vert,True,True)
        elif(Dirig and not(pond)):
            g = Grafo(Vert,True)
        elif(not(Dirig) and pond):
             g = Grafo(Vert,False,True)
        else:
            g = Grafo(Vert)
    elif(variante==2):
        g = G
    Aq = open(nome, 'w')
    texto = []
    texto.append("dl\n")
    texto.append("format=edgelist1\n")
    texto.append("n="+str(g.nv)+"\n")
    texto.append("data:\n")
    if(variante==1):
        for _ in range(Art):
            u = -1
            v = -1
            while(v in g.Vertices[u] or v==u):
                u = randint(0,g.nv-1)
                v = randint(0,g.nv-1)

            p = randint(0,100000)/1000
            if(g.Pond):
                texto.append(str(u+1)+" "+str(v+1)+" "+str(p)+"\n")
            else:
                texto.append(str(u+1)+" "+str(v+1)+"\n")
            g.aresta(u+1,v+1,p)

        Aq.writelines(texto)
        Aq.close()
        return g
    elif(variante==2):
        for i in range(g.nv):
            for v in g.Vertices[i]:
                if(g.Pond):
                    texto.append(str(i+1)+" "+str(v[1]+1)+" "+str(v[0])+"\n")
                else:
                    texto.append(str(i+1)+" "+str(v+1)+"\n")
                    
        Aq.writelines(texto)
        Aq.close()
        return g
                

#talvez  criar uma Classe Conjunto para o algoritmo de Kruskal
#Implementar depois o algoritmo de kruskal
#Passar os algoritmos em c++ para python
    
def AGM_k(G):
    
    T = Grafo(G.nv,False,True)
    L = [Conjunto() for _ in range(G.nv)]
    
    for i in range(len(L)):
        L[i].id = i
        L[i].Tam = 1
        L[i].Conj.append(i)
    E = []
    
    for i in range(len(G.Vertices)):
        for v in G.Vertices[i]:
            if(i<v[1]):
                E.append([i,v[1],v[0]])
        
                
    E = sorted(E,key = lambda f:f[2])
    m = 0
    P = 0
    while(m<G.nv-1):
        u = E[0][0]
        v = E[0][1]
        peso = E[0][2]
        if(L[u].id!=L[v].id):
            T.aresta(u+1,v+1,peso)
            P += peso
            m+=1
            MAIOR = Conjunto()
            MENOR = Conjunto()
            if(L[L[u].id].Tam<L[L[v].id].Tam):
                MAIOR=L[L[v].id]
                MENOR=L[L[u].id]
            else:
                MAIOR=L[L[u].id]
                MENOR=L[L[v].id]
                
            MAIOR.Tam += MENOR.Tam
            MAIOR.Conj += MENOR.Conj
            for u in MENOR.Conj: L[u].id = MAIOR.id
            MENOR.Tam = 0
            MENOR.Conj = []
            
        del(E[0])

    return round(P,2)
            



def Cam_Min(G,o):

    Pai = [-2 for _ in range(len(G.Vertices))]
    Atg = [False for _ in range(len(G.Vertices))]
    d = [float("inf") for _ in range(len(G.Vertices))]
    
    Atg[o-1] = True
    d[o-1] = 0
    Pai[o-1] = -1

    H = Armz_Edg(G.nv)
    for v in G.Vertices[o-1]:
        Atg[v[1]] = True
        Pai[v[1]] = o-1
        H.Adc((v[1],v[0]))


    while(H.Tam!=0):
        peso,vt = H.Men()
        d[vt]=peso
        for v in G.Vertices[vt]:
            if(not(Atg[v[1]])):
                Atg[v[1]] = True
                Pai[v[1]] = vt
                H.Adc((v[1],d[vt]+v[0]))
            else:
                EA = H.Table[v[1]]
                peso = -1 if(not(EA)) else H.Armz[v[1]]
                if(not(peso==-1) and d[vt]+v[0]<peso):
                    Pai[v[1]]=vt
                    H.Armz[v[1]] = d[vt]+v[0]
    
    return d

def Componentes(G):

    Atg = [False for _ in range(G.nv)]
    
    for i in range(G.nv):
        if(not(Atg[i])):
            Atg[i] = True
            prt = str(i+1)
            Fila = []
            Fila.append(i)
            while(len(Fila)!=0):
                frente = Fila.pop(0)
                for v in G.Vertices[frente]:
                    if(not(Atg[v])):
                        Atg[v] = True
                        Fila.append(v)
                        prt += " "+str(v+1)


            KA = prt.split()
            for i in range(len(KA)):
                KA[i] = int(KA[i])
            KA.sort()
            prt = str(KA[0])
            del(KA[0])
            for n in KA:
                prt+=" "+str(n)
            print(prt)
                

dl = input()
formato = input()
n = input().split('=')[1]
data = input()
G = Grafo(int(n),False,False)
entrada = input().split()
while(entrada!=[]):
    try:
        G.aresta(int(entrada[0]),int(entrada[1]))
        entrada = input().split()
    except(EOFError):
        break

Componentes(G)

'''
G = Grafo(5,True,True)
G.aresta(1,5,76.000)
G.aresta(1,4,53.875)
G.aresta(1,3,85.000)
G.aresta(2,5,93.125)
G.aresta(2,4,3.875)
G.aresta(3,5,68.750)
G.aresta(3,2,73.750)
G.aresta(3,1,72.000)
G.aresta(4,3,22.875)
G.aresta(4,2,82.875)
G.aresta(4,1,44.000)
G.aresta(5,3,85.750)
G.aresta(5,2,58.750)
G.aresta(5,1,68.625)
d = Cam_Min(G,1)
for i in range(len(d)):
    if(not(str(d[i])=='inf')):
        print(str(i+1)+ " " +"%.3f"%d[i])
    else:
        print(str(i+1)+" "+"INFINITO")

'''
'''
Peso = AGM_k(G)
print("\n")
print(Peso)
'''

'''
    return round(P,3)
            
                
                
        

dl = input()
formato = input()
n = input().split('=')[1]
data = input()
G = Grafo(int(n),False,True)
entrada = input().split()
while(entrada!=[]):
    try:
        G.aresta(int(entrada[0]),int(entrada[1]),float(entrada[2]))
        entrada = input().split()
    except(EOFError):
    	break

Peso = AGM_k(G)
print("%.3f"%Peso)
'''

def teste(graf):
    file1 = open(graf+"_grafo.dl",'r')
    cont = 0
    n = 0
    Art = []
    P2 = 0
    for k in file1:
        if(cont==2):
            d,n = k.split('=')
            n = int(n)
        if(cont>=4):
            u,v,peso = k.split(' ')
            Art.append((int(u),int(v),float(peso)))
        cont+=1


    G = Grafo(n,True,True)

    for a in Art:
        G.aresta(a[0],a[1],a[2])

    file1.close()
    
    file2 = open(graf+"_solucao.txt",'r')
    for k in file2:
        P = k.split(' ')
        P2 = float(P[0])
        break
    file2.close()
    
    d = Cam_Min(G,1)
    for i in range(len(d)):
        if(not(str(d[i])=='inf')):
            print(str(i+1)+ " " +"%.3f"%d[i])
        else:
            print(str(i+1)+" "+"INFINITO")
    '''
    if(P1==P2):
        print("Correto!")
        print("Matheus: "+str(P1)+" // "+"Resposta: "+str(P2))
    else:
        print("Errado!")
        print("Matheus: "+str(P1)+" // "+"Resposta: "+str(P2))
    '''


#Algum dia implementar o algoritmo de Prim

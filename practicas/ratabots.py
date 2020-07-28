#import math

from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
import math


LABERINTO = [['.', '.', '.', 'P', '.', 'P'],
             ['.', 'P', 'C', 'P', '.', '.'],
             ['.', '.', 'P', '.', 'P', '.'],
             ['P', '.', '.', '.', 'C', 'R'],
             ['C', 'P', '.', 'P', '.', 'P'],
             ['.', '.', '.', 'P', '.', '.']
             ]


FINAL = (3,5)#casilla por la cual debe salir

PAREDES = []


LONGITUD = 0 

def generarEstado(laberinto):
    """Genera el estado antes de ejecutar el problema. A partir del LABERINTO generado arriba,
    busca las posiciones de las paredes, de las comidas y la posicion inicial del robot"""
    global LONGITUD
    LONGITUD = len(laberinto)-1
    paredes = []
    comidas = []    
    
    for fila,elemento in enumerate(laberinto):
        for columna,elemento2 in enumerate(elemento):
            if elemento2 == "P":
                PAREDES.append( (fila,columna) )
            elif elemento2 =="C":
                comidas.append( (fila,columna) )
            elif elemento2 =="R":
                posicion = (fila,columna) 
    estado = "({},{})|{}".format(posicion[0],posicion[1],comidas)
    return estado


def verificarCasilla(pos,accion):
    suma = MOVIMIENTOS[accion]
    filaF,colF = pos[0]+suma[0], pos[1]+suma[1] 
    return (filaF,colF) not in PAREDES

def buscar_mas_lejana(pos,comidas):
    maximo1 = 0
    posMax1 =()
    maximo2 = 0
    posMax2 =()
    if len(comidas)> 1 :
        for c in comidas:
            cantidad = abs(pos[0] - c[0]) + abs(pos[1]-c[1] )
            if cantidad > maximo1:
                maximo1 = cantidad
                posMax1 = (c[0],c[1])
        comidas.remove(posMax1)
        for c in comidas:
            cantidad = abs(posMax1[0] -c[0]) +abs(posMax1[1]-c[1] )
            if cantidad > maximo2:
                maximo2 = cantidad
                posMax2 = (c[0],c[1])
        volver = (pos[0]-FINAL[0]) + abs(pos[1]-FINAL[1]) 
        return maximo1+maximo2+volver
    elif len(comidas) ==1 :
        c = comidas[0]
        cantidad = abs(pos[0] - c[0]) + abs(pos[1]-c[1] )
        volver = (pos[0]-FINAL[0]) + abs(pos[1]-FINAL[1])        

        return cantidad + volver
    elif len(comidas) == 0:
        return (pos[0]-FINAL[0]) + abs(pos[1]-FINAL[1]) 

#Posibles movimientos del ROBOT
MOVIMIENTOS = {"U":(-1,0),"D":(1,0),
                "L":(0,-1),"R":(0,1)
                }

class rataProblem(SearchProblem):


    def is_goal(self, state):
        posicion,comidas = state.split("|")
        posicion = eval(posicion)
        comidas = eval(comidas)
        if posicion == FINAL and len(comidas) == 0:
            return  True
        else :
            return False


    def cost(self, state1, action, state2):
        return 1


    def actions(self, state):
        acciones = []
        pos,comidas = state.split("|")
        pos = eval(pos)
        comidas = eval(comidas)
        if pos in comidas :
            acciones.append("C")
        else:
            if pos[0] > 0:#Arriba 
                if verificarCasilla(pos,"U"):
                    acciones.append("U")    
            if pos[0]<  LONGITUD :#ABAJO
                if verificarCasilla(pos,"D") :
                    acciones.append("D")
            if pos[1] >0:#izquierda
                if verificarCasilla(pos,"L"):
                    acciones.append("L")
            if pos[1]< LONGITUD:
                if verificarCasilla(pos,"R"):
                    acciones.append("R")
        return acciones 


    def heuristic(self,state):     
        """Suma la distancia de manhattan desde la posicion actual hasta la mas
        alejada de las comidas, sumado a la distancia mas lejanda desde esta comida,
        mas la suma desde la ultima a la salida """

        pos,comidas = state.split("|")
        pos = eval(pos)
        comidas = eval(comidas)
        
        return buscar_mas_lejana(pos,comidas)


    def result(self, state, action):
        pos,comidas = state.split("|")
        pos = eval(pos)
        comidas = eval(comidas)
        if action == "C":
            comidas.remove(pos)    
        else:
             pos = pos[0]+MOVIMIENTOS[action][0] ,pos[1]+MOVIMIENTOS[action][1]

        state = "({},{})|{}".format(pos[0],pos[1],comidas)     
        return state

        
def main():
    metodo = raw_input("Ingrese el metodo de busqueda-- (greedy,depth_first,breadth_first,astar)\n")
    STATE = generarEstado(LABERINTO)
    problema = rataProblem(STATE)
    if metodo == "breadth_first":    
        r = breadth_first(problema,graph_search=True,viewer=ConsoleViewer())
    
    if metodo == "greedy":    
        r = greedy(problema,graph_search=True,viewer=ConsoleViewer())

    if metodo == "depth_first":    
        r = depth_first(problema,graph_search=True,viewer=ConsoleViewer())
    
    if metodo == "astar":
        r = astar(problema,graph_search = True, viewer = ConsoleViewer() )        
   
    print("=======================================================================\n")
    print "Estado final :",r.state,"\n"
    print "Path :",r.path(),"\n"
    l = [x[0] for x in r.path()]
    print "Acciones tomadas",l,"\n"
    print "Costo :",r.cost,"\n"
    
if __name__ == '__main__':
    main()



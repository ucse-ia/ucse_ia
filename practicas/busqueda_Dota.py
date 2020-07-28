from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
import itertools


"""El estado inicila esta formado por una cadena de strings, la cual es por ejemplo:
	'0-1|2-3|4-2',donde los primeros dos numeros son la posicion del jugador, el segundo par
	de numeros es la posicion del enemigo, y el ultimo par la posicion del castillo.

	En caso de que elimine tanto al enemigo o al castillo , se reemplazan los numeros por
	XX. 
	"""

MOVIMIENTOS = { "U": (-1,0),"D":(1,0),"L":(0,-1),"R":(0,1) }

longitud = 0


def manhattan(posicion,enemigo):
	x1,y1 = posicion.split("-")
	x2,y2 = enemigo.split("-")
	return abs(int(x1)-int(x2)) + abs( int(y1)-int(y2))


def string_a_lista(string):
	return string.split("|")


def lista_a_string(lista):
	return "|".join(lista)



def generar_estados(lista):
	return lista_a_string(lista)				


def verificar_acciones(p):
	global longitud
	acciones = []
	
	#arriba
	if int(p[0]) > 0 :
		acciones.append("U")
	#Abajo
	if int(p[0]) < longitud:
		acciones.append("D")
	#izquierda
	if int(p[1]) > 0: 
		acciones.append("L")
	#derecha
	if int(p[1])< longitud:
		acciones.append("R")	

	return acciones


class prolemaDota(SearchProblem):


	def is_goal(self,state):
		"""Verifica si tanto la posicion del enemigo como la del 
		cuartel tiene valor XX"""
		estado = string_a_lista(state)
		return estado[1] == "XX"and estado[2] == "XX"


	def actions(self,state):
		"""Para ver que acciones puedo realizar.
		1- Hago un calculo en el cual, si mi posicion menos la posicion 
		del enemigo o del castillo me da = 1, entonces quiere decir que estoy 
		adyacente a alguno de ellos,por lo tanto puedo agregar la accion de atacar
		a mi lista de acciones.

		2- Verifico con la funcion verificar acciones las posiciones a las cuales
		me puedo mover.
		"""
		estado = string_a_lista(state)
		lAcciones = []
		person = estado[0].split("-")
		sumaEnemigo = 0 
		sumaCastillo = 0 
	
		if estado[1] != "XX":
			enem = estado[1].split("-")
			#verificar si el enemigo esta a mi lado 
			sumaEnemigo = abs( int(person[0])  - int(enem[0] ) ) + abs( int(person[1]) - int(enem[1]) ) 
		
		if estado[2] != "XX":
			cast = estado[2].split("-")
			#verificar si el Castillo esta a mi lado 
			sumaCastillo = abs( int(person[0]) - int(cast[0]) ) + abs( int( person[1] ) - int(cast[1]) )
		
		if sumaCastillo == 1:
			lAcciones.append("AC")
		elif sumaEnemigo == 1:
			lAcciones.append("AE")
		else:
			lAcciones = verificar_acciones(person)

		return lAcciones	



	def result(self,state,action):
		estado = string_a_lista(state)
		personaje = estado[0].split("-")
		if action =="AC":
			estado[2] = "XX"
		elif action =="AE":
			estado[1] = "XX"
		else:
			personaje[0] = str(int(personaje[0]) +MOVIMIENTOS[action][0] )
			personaje[1] = str(int(personaje[1]) +MOVIMIENTOS[action][1] )
			estado[0] ="{}-{}".format(personaje[0],personaje[1])
		return lista_a_string(estado)


	def cost(self,state1,action,state2):
		return 1

	def heuristic(self,state):
		estado = string_a_lista(state)
		enemigos = [estado[1],estado[2]]
		return sum([manhattan(x,estado[0]) for x in enemigos if x != "XX"])


def main():

	jugador = raw_input("Ingrese la posicion del jugador EJ: 0-2\n")
	enemigo = raw_input("Ingrese la posicion del enemigo EJ: 0-5\n")
	castillo = raw_input("Ingrese la posicion del castillo EJ: 3-2\n")	

	global longitud
	longitud = int( raw_input("Ingrese la longitud de la grilla \n") ) -1

	metodo = raw_input("Ingrese el metodo de busqueda-- (greedy,depth_first,breadth_first,astar)\n")

	estado = generar_estados([jugador,enemigo,castillo])
	problema = prolemaDota(estado)
	
	if metodo == "breadth_first":    
 		p = breadth_first(problema,graph_search=True,viewer=ConsoleViewer())
    	
	if metodo == "greedy":    
		p = greedy(problema,graph_search=True,viewer=ConsoleViewer())

	if metodo == "depth_first":    
		p = depth_first(problema,graph_search=True,viewer=ConsoleViewer())

	if metodo == "astar":
		p= astar(problema,graph_search=True,viewer=ConsoleViewer())	
	
	print("=======================================================================\n")
	print "Estado final :",p.state,"\n"
	print "Path :",p.path(),"\n"
	l = [x[0] for x in p.path()]
	print "Acciones tomadas",l,"\n"
	print "Costo :",p.cost,"\n"




if __name__ == '__main__':
	main()
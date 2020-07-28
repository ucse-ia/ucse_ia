
from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer

"""Estado ejemplo:
	'1-3|0-0,0-2,0-4,0-5'
	posActual|posiconesPintadas

	a lista

	[ (1,3),[(0,2),(0,4)]   ]


"""

POSIBLES = [(x,y) for x in range(3) for y in range(4)]
MOVIMIENTOS =  [ (-2,-1),(-1,-2),(-2,1),(-1,2),
				(1,-2),(2,-1),(2,1),(1,2) ]



def splitear(texto):
	(a,b) = texto.split("-")
	return ( int(a),int(b) )


def string_to_list(state):
	"""Convierto la cadena de caracteres en una lista"""
	posActual,pintados = state.split("|")
	pintados = pintados.split(",")
	lista = [splitear(x) for x in pintados]
	return [splitear(posActual),lista]


def list_to_string(a,pintados):
	"""Convierto una lista de dos componentes , posicionActual y posiciones pintadas,
	 en una cadena de strings"""
	pos = "-".join([str(a[0]),str(a[1])])	
	l= []
	for p in pintados :
		l.append("-".join([ str(p[0]),str(p[1]) ] ) )
	if len(l) >1:
		return "|".join( [pos,",".join(l)  ] )
	else:
		return "|".join([pos,l[0]])


class CaballoProblem(SearchProblem):


	def is_goal(self,state):
		"""Si las 12 casillas son rojas,es meta
		"""
		estado = string_to_list(state)
		return len(estado[1]) == 12


	def actions(self,state):
		estado = string_to_list(state)
		
		lAcciones = []
		x,y = estado[0]
		pintados = estado[1]

		global MOVIMIENTOS
		for i in MOVIMIENTOS:
			a = x+i[0]
			b = y+i[1]
			if (a,b)in POSIBLES and (a,b) not in pintados:
				lAcciones.append(i)
		return lAcciones
				
		
	def result(self,state,action):
		estado = string_to_list(state)
		pintados = estado[1]
		x ,y = estado[0]
		x += action[0]
		y += action[1]
		pintados.append([x,y])
		return list_to_string([x,y],pintados)


	def heuristic(self,state):
		estado = string_to_list(state)
		pintados = estado[1]
		return 12 - len(pintados)


def main():
	estado = "0-0|0-0"
	metodo = raw_input("Ingrese el metodo de busqueda-- (greedy,depth_first,breadth_first,astar)\n")
	problema = CaballoProblem(estado)
	
	if metodo == "breadth_first":    
		r = breadth_first(problema,graph_search=True,viewer=ConsoleViewer())
	
	if metodo == "greedy":    
		r = greedy(problema,graph_search=True,viewer=ConsoleViewer())
	
	if metodo == "depth_first":    
		r = depth_first(problema,graph_search=True,viewer=ConsoleViewer())

	if metodo == "astar":
		r = astar(problema,graph_search = False, viewer = ConsoleViewer() )
	
	print("=======================================================================\n")
	print "Estado final :",r.state,"\n"
	print "Path :",r.path(),"\n"
	l = [x[0] for x in r.path()]
	print "Acciones tomadas",l,"\n"
	print "Costo :",r.cost,"\n"


if __name__ == '__main__':
	main()


from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
import itertools





personas =["1","3","6","8","12"]
"""Las personas se representan con los segundos que tarda en cruzar dividido
10.
"""


class problemaLinterna(SearchProblem):

	def is_goal(self,state):
		"""
		Verifica si las 5 personas estan del lado derecho y el 
		costo de cruzar es menor a 30(5 minutos *60 segundos /10).
		"""
		estado = state.split("|")
		lista = estado[3].split("-")
	
		if len(lista)==5 and int(estado[1]) <30:
			return True
	
	def actions(self,state):
		estado = state.split("|")
		lado = estado [2]
		lAcciones = []	
		if lado == "D":
			if len(estado[3].split("-")) < 5:
				accion = "I"
				posibles = estado[3].split("-")
				for p in posibles:
					lAcciones.append( "{}{}".format(p,"I") )
		
		else:
			
			personas = estado[0].split("-")
			posibles = list(itertools.combinations(personas,2))
			accion = "D"
			for p in posibles:
				lAcciones.append( accion.join(p) )
		
		return lAcciones

	def result(self,state,action):
		estado = state.split("|")
		ladoActual = estado[2]
		if ladoActual =="I":
			p1,p2 = action.split("D")
			tiempo = int(estado[1]) + max(int(p1),int(p2))
			if estado[3] =="":
				listaD = []
				listaD.append(p1)
				listaD.append(p2)
				
			else:
				#Agrego a la lista de la derecha a los dos que cruzan
				listaD = estado[3].split("-")	
				listaD.append(p1)
				listaD.append(p2)
			#Los saco de la lista de la izquierda
			listaI= estado[0].split("-")
			listaI.remove(p1)
			listaI.remove(p2)		
			#Devuelvo el estado
			return "{}|{}|{}|{}".format("-".join(listaI),tiempo,"D","-".join(listaD) )	
		else:
			p1,vacio = action.split("I")
			tiempo = int(estado[1]) + int(p1)
			#saco de la lista de la derecha
			listaD = estado[3].split("-")
			listaD.remove(p1)
			#agrego a list izquierda
			listaI = estado[0].split("-")
			listaI.append(p1)
			return "{}|{}|{}|{}".format("-".join(listaI),tiempo,"I","-".join(listaD) )


	def cost(self,state1,action,state2):
		estado = state1.split("|")
		ladoActual = estado[2]
		if ladoActual == "I":
			p1,p2 = action.split("D")
			return max(int(p1),int(p2))
		else:
			p1,vacio = action.split("I")
			return int(p1)


def main():
	estado = "{}|0|I|".format("1-3-6-8-12")
	problema = problemaLinterna(estado)
	metodo = raw_input("Ingrese el metodo de busqueda-- (greedy,depth_first,breadth_first)\n")

	if metodo == "breadth_first":    
 		p = breadth_first(problema,graph_search=True,viewer=ConsoleViewer())
    	
	if metodo == "greedy":    
		p = greedy(problema,graph_search=True,viewer=ConsoleViewer())

	if metodo == "depth_first":    
		p = depth_first(problema,graph_search=True,viewer=ConsoleViewer())

	
	print("=======================================================================\n")
	print "Estado final :",p.state,"\n"
	print "Path :",p.path(),"\n"
	l = [x[0] for x in p.path()]
	print "Acciones tomadas",l,"\n"
	print "Costo :",p.cost*10,"segundos","\n"


if __name__ == '__main__':
	main()

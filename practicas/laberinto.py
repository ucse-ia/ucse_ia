from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
import itertools


nexts = {"1": ["9","12"],
	"2":["5","6","7","3"],
	"3":["2","8","4"],
	"4":["5","8","21"],
	"5":["6","2"],
	"6":["5","2","9"],
	"7":["2","9"],
	"8":["3","10","4"],
	"9":["12","6","7","1"],
	"10":["8","11","15"],
	"11":["10"],
	"12":["14","17","9","1"],
	"13":["14","17","19"],
	"14":["13","12"],
	"15":["18","10"],
	"16":["15","20"],
	"17":["13","19","12"],
	"18":["15"],
	"19":["17","13","20"],
	"20":["19","16"]
}



class problemaLaberinto(SearchProblem):


	def is_goal(self,state):
		return state == "21"

	
	def actions(self,state):
		global nexts
		return nexts[state]


	def result(self,state,action):
		return action


	def cost(self,state1,action,state2):
		return 1

	


def main():

	metodo = raw_input("Ingrese el metodo de busqueda-- (greedy,depth_first,breadth_first)\n")
	problema = problemaLaberinto("1")

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
	print "Costo :",p.cost,"\n"


if __name__ == '__main__':
		main()	




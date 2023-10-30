import math

from simpleai.search import SearchProblem, astar

from simpleai.search.viewers import BaseViewer

# (posicion_drone, cantidad agua en el dron, coordenadas por regar)
HARD_INITIAL = ((0, 2), 1000, frozenset([
    (0, 1), (1, 1), (1, 2), (1, 4), (2, 0), (2, 1), (2, 2), (2, 4), (3, 0), #(3, 4), (4, 0), (4, 1)
]))

MEDIUM_INITIAL = ((0, 2), 1000, frozenset([
    (0, 1), (1, 1), (1, 2), (1, 4), (2, 0), (2, 1), (2, 2), (2, 4)
]))

EASIER_INITIAL = ((0, 2), 1000, frozenset([
    (0, 1), (1, 1), (1, 2), (1, 4), (2, 0),
]))

TREES = {(0, 0), (0, 4), (1, 0), (1, 3), (3, 1), (4, 3), (4, 4)}
BASE = (0, 2)


def is_valid_position(position):
    r, c = position
    return (0 <= r <= 4) and (0 <= c <= 4) and position not in TREES


class DroneRegadorProblem(SearchProblem):
    def is_goal(self, state):
        position, _, pending_sectors = state
        return (position == BASE) and (len(pending_sectors) == 0)

    def actions(self, state):
        pos, water, pending_sectors = state
        available_actions = []

        # siempre me puedo mover a casillas adyacentes validas
        cr, cc = pos
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (cr+dr, cc+dc)
            if is_valid_position(new_pos):
                available_actions.append(('mover', new_pos))

        # puedo regar si estoy en algun sector por regar y ademas tengo agua
        if pos in pending_sectors and water >= 250:
            available_actions.append(('regar', None))

        # puedo recargar si no tengo el tanque lleno y estoy en la base
        if water < 1000 and pos == BASE:
            available_actions.append(('recargar', None))

        return available_actions

    def result(self, state, action):
        pos, water, pending_sectors = state
        action, new_pos = action
        if action == 'mover':
            pos = new_pos
        elif action == 'regar':
            water -= 250
            pending_sectors = pending_sectors - {pos}
        else:
            water = 1000

        return pos, water, pending_sectors

    def cost(self, state, action, state2):
        action, _ = action
        if action == 'mover':
            return 15
        if action == 'regar':
            return 60
        return 300


class DroneIrrigationCostProblem(DroneRegadorProblem):
    def heuristic(self, state):
        # la mas comun fue el costo de regar los faltantes
        pos, water, pending_sectors = state

        irrigation_cost = len(pending_sectors) * 60
        return irrigation_cost


class DroneIrrigationRefillCostsProblem(DroneRegadorProblem):
    def heuristic(self, state):
        # hubo alguien que dijo el costo de regar + el costo de moverme a esos faltantes +
        # el costo de reposicion de agua
        pos, water, pending_sectors = state
        irrigation_cost = len(pending_sectors) * (60+15)
        if pos in pending_sectors:
            irrigation_cost -= 15
        water_needs = max(len(pending_sectors) * 250 - water, 0)
        water_refill_cost = math.ceil(water_needs / 1000) * 300
        return irrigation_cost + water_refill_cost


class DroneJourneyProblem(DroneRegadorProblem):
    def heuristic(self, state):
        # aca la idea es sumar el costo de regar + refill + el peor viaje que estamos seguros
        # que vamos a hacer
        pos, water, pending_sectors = state
        irrigation_cost = len(pending_sectors) * 60
        water_needs = max(len(pending_sectors) * 250 - water, 0)
        water_refill_cost = math.ceil(water_needs / 1000) * 300

        # de minima tengo que volver a la base,
        # pero si hay pendientes tengo que llegar y luego volver
        dr, dc = pos
        worst_journey = (abs(dr - BASE[0]) + abs(dc - BASE[1])) * 15
        for pr, pc in pending_sectors:
            moves_to_point = abs(dr - pr) + abs(dc - pc)
            moves_to_base = abs(BASE[0] - pr) + abs(BASE[1] - pc)
            journey_cost = (moves_to_point + moves_to_base) * 15
            if journey_cost > worst_journey:
                worst_journey = journey_cost

        return irrigation_cost + water_refill_cost + worst_journey


approaches = [
    ('Costo de riego', DroneIrrigationCostProblem),
    ('Costo de riego + refill', DroneIrrigationRefillCostsProblem),
    ('Costo de riego + refill + viaje minimo', DroneJourneyProblem),
]

print("=" * 80)
print("Problema facil")
for name, problem_class in approaches:
    problem = problem_class(EASIER_INITIAL)
    viewer = BaseViewer()
    result = astar(problem, graph_search=True, viewer=viewer)
    print(f"Heuristica: {name:40s}", "Cost", result.cost, "Stats", viewer.stats)

print("=" * 80)
print("Problema un poco mas dificil")
for name, problem_class in approaches[1:]:
    problem = problem_class(MEDIUM_INITIAL)
    viewer = BaseViewer()
    result = astar(problem, graph_search=True, viewer=viewer)
    print(f"Heuristica: {name:40s}", "Cost", result.cost, "Stats", viewer.stats)


print("=" * 80)
print("Problema dificil")
for name, problem_class in approaches[2:]:
    problem = problem_class(HARD_INITIAL)
    viewer = BaseViewer()
    result = astar(problem, graph_search=True, viewer=viewer)
    print(f"Heuristica: {name:40s}", "Cost", result.cost, "Stats", viewer.stats)


print("=" * 80)
print("Un plan de riego")
for action, state in result.path():
    print("Action:", action, "State: ", state)

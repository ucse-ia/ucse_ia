# -*- coding: utf-8 -*-
from simpleai.machine_learning import VectorDataClassificationProblem, DecisionTreeLearner_Queued
from simpleai.machine_learning.classifiers import tree_to_str


RestaurantDataset = [
    (True, False, False, True, 'Some', '$$$', False, True, 'French', '0-10', True),
    (True, False, False, True, 'Full', '$', False, False, 'Thai', '30-60', False),
    (False, True, False, False, 'Some', '$', False, False, 'Burger', '0-10', True),
    (True, False, True, True, 'Full', '$', True, False, 'Thai', '10-30', True),
    (True, False, True, False, 'Full', '$$$', False, True, 'French', '>60', False),
    (False, True, False, True, 'Some', '$$', True, True, 'Italian', '0-10', True),
    (False, True, False, False, 'None', '$', True, False, 'Burger', '0-10', False),
    (False, False, False, True, 'Some', '$$', True, True, 'Thai', '0-10', True),
    (False, True, True, False, 'Full', '$', True, False, 'Burger', '>60', False),
    (True, True, True, True, 'Full', '$$$', False, True, 'Italian', '10-30', False),
    (False, False, False, False, 'None', '$', False, False, 'Thai', '0-10', False),
    (True, True, True, True, 'Full', '$', False, False, 'Burger', '30-60', True),
]


problema = VectorDataClassificationProblem(RestaurantDataset, 10)
arbol = DecisionTreeLearner_Queued(RestaurantDataset, problema)

print arbol.classify((True, False, True, False, 'Full', '$', False, True, 'French', '0-10'))

print tree_to_str(arbol.root)



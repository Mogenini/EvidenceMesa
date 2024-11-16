import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns

import model

'''
Format:
Semaphore: [ [ [(x,y),True],[] ] ]
'''

data = {
    "Buildings": [
        (2, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (10, 2), (11, 2), (3, 2),
        (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3),
        (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4),
        (2, 5), (3, 5), (4, 5), (5, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5),
        (2, 8), (3, 8), (4, 8), (7, 8), (9, 8), (10, 8), (11, 8), (2, 9), (3, 9),
        (4, 9), (7, 9), (8, 9), (9, 9), (10, 9), (11, 9), (2, 10), (3, 10),
        (7, 10), (8, 10), (9, 10), (10, 10), (2, 11), (3, 11), (4, 11), (7, 11),
        (8, 11), (9, 11), (10, 11), (11, 11), (2, 16), (3, 16), (4, 16), (5, 16),
        (8, 16), (9, 16), (10, 16), (11, 16), (3, 17), (4, 17), (5, 17), (8, 17),
        (9, 17), (10, 17), (11, 17), (2, 18), (3, 18), (4, 18), (5, 18), (8, 18),
        (9, 18), (10, 18), (11, 18), (2, 19), (3, 19), (4, 19), (5, 19), (8, 19),
        (9, 19), (10, 19), (11, 19), (2, 20), (3, 20), (4, 20), (9, 20), (10, 20),
        (11, 20), (2, 21), (3, 21), (4, 21), (5, 21), (8, 21), (9, 21), (10, 21),
        (11, 21), (13, 13), (14, 13), (13, 14), (14, 14), (16, 2),(16, 3),(16, 4),
        (16, 5),(16, 8), (16, 9), (16, 11), (16,16), (16,17), (16,20),(16,21),
        (17,2), (17,4),(17,5),(17,8),(17,9),(17,10),(17,11),(17,16),(17,20),(17,21),
        (18,16),(18,17),(18,20),(18,21),(19,16),(19,21),(20,2),(20,3),(20,5),(20,8),
        (20,9),(20,10),(20,11),(20,16),(20,17),(20,20),(20,21),(21,2),(21,3),(21,4),
        (21,5),(21,8),(21,10),(21,11),(21,16),(21,17),(21,20),(21,21)

    ],
    "Parking_Lots": [
        [(2, 3), False], [(9, 2), False], [(11, 4), False], [(6, 5), False],
        [(8, 8), False], [(4, 10), False], [(11, 10), False], [(17, 3), False],
        [(20, 4), False], [(21, 9), 1], [(2, 17), False], [(5, 20), False],
        [(8, 20), False], [(17, 17), 1], [(19, 17), False], [(19, 20), False]
    ],
    "Semaphores": [ [[(17, 0), True], [(17, 1), True]],
                   [[(2, 6), True],[(2, 7), True]],
                   [[(7, 6), True],[(7, 7), True]],
                   [[(21, 6), True],[(21, 7), True]],
                   [[(16, 18), True],[(16, 19), True]],
                   [[(18, 2), False],[(19, 2), False]],
                   [[(22, 5), False],[(23, 5), False]],
                   [[(0, 8), False],[(1, 8), False]],
                   [[(5, 8), False],[(6, 8), False]],
                   [[(14, 17), False],[(15, 17), False]]

    ]
}

ModelCity = model.CityModel(1,24,24,data)

ModelCity.step()





from mesa.visualization import SolaraViz, make_plot_component, make_space_component

from MoneyModel import MoneyModel

def agent_portrayal(agent):
    size = 10
    color = "tab:red"
    if agent.wealth > 0:
        size = 50
        color = "tab:blue"
    return{"size":size, "color":color}

model_params = {
    "n": {
        "type": "SliderInt",
        "value": 50,
        "label": "Number of agents:",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "width": {
        "type": "SliderInt",
        "value": 10,
        "label": "Width:",
        "min": 10,
        "max": 50,
        "step": 10,
    },
    "height":{
        "type": "SliderInt",
        "value": 10,
        "label": "Height:",
        "min": 10,
        "max": 50,
        "step": 10,
    },
}

#Create model
model1 = MoneyModel(50,10,10)

proplayer_portrayal = {"buildings": {"color": "black", "alpha": 0.25, "colorbar": False}}

SpaceGraph = make_space_component(agent_portrayal, propertylayer_portrayal=proplayer_portrayal)
GiniPlot = make_plot_component("Gini")

page = SolaraViz(
    model1,
    components = [SpaceGraph, GiniPlot],
    model_paras=model_params,
    name="Wealth Model",
)
page

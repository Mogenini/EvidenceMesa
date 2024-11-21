import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns
from mesa.visualization import Slider, SolaraViz, make_space_component
import matplotlib.pyplot as plt
from numpy.matrixlib.defmatrix import matrix
from solara import component

from agents import CarAgent,TrafficLightAgent

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
    ],
    "Left": [
        ["Y", (0,1), (0,23)],
        ["Y", (1,1), (1,23)],
        ["X", (2,23), (23,23)],
        ["Y", (2,23), (23,23)],
        ["Y", (6,16), (6,22)],
        ["Y", (7,16), (7,22)],
        ["Y", (12,16), (12,22)],
        ["Y", (13,15), (13,22)],
        ["X", (2,1), (21,1)],
        ["X", (2,15), (11,15)],
        ["Y", (12,2), (12,15)],
        ["Y", (13,2), (13,12)],
        ["X", (16,7), (17,7)],
        ["Y", (18,2), (18,6)],
        ["Y", (19,2), (19,6)],
        ["X", (17,15), (21,15)],
        ["X", (17,20), (21,20)],
        ["X", (2,13), (11,13)],
        ["X", (16,13), (21,13)],
        ["X",(3,7),(11,7)],
        ["Y",(9,2),(9,2)],
        ["Y",(8,7),(8,8)],
        ["Y",(19,19),(19,20)],
        ["Y",(5,7),(5,12)],
        ["Y",(6,6),(6,12)],
        ["Y",(17,18),(17,19)],
        ["Y",(19,18),(19,19)]
    ],
    "Right": [["X",(2,0),(23,0)],["Y",(14,1),(14,12)],["Y",(15,1),(15,21)],
              ["X",(16,6),(20,6)],["Y",(18,7),(18,11)],["Y",(19,7),(19,11)],
              ["X",(3,6),(11,6)],["X",(2,12),(11,12)],["X",(4,14),(11,14)],
              ["X",(16,12),(21,12)],["X",(16,14),(21,14)],["Y",(22,0),(22,23)],
              ["Y",(23,0),(23,22)],["X",(2,22),(21,22)],["X",(17,18),(21,18)],
              ["Y",(14,15),(14,21)],["Y",(6,5),(6,6)],["Y",(17,17),(17,18)],["Y",(19,17),(19,18)],
              ["Y",(9,1),(9,1)],["Y",(8,6),(8,7)],["Y",(19,18),(19,19)]

    ],
    "Up": [["X",(2,6),(12,6)],["X",(2,7),(12,7)],["Y",(15,2),(15,11)],
           ["Y",(19,3),(19,5)],["Y",(19,8),(19,11)],["Y",(23,2),(23,23)],["X",(1,23),(23,23)],
           ["X",(1,22),(22,22)],["Y",(1,2),(1,21)],["X",(2,15),(22,15)],["X",(16,14),(22,14)],
           ["X",(1,14),(12,14)],["X",(16,18),(22,18)],["X",(16,19),(22,19)],["Y",(15,16),(15,21)],
           ["Y",(7,16),(7,21)],["Y",(6,9),(6,12)],["Y",(1,3),(2,3)],["X",(19,4),(20,4)],["X",(15,10),(16,10)],
           ["X",(1,17),(2,17)],["Y",(7,20),(8,20)],["X",(4,10),(6,10)],["X",(11,4),(12,4)],["X",(18,3),(19,3)],
           ["X",(5,10),(6,10)],["X",(12,10),(13,10)],["X",(22,9),(23,9)],["X",(6,20),(7,20)]
    ],
    "Down": [["X",(0,0),(22,0)],["X",(0,1),(22,1)],["X",(15,6),(21,6)],["X",(15,7),(21,7)],
             ["X",(1,12),(21,12)],["X",(1,13),(11,13)],["X",(15,13),(21,13)],["Y",(0,2),(0,21)],
             ["Y",(22,2),(22,21)],["Y",(5,9),(5,11)],["Y",(6,17),(6,21)],["Y",(12,3),(12,10)],
             ["Y",(12,17),(12,20)],["X",(14,1),(15,1)],["X",(14,12),(15,12)],["Y",(18,3),(18,5)],
             ["Y",(18,9),(18,10)],["X",(11,10),(12,10)],["Y",(11,4),(12,4)],["X",(4,10),(5,10)],
             ["X",(17,3),(18,3)],["X",(21,9),(22,9)],["X",(5,20),(6,20)],["X",(0,3),(1,3)],["X",(18,4),(19,4)],
             ["X",(14,10),(15,10)],["X",(0,17),(1,17)],["X",(6,20),(7,20)]
    ]
}

from model import CityModel
from agents import TrafficLightAgent,CarAgent

proplayer_portal = {"buildingLayer":{"color": "blue","alpha":0.25,"colorbar":False},
                    "trafficLightLayer":{"color": "orange","alpha":0.25,"colorbar":False},
                    "parkingLayer":{"color": "yellow","alpha":0.25,"colorbar":False}
}

model_params = {
    "n": {
        "type": "SliderInt",
        "value": 50,
        "label": "Number of agents:",
        "min": 1,
        "max": 3,
        "step": 1,
    },
    "width": 24,
    "height": 24,
    "dataStructure":data
}

def agent_portrayal(agent):
    if isinstance(agent,TrafficLightAgent):
        size = 50
        color = "tab:green"
        shape = "circle"
    elif isinstance(agent,CarAgent):
        size = 50
        color = "tab:red"
        shape = "circle"
    return {"size":size,"color":color,"shape":shape}




#Create initial Model Instance
model = CityModel(1,24,24,data)
model.step()





spaceGraph = make_space_component(agent_portrayal,propertylayer_portrayal=proplayer_portal)
page = SolaraViz(
    model,
    components = [spaceGraph],
    model_params = model_params,
    name = "Car Agent and Traffic Light",
)
page


from flask import Flask, jsonify
from model import CityModel

model = CityModel(
    1, #agents
    24, #width
    24, #height
    data, #data
)

app = Flask(__name__)

#configure parameters in the model.py
@app.route("/")
def index():
    return jsonify({"Message": "Hello World"})
'''
@app.route("/positions")
def positions():
    #return boids.getPositions()
    boids.step()
    pos = boids.getPositions()
    p = []
    for po in pos:
        p.append({"x": po[0], "y": po[1]})
    print(pos)
    return jsonify(p)
'''
if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 8000, debug=True) ##la neta, ese host y ese port se cambian eh

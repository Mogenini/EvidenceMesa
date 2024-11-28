import mesa
import seaborn as sns
from mesa.visualization import Slider, SolaraViz, make_space_component
from model import CityModel
from agents import TrafficLightAgent,CarAgent
import dataCity
import matplotlib

CustomCmap = matplotlib.colors.ListedColormap(('white', 'green', 'red','yellow'))

proplayer_portal = {"buildingLayer":{"color": "blue","alpha":0.25,"colorbar":False},
                    "trafficLightLayer":{"colormap": CustomCmap ,
                                         "alpha":0.25,
                                         "colorbar":False},
                    "parkingLayer":{"color": "black","alpha":0.25,"colorbar":False}
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
    "dataStructure":dataCity.data
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
model = CityModel(1,24,24,dataCity.data)
model.step()

spaceGraph = make_space_component(agent_portrayal,propertylayer_portrayal=proplayer_portal)
page = SolaraViz(
    model,
    components = [spaceGraph],
    model_params = model_params,
    name = "Car Agent and Traffic Light",
)
page

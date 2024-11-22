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
import model 

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

@app.route("/positions")
def positions():
    model.step()
    positions = []

    for agent in model.schedule.agents:
        if hasattr(agent, 'pos'):  # Variables pos de model.py
            positions.append({"x": agent.pos[0], "y": agent.pos[1]})
    
    print(positions)
    return jsonify(positions)

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 8000, debug=True)

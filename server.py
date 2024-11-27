from flask import Flask, jsonify
from model import CityModel
from collections import OrderedDict
import dataCity

City = CityModel(
    7, #Number of agents
    24, #Width
    24, #Height
    dataCity.data, #Information of our City
)
app = Flask(__name__)

#configure parameters in the model.py
@app.route("/")
def index():
    return jsonify({"Message": "Hello World"})

@app.route("/stepCall")
def stepCall():
    City.step()
    return jsonify({"Action": "Step completed"})

@app.route("/positionsCar")
def dataPositionsCar():
    City.step()
    pos = City.getPositionCar()
    print(f"The data that we are recieving is: {pos}")
    p = []
    for po in pos:
        p.append({"x": po[0], "y": po[1]})
    return  jsonify(p)

@app.route("/dataTrafficLight")
def dataTrafficLightInfo():
    dataTraffic = City.getDataTrafficSigns()
    states = {f"state{index}": trafficIdx[1] for index, trafficIdx in enumerate(dataTraffic)}
    return jsonify({"states": states})


if __name__ == "_main_":
    app.run(host ='0.0.0.0', port = 8000, debug=True)

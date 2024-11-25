from flask import Flask, jsonify
from model import CityModel
import dataCity

City = CityModel(
    1, #Number of agents
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
    if City.step():
        return jsonify({"Action": "Step completed"})
    return jsonify({"Action": "Step not completed"})

@app.route("/positionsCar")
def dataPositionsCar():
    pos = City.getPositionCar()
    print(f"The data that we are recieving is: {pos}")
    p = []
    for po in pos:
        p.append({"x": po[0], "y": po[1]})
    return  jsonify(p)

@app.route("/dataTrafficLight")
def dataTrafficLightInfo():
    dataTraffic = City.getDataTrafficSigns()
    data = []
    for trafficIdx in dataTraffic:
        data.append({"trafficLight1Pos": trafficIdx[0][0],
                     "trafficLight2Pos": trafficIdx[0][1],
                     "state": trafficIdx[1]})
    return  jsonify(data)

if __name__ == "_main_":
    app.run(host ='0.0.0.0', port = 8000, debug=True)


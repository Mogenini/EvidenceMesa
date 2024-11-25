from flask import Flask, jsonify
from model import CityModel
from flask_cors import CORS
import dataCity
import agents

City = CityModel(
    3, #Number of agents
    24, #Width
    24, #Height
    dataCity.data, #Information of our City
)
app = Flask(__name__)
CORS(app)

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
    car_positions = City.getPositionCar()
    print(f"Datos enviados a Unity: {car_positions}")
    return jsonify(car_positions)


@app.route("/dataTrafficLight")
def dataTrafficLightInfo():
    dataTraffic = City.getDataTrafficSigns()
    data = []
    for trafficIdx in dataTraffic:
        data.append({"trafficLight1Pos": trafficIdx[0][0],
                     "trafficLight2Pos": trafficIdx[0][1],
                     "state": trafficIdx[1]})
    return  jsonify(data)

@app.route("/carPath", methods=["GET"])
def car_path():
    cars_data = []
    for car in City.agents_by_type[agents.CarAgent]:
        car.step()  
        car_info = {
            "isParked": car.isParked,
            "position": list(car.pos),
            "startingPosition": list(car.startingPosition),
            "endingPosition": list(car.endingPosition),
            "path": [list(step) for step in car.path]  
        }
        cars_data.append(car_info)
    
    print(f"Datos de los carros enviados: {cars_data}")
    return jsonify(cars_data)


if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 8000, debug=True)


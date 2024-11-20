from flask import Flask, jsonify
from model import CityModel

boids = BoidFlockers(
    20, #population
    100, #width
    100, #height
    1, #speed
    10, #vision
    2, #separation
    0.025, #cohere
    0.25, #separate
    0.04, #match
)
app = Flask(__name__)

#configure parameters in the model.py
@app.route("/")
def index():
    return jsonify({"Message": "Hello World"})

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

if __name__ == "_main_":
    app.run(host ='0.0.0.0', port = 8000, debug=True) ##la neta, ese host y ese port se cambian eh


#TODO this is only the code, is missing the model from the original mesa folder
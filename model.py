import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns
import agents

# Function to set cells in a specified layer
def set_layer(self, coordinate_dict, layer_name):
    for item in coordinate_dict:
        direction, start, end = item
        if direction == "Y":
            x = start[0]
            for y in range(start[1], end[1] + 1):
                self.grid.properties[layer_name].set_cell((x, y), 1)
        elif direction == "X":
            y = start[1]
            for x in range(start[0], end[0] + 1):
                self.grid.properties[layer_name].set_cell((x, y), 1)

class CityModel(mesa.Model):
    def __init__(self, n, width, height, dataStructure, seed=None):
        super().__init__(seed=seed)
        self.n = n
        self.width = width
        self.height = height
        self.buildingLayer = mesa.space.PropertyLayer("buildingLayer", self.width, self.height, default_value=np.float64(0))
        self.trafficLightLayer = mesa.space.PropertyLayer("trafficLightLayer", self.width, self.height, default_value=np.float64(0))
        self.parkingLayer = mesa.space.PropertyLayer("parkingLayer", self.width, self.height, default_value=np.float64(0))

        # Movement layers
        self.RightLayer = mesa.space.PropertyLayer("RightLayer", self.width, self.height, default_value=np.float64(0))
        self.LeftLayer = mesa.space.PropertyLayer("LeftLayer", self.width, self.height, default_value=np.float64(0))
        self.UpLayer = mesa.space.PropertyLayer("UpLayer", self.width, self.height, default_value=np.float64(0))
        self.DownLayer = mesa.space.PropertyLayer("DownLayer", self.width, self.height, default_value=np.float64(0))

        self.grid = mesa.space.MultiGrid(width, height, True, (self.buildingLayer,
                                                               self.trafficLightLayer,
                                                               self.parkingLayer,
                                                               self.RightLayer,
                                                               self.LeftLayer,
                                                               self.UpLayer,
                                                               self.DownLayer))

        def set_Data_Structures(coordinateStructurePositions):
            set_buildingsLayer(coordinateStructurePositions["Buildings"])
            set_traffic_lightsLayer(coordinateStructurePositions["Semaphores"])
            set_parking_lotsLayer(coordinateStructurePositions["Parking_Lots"])

            # Movement layers
            set_left_Layer(coordinateStructurePositions["Left"])
            set_right_Layer(coordinateStructurePositions["Right"])
            set_up_Layer(coordinateStructurePositions["Up"])
            set_down_Layer(coordinateStructurePositions["Down"])
            return

        def set_buildingsLayer(buildingsArray):
            for x, y in buildingsArray:
                self.grid.properties["buildingLayer"].set_cell((x, y), 1)

        def set_traffic_lightsLayer(coordinateStructurePositions):
            for coordinate_pair in coordinateStructurePositions:
                for (x, y), isOn in coordinate_pair:
                    if isOn:
                        self.grid.properties["trafficLightLayer"].set_cell((x, y), 1)
                    else:
                        self.grid.properties["trafficLightLayer"].set_cell((x, y), 2)

        def set_parking_lotsLayer(coordinateStructurePositions):
            for (x, y), isOccupied in coordinateStructurePositions:
                if isOccupied:
                    self.grid.properties["parkingLayer"].set_cell((x, y), 2)  # 2 occupied
                else:
                    self.grid.properties["parkingLayer"].set_cell((x, y), 1)

        # Movement layers
        def set_right_Layer(coordinateStructurePositions):
            set_layer(self, coordinateStructurePositions, "RightLayer")

        def set_left_Layer(coordinateStructurePositions):
            set_layer(self, coordinateStructurePositions, "LeftLayer")

        def set_up_Layer(coordinateStructurePositions):
            set_layer(self, coordinateStructurePositions, "UpLayer")

        def set_down_Layer(coordinateStructurePositions):
            set_layer(self, coordinateStructurePositions, "DownLayer")

        set_Data_Structures(dataStructure)
        print(self.grid.properties["LeftLayer"].data)
        print(self.grid.properties["RightLayer"].data)
        print(self.grid.properties["UpLayer"].data)
        print(self.grid.properties["DownLayer"].data)

        # Create Traffic Light Agents
        for idSemaphore in dataStructure["Semaphores"]:
            coords = []
            status = False
            for (x, y), value in idSemaphore:
                coords.append((x, y))
                status = value
            agents.TrafficLightAgent(self, idSemaphore, coords, status)

        # Create Car Agents
        for iDCar in range(self.n):
            carAgent = agents.CarAgent(self, True, (1, 9), (2, 3))  # model, isParked, startingPosition, endingPosition
            self.grid.place_agent(carAgent, (1, 9))




    def step(self):
        for agent in self.agents_by_type[agents.TrafficLightAgent]:
            agent.step()
        self.agents_by_type[agents.CarAgent].shuffle_do("step")

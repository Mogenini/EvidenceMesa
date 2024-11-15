import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns
import agents

class CityModel(mesa.Model):
    def __init__(self, n, width, height, dataStructure ,seed=None):
        super().__init__(seed=seed)
        self.n = n
        self.width = width
        self.height = height
        self.buildingLayer = mesa.space.PropertyLayer("buildingLayer", self.width, self.height, default_value = np.float64(0))
        self.trafficLightLayer = mesa.space.PropertyLayer("trafficLightLayer", self.width, self.height, default_value = np.float64(0) )
        self.parkingLayer = mesa.space.PropertyLayer("parkingLayer", self.width, self.height, default_value = np.float64(0))

        #movement layers
        self.RightLayer = mesa.space.PropertyLayer("RightLayer", self.width, self.height, default_value = np.float64(0))
        self.LeftLayer = mesa.space.PropertyLayer("LeftLayer", self.width, self.height, default_value = np.float64(0))
        self.UpLayer = mesa.space.PropertyLayer("UpLayer", self.width, self.height, default_value = np.float64(0))
        self.DownLayer = mesa.space.PropertyLayer("DownLayer", self.width, self.height, default_value = np.float64(0))


        self.grid = mesa.space.MultiGrid(width,height,True,(self.buildingLayer,
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

            #movement layers
            set_right_Layer(coordinateStructurePositions["Right"])
            set_left_Layer(coordinateStructurePositions["Left"])
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
            for (x,y),isOccupied in coordinateStructurePositions:
                if isOccupied:
                    self.grid.properties["parkingLayer"].set_cell((x, y), 2) #2 occupied
                else:
                    self.grid.properties["parkingLayer"].set_cell((x, y), 1)

        #movement layers
        def set_right_Layer(coordinateStructurePositions):
            for x,y in coordinateStructurePositions:
                self.grid.properties["RightLayer"].set_cell((x, y), 1)

        def set_left_Layer(coordinateStructurePositions):
            for x,y in coordinateStructurePositions:
                self.grid.properties["LeftLayer"].set_cell((x, y), 1)

        def set_up_Layer(coordinateStructurePositions):
            for x,y in coordinateStructurePositions:
                self.grid.properties["UpLayer"].set_cell((x, y), 1)

        def set_down_Layer(coordinateStructurePositions):
            for x,y in coordinateStructurePositions:
                self.grid.properties["DownLayer"].set_cell((x, y), 1)


        set_Data_Structures(dataStructure)


        #Create Traffic Light Agents

        for idSemaphore in dataStructure["Semaphores"]:
            coords = []
            status = False
            for (x,y),value in idSemaphore:
                coords.append((x,y))
                status = value
            agents.TrafficLightAgent(self,idSemaphore,coords,status)


        #Create car Agent:
        for iDCar in range(self.n):
            carAgent = agents.CarAgent(self,True,(0,0),(2,3)) # model, isParked,startingPosition,endingPosition
            self.grid.place_agent(carAgent,(0,0))

        #print(self.grid.properties["RightLayer"].data)

    def step(self):
        self.agents_by_type[agents.TrafficLightAgent].shuffle_do("step")
        self.agents_by_type[agents.CarAgent].shuffle_do("step")

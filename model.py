import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns

class CityModel(mesa.Model):
    def __init__(self, n, width, height, dataStructure ,seed=None):
        super().__init__(seed=seed)
        self.num_Cars = n
        self.buildingLayer = mesa.space.PropertyLayer("buildingLayer", width, height, default_value = np.float64(0))
        self.trafficLightLayer = mesa.space.PropertyLayer("trafficLightLayer", width, height, default_value = np.float64(0) )
        self.parkingLayer = mesa.space.PropertyLayer("parkingLayer", width, height, default_value = np.float64(0))

        #movement layers
        self.RightLayer = mesa.space.PropertyLayer("RightLayer", width, height, default_value = np.float64(0))
        self.LeftLayer = mesa.space.PropertyLayer("LeftLayer", width, height, default_value = np.float64(0))
        self.UpLayer = mesa.space.PropertyLayer("UpLayer", width, height, default_value = np.float64(0))
        self.DownLayer = mesa.space.PropertyLayer("DownLayer", width, height, default_value = np.float64(0))


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
            #set_right_Layer(coordinateStructurePositions["Right"])
            #set_left_Layer(coordinateStructurePositions["Left"])
            #set_up_Layer(coordinateStructurePositions["Up"])
            #set_down_Layer(coordinateStructurePositions["Down"])
            return

        def set_buildingsLayer(buildingsArray):
            for x, y in buildingsArray:
                self.grid.properties["buildingLayer"].set_cell((x, y), 1)

        def set_traffic_lightsLayer(coordinateStructurePositions):
            for (x,y),value in coordinateStructurePositions:
                if value:
                    self.grid.properties["trafficLightLayer"].set_cell((x, y), 40)
                else:
                    self.grid.properties["trafficLightLayer"].set_cell((x, y), 50)

        def set_parking_lotsLayer(coordinateStructurePositions):
            for (x,y),value in coordinateStructurePositions:
                if value:
                    self.grid.properties["parkingLayer"].set_cell((x, y), 20)
                else:
                    self.grid.properties["parkingLayer"].set_cell((x, y), 30)

        def set_round_aboutsLayer(coordinateStructurePositions):
            for x,y in coordinateStructurePositions:
                self.grid.properties["roundAboutLayer"].set_cell((x, y), 10)


        #movement layers
        def set_right_Layer(coordinateStructurePositions):
            for x,y in coordinateStructurePositions:
                self.grid.properties["RightLayer"].set_cell((x, y), 30) #si va este valor?

        def set_left_Layer(coordinateStructurePositions):
            for x,y in coordinateStructurePositions:
                self.grid.properties["LeftLayer"].set_cell((x, y), 40)

        def set_up_Layer(coordinateStructurePositions):
            for x,y in coordinateStructurePositions:
                self.grid.properties["UpLayer"].set_cell((x, y), 50)

        def set_down_Layer(coordinateStructurePositions):
            for x,y in coordinateStructurePositions:
                self.grid.properties["DownLayer"].set_cell((x, y), 60)


        set_Data_Structures(dataStructure)
        #print("Building Layer Data:\n", self.grid.properties["buildingLayer"].data)
        #print("Traffic Layer Data:\n", self.grid.properties["trafficLightLayer"].data)
        #print("Parking Layer Data:\n", self.grid.properties["parkingLayer"].data)


        def printGrid():
            # Dimensions of the grid
            grid_height = len(self.grid.properties["buildingLayer"].data)
            grid_width = len(self.grid.properties["buildingLayer"].data[0])

            for y in range(grid_height):
                row = ""
                for x in range(grid_width):
                    # Check each layer for the current position (x, y)
                    building = self.grid.properties["buildingLayer"].data[y][x]
                    traffic_light = self.grid.properties["trafficLightLayer"].data[y][x]
                    parking = self.grid.properties["parkingLayer"].data[y][x]

                    # Determine the symbol for each cell based on layer presence
                    if building:
                        row += "B "  # B for Building
                    elif traffic_light:
                        row += "T "  # T for Traffic Light
                    elif parking:
                        row += "P "  # P for Parking
                    else:
                        row += ". "  # . for empty space
                print(row)

        printGrid()
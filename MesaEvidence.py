import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns


coordinateStructures = {
    "Buildings": [
        (3,3), (3,4), (3,5), (3,6), (3,7), (3,8), (3,9), (3,11), (3,12),
        (4,4), (4,5), (4,6), (4,7), (4,8), (4,9), (4,10), (4,11), (4,12),
        (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9), (5,10), (5,11),
        (6,3), (6,4), (6,5), (6,6), (6,8), (6,9), (6,10), (6,11), (6,12),
        (9,3), (9,4), (9,5), (9,8), (9,10), (9,11), (9,12), (10,3), (10,4),
        (10,5), (10,8), (10,9), (10,10), (10,11), (10,12), (11,3), (11,4),
        (11,8), (11,9), (11,10), (11,11), (12,3), (12,4), (12,5), (12,8),
        (12,9), (12,10), (12,11), (12,12), (17,3), (17,4), (17,5), (17,6),
        (17,9), (17,10), (17,11), (17,12), (18,4), (18,5), (18,6), (18,9),
        (18,10), (18,11), (18,12), (19,3), (19,4), (19,5), (19,6), (19,9),
        (19,10), (19,11), (19,12), (20,3), (20,4), (20,5), (20,6), (20,9),
        (20,10), (20,11), (20,12), (21,3), (21,4), (21,5), (21,10), (21,11),
        (21,12), (22,3), (22,4), (22,5), (22,6), (22,9), (22,10), (22,11),
        (22,12)
    ],
    "Parking_Lots": [
    [(4, 3), 1], [(3, 10), 1], [(5, 12), 1], [(6, 7), 1],
    [(9, 9), 1], [(11, 5), 1], [(11, 12), 1], [(4, 18), 1],
    [(5, 21), 1], [(10, 22), 1], [(18, 3), 1], [(21, 6), 1],
    [(21, 9), 1], [(18, 18), 1], [(18, 20), 1], [(21, 20), 1]
    ],
    "Semaphores": [
        [(1,18), 10]
    ],
    "Round_Abouts": [
        (14,14), (14,15), (15,14), (15,15), (18,15), (18,16)
    ]
}

class CityModel(mesa.Model):
    def __init__(self, n, width, height, dataStructure ,seed=None):
        super().__init__(seed=seed)
        self.num_Cars = n
        self.buildingLayer = mesa.space.PropertyLayer("buildingLayer", width, height, default_value=0)
        self.trafficLightLayer = mesa.space.PropertyLayer("trafficLightLayer", width, height, default_value= 0 )
        self.parkingLayer = mesa.space.PropertyLayer("parkingLayer", width, height, default_value= 0)
        self.roundAboutLayer = mesa.space.PropertyLayer("roundAboutLayer", width, height, default_value=0)

        self.grid = mesa.space.MultiGrid(width,height,True,(self.buildingLayer,self.trafficLightLayer,self.parkingLayer,self.roundAboutLayer))

        def set_Data_Structures(coordinateStructurePositions):
            set_buildingsLayer(coordinateStructurePositions["Buildings"])
            set_traffic_lightsLayer(coordinateStructurePositions["Semaphores"])
            set_parking_lotsLayer(coordinateStructurePositions["Parking_Lots"])
            set_round_aboutsLayer(coordinateStructurePositions["Round_Abouts"])
            return

        def set_buildingsLayer(buildingsArray):
            for x, y in buildingsArray:
                self.grid.properties["buildingLayer"].set_cell((x, y), 1)

        def set_traffic_lightsLayer(coordinateStructurePositions):
            for (x,y),value in coordinateStructurePositions:
                self.grid.properties["trafficLightLayer"].set_cell((x, y), value)

        def set_parking_lotsLayer(coordinateStructurePositions):
            for (x,y),value in coordinateStructurePositions:
                self.grid.properties["parkingLayer"].set_cell((x, y), value)

        def set_round_aboutsLayer(coordinateStructurePositions):
            for x,y in coordinateStructurePositions:
                self.grid.properties["roundAboutLayer"].set_cell((x, y), 10)


        set_Data_Structures(dataStructure)
        print("Building Layer Data:", self.grid.properties["buildingLayer"].data)
        print("Traffic Layer Data:", self.grid.properties["trafficLightLayer"].data)
        print("Parking Layer Data:", self.grid.properties["parkingLayer"].data)
        print("Roundabout Layer Data:", self.grid.properties["roundAboutLayer"].data)


class CarAgent(mesa.Agent):
    def __init__(self, model, startPosition, isParked, destinationPosition):
        super().__init__(model)
        self.pos = startPosition
        self.startPosition = startPosition
        self.isParked = isParked
        self.destination = destinationPosition
        self.wait_time = 0  
        self.max_wait_time = 5 

    def move(self):

        if self.isParked:
            return
        
        # 1. Verificar si el coche está cerca de un semáforo y si está en rojo
        nearby_traffic_lights = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)
        for neighbor in nearby_traffic_lights:
            if isinstance(neighbor, TrafficLightAgent):
                if not neighbor.state: 
                    self.wait_time += 1
                    if self.wait_time >= self.max_wait_time:
                        self.wait_time = 0
                    return 

        # 2. Verificar si hay vehículos bloqueando el camino
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)
        for neighbor_pos in neighbors:
            if any(isinstance(agent, CarAgent) for agent in self.model.grid.get_cell_list_contents(neighbor_pos)):
                return

        direction = self.get_direction_to_destination()
        new_pos = self.calculate_new_position(direction)
        if self.is_valid_move(new_pos):
            self.model.grid.move_agent(self, new_pos)


    def park(self):
      '''
      Would only change the variables property.
      '''

    def step(self):
      #The decision to move will always happen, just how it's going to work, will be
      #Diff for the
        self.move()



'''
Depending on how me want to work with the information and the sempahore:
AKA Use just bool or have red,green,yellow
Each approach would be different.
The following approach will be with bool:
'''
class TrafficLightAgent(mesa.Agent):
    def __init__(self, model, status):
        super().__init__(self, model)
        self.state = status
        self.clock = 0

    def change_light(self):
      if self.state:
        self.state = False
        #Modify the property grid
      else:
        self.state = True

    def step(self):
      self.clock += 1

      if self.clock == 10:
        self.change_light()
        clock = 0


model = CityModel(1,24,24,coordinateStructures)

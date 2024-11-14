import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns

#Hola Mundo COmo estan
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
        (1, 18), (3, 19),  
        (2, 18), (3, 20) , 
        (7, 3), (6, 23),  
        (8, 3), (6, 24),  
        (7, 8), (9, 1), 
        (8, 8), (9, 2),  
        (7, 22), (9, 6), 
        (8, 22), (9, 7), 
        (19, 17), (18, 15),  
        (20, 17), (18, 16),  
    ],

    #might be deleted 
    "Round_Abouts": [
        (14,14), (14,15), (15,14), (15,15), (18,15), (18,16)
    ],

    "Right":[(2, 23), (3, 23), (4, 23), (5, 23), (6, 23), (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23), (13, 23), (14, 23), (15, 23), (16, 23), (17, 23), (18, 23), (19, 23), 
    (20, 23), (21, 23), (22, 23), (23, 23), (2, 24), (3, 24), (4, 24), (5, 24), (6, 24), (7, 24), (8, 24), (9, 24), (10, 24), (11, 24), (12, 24), (13, 24), (14, 24), (15, 24), (16, 24),
    (17, 24), (18, 24), (19, 24), (20, 24), (21, 24), (22, 24), (23, 24), (2, 15), (3, 15), (4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (2, 16), 
    (3, 16), (4, 16), (5, 16), (6, 16), (7, 16), (8, 16), (9, 16), (10, 16), (11, 16), (12, 16), (17, 15), (18, 15), (19, 15), (20, 15), (21, 15), (22, 15), (23, 15), (17, 16), (18, 16),
    (19, 16), (20, 16), (21, 16), (22, 16), (23, 16), (8, 19), (9, 19), (10, 19), (11, 19), (12, 19), (13, 19), (8, 20), (9, 20), (10, 20), (11, 20), (12, 20), (13, 20)],

    "Left":[(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1), (17, 1), (18, 1), (19, 1), (20, 1), (21, 1), (22, 1),
    (23, 1), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2), (15, 2), (16, 2), (17, 2), (18, 2), (19, 2), (20, 2), (21, 2), (22, 2), 
    (23, 2), (16, 7), (17, 7), (18, 7), (19, 7), (20, 7), (21, 7), (22, 7), (23, 7), (16, 8), (17, 8), (18, 8), (19, 8), (20, 8), (21, 8), (22, 8), (23, 8), (8, 7), (9, 7), (10, 7), (11, 7), (12, 7),
    (13, 7), (8, 8), (9, 8), (10, 8), (11, 8), (12, 8), (13, 8), (17, 13), (18, 13), (19, 13), (20, 13), (21, 13), (22, 13), (23, 13), (17, 14), (18, 14), (19, 14), (20, 14), (21, 14), (22, 14), (23, 14),
    (2, 13), (3, 13), (4, 13), (5, 13), (6, 13), (7, 13), (8, 13), (9, 13), (10, 13), (11, 13), (12, 13), (2, 14), (3, 14), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 14), (11, 14), (12, 14),
    (2, 19), (3, 19), (4, 19), (5, 19), (6, 19), (7, 19), (2, 20), (3, 20), (4, 20), (5, 20), (6, 20), (7, 20)] ,

    "Up":[(23, 2), (23, 3), (23, 4), (23, 5), (23, 6), (23, 7), (23, 8), (23, 9), (23, 10), (23, 11), (23, 12), (23, 13), (23, 14), (23, 15), (23, 16), (23, 17), (23, 18), (23, 19), (23, 20), (23, 21), (23, 22),
    (23, 23), (24, 2), (24, 3), (24, 4), (24, 5), (24, 6), (24, 7), (24, 8), (24, 9), (24, 10), (24, 11), (24, 12), (24, 13), (24, 14), (24, 15), (24, 16), (24, 17), (24, 18), (24, 19), (24, 20), (24, 21), (24, 22),
    (24, 23), (15, 2), (15, 3), (15, 4), (15, 5), (15, 6), (15, 7), (15, 8), (15, 9), (15, 10), (15, 11), (15, 12), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6), (16, 7), (16, 8), (16, 9), (16, 10), (16, 11), (16, 12), 
    (15, 17), (15, 18), (15, 19), (15, 20), (15, 21), (15, 22), (15, 23), (16, 17), (16, 18), (16, 19), (16, 20), (16, 21), (16, 22), (16, 23), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), 
    (7, 11), (7, 12), (7, 13), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (19, 16), (19, 17), (19, 18), (19, 19), (19, 20), (19, 21), (19, 22), (19, 23), (20, 16),
    (20, 17), (20, 18), (20, 19), (20, 20), (20, 21), (20, 22), (20, 23)],

    "Down":[(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20), (1, 21), (1, 22), (1, 23), (2, 2), (2, 3),
    (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18), (2, 19), (2, 20), (2, 21), (2, 22), (2, 23), (7, 17), (7, 18), (7, 19), (7, 20), (7, 21), 
    (7, 22), (7, 23), (8, 17), (8, 18), (8, 19), (8, 20), (8, 21), (8, 22), (8, 23), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (13, 8), (13, 9), (13, 10), (13, 11), (13, 12), (13, 13), (14, 3), (14, 4), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (13, 17), (13, 18), (13, 19), (13, 20), (13, 21), (13, 22), (13, 23), (14, 17), (14, 18), (14, 19), (14, 20), (14, 21), (14, 22), (14, 23)]

    
}

class CityModel(mesa.Model):
    def __init__(self, n, width, height, dataStructure ,seed=None):
        super().__init__(seed=seed)
        self.num_Cars = n
        self.buildingLayer = mesa.space.PropertyLayer("buildingLayer", width, height, default_value = np.float64(0))
        self.trafficLightLayer = mesa.space.PropertyLayer("trafficLightLayer", width, height, default_value = np.float64(0) )
        self.parkingLayer = mesa.space.PropertyLayer("parkingLayer", width, height, default_value = np.float64(0))
        self.roundAboutLayer = mesa.space.PropertyLayer("roundAboutLayer", width, height, default_value = np.float64(0))

        #movement layers 
        self.RightLayer = mesa.space.PropertyLayer("RightLayer", width, height, default_value = np.float64(0))
        self.LeftLayer = mesa.space.PropertyLayer("LeftLayer", width, height, default_value = np.float64(0))
        self.UpLayer = mesa.space.PropertyLayer("UpLayer", width, height, default_value = np.float64(0))
        self.DownLayer = mesa.space.PropertyLayer("DownLayer", width, height, default_value = np.float64(0))


        self.grid = mesa.space.MultiGrid(width,height,True,(self.buildingLayer,self.trafficLightLayer,self.parkingLayer,self.roundAboutLayer, self.RightLayer, self.LeftLayer, self.UpLayer, self.DownLayer))

        def set_Data_Structures(coordinateStructurePositions):
            set_buildingsLayer(coordinateStructurePositions["Buildings"])
            set_traffic_lightsLayer(coordinateStructurePositions["Semaphores"])
            set_parking_lotsLayer(coordinateStructurePositions["Parking_Lots"])
            set_round_aboutsLayer(coordinateStructurePositions["Round_Abouts"])

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
            for (x,y),value in coordinateStructurePositions:
                self.grid.properties["trafficLightLayer"].set_cell((x, y), value)

        def set_parking_lotsLayer(coordinateStructurePositions):
            for (x,y),value in coordinateStructurePositions:
                self.grid.properties["parkingLayer"].set_cell((x, y), value)

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
        print("Building Layer Data:", self.grid.properties["buildingLayer"].data)
        print("Traffic Layer Data:", self.grid.properties["trafficLightLayer"].data)
        print("Parking Layer Data:", self.grid.properties["parkingLayer"].data)
        print("Roundabout Layer Data:", self.grid.properties["roundAboutLayer"].data)

        #movement layers 
        print("Right Layer Data:", self.grid.properties["RightLayer"].data)
        print("Down Layer Data:", self.grid.properties["DownLayer"].data)
        print("Up Layer Data:", self.grid.properties["UpLayer"].data)
        print("Down Layer Data:", self.grid.properties["DownLayer"].data)


class CarAgent(mesa.Agent):
  #Decide which position the car starts, will be done in the model.
    def __init__(self, model, startPosition,isParked,destinationPosition):
        super().__init__(model)
        self.startPosition = startPosition
        self.isParked = isParked
        self.destination = destinationPosition

    def move(self):
      '''
      Possible PSEUDOCODE:

      1. Check if car is parked:
        If the car is parked and doesn't need to move we don't advance the movement.

      2. Check for Semaphore near you.
        IF there is and it's green we can continue.
        If not we don't advance.

      3. Check for any car that is in front or right,left...:
        If there is no car in front or right,left:
      '''

      if self.isParked:
            return

        

    def park(self):
      #Park implementar 
      #moore property
      neighbors = self.model.grid.get_neighbors(self.pos, moore = True, include_center=False, radius = 1)
      found_parking_spot = False

      for neighbor_pos in neighbors:
        if not any(isinstance(agent, CarAgent) for agent in self.model.grid.get_cell_list_contents(neighbor_pos)):
           self.model.grid.move_agent(self, neighbor_pos)
           self.isParked = True
           found_parking_spot = True
           break
        
      if not found_parking_spot:
         radius = 2
         while not found_parking_spot and radius <= 3:
            extended_neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=radius)
            for neighbor_pos in extended_neighbors:
                if not any(isinstance(agent, CarAgent) for agent in self.model.grid.get_cell_list_contents(neighbor_pos)):
                    self.model.grid.move_agent(self, neighbor_pos)
                    self.isParked = True
                    found_parking_spot = True
                    break
            radius += 1
        
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

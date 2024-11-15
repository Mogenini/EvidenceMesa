import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns
import model

class CarAgent(mesa.Agent):
    def __init__(self, model, isParked,startingPosition,endingPosition):
        super().__init__(model)
        self.model = model
        self.has_parked = isParked
        self.startingPosition = startingPosition
        self.endingPosition = endingPosition

    def move(self):
        '''
        The Movement is gonna be inverse first Y then X
        '''
        if self.pos == self.endingPosition:
            self.has_parked = True
            return

        self.has_parked = False
        x,y = self.pos
        if self.model.grid.properties["trafficLightLayer"].data[y,x] == 2:
            return

        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)


        print(neighbors)









    def step(self):
        self.move()
        pass
        #if not self.has_parked:
        #    if self.destination is None:
        #        self.find_parking_spot()
        #    else:
        #        self.move()

class TrafficLightAgent(mesa.Agent):
    def __init__(self, model, idSemaphore,coordinatesPosition,Status):
        super().__init__(model)
        self.clock = 0
        self.semaphorePosition = coordinatesPosition
        self.semaphoreId = idSemaphore
        self.state = Status

    def change_light(self):
        if self.state:
            self.state = False
            for x,y in self.semaphorePosition:
                self.model.grid.properties["trafficLightLayer"].set_cell((x, y), 1) #Change to red

        else:
            self.state = True
            for x,y in self.semaphorePosition:
                self.model.grid.properties["trafficLightLayer"].set_cell((x, y), 2) #Change to green


    def step(self):
        self.clock += 1
        if self.clock == 1:
            self.change_light()
            clock = 0

import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns


class CarAgent(mesa.Agent):
    # Decide which position the car starts, will be done in the model.
    def __init__(self, model, startPosition, isParked, destinationPosition):
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
        '''
        Would only change the variables property.
        '''

    def step(self):
        # The decision to move will always happen, just how it's going to work, will be
        # Diff for the
        self.move()


'''
Depending on how me want to work with the information and the sempahore:
AKA Use just bool or have red,green,yellow
Each approach would be different.
The following approach will be with bool:
'''

'''

'''

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
                self.model.grid.properties["trafficLightLayer"].set_cell((x, y), 50) #Change to red

        else:
            self.state = True
            for x,y in self.semaphorePosition:
                self.model.grid.properties["trafficLightLayer"].set_cell((x, y), 40) #Change to red


    def step(self):
        self.clock += 1
        if self.clock == 1:
            self.change_light()
            clock = 0
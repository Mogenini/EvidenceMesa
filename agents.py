import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns
import model

def calculate_distance(start, end):
    """Calculate the Manhattan distance between two points."""
    x1, y1 = start
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)


class CarAgent(mesa.Agent):
    def __init__(self, model, isParked,startingPosition,endingPosition):
        super().__init__(model)
        self.model = model
        self.has_parked = isParked
        self.startingPosition = startingPosition
        self.endingPosition = endingPosition

    def move(self):

        print(f"Starting Position: {self.pos}")
        if self.pos == self.endingPosition:
            self.has_parked = True
            print(f"The car reached: {self.pos} from {self.startingPosition}")
            return

        '''
        If it isn't in it's endingPosition it means it's moving
        Check if there is a trafficLight on or off
        '''
        self.has_parked = False
        x,y = self.pos
        if self.model.grid.properties["trafficLightLayer"].data[x,y] == 2:
            print(f"Semaphore in red: {self.pos}")
            return

        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        possibleMoves = []
        for neighbor in neighbors:
            xNeighbor,yNeighbor = neighbor

            #Right Movment
            if xNeighbor == x + 1:
                if self.model.grid.properties["RightLayer"].data[xNeighbor, yNeighbor] == 1:
                    possibleMoves.append(neighbor)
            #Left Movement
            if xNeighbor == x - 1:
                if self.model.grid.properties["LeftLayer"].data[xNeighbor, yNeighbor] == 1:
                    possibleMoves.append(neighbor)
            #Up Movement
            if yNeighbor == y + 1:
                if self.model.grid.properties["DownLayer"].data[xNeighbor, yNeighbor] == 1:
                    possibleMoves.append(neighbor)
            #Down Movemnt
            if yNeighbor == y - 1:
                if self.model.grid.properties["UpLayer"].data[xNeighbor, yNeighbor] == 1:
                    possibleMoves.append(neighbor)

        if possibleMoves:
            '''
            Right Now we can do a distance method to obtain the quickest possible path, 
            But in the final delivery we can do a BFS. 
            '''
            possibleMoves.sort(key=lambda move: calculate_distance(move, self.endingPosition))
            xNewPos,yNewPos = possibleMoves[0]

            if self.model.grid.is_cell_empty((xNewPos,yNewPos)):
                print(f"New position: {xNewPos,yNewPos}")
                self.model.grid.move_agent(self, (xNewPos, yNewPos))
            return


    def step(self):
        self.move()


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

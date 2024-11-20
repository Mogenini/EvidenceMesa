from collections import deque

import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns
import model

def calculate_distance(start, end):
    x1, y1 = start
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)


class CarAgent(mesa.Agent):
    def __init__(self, model, isParked,startingPosition,endingPosition):
        super().__init__(model)
        self.model = model
        self.isParked = isParked
        self.startingPosition = startingPosition
        self.endingPosition = endingPosition
        self.path = []

    def move(self):
        #Change the value of the grid if the car was parked

        print(f"Starting Position: {self.pos}")
        if self.pos == self.endingPosition:
            self.isParked = True
            print(f"The car reached: {self.pos} from {self.startingPosition}")
            return

        '''
        If it isn't in it's endingPosition it means it's moving
        Check if there is a trafficLight on or off
        '''
        self.isParked = False
        x,y = self.pos
        if self.model.grid.properties["trafficLightLayer"].data[x,y] == 2:
            print(f"Semaphore in red: {self.pos}")
            return

        if self.path: #We have [initial position saved, all other are the position we move]
            xNewPos, yNewPos = self.path[0]
            if self.model.grid.is_cell_empty((xNewPos, yNewPos)):
                self.model.grid.move_agent(self, (xNewPos, yNewPos))
                self.path.pop(0)
        return


    def step(self):
        if not self.path:
            self.obtainRoute()
        self.move()

    def obtainRoute(self):
        route = self.bfs(self.startingPosition,self.endingPosition)
        print(route)
        if route:
            route.pop(0)
            self.path = route
            print(f"The path he will take is: {self.path}")


    def bfs(self,startingPosition, endingPosition):
        print(f"Data on right layer  {self.model.grid.properties["RightLayer"].data} ")
        queue = deque([startingPosition])
        visitedPositions = set()
        visitedPositions.add(startingPosition)
        path = {startingPosition: None}
        while queue:
            currentPosition = queue.popleft()
            print(f"current Position: {currentPosition}")
            if currentPosition == endingPosition:
                print(path)
                route = []
                while currentPosition:
                    route.append(currentPosition)
                    currentPosition = path[currentPosition]
                route.reverse()
                return route

            neighbors = self.model.grid.get_neighborhood(currentPosition, moore=False, include_center=False)
            for neighbor in neighbors:
                if neighbor not in visitedPositions:
                    if self.checkMovementBFS(currentPosition, neighbor):
                        visitedPositions.add(neighbor)
                        path[neighbor] = currentPosition
                        queue.append(neighbor)
        return False

    def checkMovementBFS(self,currentPosition, positionToMove):
        x, y = currentPosition
        xNeighbor, yNeighbor = positionToMove
        #Down
        if xNeighbor == x + 1:
            print(f"Down Movement: {currentPosition}")
            if self.model.grid.properties["DownLayer"].data[x, y] == 1:
                print("Entered Down")
                return True

        # LUp
        if xNeighbor == x - 1:
            print(f"Up Movement: {currentPosition}")
            if self.model.grid.properties["UpLayer"].data[x, y] == 1:
                print("Entered Up")
                return True

        # Right
        if yNeighbor == y + 1:

            if self.model.grid.properties["RightLayer"].data[x, y] == 1:
                print("Entered Right")
                return True

        # Left
        if yNeighbor == y - 1:
            print(f"Left Movement: {currentPosition}")
            if self.model.grid.properties["LeftLayer"].data[x, y] == 1:
                print("Entered Left")
                return True
        return False


class TrafficLightAgent(mesa.Agent):
    def __init__(self, model, idSemaphore,coordinatesPosition,Status):
        super().__init__(model)
        self.clock = 0
        self.semaphorePosition = coordinatesPosition
        self.semaphoreId = idSemaphore
        self.state = Status

    def change_light(self):
        self.clock += 1
        if self.clock == 5:
            #print(f"Changing the light of: {self.semaphorePosition}")
            self.clock = 0
            if self.state:
                self.state = False
                for x,y in self.semaphorePosition:
                    self.model.grid.properties["trafficLightLayer"].set_cell((x, y), 1) #Change to red
            else:
                self.state = True
                for x,y in self.semaphorePosition:
                    self.model.grid.properties["trafficLightLayer"].set_cell((x, y), 2) #Change to green


    def step(self):
        self.change_light()


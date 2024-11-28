from collections import deque
import mesa

import mesa
from collections import deque

'''
Agent: Traffic Light
    Data Management:
    [[],[]] Group of semaphores
    [status,status]
    idSemaphore
    [clock1,clock2]
    [[Set of coordinates],[Set of coordinates]]
    '''
class TrafficLightAgent(mesa.Agent):
    def __init__(self, model, idSemaphore,semaphorePositions,Status,sensorPositions):
        super().__init__(model)
        self.clock = [0,0]
        self.semaphorePosition = semaphorePositions
        self.semaphoreId = idSemaphore
        self.state = Status
        self.sensorsCoordinates = sensorPositions
        self.activeSemaphore = None


    def change_light(self):
        if self.activeSemaphore is not None:
            if self.clock[self.activeSemaphore] > 0:
                self.clock[self.activeSemaphore] -= 1
                print(f"The Semaphore {self.semaphorePosition[self.activeSemaphore]} is now green.")
                print(f"The Semaphore {self.semaphorePosition[self.activeSemaphore]} is now red.")
                return
            else:
                nextSemaphore = 1 if self.activeSemaphore == 0 else 0
                if self.clock[nextSemaphore] > 0:
                    self.state = [self.activeSemaphore == 0, self.activeSemaphore == 1] #If the numbers are the same that means True else False
                    self.activeSemaphore = nextSemaphore
                    self.changeProperty()
                    return
                else:
                    self.activeSemaphore = None
                    self.state = [False,False]
                    for positionArray in self.semaphorePosition:
                        for pos in positionArray:
                            self.model.grid.properties["trafficLightLayer"].set_cell(pos, 3)  # Change to YELLOW
                    return


        #Start changing the logic
        amountCards = []
        for semaphoreSensorArray in self.sensorsCoordinates:
            temp = 0
            for pos in semaphoreSensorArray:
                if self.model.grid.is_cell_empty(pos) == False:
                    temp += 1
            amountCards.append(temp)

        if amountCards[0] == 0 and amountCards[1] == 0:
            print(f"The Semaphore in {self.semaphorePosition} are in yellow")
            self.activeSemaphore = None
            self.state = [False, False]
            for positionArray in self.semaphorePosition:
                for pos in positionArray:
                    self.model.grid.properties["trafficLightLayer"].set_cell(pos, 3)  # Change to YELLOW
            return

        timeClock = len(self.sensorsCoordinates[0]) // 2
        self.clock[0] = amountCards[0] * timeClock + timeClock
        timeClock = len(self.sensorsCoordinates[1]) // 2
        self.clock[1] = amountCards[1] * timeClock + timeClock
        self.activeSemaphore = 0 if self.clock[0] >= self.clock[1] else 1
        self.state = [self.activeSemaphore == 0, self.activeSemaphore == 1]
        self.changeProperty()


    def changeProperty(self):
        for idx,semaphorePositionArray in enumerate(self.semaphorePosition):
            for pos in semaphorePositionArray:
                if self.state[idx]: #They are green
                    self.model.grid.properties["trafficLightLayer"].set_cell(pos, 1) #Change to Red
                else:
                    self.model.grid.properties["trafficLightLayer"].set_cell(pos, 2) #Change to Green

    def step(self):
        self.change_light()

    def getPositions(self):
        return self.semaphorePosition

    def getState(self):
        return self.state


'''
Agent: Car Agent
'''
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

        #print(f"Starting Position: {self.pos}")
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
        print(f"Data on right layer  {self.model.grid.properties['RightLayer'].data} ")
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







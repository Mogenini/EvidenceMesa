import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns
import model

class CarAgent(mesa.Agent):
    def _init_(self, model, has_parked):
        super()._init_(model)
        self.model = model
        self.destination = None 
        self.has_parked = has_parked 
        

    def move(self):
        if self.destination:
            next_moves = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            possible_moves = [move for move in next_moves if self.valid_move(move)]
            #agregar lo de valid direction 

            if possible_moves:
                new_position = min(possible_moves, key=lambda x: self.distance_to_destination(x))
                if not self.is_blocked_by_semaphore(new_position):
                    if self in self.model.grid.get_cell_list_contents([self.pos]):
                        self.model.grid.remove_agent(self)
                    self.model.grid.place_agent(self, new_position)
                    self.pos = new_position
                    if self.pos == self.destination:
                        self.has_parked = True
                        self.check_relocation()

    def park(self):
        if self.destination:  
            parking_layer = self.model.grid.properties["parkingLayer"]
            if parking_layer.get_cell(self.destination) == 30:  
                parking_layer.set_cell(self.destination, 20)  
                self.model.grid.remove_agent(self)  
                self.model.grid.place_agent(self, self.destination)  
                self.pos = self.destination  
                self.has_parked = True  


    def check_relocation(self):
        parking_layer = self.model.grid.properties["parkingLayer"]
        if parking_layer.get_cell(self.pos) == 20:
            self.model.cars_relocated += 1


    def valid_move(self, pos):
        #x,y = pos 
        if self.grid.properties["buildinglayer"].data[pos.x,pos.y] == 1:
            return False
        return self.valid_direction(pos)
    
    #ver que no haya un carro adelante 
    def valid_car(self,pos):
            neighbors = self.model.grid.get_neighborhood(pos, moore=False, include_center=False)
            for neighbor in neighbors:
                cell_contents = self.model.grid.get_cell_list_contents([neighbor])  
                if any(isinstance(agent, CarAgent) for agent in cell_contents):  
                    return False  
            return True

    def valid_direction(self,pos):
        Right_layer = self.model.grid.properties["RightLayer"]
        Left_layer = self.model.grid.properties["LeftLayer"]
        Up_layer = self.model.grid.properties["UpLayer"]
        Down_layer = self.model.grid.properties["buildLayer"]

        current_x, current_y = self.pos
        new_x, new_y = pos

        if new_x > current_x:
            current_direction = "Down"
        elif new_x < current_x:
            current_direction = "Up"
        elif new_y > current_y:
            current_direction = "Right"
        elif new_y < current_y:
            current_direction = "Left"
        else:
            return False

        if current_direction == "Right" and Right_layer.get_cell(pos) <= 0:
            return True
        elif current_direction == "Left" and Left_layer.get_cell(pos) <= 0:
            return True
        elif current_direction == "Up" and Up_layer.get_cell(pos) <= 0:
            return True
        elif current_direction == "Down" and Down_layer.get_cell(pos) <= 0:
            return True
        
        return False
            

    def trafficLightCondition(self, pos):
        #40 is green 50 is red 
        if self.grid.properties["Sempahores"].data[pos.x,pos.y] == 40: 
            return True
        return False 
        

    def step(self):
        if not self.has_parked:
            if self.destination is None:
                self.find_parking_spot()
            else:
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

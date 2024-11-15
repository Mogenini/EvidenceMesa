import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns
import model

class CarAgent(mesa.Agent):
    def __init__(self, model, has_parked):
        super().__init__(model)
        self.model = model
        self.destination = None 
        self.has_parked = has_parked 
        
    #definir estacionamiento aleatorio 

    #como lo quiere el profe 
    #llegar a un coordinada y comprobar si esta ocupada o no 
    def find_parking_spot(self):
        parking_layer = self.model.grid.properties["parkingLayer"]
        for (x, y), value in np.ndenumerate(parking_layer.data):
            if value == 30:  # 30 representa un estacionamiento disponible
                self.destination = (x, y)
                parking_layer.set_cell((x, y), 20)  # Reservar el espacio
                return True
        return False


    def move(self):
        """Mueve el auto hacia su destino evitando edificios y respetando semáforos."""
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

    def check_relocation(self):
        """Verifica si el auto se trasladó entre estacionamientos."""
        parking_layer = self.model.grid.properties["parkingLayer"]
        if parking_layer.get_cell(self.pos) == 20:
            self.model.cars_relocated += 1


    def valid_move(self, pos):
        #x,y = pos 
        if self.grid.properties["buildinglayer"].data[pos.x,pos.y] == 1:
            return False
        return self.valid_direction(pos)
    
    #ver que no haya un carro adelante 
    def valid_car(self,pos)



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
        """Busca estacionamiento o se mueve hacia él."""
        if not self.has_parked:
            if self.destination is None:
                self.find_parking_spot()
            else:
                self.move()






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
      Would only change the variables property. Implemented the logic behind the neighbors
      '''
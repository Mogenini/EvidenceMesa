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
        
    def park(self):
            if self.destination:  
                parking_layer = self.model.grid.properties["parkingLayer"]
                if parking_layer.get_cell(self.destination) == 30:  
                    parking_layer.set_cell(self.destination, 20)  
                    self.model.grid.remove_agent(self)  
                    self.model.grid.place_agent(self, self.destination) 
                    self.pos = self.destination  
                    self.has_parked = True  

    #verificar que no haya un edificio 
    def valid_move(self, pos):
        #x,y = pos 
        if self.grid.properties["buildinglayer"].data[pos.x,pos.y] == 1:
            return False
        return self.valid_direction(pos)
    
    #verificar que no haya un carro adelante 
    def valid_car(self,pos):
        neighbors = self.model.grid.get_neighborhood(pos, moore=False, include_center=False)
        for neighbor in neighbors:
            cell_contents = self.model.grid.get_cell_list_contents([neighbor])  
            if any(isinstance(agent, CarAgent) for agent in cell_contents):  
                return False  
        return True 


    #verificar a donde te puedes mover 
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

def move(self):

    if self.has_parked:  
        return

    if self.destination:  
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)

        # Filtrar los movimientos válidos según las reglas
        possible_moves = [
            move for move in next_moves
            if self.valid_move(move) and self.valid_direction(move) and not self.is_blocked_by_semaphore(move)
        ]

        if possible_moves:  # Si hay movimientos válidos
            # Seleccionar el movimiento más cercano al destino
            new_position = min(possible_moves, key=lambda x: self.distance_to_destination(x))

            # Verificar si hay un carro en el próximo movimiento
            if not self.valid_car(new_position):
                # Intentar cambiar de carril
                side_moves = self.get_side_moves(new_position)
                side_moves = [
                    move for move in side_moves
                    if self.valid_move(move) and self.valid_direction(move) and self.valid_car(move) and not self.is_blocked_by_semaphore(move)
                ]

                if side_moves:
                    # Si hay movimientos laterales válidos, elige el más cercano al destino
                    new_position = min(side_moves, key=lambda x: self.distance_to_destination(x))
                else:
                    # No puede cambiar de carril ni avanzar, termina el movimiento
                    print(f"Car {self.unique_id}: No puede avanzar ni cambiar de carril.")
                    return

            # Mover al agente a la posición seleccionada
            self.model.grid.move_agent(self, new_position)
            self.pos = new_position

            # Si llegó al destino, intentar estacionarse
            if self.pos == self.destination:
                self.park()
        

    def step(self):

        if self.has_parked:  # Si ya está estacionado, no hace nada
            return

        if not self.destination:  # Si no tiene destino, buscar espacio de estacionamiento
            self.find_parking_spot()
        else:
            self.move()  # Moverse hacia el destino

            if self.pos == self.destination:  # Si llegó al destino, estacionarse
                self.park()



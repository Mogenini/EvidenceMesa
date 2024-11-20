import mesa
from mesa.space import MultiGrid
import numpy as np
import seaborn as sns
import model
from collections import deque

def calculate_distance(start, end):
    x1, y1 = start
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)


class CarAgent(mesa.Agent):
    def __init__(self, model, isParked, startingPosition, endingPosition):
        super().__init__(model)
        self.model = model
        self.isParked = isParked
        self.startingPosition = startingPosition
        self.endingPosition = endingPosition

    def bfs(self, start, goal):
        """
        Implementación de BFS para encontrar el camino más corto de start a goal.
        """
        print(f"CarAgent {self.unique_id} starting BFS from {start} to {goal}")

        # Inicializa la cola con la posición inicial
        queue = deque([(start, [start])])  # Cada elemento: (posición actual, camino recorrido hasta ahora)
        visited = set()  # Conjunto para rastrear posiciones visitadas

        while queue:
            # Extrae la primera posición de la cola
            current, path = queue.popleft()
            print(f"BFS - Current: {current}, Path so far: {path}")

            if current in visited:
                continue
            visited.add(current)

            # Si llegamos al destino, devolvemos el camino
            if current == goal:
                print(f"BFS - Path found for CarAgent {self.unique_id}: {path}")
                return path

            # Obtén los vecinos de la posición actual
            neighbors = self.model.grid.get_neighborhood(
                current, moore=False, include_center=False
            )
            print(f"BFS - Neighbors for {current}: {neighbors}")

            for neighbor in neighbors:
                x, y = neighbor

                # Verifica si el vecino está bloqueado en la capa de edificios
                if self.model.buildingLayer.data[x, y] != 0:
                    print(f"Neighbor {neighbor} is blocked by a building.")
                    continue

                # Agrega el vecino a la cola si no ha sido visitado
                if neighbor not in visited:
                    print(f"Adding neighbor {neighbor} to queue.")
                    queue.append((neighbor, path + [neighbor]))

        # Si no encontramos un camino, devolvemos un camino vacío
        print(f"BFS - No path found for CarAgent {self.unique_id}")
        return []

    def move(self):
        print(f"Starting Position: {self.pos}")

        # Verifica si el agente ya llegó a su destino
        if self.pos == self.endingPosition:
            self.isParked = True
            print(f"The car reached: {self.pos} from {self.startingPosition}")
            return

        self.isParked = False  # El agente no está estacionado aún
        x, y = self.pos

        # Si el semáforo está en rojo, el agente no se mueve
        if self.model.trafficLightLayer.data[x, y] == 2:
            print(f"Semaphore in red: {self.pos}")
            return

        # Calcula el camino más corto con BFS
        path = self.bfs(self.pos, self.endingPosition)
        print(f"Calculated path for CarAgent {self.unique_id}: {path}")

        # Intenta moverse al siguiente paso si hay un camino
        if len(path) > 1:  # El camino incluye el siguiente movimiento
            next_position = path[1]
            if self.model.grid.is_cell_empty(next_position):  # Verifica si la celda está vacía
                print(f"Agent {self.unique_id} moving from {self.pos} to {next_position}")
                self.model.grid.move_agent(self, next_position)
            else:
                print(f"Agent {self.unique_id} cannot move to {next_position}, cell occupied.")
        else:
            print(f"Agent {self.unique_id} has no valid moves.")

            #Aqui termina 


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
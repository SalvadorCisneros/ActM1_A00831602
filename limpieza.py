#Salvador Alejandro Cisneros Sanchez - A00831602

from copy import deepcopy
from mesa import Agent, Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.batchrunner import BatchRunner

class CeldasBasura(Agent): 
    '''
    Clase para representar la basura dentro de una celda.
    '''
    def _init_(self, unique_id, model):
        super()._init_(unique_id, model)
        
class RobotLimpiador(Agent):
    '''
    Clase que representa a una aspiradora.
    Su inicializador recibe una id única: unique_id, y el modelo al que pertenece
    '''
    # Número de pasos realizados
    PasosRobot = 0
    
    # Constructor
    def __init__(self, unique_id, model): 
        super().__init__(unique_id, model)
    
    def moveAgent(self): 
        '''
        Función que representa un movimiento del robot,
        eligiendo un vecino aleatorio.
        '''
        
        # Se buscan las celdas vecinas a las que se puede mover el agente
        posiblespasos = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        
        # Se escoge una celda de manera aleatoria
        nuevaposicion = self.random.choice(posiblespasos)
        
        # Se mueve al agente a dicha celda
        self.model.grid.move_agent(self, nuevaposicion)

    def limpiar(self, agent): 
        '''
        Se elimina la basura de una celda.
        '''
        self.model.grid.remove_agent(agent)
        self.model.celdasLimpias += 1
        self.model.cont -= 1


    def step(self): 
        '''
        Función que modela el comportamiento de una aspiradora en cada paso
        del modelo. Debe limpiar una celda o moverse.
        '''
        # Se obtienen todos los agentes en la celda donde está la aspiradora
        gridContent = self.model.grid.get_cell_list_contents([self.pos])
        trash = False
        trashElement = None
        
        # Se busca basura en la celda
        for element in gridContent:
            if isinstance(element, CeldasBasura):
                trash = True
                trashElement = element
        # Si no se encuentra basura, se mueve al agente
        if not trash:
            RobotLimpiador.PasosRobot += 1
            self.moveAgent()
        # Si se encuentra basura, se elimina 
        else:
            self.limpiar(trashElement)

class RobotModel(Model): 
    '''
    Modelo que representa la simulación.
    Recibe el número de agentes: numAgents, las dimensiones de la cuadrícula: height y width,
    el porcentaje de celdas sucias: litterpercetage y el tiempo límite de la simulación: steps.
    '''
    def __init__(self, numAgents, height, width, litterpercentage, steps):
        self.grid = MultiGrid(height, width, False)                 # Crear cuadrícula
        self.numAgents = numAgents                                  # Establecer el número de agentes
        self.time = steps                                           # Tiempo límite 
        self.pasoscursados = 0                                      # Número de pasos transcurridos
        self.celdasSucias = int((litterpercentage * (width*height)) / 100) # Número de celdas sucias (porcentaje)
        self.celdasLimpias = 0 
        self.cont = deepcopy(self.celdasSucias)                     # Número de celdas que han sido limpiadas
        self.schedule = RandomActivation(self)                      # Schedule
        self.running = True                                         # Estado de la simulación
        self.limpiezalimite = False                                 # Booleano que representa si ya se terminó de limpiar toda la basura
        
        # Creación de los agentes aspiradoras
        for i in range(0,self.numAgents):
            # Crear agente y agregarlo al schedule
            a = RobotLimpiador(i, self)
            self.schedule.add(a)
            
            # Colocar al agente en la posición (1,1) de la cuadricula en la parte inferior izquierda
            self.grid.place_agent(a, (1, 1))

        # Creación de celdas sucias por medio de un set
        celdasSucias = set()
        for t in range(self.numAgents+1,self.celdasSucias+self.numAgents+1):
            # Crear agente basura y agregarlo al schedule
            b = CeldasBasura(t,self)
            self.schedule.add(b)
            RobotLimpiador.PasosRobot = 0

            # Establecer coordenadas aleatorias para la basura
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            
            # Evitar poner doble basura en una misma celda
            while (x,y) in celdasSucias:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            celdasSucias.add((x,y))
                        
            # Colocar al agente en su posición
            self.grid.place_agent(b, (x, y))

    def step(self): 
        '''
        Representación de cada paso de la simulación
        '''

        # Determinar si ya se limpiaron todas las celdas
        if(self.celdasLimpias == self.celdasSucias):
            self.limpiezalimite = True

        # Imprimir la información solicitada sobre la corrida del modelo
        if(self.limpiezalimite or self.time == self.pasoscursados):
                self.running = False

                if(self.limpiezalimite):
                    print("\nTodas las celdas están limpias \n")
                else:
                    print("Se ha agotado el tiempo límite")

                print("Tiempo transcurrido: " + str(self.pasoscursados) + 
                " steps, Porcentaje de celdas limpiadas: " + 
                str(int((self.celdasLimpias*100)/self.celdasSucias)) + "%")
                print("Celdas sucias restantes: " + str(self.cont))
                #print("Celdas sucias restantes: " + str(int((self.celdasSucias*100)/self.celdasLimpias)))
                print("Número de movimientos: " + str(RobotLimpiador.PasosRobot))
                

        # Hacer que todos los agentes den un paso (determinado en sus respectivos modelos)
        else:
            self.pasoscursados += 1
            self.schedule.step()










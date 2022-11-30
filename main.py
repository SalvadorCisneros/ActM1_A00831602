#Salvador Alejandro Cisneros Sanchez - A00831602
from limpieza import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

# Visualización gráfica de los agentes
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "false",
                 "r":0.7}

    # Distinción entre el agente Robot y la Basura
    if isinstance(agent, RobotLimpiador):
        portrayal["Color"] = "lightgreen"
        portrayal["Layer"] = 0.2
    else:
        portrayal["Color"] = "brown"
        portrayal["Layer"] = 0.1
        portrayal["r"] = 0.5
    return portrayal

# Datos de simulación
width = 15                  # Ancho
height = 15                  # Alto
numAgents = 10           # Aspiradoras
litterpercentage = 50       # Cantidad de basura
steps = 100     # Tiempo

# Crear instancia del servidor con el modelo
grid = CanvasGrid(agent_portrayal, width, height, 400, 400)
server = ModularServer(RobotModel,
                       [grid],
                       "Robolimp",
                       {"width": width,
                        "height": height,
                        "numAgents": numAgents,
                        "litterpercentage": litterpercentage,
                        "steps": steps})
server.port = 8521  # Puerto default
server.launch()

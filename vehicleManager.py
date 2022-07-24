# File Information ---------------------------------------------
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
# 	File Name: vehicleManager.py
#
# 	File Description: Contains Vehicle and VehicleManager classes
# 
# 	File History:
# 		- 2022-07-24: Adapted from main.py by Rohit S.
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 

# Imports --------------------------------------------------------

# Global Variables -----------------------------------------------
INFINITY = 100000000000000000

# Class Declarations ---------------------------------------------
class Vehicle:
    def __init__(self, startNode, endNode, id):
        self.id             = id
        self.startNode      = startNode
        self.endNode        = endNode
        self.timeLeftOnEdge = INFINITY

    def setStartingEdge(self):
        self.currentEdgeIndex   = 0
        self.travelTimes        = []
        edge = self.pathEdges[0]
        edge.addVehicle()
        self.currentEdge = edge

    def setNextEdge(self):
        self.travelTimes.append(self.timeOnEdge)
        self.timeOnEdge = 0
        self.currentEdgeIndex += 1
        # Check if we are target
        if self.currentEdgeIndex == len(self.pathEdges):
            return None
        else:
            self.currentEdge.removeVehicle()
            self.currentEdge = self.pathEdges[self.currentEdgeIndex]
            self.currentEdge.addVehicle()
            return self.currentEdge

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#	Class Name: VehicleManager
#
#	Class Description: Manages all instances of Vehicle
# 
#	Class History: 
# 		- 2022-07-24: Created by Rohit S.
# 
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
class VehicleManager:
    def __init__(self):
        self.__vehicles = []

    def getVehicles(self):
        return self.__vehicles

    def createVehicle(self, startNode, endNode):
        vehicle = Vehicle(startNode, endNode, id=len(self.__vehicles))
        self.__vehicles.append(vehicle)
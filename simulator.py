# File Information ---------------------------------------------
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
# 	File Name: simulator.py
#
# 	File Description: File containing simulator class
# 
# 	File History:
# 		- 2022-07-24: Adapted from main.py by Rohit S.
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 

# Imports --------------------------------------------------------
from vehicleManager import VehicleManager
from edgeManager import EdgeManager
from nodeManager import NodeManager
from random import randint
from time import sleep

# Global Variables -----------------------------------------------


# Class Declarations ---------------------------------------------

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#	Class Name: SimulationResult
#
#	Class Description:
# 
#	Class History: 
# 		- 2022-07-24: Created by Rohit S.
# 
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
class SimulationResult:
    def __init__(self, vehicle):
        self.id             = vehicle.id
        self.startNode      = vehicle.startNode
        self.endNode        = vehicle.endNode
        self.baselineTime   = vehicle.baselineExpectedTime
        self.actualTime     = sum([e for e in vehicle.travelTimes])
        self.percentDelay   = round(self.actualTime / self.baselineTime, 4)

    def __str__(self):
        return f"Vehicle {self.id} completed trip from {self.startNode} -> {self.endNode} with {self.percentDelay}% delays"

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#	Class Name: Simulator
#
#	Class Description: 
#       - Implements the discrete event simulator
# 
#	Class History: 
# 		- 2022-07-18: Created by Rohit S.
# 
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
class Simulator:
    def __init__(self, nodeManager=NodeManager(), edgeManager=EdgeManager(), vehicleManager=VehicleManager()):
        # Private Attributes, we shouldn't access these directly
        self.__nodeManager        = nodeManager
        self.__edgeManager        = edgeManager
        self.__vehicleManager     = vehicleManager
        # Public Attributes that can be accessed directly
        self.nodes      = self.__nodeManager.getNodes()
        self.edges      = self.__edgeManager.getEdges()
        self.vehicles   = self.__vehicleManager.getVehicles()

    def createNode(self, lat=0, long=0):
        return self.__nodeManager.createNode(lat, long)

    def createEdge(self, sourceNode, sinkNode, length=100, maxSpeed=50, isBidirectional=True):
        if isBidirectional:
            return self.__edgeManager.createBidirectionalEdge(sourceNode, sinkNode, length, maxSpeed)
        else:
            return self.__edgeManager.createEdge(sourceNode, sinkNode, length, maxSpeed)

    def createVehicle(self, sourceNode, targetNode):
        return self.__vehicleManager.createVehicle(sourceNode, targetNode)

    def runBaselineSimulation(self):
        # Create a copy of the waiting vehicles
        waitingVehicles     = self.vehicles[:]
        # Create an empty array to store vehicles currently travelling
        travellingVehicles  = []
        # Create an empty array to store completed vehicles
        completeVehicles    = []
        # Create starting time
        time = 0
        # Simulation completes until all vehicles are complete
        while (len(waitingVehicles) >= 0) and (len(completeVehicles) < len(self.vehicles)):
            # Check if we have vehicles waiting to start travelling
            if len(waitingVehicles) != 0:
                # We only deploy vehicles every ten seconds
                if time % 10 == 0:
                    # Randomly select a vehicle from the list
                    deployedVehicle                     = waitingVehicles[randint(0, len(waitingVehicles) - 1)]
                    # Run baseline path finding
                    baselinePathResults = self.__nodeManager.determinePath(deployedVehicle.startNode, deployedVehicle.endNode, isBaseline=True)
                    # Store results
                    deployedVehicle.baselineExpectedTime    = baselinePathResults[0]
                    deployedVehicle.pathNodes               = baselinePathResults[1]
                    deployedVehicle.pathEdges               = baselinePathResults[2]
                    # Add the vehicle to the first edge in baselinePathEdges
                    deployedVehicle.setStartingEdge()
                    # Initialize the time spent on the edge
                    deployedVehicle.timeOnEdge = 0
                    deployedVehicle.deploymentTime = time
                    # Remove the deployed vehicle from waiting
                    waitingVehicles.remove(deployedVehicle)
                    # Add the deployed vehicle to travelling
                    travellingVehicles.append(deployedVehicle)
                    print(f"Vehicle {deployedVehicle.id} deployed at {deployedVehicle.deploymentTime}")

            # Each travelling vehicle has to move one additional time step
            for travellingVehicle in travellingVehicles:
                travellingVehicle.timeOnEdge += 1
                # Check if we are done on this edge
                if travellingVehicle.timeOnEdge >= travellingVehicle.currentEdge.realTime:
                    # If we are, update the edge
                    nextEdge = travellingVehicle.setNextEdge()
                    # Check if we are done
                    if nextEdge == None:
                        completeVehicles.append(travellingVehicle)
                        travellingVehicles.remove(travellingVehicle)
                        res = SimulationResult(travellingVehicle)
                        print(res)

            # Increment time
            time += 1
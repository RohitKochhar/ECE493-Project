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
from vehicleManager import Vehicle, VehicleManager
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

    def setBaselineData(self, vehicle):
        self.baselineExpectedTime   = vehicle.baselineExpectedTime
        self.baselineActualTime     = sum([e for e in vehicle.travelTimes])
        self.baselinePath           = ' -> '.join([str(e) for e in vehicle.pathEdges])
        self.baselinePercentDelay   = round(self.baselineActualTime / self.baselineExpectedTime, 4)

    def printBaselineData(self):
        print(f"Vehicle {self.id} completed trip from {self.startNode} -> {self.endNode} via {self.baselinePath} in {self.baselineActualTime} with {self.baselinePercentDelay}% delays")

    def setOptimizedData(self, vehicle):
        self.optimizedExpectedTime   = vehicle.optimizedExpectedTime
        self.optimizedActualTime     = sum([e for e in vehicle.travelTimes])
        self.optimizedPath           = ' -> '.join([str(e) for e in vehicle.pathEdges])
        self.optimizedPercentDelay   = round(self.optimizedActualTime / self.optimizedExpectedTime, 4)

    def printOptimizedData(self):
        print(f"Vehicle {self.id} completed trip from {self.startNode} -> {self.endNode} via {self.optimizedPath} in {self.optimizedActualTime} with {self.optimizedPercentDelay}% delays")

    

class SimulationResultManager:
    def __init__(self):
        self.__results = []

    def getResults(self):
        return self.__results

    def addRecord(self, vehicle):
        record = SimulationResult(vehicle)
        self.__results.append(record)

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
        self.__resultsManager     = SimulationResultManager()
        # Public Attributes that can be accessed directly
        self.nodes      = self.__nodeManager.getNodes()
        self.edges      = self.__edgeManager.getEdges()
        self.vehicles   = self.__vehicleManager.getVehicles()
        self.results    = self.__resultsManager.getResults()

    def createNode(self, lat=0, long=0):
        return self.__nodeManager.createNode(lat, long)

    def createEdge(self, sourceNode, sinkNode, length=100, maxSpeed=50, isBidirectional=True):
        if isBidirectional:
            return self.__edgeManager.createBidirectionalEdge(sourceNode, sinkNode, length, maxSpeed)
        else:
            return self.__edgeManager.createEdge(sourceNode, sinkNode, length, maxSpeed)

    def createVehicle(self, sourceNode, targetNode):
        vehicle = self.__vehicleManager.createVehicle(sourceNode, targetNode)
        self.__resultsManager.addRecord(vehicle)
        return vehicle

    def getRecordByID(self, id):
        for rec in self.results:
            if rec.id == id:
                return rec

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
                        record = self.getRecordByID(travellingVehicle.id)
                        record.setBaselineData(travellingVehicle)

            # Increment time
            time += 1

        # Clean up
        for edge in self.edges:
            edge.numCars = 0

    def runOptimizedSimulation(self):
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
                    optimizedPathResults = self.__nodeManager.determinePath(deployedVehicle.startNode, deployedVehicle.endNode, isBaseline=False)
                    # Store results
                    deployedVehicle.optimizedExpectedTime       = optimizedPathResults[0]
                    deployedVehicle.pathNodes                   = optimizedPathResults[1]
                    deployedVehicle.pathEdges                   = optimizedPathResults[2]
                    # Add the vehicle to the first edge in baselinePathEdges
                    deployedVehicle.setStartingEdge()
                    # Initialize the time spent on the edge
                    deployedVehicle.timeOnEdge = 0
                    deployedVehicle.deploymentTime = time
                    # Remove the deployed vehicle from waiting
                    waitingVehicles.remove(deployedVehicle)
                    # Add the deployed vehicle to travelling
                    travellingVehicles.append(deployedVehicle)

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
                        record = self.getRecordByID(travellingVehicle.id)
                        record.setOptimizedData(travellingVehicle)

            # Increment time
            time += 1

        # Clean up
        for edge in self.edges:
            edge.numCars = 0

    def showResults(self):
        for result in self.results:
            result.printBaselineData()
            result.printOptimizedData()
            print("")
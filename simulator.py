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
TIME_FACTOR = 100

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
        self.baselineExpectedTime   = sum([e.minTime for e in vehicle.traversedEdges])
        self.baselineActualTime     = vehicle.finishingTime - vehicle.deploymentTime
        self.baselinePath           = ' -> '.join([str(e) for e in vehicle.pathEdges])
        self.baselinePercentDelay   = round((self.baselineActualTime / self.baselineExpectedTime)*100 - 100, 4)

    def printBaselineData(self):
        print(f"Vehicle {self.id} completed trip from {self.startNode} -> {self.endNode} via {self.baselinePath} in {self.baselineActualTime} instead of the expected {self.baselineExpectedTime} with {self.baselinePercentDelay}% delays")

    def setOptimizedData(self, vehicle):
        self.optimizedExpectedTime   = sum([e.minTime for e in vehicle.traversedEdges])
        self.optimizedActualTime     = vehicle.finishingTime - vehicle.deploymentTime
        self.baselineRealTime        = sum([e.realTime for e in vehicle.baseLinePath])
        self.optimizedPath           = ' -> '.join([str(e) for e in vehicle.pathEdges])
        self.optimizedPercentDelay   = round((self.optimizedActualTime / self.optimizedExpectedTime)*100 - 100, 4)

    def printOptimizedData(self):
        print(f"Vehicle {self.id} completed trip from {self.startNode} -> {self.endNode} via {self.optimizedPath} in {self.optimizedActualTime} instead of the expected {self.baselineRealTime} with {self.optimizedPercentDelay}% delays")

    def exportData(self, metrics, filename='test.csv'):
        metrics['numSimulations'] += 1
        if self.baselinePath != self.optimizedPath:
            self.isOptimized = True
            metrics['numOptimizations'] += 1
            self.isSuccess = (self.baselineRealTime > self.optimizedExpectedTime)
            if self.isSuccess:
                metrics['numSuccesses'] += 1
            self.isFailure = (self.baselineRealTime < self.optimizedExpectedTime - 5)
            if self.isFailure:
                metrics['numFailures'] += 1
        else:
            self.isOptimized = False
            self.isSuccess   = None

        if self.isOptimized and self.isFailure:
            print(self.id, self.isOptimized, self.baselineActualTime, self.baselineExpectedTime, self.baselineRealTime, self.optimizedActualTime, self.optimizedExpectedTime, self.isSuccess)


    

class SimulationResultManager:
    def __init__(self):
        self.__results = []

    def getResults(self):
        return self.__results

    def addRecord(self, vehicle):
        record = SimulationResult(vehicle)
        self.__results.append(record)
        return record

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

    def __del__(self):
        del(self.__nodeManager)
        del(self.__edgeManager)
        del(self.__vehicleManager)
        del(self.__resultsManager)

    def createNode(self, lat=0, long=0):
        return self.__nodeManager.createNode(lat, long)

    def createEdge(self, sourceNode, sinkNode, length=100, maxSpeed=50, isBidirectional=True):
        if isBidirectional:
            return self.__edgeManager.createBidirectionalEdge(sourceNode, sinkNode, length, maxSpeed)
        else:
            return self.__edgeManager.createEdge(sourceNode, sinkNode, length, maxSpeed)

    def createVehicle(self, sourceNode, targetNode):
        vehicle = self.__vehicleManager.createVehicle(sourceNode, targetNode)
        rec = self.__resultsManager.addRecord(vehicle)
        assert rec.id == vehicle.id
        return vehicle

    def getRecordByID(self, id):
        foundRec = None
        for rec in self.results:
            if rec.id == id:
                foundRec = rec
        if foundRec == None:
            raise ValueError(f"Couldn't find a record for vehicle {id}")
        else:
            return foundRec

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
                if time*TIME_FACTOR % 300 == 0:
                    # Randomly select a vehicle from the list
                    deployedVehicle                     = waitingVehicles[len(waitingVehicles) - 1]
                    # Run baseline path finding
                    baselinePathResults = self.__nodeManager.determinePath(deployedVehicle.startNode, deployedVehicle.endNode, isBaseline=True)
                    # Store results
                    deployedVehicle.baselineExpectedTime    = baselinePathResults[0]
                    deployedVehicle.pathNodes               = baselinePathResults[1]
                    deployedVehicle.baseLinePath            = baselinePathResults[2]
                    deployedVehicle.pathEdges               = baselinePathResults[2]
                    if len(deployedVehicle.pathEdges) == 0 or (deployedVehicle.pathEdges[0].isFull):
                        pass
                    else:
                        deployedVehicle.traversedEdges        = []
                        deployedVehicle.traversedNodes        = []
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
                travellingVehicle.timeOnEdge += 1*TIME_FACTOR
                # Check if we are done on this edge
                if travellingVehicle.timeOnEdge >= travellingVehicle.currentEdge.realTime:
                    # Saved the traversed edges and nodes
                    travellingVehicle.traversedEdges.append(travellingVehicle.currentEdge)
                    travellingVehicle.traversedNodes.append(travellingVehicle.currentEdge.sinkNode)
                    if travellingVehicle.currentEdge.sinkNode == travellingVehicle.endNode:
                        travellingVehicle.finishingTime = time + 1
                        completeVehicles.append(travellingVehicle)
                        travellingVehicles.remove(travellingVehicle)
                        record = self.getRecordByID(travellingVehicle.id)
                        record.setBaselineData(travellingVehicle)
                    else:
                        baselinePathResults = self.__nodeManager.determinePath(travellingVehicle.currentEdge.sinkNode, travellingVehicle.endNode, isBaseline=True)
                        travellingVehicle.baselineExpectedTime    = baselinePathResults[0]
                        travellingVehicle.pathNodes               = travellingVehicle.traversedNodes + baselinePathResults[1]
                        travellingVehicle.pathEdges               = travellingVehicle.traversedEdges + baselinePathResults[2]
                        nextEdge = travellingVehicle.setNextEdge()

            # Increment time
            time += 1*TIME_FACTOR

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
            print(len(waitingVehicles), len(travellingVehicles), len(completeVehicles))
            # Check if we have vehicles waiting to start travelling
            if len(waitingVehicles) != 0:
                # We only deploy vehicles every ten seconds
                if time*TIME_FACTOR % 300 == 0:
                    # Randomly select a vehicle from the list
                    deployedVehicle                     = waitingVehicles[len(waitingVehicles) - 1]
                    # Run optimal path finding
                    optimizedPathResults = self.__nodeManager.determinePath(deployedVehicle.startNode, deployedVehicle.endNode, isBaseline=False)
                    # Store results
                    deployedVehicle.optimizedExpectedTime       = optimizedPathResults[0]
                    deployedVehicle.pathNodes                   = optimizedPathResults[1]
                    deployedVehicle.pathEdges                   = optimizedPathResults[2]
                    if len(deployedVehicle.pathEdges) == 0 or (deployedVehicle.pathEdges[0].isFull):
                        pass
                    else:
                        deployedVehicle.traversedEdges        = []
                        deployedVehicle.traversedNodes        = []
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
                travellingVehicle.timeOnEdge += 1*TIME_FACTOR
                # Check if we are done on this edge
                if travellingVehicle.timeOnEdge >= travellingVehicle.currentEdge.realTime:
                    # Saved the traversed edges and nodes
                    travellingVehicle.traversedEdges.append(travellingVehicle.currentEdge)
                    travellingVehicle.traversedNodes.append(travellingVehicle.currentEdge.sinkNode)
                    if travellingVehicle.currentEdge.sinkNode == travellingVehicle.endNode:
                        travellingVehicle.finishingTime = time + 1
                        completeVehicles.append(travellingVehicle)
                        travellingVehicles.remove(travellingVehicle)
                        record = self.getRecordByID(travellingVehicle.id)
                        record.setOptimizedData(travellingVehicle)
                    else:
                        optimizedPathResults = self.__nodeManager.determinePath(travellingVehicle.currentEdge.sinkNode, travellingVehicle.endNode, isBaseline=False)
                        travellingVehicle.optimizedExpectedTime     = optimizedPathResults[0]
                        travellingVehicle.pathNodes                 = travellingVehicle.traversedNodes + optimizedPathResults[1]
                        travellingVehicle.pathEdges                 = travellingVehicle.traversedEdges + optimizedPathResults[2]
                        nextEdge = travellingVehicle.setNextEdge()

            # Increment time
            time += 1*TIME_FACTOR

        # Clean up
        for edge in self.edges:
            edge.numCars = 0

    def showResults(self):
        for result in self.results:
            result.printBaselineData()
            result.printOptimizedData()
            print("")

    def exportResults(self):
        self.metrics = {
            "numSimulations": 0,
            "numOptimizations": 0,
            "numSuccesses": 0,
            "numFailures": 0,
        }
        for result in self.results:
            result.exportData(self.metrics)

        print(self.metrics)
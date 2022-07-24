# File Information ---------------------------------------------
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
# 	File Name: edgeManager.py
#
# 	File Description: 
# 
# 	File History:
# 		- 2022-07-24: Adapted from main.py by Rohit S.
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 

# Imports --------------------------------------------------------

# Global Variables -----------------------------------------------
CAR_LENGTH = 5

# Class Declarations ---------------------------------------------
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#	Class Name:         Edge
#
#	Class Description: 
#       -   Models traffic flow between intersections
# 
#	Class History: 
# 		- 2022-07-14: Created by Rohit S.
# 
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
class Edge:
    def __init__(self, sourceNode, sinkNode, length=100, maxSpeed=50):
        self.sourceNode = sourceNode
        self.sinkNode   = sinkNode
        self.length     = length*10
        self.maxSpeed   = maxSpeed
        self.minTime    = (self.length / maxSpeed) * 3600
        self.numCars    = 0
        self.d          = self.length
        self.realSpeed  = self.setRealSpeed()
        self.congestion = 1
        self.isFull     = False

        self.sourceNode.setEdge(self)
        self.sinkNode.setEdge(self)

    def setD(self):
        self.d = float((self.length - CAR_LENGTH*self.numCars) / self.numCars)
        if self.d < 1:
            raise ValueError("Edge is full, cannot add vehicle")

    def setRealSpeed(self):
        if self.d > 10:
            self.realSpeed = self.maxSpeed
        elif self.d > 1:
            self.realSpeed = self.maxSpeed*(1 - (1/self.d))

        self.realTime = (self.length / self.realSpeed) * 3600

    def setCongestion(self):
        self.congestion = self.realTime / self.minTime

    def addVehicle(self):
        # First we need to check if we can add an edge
        if self.isFull:
            raise ValueError(f"Edge is full, cannot add vehicle")
        # If it isn't, try to add a car
        else:
            self.numCars += 1
            try:
                # If we can't add a car, setD will return a ValueError
                self.setD()
                self.setRealSpeed()
                self.setCongestion()
                self.isFull = False
            except ValueError as e:
                self.numCars -= 1
                self.isFull = True

    def removeVehicle(self):
        if self.numCars > 1:
            self.numCars -= 1
            self.setD()
            self.setRealSpeed()
            self.setCongestion()
            self.isFull = False

    def __str__(self):
        return f"edge{self.sourceNode.id}->{self.sinkNode.id}"

    def getEdgeInfo(self):
        return f"Edge information: \n\tCars: {self.numCars}, d: {self.d} \n\tIdeal speed: {self.maxSpeed}, Real speed: {self.realSpeed}\n\tMin time: {self.minTime}, Real time: {self.realTime}\n\tCongestion: {self.congestion}"


# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#	Class Name:     EdgeManager
#
#	Class Description: 
#       -   Manages edge instances
# 
#	Class History: 
# 		- 2022-07-14: Created by Rohit S.
# 
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
class EdgeManager:
    def __init__(self):
        self.__edges = []

    def getEdges(self):
        return self.__edges
    
    def createEdge(self, sourceNode, sinkNode, length=100, maxSpeed=50):
        # Check that the edge doesn't exist already
        for existingEdge in self.__edges:
            if (existingEdge.sourceNode == sourceNode) and (existingEdge.sinkNode == sinkNode):
                raise ValueError(f"Error, trying to create an edge between two connected nodes")

        edge = Edge(sourceNode, sinkNode, length, maxSpeed)
        self.__edges.append(edge)
        return edge

    def createBidirectionalEdge(self, nodeA, nodeB, length=1, maxSpeed=50):
        self.createEdge(nodeA, nodeB, length, maxSpeed)
        self.createEdge(nodeB, nodeA, length, maxSpeed)
# File Information ---------------------------------------------
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
# 	File Name: main.py
#
# 	File Description: 
# 
# 	File History:
# 		- 2022-07-14: Created by Rohit S.
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 

# Imports --------------------------------------------------------

# Global Variables -----------------------------------------------
CAR_LENGTH = 5

# Class Declarations ---------------------------------------------

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#	Class Name:         Node
#
#	Class Description: 
#       -   Models traffic intersections
# 
#	Class History: 
# 		- 2022-07-14: Created by Rohit S.
# 
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
class Node:
    def __init__(self, id, lat, long):
        self.id     = id
        self.edges  = []
        self.lat    = lat
        self.long   = long

    def setEdge(self, edge):
        self.edges.append(edge)

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#	Class Name:     NodeManager
#
#	Class Description: 
#       -   Manages nodes
# 
#	Class History: 
# 		- 2022-07-14: Created by Rohit S.
# 
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
class NodeManager:
    def __init__(self):
        self.nodes = []

    def createNode(self, lat, long):
        node = Node(len(self.nodes), lat, long)
        self.nodes.append(node)
        return node

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
    def __init__(self, sourceNode, sinkNode, length=1, maxSpeed=50):
        self.sourceNode = sourceNode
        self.sinkNode   = sinkNode
        self.length     = length
        self.maxSpeed = maxSpeed
        self.minTime    = (length / maxSpeed) * 3600
        self.numCars    = 0
        self.d          = self.length
        self.realSpeed  = 0
        self.congestion = 1

        self.sourceNode.setEdge(self)
        self.sinkNode.setEdge(self)

    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 
    #
    #	Method Name:    setD
    #
    #	Method Description:
    #		-   Set D of edge from equation 2 in paper
    #
    #	Method History:
    #		- 2022-07-15: Created by Rohit S.
    #
    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 
    def setD(self):
        self.d = float((self.length - CAR_LENGTH*self.numCars) / self.numCars)

    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 
    #
    #	Method Name:    setRealSpeed
    #
    #	Method Description:
    #		-   Calculates v real and t real based on equation 3 in paper
    #
    #	Method History:
    #		- 2022-07-15: Created by Rohit S.
    #
    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 
    def setRealSpeed(self):
        if self.d > 10:
            self.realSpeed = self.maxSpeed
        elif self.d > 1:
            self.realSpeed = self.maxSpeed*(1 - (1/self.d))
        
        self.realTime = (self.length / self.realSpeed) * 3600

    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 
    #
    #	Method Name:    setCongestion
    #
    #	Method Description:
    #		-   Calculates congestion based on equation 5 in paper
    #
    #	Method History:
    #		- 2022-07-15: Created by Rohit S.
    #
    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 
    def setCongestion(self):
        self.congestion = self.realTime / self.minTime

    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 
    #
    #	Method Name:    addVehicle
    #
    #	Method Description:
    #		-   Add a vehicle to the edge and update d, realSpeed and congestion
    #
    #	Method History:
    #		- 2022-07-15: Created by Rohit S.
    #
    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 

    def addVehicle(self):
        self.numCars += 1
        self.setD()
        self.setRealSpeed()
        self.setCongestion()

    def __str__(self):
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
        self.edges = []
    
    def createEdge(self, sourceNode, sinkNode, length=1, maxSpeed=50):
        edge = Edge(sourceNode, sinkNode, length, maxSpeed)
        self.edges.append(edge)
        return edge

# Function Declarations ------------------------------------------

# Main Call ------------------------------------------------------
if __name__ == '__main__':
    print('Running main')
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
INFINITY = 10000000000000

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
    def __init__(self, id, manager, lat, long):
        self.manager    = manager
        self.id         = id
        self.edges      = []
        self.lat        = lat
        self.long       = long

    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 
    #
    #	Method Name:    setEdge
    #
    #	Method Description:
    #		-   Add an edge to the node
    #
    #	Method History:
    #		- 2022-07-16: Created by Rohit S.
    #
    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 
    def setEdge(self, edge):
        self.edges.append(edge)

    def __str__(self):
        return f"Node {self.id}"

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
        node = Node(len(self.nodes), self, lat, long)
        self.nodes.append(node)
        return node

    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 
    #
    #	Method Name:    determinePath
    #
    #	Method Description:
    #		-   Run Djikstras from self node to a target node
    #
    #	Method History:
    #		- 2022-07-16: Created by Rohit S.
    #
    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 
    def determinePath(self, currentNode, targetNode):
        # Mark all nodes unvisited
        for node in self.nodes:
            node.isVisited = False
            # Mark all nodes with a tentative distance of infinity
            if node != currentNode:
                node.tentativeDistance = INFINITY
            else:
                node.tentativeDistance = 0
        # Consider all unvisited nodes
        while all([x.isVisited for x in self.nodes]) != True:
            # Get remaining unvisted nodes:
            unvisitedNodes = []
            for node in self.nodes:
                if node.isVisited == False:
                    unvisitedNodes.append(node)
            # Get the next smallest 
            current = min(unvisitedNodes, key=lambda x: x.tentativeDistance)
            if current == targetNode:
                break
            else:
                # Consider the neighbours of current
                for edge in current.edges:
                    if current == edge.sourceNode:
                        neighbour = edge.sinkNode
                        # Check that the neighbour hasn't been visited
                        if neighbour in self.nodes:
                            # Check if a shorter path exists
                            if edge.realTime + current.tentativeDistance <= neighbour.tentativeDistance:
                                neighbour.tentativeDistance = edge.realTime + current.tentativeDistance
                                current.isVisited = True

        print(f"Min path from Node {currentNode.id} -> {targetNode.id} = {targetNode.tentativeDistance}")
        return targetNode.tentativeDistance

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
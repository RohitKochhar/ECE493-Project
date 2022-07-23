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
from random import randint
from time import sleep


CAR_LENGTH = 5
INFINITY = 100000000000000000

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
        self.prev       = None

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

    def getEdgeBySink(self, sink):
        for edge in self.edges:
            if edge.sinkNode == sink:
                return edge

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
        if currentNode == targetNode:
            return 0, []
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
                                neighbour.prev = current
                
                current.isVisited = True

        if targetNode.tentativeDistance == INFINITY:
            path = []
        else:
            lastNode = targetNode
            path = []
            path.append(targetNode)
            while lastNode.prev != currentNode:
                path.append(lastNode.prev)
                lastNode = lastNode.prev
            path.append(currentNode)

        print(f"Min path from Node {currentNode.id} -> {targetNode.id} = {targetNode.tentativeDistance/3600} hours")
        reversedPath = list(reversed(path))
        print(f"{' -> '.join([str(x) for x in reversedPath]) }")
        edges = []
        for i in range(0, len(reversedPath) - 1):
            edge = reversedPath[i].getEdgeBySink(reversedPath[i + 1])
            edges.append(edge)
            print(edge)
        return targetNode.tentativeDistance, reversedPath, edges

    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 
    #
    #	Method Name:    determineBaselinePath
    #
    #	Method Description:
    #		-   Run Djikstras from self node to a target node
    #
    #	Method History:
    #		- 2022-07-16: Created by Rohit S.
    #
    # .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . 
    def determineBaselinePath(self, currentNode, targetNode):
        if currentNode == targetNode:
            return 0, []
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
                                neighbour.tentativeDistance = edge.minTime + current.tentativeDistance
                                neighbour.prev = current
                
                current.isVisited = True

        if targetNode.tentativeDistance == INFINITY:
            path    = []
        else:
            lastNode = targetNode
            path = []
            path.append(targetNode)
            while lastNode.prev != currentNode:
                path.append(lastNode.prev)
                lastNode = lastNode.prev
            path.append(currentNode)


        print(f"Min path from Node {currentNode.id} -> {targetNode.id} = {targetNode.tentativeDistance/3600} hours")
        reversedPath = list(reversed(path))
        print(f"{' -> '.join([str(x) for x in reversedPath]) }")
        edges = []
        for i in range(0, len(reversedPath) - 1):
            edge = reversedPath[i].getEdgeBySink(reversedPath[i + 1])
            edges.append(edge)
            print(edge)
        return targetNode.tentativeDistance, reversedPath, edges


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
        self.length     = length
        self.maxSpeed = maxSpeed
        self.minTime    = (length / maxSpeed) * 3600
        self.numCars    = 0
        self.d          = self.length
        self.realSpeed  = self.setRealSpeed()
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
        return f"edge{self.sourceNode.id}{self.sinkNode.id}"

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
        self.edges = []
    
    def createEdge(self, sourceNode, sinkNode, length=100, maxSpeed=50):
        edge = Edge(sourceNode, sinkNode, length, maxSpeed)
        self.edges.append(edge)
        return edge

    def createBidirectionalEdge(self, nodeA, nodeB, length=1, maxSpeed=50):
        self.createEdge(nodeA, nodeB, length, maxSpeed)
        self.createEdge(nodeB, nodeA, length, maxSpeed)

    def getEdgeFromNodes(self, sourceNode, sinkNode):
        for edge in self.edges:
            if (edge.sourceNode == sourceNode) and (edge.sinkNode == sinkNode):
                return edge

class Vehicle:
    def __init__(self, startNode, endNode, nodeManager):
        self.startNode      = startNode
        self.endNode        = endNode
        self.baselinePath   = nodeManager.determineBaselinePath(self.startNode, self.endNode)
        timeLeftOnEdge      = INFINITY

    def updateEdge(self):
        for i in range(0, len(self.edges)):
            if self.edges[i] == self.currentEdge:
                try:
                    self.nextEdge = self.edges[i + 1]
                    self.currentEdge = self.nextEdge
                    self.timeLeftOnEdge = self.currentEdge.minTime
                except IndexError as e:
                    self.nextEdge = None    
                    self.currentEdge = self.nextEdge


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
    def __init__(self, nodeManager, edgeManager):
        self.nodeManager    = nodeManager
        self.edgeManager    = edgeManager
        self.vehicles       = []

    def addRandomVehicle(self):
        numNodes = len(self.nodeManager.nodes)
        startNode   = self.nodeManager.nodes[randint(0, numNodes - 1)]
        endNode     = self.nodeManager.nodes[randint(0, numNodes - 1)]
        while endNode == startNode:
            endNode     = self.nodeManager.nodes[randint(0, numNodes - 1)]
        vehicle     = Vehicle(startNode, endNode, self.nodeManager)
        self.vehicles.append(vehicle)

    def startSimulation(self):
        print(f"-------------------------------")
        print(f"Starting Simulation...")
        print(f"\tNumber of Vehicles: {len(self.vehicles)}")
        for i in range(0, len(self.vehicles)):
            print(f"\t\tVehicle {i} travelling from {self.vehicles[i].startNode} to {self.vehicles[i].endNode}")
            minTime, minPath, minEdges = self.vehicles[i].baselinePath
            print(f"\t\t\tBaseline Path: {' -> '.join(str(node) for node in minPath)}")
            print(f"\t\t\tStarting on edge: {minEdges[0]}")
            self.vehicles[i].currentEdge = minEdges[0]
            self.vehicles[i].edges       = minEdges
            print(f"\t\t\tTime remaining on edge: {minEdges[0].minTime} seconds")
            self.vehicles[i].timeLeftOnEdge = minEdges[0].minTime
        step = 0
        while len(self.vehicles) != 0:
            print(f"- - - - - Simulation Step {step} - - - - -")
            self.updateSimulation()
            step += 1

    def updateSimulation(self):
        for vehicle in self.vehicles:
            print(f"Vehicle on edge: {vehicle.currentEdge}")
            vehicle.timeLeftOnEdge -= 1
            if vehicle.timeLeftOnEdge <= 0:
                print(f"\tCompleted Trip on edge")
                vehicle.updateEdge()
                if vehicle.currentEdge == None:
                    self.vehicles.remove(vehicle)
                    del(vehicle)
                    print(len(self.vehicles))
            else:
                print(f"\tTime left on edge: {vehicle.timeLeftOnEdge}")

        
# Function Declarations ------------------------------------------

# Main Call ------------------------------------------------------
if __name__ == '__main__':
    print('Running main')
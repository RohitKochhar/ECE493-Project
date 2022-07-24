# File Information ---------------------------------------------
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
# 	File Name: nodeManager.py
#
# 	File Description: Contains nodeManager and node class
# 
# 	File History:
# 		- 2022-07-24: Adapted from main.py by Rohit S.
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 

# Imports --------------------------------------------------------

# Global Variables -----------------------------------------------
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
        self.__nodes = []

    def getNodes(self):
        return self.__nodes

    def createNode(self, lat, long):
        node = Node(len(self.__nodes), self, lat, long)
        self.__nodes.append(node)
        return node

    def determinePath(self, currentNode, targetNode, isBaseline=False):
        if currentNode == targetNode:
            return 0, []
        # Mark all nodes unvisited
        for node in self.__nodes:
            node.isVisited = False
            # Mark all nodes with a tentative distance of infinity
            if node != currentNode:
                node.tentativeDistance = INFINITY
            else:
                node.tentativeDistance = 0
        # Consider all unvisited nodes
        while all([x.isVisited for x in self.__nodes]) != True:
            # Get remaining unvisted nodes:
            unvisitedNodes = []
            for node in self.__nodes:
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
                        if neighbour in self.__nodes:
                            # Check if a shorter path exists
                            if edge.isFull:
                                edge.minTime = INFINITY
                                edge.realTime = INFINITY
                            if isBaseline:
                                if (edge.minTime + current.tentativeDistance <= neighbour.tentativeDistance):
                                    # In baseline simulations, decisions are made based on minTime
                                    neighbour.tentativeDistance = edge.minTime + current.tentativeDistance
                                    neighbour.prev = current
                            else:
                                if (edge.realTime + current.tentativeDistance <= neighbour.tentativeDistance):
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

        # print(f"Min path from Node {currentNode.id} -> {targetNode.id} = {targetNode.tentativeDistance/3600} hours")
        reversedPath = list(reversed(path))
        # print(f"{' -> '.join([str(x) for x in reversedPath]) }")
        edges = []
        for i in range(0, len(reversedPath) - 1):
            edge = reversedPath[i].getEdgeBySink(reversedPath[i + 1])
            edges.append(edge)
            # print(edge)
        return targetNode.tentativeDistance, reversedPath, edges
# File Information ---------------------------------------------
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
# 	File Name: test_main.py
#
# 	File Description: 
#       -   Tests for main.py
# 
# 	File History:
# 		- 2022-07-14: Created by Rohit S.
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 

# Imports --------------------------------------------------------
from main import EdgeManager, Node, Edge, NodeManager

# Global Variables -----------------------------------------------

# Class Declarations ---------------------------------------------

# Function Declarations ------------------------------------------
def test_simple_connect():
    # Create node and edge manager
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create Nodes
    sourceNode = nodeManager.createNode(0, 0)
    sinkNode = nodeManager.createNode(0, 0)
    # Create edge connecting node
    edge = edgeManager.createEdge(sourceNode, sinkNode)
    assert edge.sourceNode == sourceNode
    assert edge.sinkNode == sinkNode
    assert edge in sourceNode.edges
    assert edge in sinkNode.edges

def test_multi_connect():
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create central node
    centralNode = nodeManager.createNode(0, 0)
    # Create 10 connecting nodes
    subnodes = []
    for i in range(0, 9):
        subNode = nodeManager.createNode(0, 0)
        subnodes.append(subNode)
        edgeManager.createEdge(centralNode, subNode)

    for i in range(0, len(subnodes)):
        assert centralNode == subnodes[i].edges[0].sourceNode
        assert subnodes[i].edges[0] in centralNode.edges
    
    assert len(centralNode.edges) == len(subnodes)

def test_speed_and_length():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create two nodes
    sourceNode  = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add an edge between them
    edge        = edgeManager.createEdge(sourceNode, sinkNode, 50, 100)
    # Test correct minTime is found
    assert edge.minTime == 1800

def test_delay():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create two nodes
    sourceNode  = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add an edge
    edge        = edgeManager.createEdge(sourceNode, sinkNode, 5000, 100)
    # Add vehicles to edge
    while edge.d > 1:
        edge.addVehicle()
        print(edge)
    

def test_congestion():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create two nodes
    sourceNode  = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add an edge
    edge        = edgeManager.createEdge(sourceNode, sinkNode, 50, 100)
    # Save data
    congestion = edge.congestion
    # add cars
    for i in range(0, 100):
        edge.addVehicle()
    # assert congestion != edge.congestion
    
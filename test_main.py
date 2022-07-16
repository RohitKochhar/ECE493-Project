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
INFINITY = 10000000000000

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
        #print(edge)
    
def test_simple_djikstras():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create two nodes
    sourceNode  = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add an edge
    edge        = edgeManager.createEdge(sourceNode, sinkNode, 5000, 100)
    # Add a vehicle
    edge.addVehicle()
    # Get min path
    minPath = nodeManager.determinePath(sourceNode, sinkNode)
    assert minPath == edge.realTime

def test_double_djikstras():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create three nodes
    sourceNode  = nodeManager.createNode(0, 0)
    interNode   = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add edges
    edge1       = edgeManager.createEdge(sourceNode, interNode, 5000, 100)
    edge2       = edgeManager.createEdge(interNode, sinkNode, 1000, 100)
    # Add vehicles
    edge1.addVehicle()
    edge2.addVehicle()    
    # Get min path
    minPath = nodeManager.determinePath(sourceNode, sinkNode)
    assert minPath == edge1.realTime + edge2.realTime
    
def test_djikstras_with_trick_double_path():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create three nodes
    sourceNode  = nodeManager.createNode(0, 0)
    interNode   = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add edges
    edge1       = edgeManager.createEdge(sourceNode, interNode, 5000, 100)
    edge2       = edgeManager.createEdge(interNode, sinkNode, 1000, 100)
    edge3       = edgeManager.createEdge(sourceNode, sinkNode, 1000000, 100)
    # Add vehicles
    edge1.addVehicle()
    edge2.addVehicle()    
    edge3.addVehicle()
    # Get min path
    minPath = nodeManager.determinePath(sourceNode, sinkNode)
    assert minPath == edge1.realTime + edge2.realTime

def test_djikstras_with_trick_single_path():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create three nodes
    sourceNode  = nodeManager.createNode(0, 0)
    interNode   = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add edges
    edge1       = edgeManager.createEdge(sourceNode, interNode, 5000, 100)
    edge2       = edgeManager.createEdge(interNode, sinkNode, 1000, 100)
    edge3       = edgeManager.createEdge(sourceNode, sinkNode, 10, 100)
    # Add vehicles
    edge1.addVehicle()
    edge2.addVehicle()    
    edge3.addVehicle()
    # Get min path
    minPath = nodeManager.determinePath(sourceNode, sinkNode)
    assert minPath == edge3.realTime

def test_djikstras_no_path():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create two nodes
    sourceNode  = nodeManager.createNode(0, 0)
    interNode   = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add an edge
    edge        = edgeManager.createEdge(sourceNode, interNode, 5000, 100)
    # Add a vehicle
    edge.addVehicle()
    # Get min path
    minPath = nodeManager.determinePath(sourceNode, sinkNode)
    assert minPath == INFINITY

def test_complex_djikstras():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create nodes
    node0 = nodeManager.createNode(0, 0)
    node1 = nodeManager.createNode(0, 0)
    node2 = nodeManager.createNode(0, 0)
    node3 = nodeManager.createNode(0, 0)
    node4 = nodeManager.createNode(0, 0)
    node5 = nodeManager.createNode(0, 0)
    node6 = nodeManager.createNode(0, 0)
    node7 = nodeManager.createNode(0, 0)
    node8 = nodeManager.createNode(0, 0)
    # Connect edges
    edge01 = edgeManager.createEdge(node0, node1, 400, 1)
    edge01.addVehicle()
    edge06 = edgeManager.createEdge(node0, node6, 700, 1)
    edge06.addVehicle()
    edge16 = edgeManager.createEdge(node1, node6, 400, 1)
    edge16.addVehicle()
    edge67 = edgeManager.createEdge(node6, node7, 100, 1) 
    edge67.addVehicle()
    edge17 = edgeManager.createEdge(node1, node7, 2000, 1)
    edge17.addVehicle()
    edge74 = edgeManager.createEdge(node7, node4, 100, 1)
    edge74.addVehicle()
    edge12 = edgeManager.createEdge(node1, node2, 900, 1)
    edge12.addVehicle()
    edge42 = edgeManager.createEdge(node4, node2, 200, 1)
    edge42.addVehicle()
    edge23 = edgeManager.createEdge(node2, node3, 600, 1)
    edge23.addVehicle()
    edge43 = edgeManager.createEdge(node4, node3, 1000, 1)
    edge43.addVehicle()




    assert nodeManager.determinePath(node0, node1) == 400 * 3600
    assert nodeManager.determinePath(node0, node6) == 700 * 3600
    assert nodeManager.determinePath(node0, node7) == 800 * 3600
    assert nodeManager.determinePath(node0, node4) == 900 * 3600
    assert nodeManager.determinePath(node0, node2) == 1100 * 3600
    assert nodeManager.determinePath(node0, node3) == 1700 * 3600
    
# ToDo: Test with bi-directional paths
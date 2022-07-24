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
import pytest
from nodeManager import NodeManager
from simulator import Simulator
from edgeManager import EdgeManager
from vehicleManager import VehicleManager

# Global Variables -----------------------------------------------
INFINITY = 100000000000000000

# Class Declarations ---------------------------------------------

# Function Declarations -----------------------------------------
@pytest.mark.setup
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

@pytest.mark.setup
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

@pytest.mark.setup
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
    
@pytest.mark.setup
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

@pytest.mark.setup
def test_invalid_edge():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create two nodes
    sourceNode  = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add an edge
    edge        = edgeManager.createEdge(sourceNode, sinkNode, 5000, 100)
    with pytest.raises(ValueError) as e_info:
        edge2        = edgeManager.createEdge(sourceNode, sinkNode, 5000, 100)

@pytest.mark.setup
def test_full_edge():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create two nodes
    sourceNode  = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add an edge
    edge        = edgeManager.createEdge(sourceNode, sinkNode, 100, 100)
    for i in range(0, 1000):
        try:
            edge.addVehicle()
        except ValueError as e:
            break
           
    assert edge.isFull
    assert edge.numCars < 1000

@pytest.mark.setup
def test_unfull_edge():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create two nodes
    sourceNode  = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add an edge
    edge        = edgeManager.createEdge(sourceNode, sinkNode, 100, 100)
    for i in range(0, 1000):
        try:
            edge.addVehicle()
        except ValueError as e:
            break
    
    assert edge.isFull
    assert edge.numCars < 1000

    while edge.isFull:
        edge.removeVehicle()

    assert edge.isFull == False

@pytest.mark.setup
def test_simple_djikstras():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create two nodes
    sourceNode  = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add an edge
    edge        = edgeManager.createEdge(sourceNode, sinkNode, 5000, 100)
    # Get min path
    minPath, path, edges = nodeManager.determinePath(sourceNode, sinkNode)
    assert minPath == edge.realTime
    
@pytest.mark.setup
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
    # Get min path
    minPath, path, edges = nodeManager.determinePath(sourceNode, sinkNode)
    assert minPath == edge1.realTime + edge2.realTime
        
@pytest.mark.setup
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
    # Get min path
    minPath, path, edges = nodeManager.determinePath(sourceNode, sinkNode)
    assert minPath == edge1.realTime + edge2.realTime
    
@pytest.mark.setup
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
    # Get min path
    minPath, path, edges = nodeManager.determinePath(sourceNode, sinkNode)
    assert minPath == edge3.realTime
    
@pytest.mark.setup
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
    minPath, path, edges = nodeManager.determinePath(sourceNode, sinkNode)
    assert minPath == INFINITY
    
@pytest.mark.setup
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
    edge06 = edgeManager.createEdge(node0, node6, 700, 1)
    edge16 = edgeManager.createEdge(node1, node6, 400, 1)
    edge67 = edgeManager.createEdge(node6, node7, 100, 1) 
    edge17 = edgeManager.createEdge(node1, node7, 2000, 1)
    edge74 = edgeManager.createEdge(node7, node4, 100, 1)
    edge12 = edgeManager.createEdge(node1, node2, 900, 1)
    edge42 = edgeManager.createEdge(node4, node2, 200, 1)
    edge23 = edgeManager.createEdge(node2, node3, 600, 1)
    edge43 = edgeManager.createEdge(node4, node3, 1000, 1)

    assert nodeManager.determinePath(node0, node1)[0] == 400 * 3600
    assert nodeManager.determinePath(node0, node6)[0] == 700 * 3600
    assert nodeManager.determinePath(node0, node7)[0] == 800 * 3600
    assert nodeManager.determinePath(node0, node4)[0] == 900 * 3600
    assert nodeManager.determinePath(node0, node2)[0] == 1100 * 3600
    assert nodeManager.determinePath(node0, node3)[0] == 1700 * 3600
        
@pytest.mark.setup
def test_simple_bidirectional_network():
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
    edge3       = edgeManager.createEdge(interNode, sourceNode, 100, 10)
    # Get min path
    minPath, path, edges = nodeManager.determinePath(sourceNode, sinkNode)
    assert minPath == edge1.realTime + edge2.realTime
    
@pytest.mark.oldsim
def test_simple_simulation():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create nodes
    sourceNode  = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add edges
    edge        = edgeManager.createBidirectionalEdge(sourceNode, sinkNode, 5000, 100)
    # Create simulator
    sim = Simulator(nodeManager, edgeManager)
    sim.addRandomVehicle()
    sim.startBaselineSimulation()
    
@pytest.mark.oldsim
def test_two_step_simulation():
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create nodes
    sourceNode  = nodeManager.createNode(0, 0)
    interNode   = nodeManager.createNode(0, 0)
    sinkNode    = nodeManager.createNode(0, 0)
    # Add edges
    edge01          = edgeManager.createBidirectionalEdge(sourceNode, interNode, 40, 110)
    edge12          = edgeManager.createBidirectionalEdge(interNode, sinkNode, 40, 110)
    # Create simulator
    sim = Simulator(nodeManager, edgeManager)
    for i in range(0, 1000):
        sim.addVehicle(sourceNode, sinkNode)
    sim.startBaselineSimulation()

@pytest.mark.oldsim
def test_network_1():
    greenLength     = 40
    greenSpeed      = 110
    yellowLength    = 20
    yellowSpeed     = 80
    redLength       = 10
    redSpeed        = 30
    # Create managers
    nodeManager = NodeManager()
    edgeManager = EdgeManager()
    # Create nodes
    nodeA       = nodeManager.createNode(0, 0)
    nodeB       = nodeManager.createNode(0, 0)
    nodeC       = nodeManager.createNode(0, 0)
    nodeD       = nodeManager.createNode(0, 0)
    nodeE       = nodeManager.createNode(0, 0)
    nodeF       = nodeManager.createNode(0, 0)
    nodeG       = nodeManager.createNode(0, 0)
    nodeH       = nodeManager.createNode(0, 0)
    nodeI       = nodeManager.createNode(0, 0)
    nodeJ       = nodeManager.createNode(0, 0)
    nodeK       = nodeManager.createNode(0, 0)
    nodeL       = nodeManager.createNode(0, 0)
    nodeM       = nodeManager.createNode(0, 0)
    nodeN       = nodeManager.createNode(0, 0)
    nodeO       = nodeManager.createNode(0, 0)
    nodeP       = nodeManager.createNode(0, 0)
    # Create edges
    #   Highway edges
    edgeAB      = edgeManager.createBidirectionalEdge(nodeA, nodeB, greenLength, greenSpeed)
    edgeAO      = edgeManager.createBidirectionalEdge(nodeA, nodeO, greenLength, greenSpeed)
    edgeBP      = edgeManager.createBidirectionalEdge(nodeB, nodeP, greenLength, greenSpeed)
    edgeOP      = edgeManager.createBidirectionalEdge(nodeO, nodeO, greenLength, greenSpeed)
    #   Rural edges
    edgeAD      = edgeManager.createBidirectionalEdge(nodeA, nodeD, yellowLength, yellowSpeed)
    edgeAH      = edgeManager.createBidirectionalEdge(nodeA, nodeH, yellowLength, yellowSpeed)
    edgeBD      = edgeManager.createBidirectionalEdge(nodeB, nodeD, yellowLength, yellowSpeed)
    edgeBK      = edgeManager.createBidirectionalEdge(nodeB, nodeK, yellowLength, yellowSpeed)
    edgeOH      = edgeManager.createBidirectionalEdge(nodeO, nodeH, yellowLength, yellowSpeed)
    edgeOM      = edgeManager.createBidirectionalEdge(nodeO, nodeM, yellowLength, yellowSpeed)
    edgePM      = edgeManager.createBidirectionalEdge(nodeP, nodeM, yellowLength, yellowSpeed)
    edgePK      = edgeManager.createBidirectionalEdge(nodeP, nodeK, yellowLength, yellowSpeed)
    #   City edges
    edgeAC      = edgeManager.createBidirectionalEdge(nodeA, nodeC, redLength, redSpeed)
    edgeEB      = edgeManager.createBidirectionalEdge(nodeE, nodeB, redLength, redSpeed)
    edgeNP      = edgeManager.createBidirectionalEdge(nodeN, nodeP, redLength, redSpeed)
    edgeOL      = edgeManager.createBidirectionalEdge(nodeO, nodeL, redLength, redSpeed)

    edgeCD      = edgeManager.createBidirectionalEdge(nodeC, nodeD, redLength, redSpeed)
    edgeDE      = edgeManager.createBidirectionalEdge(nodeD, nodeE, redLength, redSpeed)
    edgeEK      = edgeManager.createBidirectionalEdge(nodeE, nodeK, redLength, redSpeed)
    edgeKN      = edgeManager.createBidirectionalEdge(nodeK, nodeN, redLength, redSpeed)
    edgeNM      = edgeManager.createBidirectionalEdge(nodeN, nodeM, redLength, redSpeed)
    edgeML      = edgeManager.createBidirectionalEdge(nodeM, nodeL, redLength, redSpeed)
    edgeLH      = edgeManager.createBidirectionalEdge(nodeL, nodeH, redLength, redSpeed)
    edgeCH      = edgeManager.createBidirectionalEdge(nodeC, nodeH, redLength, redSpeed)
    
    edgeCF      = edgeManager.createBidirectionalEdge(nodeC, nodeF, redLength, redSpeed)
    edgeFD      = edgeManager.createBidirectionalEdge(nodeF, nodeD, redLength, redSpeed)
    edgeDG      = edgeManager.createBidirectionalEdge(nodeD, nodeG, redLength, redSpeed)
    edgeGE      = edgeManager.createBidirectionalEdge(nodeG, nodeE, redLength, redSpeed)
    edgeGK      = edgeManager.createBidirectionalEdge(nodeG, nodeK, redLength, redSpeed)
    edgeKJ      = edgeManager.createBidirectionalEdge(nodeK, nodeJ, redLength, redSpeed)
    edgeJN      = edgeManager.createBidirectionalEdge(nodeJ, nodeN, redLength, redSpeed)
    edgeJM      = edgeManager.createBidirectionalEdge(nodeJ, nodeM, redLength, redSpeed)
    edgeMI      = edgeManager.createBidirectionalEdge(nodeM, nodeI, redLength, redSpeed)
    edgeIL      = edgeManager.createBidirectionalEdge(nodeI, nodeL, redLength, redSpeed)
    edgeIH      = edgeManager.createBidirectionalEdge(nodeI, nodeH, redLength, redSpeed)
    edgeHF      = edgeManager.createBidirectionalEdge(nodeH, nodeL, redLength, redSpeed)

    edgeFG      = edgeManager.createBidirectionalEdge(nodeF, nodeG, redLength, redSpeed)
    edgeGJ      = edgeManager.createBidirectionalEdge(nodeG, nodeJ, redLength, redSpeed)
    edgeJI      = edgeManager.createBidirectionalEdge(nodeJ, nodeI, redLength, redSpeed)
    edgeIF      = edgeManager.createBidirectionalEdge(nodeI, nodeF, redLength, redSpeed)

    edgeJF      = edgeManager.createBidirectionalEdge(nodeJ, nodeF, redLength, redSpeed)
    edgeGI      = edgeManager.createBidirectionalEdge(nodeG, nodeI, redLength, redSpeed)

    sim = Simulator(nodeManager, edgeManager)
    for i in range(0, 1000):
        sim.addVehicle(nodeA, nodeC)
    sim.startBaselineSimulation()

@pytest.mark.sim
def test_simulation_setup():
    # Create a simulator
    sim = Simulator()
    # Create nodes
    nodeA = sim.createNode(0, 0)
    nodeB = sim.createNode(0, 0)
    nodeC = sim.createNode(0, 0)
    nodeD = sim.createNode(0, 0)
    assert len(sim.nodes) == 4
    # Create edges
    edgeAB = sim.createEdge(nodeA, nodeB, 100, 100)
    edgeBC = sim.createEdge(nodeB, nodeC, 100, 100, False)
    edgeCD = sim.createEdge(nodeC, nodeD, 100, 100)
    edgeDA = sim.createEdge(nodeD, nodeA, 100, 100, False)
    assert len(sim.edges) == 2*2 + 2
    # Add 3 vehicles to each path
    for startingNode in sim.nodes:
        for targetNode in sim.nodes:
            if startingNode != targetNode:
                for i in range(0, 3):
                    sim.createVehicle(startingNode, targetNode)
    assert len(sim.vehicles) == 36
    # Run the baseline simulation
    sim.runBaselineSimulation()




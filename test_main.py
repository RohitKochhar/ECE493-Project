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
from random import randint
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
    edge        = sim.createEdge(sourceNode, sinkNode, 5000, 100)
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
    edge01          = sim.createEdge(sourceNode, interNode, 40, 110)
    edge12          = sim.createEdge(interNode, sinkNode, 40, 110)
    # Create simulator
    sim = Simulator(nodeManager, edgeManager)
    for i in range(0, 1000):
        sim.addVehicle(sourceNode, sinkNode)
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
    sim.runOptimizedSimulation()
    sim.showResults()

    # Clean up
    del sim

@pytest.mark.sim
def test_network_2():
    length       = 10
    speed        = 30
    # Create sim
    print(f"Starting Simulation...")
    sim = Simulator()
    # Create nodes
    print(f"Creating nodes...")
    nodeA       = sim.createNode(0, 0)
    nodeB       = sim.createNode(0, 0)
    nodeC       = sim.createNode(0, 0)
    nodeD       = sim.createNode(0, 0)
    nodeE       = sim.createNode(0, 0)
    nodeF       = sim.createNode(0, 0)
    nodeG       = sim.createNode(0, 0)
    nodeH       = sim.createNode(0, 0)
    nodeI       = sim.createNode(0, 0)
    nodeJ       = sim.createNode(0, 0)
    nodeK       = sim.createNode(0, 0)
    nodeL       = sim.createNode(0, 0)
    nodeM       = sim.createNode(0, 0)
    nodeN       = sim.createNode(0, 0)
    nodeO       = sim.createNode(0, 0)
    nodeP       = sim.createNode(0, 0)
    print(f"\tCreated nodes")
    print(f"Creating edges...")
    # Create edges
    #   Outer edges
    edgeAB      = sim.createEdge(nodeA, nodeB, length, speed)
    edgeBC      = sim.createEdge(nodeB, nodeC, length, speed)
    edgeCD      = sim.createEdge(nodeC, nodeD, length, speed)

    edgeDH      = sim.createEdge(nodeD, nodeH, length, speed)
    edgeHL      = sim.createEdge(nodeH, nodeL, length, speed)
    edgeLP      = sim.createEdge(nodeL, nodeP, length, speed)
    
    edgePO      = sim.createEdge(nodeP, nodeO, length, speed)
    edgeON      = sim.createEdge(nodeO, nodeN, length, speed)
    edgeNM      = sim.createEdge(nodeN, nodeM, length, speed)

    edgeDH      = sim.createEdge(nodeM, nodeI, length, speed)
    edgeHL      = sim.createEdge(nodeI, nodeE, length, speed)
    edgeLP      = sim.createEdge(nodeE, nodeA, length, speed)

    #   Mid edges
    edgeBF      = sim.createEdge(nodeB, nodeF, length, speed)
    edgeCG      = sim.createEdge(nodeC, nodeG, length, speed)

    edgeGH      = sim.createEdge(nodeG, nodeH, length, speed)
    edgeKL      = sim.createEdge(nodeK, nodeL, length, speed)

    edgeKO      = sim.createEdge(nodeK, nodeO, length, speed)
    edgeJN      = sim.createEdge(nodeJ, nodeN, length, speed)

    edgeIJ      = sim.createEdge(nodeI, nodeJ, length, speed)
    edgeEF      = sim.createEdge(nodeE, nodeF, length, speed)

    #   Inner edges
    edgeFG      = sim.createEdge(nodeF, nodeG, length, speed)
    edgeGK      = sim.createEdge(nodeG, nodeK, length, speed)
    edgeKJ      = sim.createEdge(nodeK, nodeJ, length, speed)
    edgeFJ      = sim.createEdge(nodeF, nodeJ, length, speed)

    assert len(sim.edges) == 2*24

    print(f"\tCreated Edges")
    print(f"Adding vehicles to simulation...")
    for i in range(0, 150):
        node1 = sim.nodes[randint(0, len(sim.nodes) - 1)]
        node2 = sim.nodes[randint(0, len(sim.nodes) - 1)]
        while node1 == node2:
            node2 = sim.nodes[randint(0, len(sim.nodes) - 1)]
        sim.createVehicle(node1, node2)
    print(f"\tVehicles added to simulation.")

    print(f"Running Baseline Simulation")
    sim.runBaselineSimulation()
    print(f"\tBaseline Simulation complete")
    print(f"Running Optimized Simulation")
    sim.runOptimizedSimulation()
    print(f"\tOptimized Simulation complete")
    sim.showResults()
    sim.exportResults()

    # Clean up
    del sim

@pytest.mark.sim
def test_network_1():
    greenLength     = 40
    greenSpeed      = 110
    yellowLength    = 20
    yellowSpeed     = 80
    redLength       = 10
    redSpeed        = 30
    # Create sim
    print(f"Starting Simulation...")
    sim = Simulator()
    # Create nodes
    print(f"Creating nodes...")
    nodeA       = sim.createNode(0, 0)
    nodeB       = sim.createNode(0, 0)
    nodeC       = sim.createNode(0, 0)
    nodeD       = sim.createNode(0, 0)
    nodeE       = sim.createNode(0, 0)
    nodeF       = sim.createNode(0, 0)
    nodeG       = sim.createNode(0, 0)
    nodeH       = sim.createNode(0, 0)
    nodeI       = sim.createNode(0, 0)
    nodeJ       = sim.createNode(0, 0)
    nodeK       = sim.createNode(0, 0)
    nodeL       = sim.createNode(0, 0)
    nodeM       = sim.createNode(0, 0)
    nodeN       = sim.createNode(0, 0)
    nodeO       = sim.createNode(0, 0)
    nodeP       = sim.createNode(0, 0)
    print(f"\tCreated edges")
    # Create edges
    #   Highway edges
    print(f"Creating edges...")
    edgeAB      = sim.createEdge(nodeA, nodeB, greenLength, greenSpeed)
    edgeAO      = sim.createEdge(nodeA, nodeO, greenLength, greenSpeed)
    edgeBP      = sim.createEdge(nodeB, nodeP, greenLength, greenSpeed)
    edgeOP      = sim.createEdge(nodeO, nodeP, greenLength, greenSpeed)
    #   Rural edges
    edgeAD      = sim.createEdge(nodeA, nodeD, yellowLength, yellowSpeed)
    edgeAH      = sim.createEdge(nodeA, nodeH, yellowLength, yellowSpeed)
    edgeBD      = sim.createEdge(nodeB, nodeD, yellowLength, yellowSpeed)
    edgeBK      = sim.createEdge(nodeB, nodeK, yellowLength, yellowSpeed)
    edgeOH      = sim.createEdge(nodeO, nodeH, yellowLength, yellowSpeed)
    edgeOM      = sim.createEdge(nodeO, nodeM, yellowLength, yellowSpeed)
    edgePM      = sim.createEdge(nodeP, nodeM, yellowLength, yellowSpeed)
    edgePK      = sim.createEdge(nodeP, nodeK, yellowLength, yellowSpeed)
    #   City edges
    edgeAC      = sim.createEdge(nodeA, nodeC, redLength, redSpeed)
    edgeEB      = sim.createEdge(nodeE, nodeB, redLength, redSpeed)
    edgeNP      = sim.createEdge(nodeN, nodeP, redLength, redSpeed)
    edgeOL      = sim.createEdge(nodeO, nodeL, redLength, redSpeed)

    edgeCD      = sim.createEdge(nodeC, nodeD, redLength, redSpeed)
    edgeDE      = sim.createEdge(nodeD, nodeE, redLength, redSpeed)
    edgeEK      = sim.createEdge(nodeE, nodeK, redLength, redSpeed)
    edgeKN      = sim.createEdge(nodeK, nodeN, redLength, redSpeed)
    edgeNM      = sim.createEdge(nodeN, nodeM, redLength, redSpeed)
    edgeML      = sim.createEdge(nodeM, nodeL, redLength, redSpeed)
    edgeLH      = sim.createEdge(nodeL, nodeH, redLength, redSpeed)
    edgeCH      = sim.createEdge(nodeC, nodeH, redLength, redSpeed)
    
    edgeCF      = sim.createEdge(nodeC, nodeF, redLength, redSpeed)
    edgeFD      = sim.createEdge(nodeF, nodeD, redLength, redSpeed)
    edgeDG      = sim.createEdge(nodeD, nodeG, redLength, redSpeed)
    edgeGE      = sim.createEdge(nodeG, nodeE, redLength, redSpeed)
    edgeGK      = sim.createEdge(nodeG, nodeK, redLength, redSpeed)
    edgeKJ      = sim.createEdge(nodeK, nodeJ, redLength, redSpeed)
    edgeJN      = sim.createEdge(nodeJ, nodeN, redLength, redSpeed)
    edgeJM      = sim.createEdge(nodeJ, nodeM, redLength, redSpeed)
    edgeMI      = sim.createEdge(nodeM, nodeI, redLength, redSpeed)
    edgeIL      = sim.createEdge(nodeI, nodeL, redLength, redSpeed)
    edgeIH      = sim.createEdge(nodeI, nodeH, redLength, redSpeed)
    edgeHF      = sim.createEdge(nodeH, nodeF, redLength, redSpeed)

    edgeFG      = sim.createEdge(nodeF, nodeG, redLength, redSpeed)
    edgeGJ      = sim.createEdge(nodeG, nodeJ, redLength, redSpeed)
    edgeJI      = sim.createEdge(nodeJ, nodeI, redLength, redSpeed)
    edgeIF      = sim.createEdge(nodeI, nodeF, redLength, redSpeed)

    edgeJF      = sim.createEdge(nodeJ, nodeF, redLength, redSpeed)
    edgeGI      = sim.createEdge(nodeG, nodeI, redLength, redSpeed)
    print(f"\tCreated Edges")
    print(f"Adding vehicles to simulation...")
    for i in range(0, 400):
        node1 = sim.nodes[randint(0, len(sim.nodes) - 1)]
        node2 = sim.nodes[randint(0, len(sim.nodes) - 1)]
        while node1 == node2:
            node2 = sim.nodes[randint(0, len(sim.nodes) - 1)]
        sim.createVehicle(node1, node2)
    print(f"\tVehicles added to simulation.")

    print(f"Running Baseline Simulation")
    sim.runBaselineSimulation()
    print(f"\tBaseline Simulation complete")
    print(f"Running Optimized Simulation")
    sim.runOptimizedSimulation()
    print(f"\tOptimized Simulation complete")
    sim.showResults()
    sim.exportResults()

    # Clean up
    del sim



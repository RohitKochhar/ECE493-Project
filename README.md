# ECE493 Final Project: IoT Traffic Management System

While the associated software with this project is open-source under the MIT license, the associated research paper is the creation and academic and property of the authors, Rohit Singh and Vojdan Bojcev. 

## Research Paper
The LaTeX source code for the research paper this code is based off is located at `main.tex`. The compiled PDF can be found [here](https://github.com/RohitKochhar/ECE493-Project/blob/main/FinalReport.pdf)

## Motivation

In this work, we aim to propose a novel solution that transforms traditional traffic networks into dynamic sensor networks that communicate traffic flow information to autonomous vehicles within the network. Our proposed solution would allow traffic lights to act as communicating beacons, relaying information about real-time traffic flow to the path planning systems of autonomous vehicles to allow them to adopt the ideal route to reach their target destination.

## Implementation

To test the created model, a discrete event simulator was designed and implemented. The `Simulator` model can be found in `simulator.py`, and depends on the models located in `edgeManager.py`, `nodeManager.py` and `vehicleManager.py`. All code files can be found in `.src/` folder.

Unit tests and different simulation scenarios were implemented using `pytest`, and can be found in `test_main.py` 



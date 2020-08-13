# bachelor-thesis-ros
## Thesis title: Sensor-based navigation of a robot under ROS with triangulation scanner

The final aim of this project is to build a ROS system consisting of a Lego Boost robot,
a triangulation sensor, a localization and control algorithm. All these components are rep-
resented by individual ROS nodes. The triangulation sensor is fixed in the room, and the
controller lets the robot follow a user-predefined path in the room




## Problem Statement
This project is divided into several hardware and software components. The main element
is the PC, which can be seen as a master. Other elements, such as a triangulation laser
scanner, a lego boost robot, localization algorithms, and motion control algorithms can be
viewed as slaves.
First, a ROS system must be installed and created on the PC. Then a simple Lego Boost
robot must be assembled, including the robot’s connection to the PC. A triangulation laser
scanner must be later integrated into the system. The next problem is the implementation
of the localization algorithms. Lastly, the motion control algorithms must be implemented
and integrated into the system.


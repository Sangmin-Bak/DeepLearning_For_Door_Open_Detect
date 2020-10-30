# DeepLearning_For_Lift_Open_Detect
The purpose of this project is to allow robots to enter and exit elevators by recognizing whether the elevator doors are open.

## Requirements
1. Ubuntu16.04
2. ROS Kinetic
3. Tensorflow 1.14.0 
4. python2.7
5. 2GB GPU

## Installation
```
cd ~/catkin_ws/src
git clone https://github.com/Sangmin-Bak/DeepLearning_For_Lift_Open_Detect
cd ~/catkin_ws && catkin_make
```

## Run
```
roslaunch lift_detect lift_door_detect.launch

node without ROS
roscd lift_detect/node
./lift_detect_with_tensorflow.py
```

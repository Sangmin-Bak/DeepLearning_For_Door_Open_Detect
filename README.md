# DeepLearning_For_Door_Open_Detect
The purpose of this project is to allow robots to enter and exit elevators by recognizing whether the lift doors are open.

## Requirements
1. Ubuntu16.04
2. ROS Kinetic
3. Tensorflow 1.14.0 
4. python2.7
5. 2GB GPU

## Installation
```
cd ~/catkin_ws/src
git clone https://github.com/Sangmin-Bak/DeepLearning_For_Door_Open_Detect
cd ~/catkin_ws && catkin_make
```

## Install Model
https://drive.google.com/file/d/1ZX20tCJG9SV3STvSC_Nqvaoak3alEdCg/view?usp=sharing
```
unzip model.zip
mkdir ~/catkin_ws/src/DeepLearning_For_Door_Open_Detect/lift_detect/models
cp model.pb ~/catkin_ws/src/DeepLearning_For_Door_Open_Detect/lift_detect/models
```

## Run node with ROs
```
roslaunch door_detect door_detect.launch
```

## Run node without ROS
```
roscd door_detect/node
./door_detect_with_tensorflow.py
```

## Original Repository
https://github.com/namjoshiniks/Deep_Learning_For_Indoor_Robots

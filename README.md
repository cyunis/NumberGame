# QTNumberGame and NumberGame
Games for the summer 2019 Tommy Thumb study - both are in the folder "Final Versions"

## QTNumberGame
This game is part of the Tommy Thumb system. It is meant to be played on the [QTRobot built by LuxAI](http://wiki.ros.org/Robots/qtrobot) running ROS Kinetic on Ubuntu 16.04. The game is run during an experimental set up combined with several other subsystems (each on their own computer/microprocessor): [orthosis](https://github.com/jonreal/openWearable/tree/thumbsup), [camera](https://github.com/HeegerGao/USC), [CoRDial](https://github.com/ndennler/cordial-public) and EMG. 

Before running the game a package must be made for the games and the catkin workspace set up. Several functions in the game use ROS publishers developed on QT or through the other subsystems and these must be set up as well (see links for QTRobot wiki, orthosis,  camera and CoRDial). <br><br>

## Setting up CoRDial
Git pull from the repository linked above.
In the first terminal window run:
```
> roslaunch cordial_example test_setup.launch
```
In the second terminal window run:
```
> roscd cordial_face/web
> http-server
```
Look for the number of the available ports - use this port number (it is 8081 in my case) for the third window (first switch to QT's wifi and ssh to QT's head computer):
```
> ssh qtrobot@qtrobot
> luakit -U 192.168.100.2:8081/KiwiLite.html
```
This command runs the web browser in private mode using the body computer's processor, the available port and the KiwiLite version of CoRDial. The CoRDial face should show up on the screen after this command is run.

In the fourth window run your python game script (you can run this on any wifi and it should be on the body computer):
```
> rosrun packagename QTNumberGame.py
```

## Instructions

## Playing the Game

## Ending the Game

## Data Collection

# QT Number Guessing Game

These notes are written to run the QT Demo for filming.


## Dependencies

First make sure the following packages are correctly built in a workspace together:

- cordial-public
- hand_tracking_ros_package
- NumberGame  (feedback-function branch)


The packages were successfully built on Ubuntu 18.04, with ROS melodic using catkin_build.

Cordial has also been built on 16.04 and ros kinetic. You are free to attempt to build the packages on other verions of ROS but your mileage may vary. If using a different version of ROS, make sure to update the installation of ros packages to include the name of the version you are using.

## Generating the script
To generate the script, first make sure you know the name of the participant and which hand they will be using to play the game

```
# in NumberGame/scripts, edit generate.py
# copy the produced script.txt to cordial-public/cordial_example/speech/script.txt
roscd cordial-public/cordial_example/speech
./gen_audio.sh
```

##  Sending the audio files to QTRobot

Once the audio files are generated, send them to QTRobot.

## Playing the Game

To play the game, you will need to do several things. There is probably a way to make it easier, but there are issues with things being in python3 vs python2 because thank you robotics for not supporting python3 easily until 20.04 :)))).

First, launch the cordial manager, which sets up all of the robot speaking things

```
roslaunch number_game start_demo.launch
```

Next, launch the face on QTRobot (connected to the belly computer)
```

ssh qtrobot@192.168.0.1
roscd cordial_face/web
http-server
```
Then launch the browser (still ssh'd into the belly computer)
mayyyybe, I still have to verify this....

```
luakit -U 192.168.100.2:8081/KiwiLite.html
##########################################
#########################################
        fill this out babe
############################################
######################################
```

Next, launch the webcam script to track the participant's hand, include the number of the device that is being used to track the hand:

```
roscd hand_tracking_ros_package/src
python3 publish_angle_node.py <number of device>
```

You will also want to calibrate the angle tracking algorithm by pressing c on the screen that pops up when the participant is making a neutral gesture. Once this is done, the angle values will start publishing.

Finally, start the game!
```
roscd number_game/scripts
python GameStateMachine.py
```
# QT Number Guessing Game

These notes are written to run the QT Demo for filming. These should all be downloaded onto QTPC for the demo to work correctly.


## Dependencies

First make sure the following packages are correctly built in a workspace together:

- cordial-public
- hand_tracking_ros_package
- NumberGame  (demo branch)


The packages were successfully built on Ubuntu 18.04, with ROS melodic using catkin_build.

Cordial has also been built on 16.04 and ros kinetic. You are free to attempt to build the packages on other verions of ROS but your mileage may vary. If using a different version of ROS, make sure to update the installation of ros packages to include the name of the version you are using.

## Generating the script
To generate the script, first make sure you know the name of the participant and which hand they will be using to play the game

```
# in [tommy-thumb-ws]/src/NumberGame/scripts, edit generate.py
roscd number_game/scripts
python3 generate.py
# copy the produced script.txt to cordial-public/cordial_example/speech/script.txt
roscd cordial_example/speech
./gen_audio.sh
```

##  Sending the audio files to QTRobot

Once the audio files are generated, send them to QTRobot.
```
roscd number_game/scripts
./send_to_qt_head.sh
```

## Playing the Game

To play the game, you will need to do several things. There is probably a way to make it easier, but there are issues with things being in python3 vs python2 because thank you ros robotics for not supporting python3 easily until 20.04 :)))).

First, launch the cordial manager, which sets up all of the robot speaking things

```
roslaunch number_game start_demo.launch
```

Next in a different terminal tab, launch the face on QTRobot (connected to the belly computer)

```
roscd cordial_face/web
http-server
```

Then in a different terminal tab launch the browser (ssh'd into the head computer)

```
ssh qtrobot@192.168.100.1
luakit -U 192.168.100.2:8081/KiwiLite.html

# NOTE: make sure the phrase file is loaded when you launch start_demo.launch before running this command
# when connected, the terminal for start_demo.launch should read [Client <#>] Subscribed to DB1/face
# if it reads [Client <#>] Subscribed to cordial/behavior/face/expressing, wait for it to load and rerun
# the luakit command
```

Next, in a different terminal tab launch the webcam script to track the participant's hand, include the number of the device that is being used to track the hand:

```
roscd hand_tracking_ros_package/src
python3.7 publish_angle_node.py <number of device>
#NOTE: To find the number of the device try 0, 1, 2, 3... Also the camera tracks correctly if the knuckles are facing the camera (not side view)
```

You will also want to calibrate the angle tracking algorithm by pressing c on the screen that pops up when the participant is making a neutral gesture. Once this is done, the angle values will start publishing to the topic /thumb_angle.


Finally, start the game (in a different terminal tab)!

```
roscd number_game/scripts
python GameStateMachine.py
```

At this point you should have 5 different terminal tabs running and QT should have started playing the game.


If the volume is too low, you can ssh into qt's head and adjust the volume with alsamixer (around 65-70 is usually appropriate) as follows:

```
ssh qtrobot@192.168.100.1
alsamixer
```

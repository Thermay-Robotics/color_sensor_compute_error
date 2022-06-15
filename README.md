# color_sensor_compute_error

Compute the error between a targeted luminious intensity and the one measured.

# Notice
It subscribes to the colorSensorValue of the color sensor node. These values are used to determine two things:
* The color. If it corresponds to a known color (blue or orange), the color will be published as a String on the Color topic.
* The luminious intensity. If the color measured is unknown, the average between the three measured values (R,G,B) will be computed to get the luminious inntensity. This value will be compared to the targeted value and the error will be send to the Error topic.

### Subscribed Topics

* ```/colorSensorValue``` ([std_msgs/Int16MultiArray])
    Array of the values (R,G,B) measured by the color sensor.

### Published Topics

* ``` /Color``` ([std_msgs/String])
    Publishes the detected color if it is known.
* ``` /Error``` ([std_msgs/Float32])
    Publishes the computed error.

# How to build
```
cd ~/catkin_ws/src/
git clone https://github.com/Thermay-Robotics/color_sensor_compute_error.git
cd ~/catkin_ws
catkin_make
```

# Run
Launch 
```
roslaunch calcul_erreur calcul_erreur.launch
```


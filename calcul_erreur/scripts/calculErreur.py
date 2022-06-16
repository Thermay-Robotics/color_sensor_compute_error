#!/usr/bin/env python

from datetime import date
import rospy
from std_msgs.msg import Int16MultiArray,MultiArrayDimension,MultiArrayLayout,String,Float32


node = None
nodePublisherColor = None
nodePublisherError = None

orange_red = 0
orange_green = 0
orange_blue = 0

dark_blue_red = 0
dark_blue_green = 0
dark_blue_blue = 0

light_blue_red = 0
light_blue_green = 0
light_blue_blue = 0

white_avg = 0

black_avg = 0

cible = 0
error = 0

threshold = 0

def callback(data):
    global threshold, orange_red, orange_green, orange_blue, white_avg, black_avg,cible,error, dark_blue_red, dark_blue_green, dark_blue_blue, light_blue_red, light_blue_green, light_blue_blue
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    data_red = data.data[0]
    data_green = data.data[1]
    data_blue = data.data[2]

    if data_red > orange_red - threshold and data_red < orange_red + threshold and data_green > orange_green - threshold and data_green < orange_green + threshold and data_blue > orange_blue - threshold and data_blue < orange_blue + threshold:
        rospy.loginfo("[COLOR]orange")
        publishColor("orange")
    elif data_red > dark_blue_red - threshold and data_red < dark_blue_red + threshold and data_green > dark_blue_green - threshold and data_green < dark_blue_green + threshold and data_blue > dark_blue_blue - threshold and data_blue < dark_blue_blue + threshold:
        rospy.loginfo("[COLOR]blue")
        publishColor("blue")
    elif data_red > light_blue_red - threshold and data_red < light_blue_red + threshold and data_green > light_blue_green - threshold and data_green < light_blue_green + threshold and data_blue > light_blue_blue - threshold and data_blue < light_blue_blue + threshold:
        rospy.loginfo("[COLOR]blue")
        publishColor("blue")
    else:
        avg = (data_red + data_green + data_blue) / 3
        error = avg - cible
        publishError()
    


def calibrate():
    global orange_red, orange_green, orange_blue, white_avg, black_avg, threshold, cible, dark_blue_red, dark_blue_green, dark_blue_blue, light_blue_red, light_blue_green, light_blue_blue
    
    orange_red = rospy.get_param('/calculEr/orange_red')
    orange_green = rospy.get_param('/calculEr/orange_green')
    orange_blue = rospy.get_param('/calculEr/orange_blue')
    dark_blue_red = rospy.get_param('/calculEr/dark_blue_red')
    dark_blue_green = rospy.get_param('/calculEr/dark_blue_green')
    dark_blue_blue = rospy.get_param('/calculEr/dark_blue_blue')
    light_blue_red = rospy.get_param('/calculEr/light_blue_red')
    light_blue_green = rospy.get_param('/calculEr/light_blue_green')
    light_blue_blue = rospy.get_param('/calculEr/light_blue_blue')
    white_avg = rospy.get_param('/calculEr/white_avg')
    black_avg = rospy.get_param('/calculEr/black_avg')
    threshold = rospy.get_param('/calculEr/threshold')
    
    cible = (white_avg + black_avg)/2

 
def init():
    global node, nodePublisherColor, nodePublisherError
    rospy.init_node('subscriber_node')
    node = rospy.Subscriber("colorSensorValue", Int16MultiArray, callback)
    nodePublisherColor = rospy.Publisher("Color", String, queue_size=10)
    nodePublisherError = rospy.Publisher("Error", Float32, queue_size=10)
    

def publishError():
    global node,error
    data = error
    nodePublisherError.publish(data)
    rospy.loginfo(rospy.get_caller_id() + "I published %s", data)

def publishColor(couleur):
    global node
    data = couleur
    nodePublisherColor.publish(couleur)
    rospy.loginfo(rospy.get_caller_id() + "I published %s", data)

if __name__ == '__main__':
    init()
    
    rospy.loginfo(rospy.get_caller_id() + " I'm alive")
    rospy.loginfo(node)
    calibrate()
    rospy.spin()

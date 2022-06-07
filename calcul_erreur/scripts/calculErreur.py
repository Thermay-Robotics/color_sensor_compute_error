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
blue_red = 0
blue_green = 0
blue_blue = 0
white_avg = 0

black_avg = 0

cible = 0
error = 0

threshold = 0

def callback(data):
    global threshold, orange_red, orange_green, orange_blue, white_avg, black_avg,cible,error
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    data_red = data.data[0]
    data_green = data.data[1]
    data_blue = data.data[2]
    #rospy.loginfo(f" r : {data_red} ; g : {data_green} ; b : {data_blue}")

    if data_red > orange_red - threshold and data_red < orange_red + threshold and data_green > orange_green - threshold and data_green < orange_green + threshold and data_blue > orange_blue - threshold and data_blue < orange_blue + threshold:
        rospy.loginfo("[COLOR]orange")
        publishColor("orange")
    elif data_red > blue_red - threshold and data_red < blue_red + threshold and data_green > blue_green - threshold and data_green < blue_green + threshold and data_blue > blue_blue - threshold and data_blue < blue_blue + threshold:
        rospy.loginfo("[COLOR]blue")
        publishColor("blue")
    else:
        avg = (data_red + data_green + data_blue) / 3
        error = avg - cible
        #rospy.loginfo(f"erreur : {error}")
        publishError()
    


def calibrate():
    global orange_red, orange_green, orange_blue, white_avg, black_avg, threshold, cible, blue_red, blue_green, blue_blue
    
    orange_red = rospy.get_param('/calculEr/orange_red')
    orange_green = rospy.get_param('/calculEr/orange_green')
    orange_blue = rospy.get_param('/calculEr/orange_blue')
    blue_red = rospy.get_param('/calculEr/blue_red')
    blue_green = rospy.get_param('/calculEr/blue_green')
    blue_blue = rospy.get_param('/calculEr/blue_blue')
    white_avg = rospy.get_param('/calculEr/white_avg')
    black_avg = rospy.get_param('/calculEr/black_avg')
    threshold = rospy.get_param('/calculEr/threshold')
    
    cible = (white_avg + black_avg)/2

    #rospy.loginfo(f"[CALIBRATION]orange_red = {orange_red} ; orange_green = {orange_green} ; orange_blue = {orange_blue} ; white_avg = {white_avg} ; black_avg = {black_avg} ; threshold = {threshold}")


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
    #rospy.loginfo(f"orange_red = {orange_red} ; orange_green = {orange_green} ; orange_blue = {orange_blue} ; white_avg = {white_avg} ; black_avg = {black_avg}")
    rospy.spin()

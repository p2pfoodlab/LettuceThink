#!/usr/bin/env python

import roslib
roslib.load_manifest('p2p')
from sensor_msgs.msg import Image
import rospy


def callback(msg):
    img = msg
    sub.unregister()
    print '1 image recevied'

def listener():
    rospy.init_node('comput', anonymous=True)
    print 'node init'
    global sub
    sub = rospy.Subscriber('camera_pi/image_rect_color', Image, callback)
    print'success sub topic'
    rospy.spin()

if __name__ == "__main__":
    listener()

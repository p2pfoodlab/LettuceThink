#!/usr/bin/env python

import roslib
roslib.load_manifest('p2p')
from p2p.srv import *
import rospy

def client():
    rospy.wait_for_service('killer')

    try:
        rospy.ServiceProxy('killer', Empty)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    client()

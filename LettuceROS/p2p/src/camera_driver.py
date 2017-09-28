#!/usr/bin/env python

import roslib
roslib.load_manifest('p2p')
from sensor_msgs.msg import Image, CameraInfo
from sensor_msgs.srv import SetCameraInfo
import rospy
import time
import picamera
import cv2
import numpy as np
from cv_bridge import CvBridge
import camera_info_manager

camera = picamera.PiCamera()
h = rospy.get_param('resolution')
camera.resolution = (h[0],h[1])
camera.framerate = 60
time.sleep(2)
bridge = CvBridge()

def camera_driver():
    pub = rospy.Publisher('camera_pi/image_raw', Image, queue_size=10)
    pub2= rospy.Publisher('camera_pi/camera_info', CameraInfo, queue_size=10)
    rospy.init_node('camera_driver', anonymous=True)
    rate = rospy.Rate(24)

    picam = camera_info_manager.CameraInfoManager(cname='camera_pi', url='file:///home/p2p/.ros/camera_info/camera_pi.yaml',  namespace='camera_pi')
    picam.loadCameraInfo()

    while not rospy.is_shutdown():
        image = np.empty((h[1],h[0],3), dtype=np.uint8).flatten()
        camera.capture(image, format='bgr', use_video_port=True)
        image = image.reshape([h[1],h[0],3])
        image = bridge.cv2_to_imgmsg(image, 'bgr8')
        pub.publish(image)
        pub2.publish(picam.getCameraInfo())
        rate.sleep()

if __name__=="__main__":
    try:
        camera_driver()
    except rospy.ROSInterruptException:
        pass

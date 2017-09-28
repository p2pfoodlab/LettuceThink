#!/usr/bin/env python

import roslib
roslib.load_manifest('p2p')
from sensor_msgs.msg import Image
from p2p.msg import *
from p2p.srv import *
from std_srvs.srv import EmptyResponse
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
import lettucehoe2 as lh
import numpy as np
import actionlib
import workspace as ws
import plot_utils as pu

def handle_service(req):
    rospy.loginfo('called!')
    return EmptyResponse()

def genfig(im,Cmask,c0,dx,dy, Pmask, stp, path="./", alpha=.5, margin=0.05):
    pu.corners(im, Cmask, path, alpha)
    imc=pu.workspace(im, c0, dx, dy, path, margin)
    res=pu.plant_mask(imc, Pmask, c0, dx, dy, path, margin, alpha)
    pu.tpath(res, stp, c0, dx, dy, path, margin)

def feedback_cb(feedback):
    print "[Feedback] postion cnc: %s"%(feedback.pos_cnc)

def callback(msg):
    img = msg
    sub.unregister()

    print 'sub unregister'

    bridge = CvBridge()
    cv_im = bridge.imgmsg_to_cv2(img,"bgr8")

    ###########################
    im=lh.cv2.imread(rospy.get_param('path/test'))
    ###########################

    th = rospy.get_param('th')
    morpho_it = rospy.get_param('morpho_it')
    margin = rospy.get_param('margin')
    tool_size = rospy.get_param('tool_size')
    x0 = rospy.get_param('calib/x0')
    y0 = rospy.get_param('calib/y0')

    c0, dx, dy, Cmask = ws.getCorners(im, th, morpho_it)

    x0 -= c0[1]+margin*dx
    y0 -= c0[0]+margin*dy

    im_ws = im[c0[0]+margin*dy:c0[0]+(1-margin)*dy, c0[1]+margin*dx:c0[1]+(1-margin)*dx]
    Pmask = lh.plantmask(im_ws, tool_size*.6)
    ws_par1 = [im_ws.shape[1], 0, im_ws.shape[1], im_ws.shape[0]]
    #ws_par2 = [min(im_ws.shape[1]-tool_size, 700), 0, min(im_ws.shape[1]-tool_size, 700), min(im_ws.shape[0]-tool_size, 580)]
    toolPath = lh.mod_boustrophedon(Pmask, tool_size, ws_par1)
    stp = np.round(toolPath.T,0).reshape((-1,1,2)).astype(np.int32)

    genfig(im,Cmask,c0,dx,dy, Pmask, stp, rospy.get_param('path/img'), .5, margin)
    np.savetxt(rospy.get_param('path/txt'), toolPath)

    print 'toolPath saved'

    goal = gotoGoal()
    goal.x0 = x0
    goal.y0 = y0
    goal.data.x = toolPath[0,:]
    goal.data.y = toolPath[1,:]

    print 'goal create'

    client = actionlib.SimpleActionClient('cnc_action', gotoAction)
    client.wait_for_server()
    client.send_goal(goal, feedback_cb = feedback_cb)
    client.wait_for_result()
    result = client.get_result()
    print "[Result]: %d"%(result.success)

    s = rospy.Service('killer', Empty, handle_service)

def listener():
    rospy.init_node('comput', anonymous=True)
    print 'node init'
    global sub
    sub = rospy.Subscriber('camera_pi/image_rect_color', Image, callback)
    print'success sub topic'
    rospy.spin()

if __name__ == "__main__":
    listener()


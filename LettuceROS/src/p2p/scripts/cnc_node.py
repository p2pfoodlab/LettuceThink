#!/usr/bin/env python

import roslib
roslib.load_manifest('p2p')
from p2p.msg import *
import rospy
import actionlib
import cnc_utils as cnc
import numpy as np
import Queue
import time

def cqueue(xs,ys,z,rotspeed,fr):
    q = Queue.Queue(maxsize=0)

    q.put('G0 x%s y%s \n'%(xs[0],ys[0]))
    q.put('G0 Z-%s \n'%z)
    #q.put('M3 \n S%s \n'%rotspeed)

    for i in range(1,len(xs)):
        q.put('G1 x%s y%s F%s \n'%(min(500,xs[i]),max(0,ys[i]),fr))
        q.put('?')

    q.put('G0 Z0 \n')
    #q.put('M5 \n')
    q.put('G0 x0 y0 \n')

    for i in range(200):
        q.put('?')

    q.put('G4 P1 \n')
    print 'queue create'
    return q

def path(goal):
    if server.is_preempt_requested():
        result = gotoResult()
        result.success = False
        server.set_preempted(result, "Server preempted")
        return

    x0 = goal.x0
    y0 = goal.y0
    sfactor = rospy.get_param('calib/scale')
    fr = rospy.get_param('tool/feed_rate')
    z = rospy.get_param('tool/z')
    rotspeed = rospy.get_param('tool/rotspeed')

    ####################
    #s = cnc.init(False)
    ####################

    print 'cnc init'

    xs = np.asarray(goal.data.x)
    ys = np.asarray(goal.data.y)
    #xs,ys = cnc.convert_im2ws(xs, ys, x0, y0, sfactor)

    np.savetxt(rospy.get_param('path/txtmod'),(xs,ys))

    print 'path mod saved'

    q = cqueue(xs,ys,z,rotspeed,fr)
    f = open ('g_data.txt', 'w') #file in ~/.ros directory

    while not q.empty():
        a = q.get()
        f.write(a)
        res = cnc.send_cmd(a,s)

        if res.find('<') >= 0:
           feedback = gotoFeedback()
           feedback.pos_cnc = res
           server.publish_feedback(feedback)

        q.task_done()

    f.close
    q.join
    s.close()

    print 'queue send'

    result = gotoResult()
    result.success = True
    server.set_succeeded(result)

if __name__=="__main__":
    rospy.init_node('cnc_node')
    print 'node init'
    server = actionlib.SimpleActionServer('cnc_action', gotoAction, path, False)
    server.start()
    print 'server start'
    rospy.spin()

from flask import Flask, render_template, Response,request
import requests
import cnc_utils as cnc
import time
import json
import cv2
import numpy as np
import serial
import urllib
import lettucehoe2 as lh
import workspace as ws
import plot_utils as pu
import os


params=json.load(open("params/params.json","r"))
app=Flask(__name__)
s=[]
s=cnc.init(False)


def grab_url(url):
   req = urllib.urlopen(url)
   arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
   img = cv2.imdecode(arr,-1)
   return img

def topcam_pic(imdir,s):
   cnc.send_cmd("G0 y500 \n",s)
   cnc.send_cmd("G4 P1 \n",s)
   im=ut.grab_url('/lettucesee/raspicam/?action=snapshot')
   cv2.imwrite(imdir+"topcam.jpg",im)
   cnc.send_cmd("G0 y0 \n",s)

def clean():
   path=np.load("data/tool_path.npy")
   cnc.run_path(path[0],path[1],params["calib"]["x0"],params["calib"]["y0"],params["calib"]["scale"], params["tool"]["feed_rate"], params["tool"]["z"],  params["tool"]["rotspeed"], s)
   return "ok"   

def genfig(im,Cmask,c0,dx,dy, Pmask, stp, path="./", alpha=.5, margin=0.05):
   pu.corners(im, Cmask, path, alpha)
   imc=pu.workspace(im, c0, dx, dy, path, margin)
   res=pu.plant_mask(imc, Pmask, c0, dx, dy, path, margin, alpha)
   pu.tpath(res, stp, c0, dx, dy, path, margin)


@app.route('/scan')
def scan(impath="/home/pi/html/pics/", th=None,morpho_it=[5,5],margin=0.05):
   im=cnc.grab_url(params["cams"]["url_topcam"],params["mask"]["y"],s)
   cv2.imwrite("/home/pi/html/pics/topcam.jpg",im)
   c0,dx,dy,Cmask=ws.getCorners(im,th,morpho_it)
   params["calib"]["x0"]-=c0[1]+margin*dx
   params["calib"]["y0"]-=c0[0]+margin*dy
   print params["calib"]         
   im_ws=im[c0[0]+margin*dy:c0[0]+(1-margin)*dy,c0[1]+margin*dx:c0[1]+(1-margin)*dx]
   ws_par1=[im_ws.shape[1],0,im_ws.shape[1],im_ws.shape[0]]
   Pmask=lh.plantmask(im_ws,  params["tool_size"]*.6,morpho_it=[5,5])

   ws_par2=[min(im_ws.shape[1]-params["tool_size"],700),0,min(im_ws.shape[1]-params["tool_size"],700),min(im_ws.shape[0]-params["tool_size"],580)]
   path=lh.mod_boustrophedon(Pmask, params["tool_size"], ws_par2)
   stp=np.round(path.T,0).reshape((-1,1,2)).astype(np.int32)
   np.save("data/tool_path",path)
         
   genfig(im,Cmask,c0,dx,dy, Pmask, stp, impath, .5, margin)
   return "ok"

@app.route('/clean')
def clean():
   s=cnc.init(False)
   path=np.load("data/tool_path.npy")
   cnc.run_path(path[0],path[1],params["calib"]["x0"],params["calib"]["y0"],params["calib"]["scale"], params["tool"]["feed_rate"], params["tool"]["z"],  params["tool"]["rotspeed"], s)
   cnc.send_cmd("G0 x0 y0 \n",s)
   s.close()
   return "ok"

@app.route('/boustro')
def boustro():
   print "running boustro"
   #if params["notif"]["port"]: sendNotif("ON", params["notif"]["port"])
   s=cnc.init(False)
   path=np.load("data/boustro.npy")
   print path.shape
   cnc.run_path(path[0],path[1], params["calib"]["x0"], params["calib"]["y0"], params["calib"]["scale"], params["tool"]["feed_rate"], params["tool"]["z"],  params["tool"]["rotspeed"], s,False)
   cnc.send_cmd("G0 x0 y0 \n",s)
   s.close()
   #if params["notif"]["port"]: sendNotif("OFF", params["notif"]["port"])
   print '...'
   return "ok"
   
@app.route('/homing')
def homing():
   print "running boustro"
   #if params["notif"]["port"]: sendNotif("ON", params["notif"]["port"])
   s=cnc.init(True)
   s.close()
   #if params["notif"]["port"]: sendNotif("OFF", params["notif"]["port"])
   return "ok"
                  
   
if __name__=='__main__':
   app.run(host='0.0.0.0',debug=True)
       

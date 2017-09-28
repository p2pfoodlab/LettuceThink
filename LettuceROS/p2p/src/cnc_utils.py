import serial
import time
import urllib
import cv2
import numpy as np

def grab_url(url,y="cur",s=None):
   if y!="cur":
      send_cmd("G0 y%s \n"%y,s)
      send_cmd("G4 P1 \n",s)
   req = urllib.urlopen(url)
   arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
   img = cv2.imdecode(arr,-1)
   if y!="cur": send_cmd("G0 y0 \n",s)
   return img


def convert_im2ws(xs, ys, x0, y0, sfactor):
   resx=(x0-xs)/sfactor
   resy=(ys-y0)/sfactor
   return resx.clip(0,700), resy.clip(0,500)

"""
def convert_im2ws(xs, ys, x0, y0, sfactor):
   resx=(y0-xs)/sfactor
   resy=(ys-x0)/sfactor
   return resx, resy
"""

def init(homing=False):
   s = serial.Serial("/dev/ttyUSB0",115200)
   s.write("\r\n\r\n")
   time.sleep(2)
   s.flushInput()

   if homing: home(s)

   s.write("G90 \n")
   grbl_out=s.readline()
   print ' : ' + grbl_out.strip()
   s.write("G21 \n")
   grbl_out=s.readline()
   print ' : ' + grbl_out.strip()
   return s

def home(s):
  send_cmd("$H \n",s)
  #send_cmd("g28 \n",s)
  send_cmd("g92 x0 y0 z0 \n",s)

def send_cmd(cmd,s):
   print cmd
   s.write(cmd)

   grbl_out=s.readline()
   print ' : ' + grbl_out.strip()
   return grbl_out.strip()

def run_path(xs, ys, x0, y0, sfactor, fr, z, rotspeed,s,cvt=True):
   if cvt:
      xs,ys=convert_im2ws(xs, ys, x0, y0, sfactor)
      xs=xs.clip(0,700)
      ys=ys.clip(0,700)

   cmd="G0 x%s y%s \n"%(xs[0],ys[0])
   send_cmd(cmd,s)
   send_cmd("G0 Z-%s \n"%z,s)
   send_cmd("M3 \n S%s \n"%rotspeed,s)
   time.sleep(1)
   #print "n",len(xs)
   for i in range(1,len(xs)):
      if fr>0: cmd="G1 x%s y%s F%s \n"%(xs[i],ys[i],fr)
      else: cmd="G0 x%s y%s \n"%(xs[i],ys[i])
      send_cmd(cmd,s)
      time.sleep(.1)

   send_cmd("G0 Z0 \n",s)
   send_cmd("M5 \n",s)
   send_cmd("G0 x0 y0 \n",s)
   #s.close()


def scanPath(xs, ys, x0, y0, sfactor, z, imdir, s):
   xs,ys=convert_im2ws(xs, ys, x0, y0, sfactor)
   xs=xs.clip(0,700)
   ys=ys.clip(0,700)
   print xs,ys
   cmd="G0 x%s y%s \n"%(xs[0],ys[0])
   send_cmd(cmd,s)
   send_cmd("G0 Z-%s \n"%z,s)
   time.sleep(1)
   #print "n",len(xs)
   for i in range(1,len(xs)):
      cmd="G0 x%s y%s \n"%(xs[i],ys[i])
      send_cmd(cmd,s)
      cmd="G4 P0.01 \n"
      send_cmd(cmd,s)
      im=grab_url(parama["cams"]["url_DS_depth"],s=s)
      cv2.imwrite(imdir+"DS_depth_%s.jpg"%i, im)
      im=grab_url(parama["cams"]["url_DS_color"],s=s)
      cv2.imwrite(imdir+"DS_color_%s.jpg"%i, im)
      time.sleep(.1)

   send_cmd("G0 Z0 \n",s)
   send_cmd("M5 \n",s)
   send_cmd("G0 x0 y0 \n",s)

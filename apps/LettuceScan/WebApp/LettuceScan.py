# LettuceScan.py
#
# Copyright (C) 2017 Peter Hanappe, Sony Computer Science
# Laboratories
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from flask import redirect
from flask import url_for
from flask import send_file
import datetime
import serial
import time
import DepthSense as DS
import cv2
import numpy as np
import os
import math
import subprocess
import zipfile

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

dir_path = os.path.dirname(os.path.realpath(__file__))

############################################################
# Global coordinates of the CNC and camera
#
# The access to the global variables is encapsulated in three get/set
# functions. This makes it easier to modify the code when we stop
# using global variables in favour of a more (thread-)safe solution.
#
x = 50
y = 50
z = 0
pan = 0
tilt = 0

def get_position():
    global x, y, z, pan, tilt
    return {'x': x, 'y': y, 'z': z, 'pan': pan, 'tilt': tilt }

def set_cnc_position(newx, newy, newz):
    global x, y, z
    x = newx
    y = newy
    z = newz

def set_camera_position(newpan, newtilt):
    global pan, tilt
    pan = newpan
    tilt = newtilt

############################################################
# CNC functions

cnc = 0;

def cnc_init(port="/dev/ttyUSB0"):
    global cnc
    cnc = serial.Serial(port, 115200)
    cnc.write("\r\n\r\n")
    time.sleep(2)
    cnc.flushInput()
    cnc_homing()
    cnc_send_cmd("G90")
    cnc_send_cmd("G21")
    return

def cnc_send_cmd(cmd):
    global cnc
    print cmd
    cnc.write(cmd + " \n")
    grbl_out = cnc.readline()
    print ' : ' + grbl_out.strip()
    return grbl_out

def cnc_update_position(newx, newy, newz):
    if False: # TODO: Doesn't work, yet
        cnc.write("$?")
        pos = cnc.readline()
        print pos
        start = pos.index("WPos:") + 5
        end = pos.index(">")
        pos = pos[start:end].split(",")
        print pos
        set_cnc_position(float(pos[0]) / 10,
                         float(pos[1]) / 10,
                         -float(pos[2]) / 10)
    else:
        set_cnc_position(newx, newy, newz)
    return

def cnc_moveto(newx, newy, newz):
    # tell CNC to move to new position
    cnc_send_cmd("G0 x%s y%s z%s\n"%(int(10*newx), int(10*newy), -int(10*newz)))
    # wait for reply from CNC
    cnc_send_cmd("G4 P1")
    # update new position
    cnc_update_position(newx, newy, newz)
    return

def cnc_homing():
    cnc_send_cmd("$H")
    cnc_send_cmd("g28")
    cnc_send_cmd("g92 x0 y0 z0")
    # get new position
    cnc_update_position(0, 0, 0)
    return

def cnc_stop():
    return

############################################################
# camera functions

ds = DS.initDepthSense()
imdir = "static/img"
panTilt = 0;

def camera_init(port="/dev/ttyACM0"):
    global panTilt
    panTilt = serial.Serial(port, 9600)
    return

def camera_homing():
    camera_moveto(0, 0)
    return

def camera_stop():
    return

def camera_moveto(newpan, newtilt):
    panTilt.write("p%s t%s\n"%(int(10*newpan), int(10*newtilt)))
    pos = panTilt.readline()
    print pos
    set_camera_position(newpan, newtilt)
    return

def grab_images(imdir, i):
    im = DS.getColourMap()
    cv2.imwrite("%s/rgb-%03d.png"%(imdir,i), im)       

    im = DS.getDepthMap()
    cv2.imwrite("%s/depth-%03d.png"%(imdir,i), im)   

    im = DS.getConfidenceMap()
    cv2.imwrite("%s/confidence-%03d.png"%(imdir,i), im)   
     
    im = DS.getDepthColouredMap()
    cv2.imwrite("%s/rgbd-%03d.png"%(imdir,i), im)   
  
    im = DS.getGreyScaleMap()
    cv2.imwrite("%s/gscale-%03d.png"%(imdir,i), im)   
    
    im = DS.getSyncMap()
    print im.shape
    np.save("%s/sync-%03d"%(imdir,i), im)   
    
    im = DS.getUVMap()
    np.save("%s/uv-%03d"%(imdir,i), im)   

    im = DS.getVertices()
    np.save("%s/vert-%03d"%(imdir,i), im)   
    
    #subprocess.call(['python', dir_path + '/dsgrab.py'])
    """
            {"href": "static/img/confidence.png", "name": "Confidence levels (image)"},
            {"href": "static/img/rgbd.png", "name": "Coloured depth image"},
            {"href": "static/img/gscale.png", "name": "Grey-scale image"}
    """
    return [{"href": imdir+"/rgb-%03d.png"%i, "name": "RGB image"},
            {"href": imdir+"/depth-%03d.png"%i, "name": "Depth image"},
            {"href": imdir+"/confidence-%03d.png"%i, "name": "Confidence levels (image)"},
            {"href": imdir+"/rgbd-%03d.png"%i, "name": "Coloured depth image"},
            {"href": imdir+"/gscale-%03d.png"%i, "name": "Grey-scale image"}]


############################################################
# scanning functions
        
def scanAt(x, y, z, pan, tilt, i, files):
    cnc_moveto(x, y, z)
    camera_moveto(pan, tilt)
    time.sleep(5)
    ims=["rgb", "depth", "confidence", "rgbd", "gscale"]
    np_arrays=["sync", "uv", "vert"]

    grab_images("static/scan", i)
    for im in ims: files.append({"href": "scan/" + im +"-%03d.png"%i,
                                 "name": im +"-%03d.png"%i})
    for a in np_arrays: files.append({"href": "scan/" + a +"-%03d.npy"%i,
                                 "name": a +"-%03d.npy"%i})    
    return

def createArchive(files):
    zf = zipfile.ZipFile('static/scan/all.zip', mode = 'w')
    try:
        for f in files:
            print "adding", "static/scan/" + f["name"]
            zf.write("static/scan/" + f["name"])
    finally:
        zf.close()
        return {"href": "scan/all.zip", "name": "all.zip"}

def circular_coordinates(cx, cy, R, N):
   alpha = np.linspace(0, 2 * np.pi, N + 1)
   pan = np.linspace(0, -360.0, N + 1)
   x, y = [], []
   for i in range(0, N):
      x.append(cx + R * math.sin(alpha[i]))
      y.append(cy - R * math.cos(alpha[i]))
   return x, y, pan

def circularscan(xc, yc, zc, r, nc):
    pos = get_position()
    tilt = pos['tilt']
    files = []    
    x, y, pan = circular_coordinates(xc, yc, r, nc)
    swivel = 0;
    for i in range(0, nc):
        if pan[i] < -180.0:
            swivel = 360.0
        scanAt(x[i], y[i], zc, pan[i] + swivel, tilt, i, files)
    cnc_moveto(x[0], y[0], zc)
    camera_moveto(0, tilt)
    files.append(createArchive(files))
    return files

def squarescan(xs, ys, zs, d, ns):
    return []

############################################################
# REST API

@app.route('/')
@app.route('/lettucescan')
def index():
    return redirect("/static/index.html")

@app.route('/moveto', methods=['POST'])
@app.route('/lettucescan/moveto', methods=['POST'])
def rest_moveto():
    newx = clamp(float(request.form['x']), 0.0, 80.0)
    newy = clamp(float(request.form['y']), 0.0, 80.0)
    newz = clamp(float(request.form['z']), 0.0, 10.0)
    newpan = clamp(float(request.form['pan']), -360.0, 360.0)
    newtilt = clamp(float(request.form['tilt']), -90.0, 90.0)
    cnc_moveto(newx, newy, newz)
    camera_moveto(newpan, newtilt) # should be done in parallel to cnc_moveto
    return jsonify(get_position())

@app.route('/move', methods=['POST'])
@app.route('/lettucescan/move', methods=['POST'])
def rest_move():
    dx = 0.0
    dy = 0.0
    dz = 0.0
    p = get_position()
    if 'dx' in request.form:
        dx = float(request.form['dx'])
    if 'dy' in request.form:
        dy = float(request.form['dy'])
    if 'dz' in request.form:
        dz = float(request.form['dz'])
    x = clamp(p['x'] + dx, 0.0, 80.0)
    y = clamp(p['y'] + dy, 0.0, 80.0)
    z = clamp(p['z'] + dz, 0.0, 10.0)
    cnc_moveto(x, y, z)
    return jsonify(get_position())

@app.route('/position')
@app.route('/lettucescan/position')
def rest_position():
    return jsonify(get_position())

@app.route('/homing')
@app.route('/lettucescan/homing')
def rest_homing():
    cnc_homing()
    camera_homing()
    return jsonify(get_position())

@app.route('/stop')
@app.route('/lettucescan/stop')
def rest_stop():
    # TODO
    return jsonify(get_position())

@app.route('/circularscan', methods=['POST'])
@app.route('/lettucescan/circularscan', methods=['POST'])
def rest_circularscan():
    print "rest_circularscan"
    xc = 0.0
    yc = 0.0
    zc = 0.0
    r = 0.0
    nc = 0
    if 'xc' in request.form:
        xc = float(request.form['xc'])
    else:
        return error_message("missing xc");
    if 'yc' in request.form:
        yc = float(request.form['yc'])
    else:
        return error_message("missing yc");
    if 'zc' in request.form:
        zc = float(request.form['zc'])
    else:
        return error_message("missing zc");
    if 'r' in request.form:
        r = float(request.form['r'])
    else:
        return error_message("missing r");
    if 'nc' in request.form:
        nc = int(request.form['nc'])
    else:
        return error_message("missing nc");
    if ((r < 1) or (r > 40)
        or (xc - r < 0) or (xc + r > 80)
        or (yc - r < 0) or (yc + r > 80)
        or (zc < 0) or (zc > 10)
        or (nc < 1) or (nc > 360)):
        return error_message("invalid parameters");
    print "xc: ", xc
    print "yc: ", yc
    files = circularscan(xc, yc, zc, r, nc)
    result = { "error": False,
               "files": files,
               "position": get_position() }
    return jsonify(result)

@app.route('/squarescan', methods=['POST'])
@app.route('/lettucescan/squarescan', methods=['POST'])
def rest_squarescan():
    xs = 0.0
    ys = 0.0
    zs = 0.0
    r = 0.0
    ns = 0
    if 'xs' in request.form:
        xs = float(request.form['xs'])
    else:
        return error_message("missing xs");
    if 'ys' in request.form:
        ys = float(request.form['ys'])
    else:
        return error_message("missing ys");
    if 'zs' in request.form:
        zs = float(request.form['zs'])
    else:
        return error_message("missing zs");
    if 'd' in request.form:
        d = float(request.form['d'])
    else:
        return error_message("missing d");
    if 'ns' in request.form:
        ns = int(request.form['ns'])
    else:
        return error_message("missing ns");
    if ((d < 1) or (d > 40)
        or (xs - d < 0) or (xs + d > 80)
        or (ys - d < 0) or (ys + d > 80)
        or (zs < 0) or (zs > 10)
        or (ns < 1) or (ns > 30)):
        return error_message("invalid parameters");
    files = squarescan(xs, ys, zs, d, ns)
    result = { "error": False,
               "files": files,
               "position": get_position() }
    return jsonify(result)

@app.route('/grab')
@app.route('/lettucescan/grab')
def rest_grab():
    files = grab_images(imdir, 0)
    return jsonify(files)

@app.route('/rgb.png')
@app.route('/lettucescan/rgb.png')
def rest_rgb():
    return send_file("static/img/rgb-000.png", mimetype='image/png')

@app.route('/depth.png')
@app.route('/lettucescan/depth.png')
def rest_depth():
    return send_file("static/img/depth-000.png", mimetype='image/png')

############################################################
# Utility functions

def error_message(s):
    return jsonify({ "error": True, "message": s })

def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n

############################################################

def lettucescan_init(app):
    cnc_init("/dev/ttyUSB0")
    camera_init("/dev/ttyACM0")


lettucescan_init(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0")

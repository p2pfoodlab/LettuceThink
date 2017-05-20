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

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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
# CNC, camera and scanning functions

def cnc_moveto(newx, newy, newz):
    # tell CNC to move to new position
    # wait for reply from CNC
    # extract new position from CNC's reply
    set_cnc_position(newx, newy, newz)
    return

def camera_moveto(newpan, newtilt):
    # tell camera to move to new position
    # wait for reply 
    # extract new position from camera's reply
    set_camera_position(newpan, newtilt)
    return

def circularscan(xc, yc, zc, r, nc):
    # TODO
    return

def squarescan(xs, ys, zs, d, ns):
    # TODO
    return

def grab_rgb_image(filename):
    # TODO
    return

def grab_depth_image(filename):
    # TODO
    return

# Returns the list of files of the most recent scan
def get_file_list():
    return [{"href": "static/scan/file1", "name": "file1"},
            {"href": "static/scan/file2", "name": "file2"}]

############################################################
# REST API

@app.route('/')
def index():
    return redirect("/static/index.html")

@app.route('/moveto', methods=['POST'])
def rest_moveto():
    newx = clamp(float(request.form['x']), 0.0, 80.0)
    newy = clamp(float(request.form['y']), 0.0, 80.0)
    newz = clamp(float(request.form['z']), 0.0, 15.0)
    newpan = clamp(float(request.form['pan']), -360.0, 360.0)
    newtilt = clamp(float(request.form['tilt']), -90.0, 90.0)
    cnc_moveto(newx, newy, newz)
    camera_moveto(newpan, newtilt) # should be done in parallel to cnc_moveto
    return jsonify(get_position())

@app.route('/move', methods=['POST'])
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
    z = clamp(p['z'] + dz, 0.0, 15.0)
    cnc_moveto(x, y, z)
    return jsonify(get_position())

@app.route('/position')
def rest_position():
    return jsonify(get_position())

@app.route('/homing')
def rest_homing():
    # TODO
    return jsonify(get_position())

@app.route('/stop')
def rest_stop():
    # TODO
    return jsonify(get_position())

@app.route('/circularscan', methods=['POST'])
def rest_circularscan():
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
        or (zc < 0) or (zc > 15)
        or (nc < 1) or (nc > 360)):
        return error_message("invalid parameters");
    circularscan(xc, yc, zc, r, nc)
    files = get_file_list()
    result = { "error": False,
               "files": files,
               "position": get_position() }
    return jsonify(result)

@app.route('/squarescan', methods=['POST'])
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
        or (zs < 0) or (zs > 15)
        or (ns < 1) or (ns > 30)):
        return error_message("invalid parameters");
    squarescan(xs, ys, zs, d, ns)
    files = get_file_list()
    result = { "error": False,
               "files": files,
               "position": get_position() }
    return jsonify(result)

@app.route('/rgb.png')
def rest_rgb():
    d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = "static/img/rgb-" + d + ".png" 
    grab_rgb_image(filename)
    return send_file("static/img/rgb.png", mimetype='image/png')

@app.route('/depth.png')
def rest_depth():
    d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = "static/img/depth-" + d + ".png" 
    grab_depth_image(filename)
    return send_file("static/img/depth.png", mimetype='image/png')

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

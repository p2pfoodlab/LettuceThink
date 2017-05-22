/*
    LettuceScan.js

    Copyright (C) 2017 Peter Hanappe, Sony Computer Science
    Laboratories

    LettuceScan.js is part of LettuceThink.

    LettuceThink is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

 */
var position = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'pan': 0.0, 'tilt': 0.0 };
var xypanCanvas;
var xypanTriangle;
var ztiltCanvas;
var ztiltTriangle;

function set_position2(p)
{
    position = p;
    document.getElementById("x").value = position.x;
    document.getElementById("y").value = position.y;
    document.getElementById("z").value = position.z;
    document.getElementById("pan").value = position.pan;
    document.getElementById("tilt").value = position.tilt;
}

function set_position(p)
{
    position = p;
    document.getElementById("x").value = position.x;
    document.getElementById("y").value = position.y;
    document.getElementById("z").value = position.z;
    document.getElementById("pan").value = position.pan;
    document.getElementById("tilt").value = position.tilt;

    xypanTriangle.setLeft(160 - 2 * position.x);
    xypanTriangle.setTop(160 - 2 * position.y);
    xypanTriangle.set('angle', 180 + position.pan);
    xypanTriangle.setCoords();
    xypanCanvas.renderAll();
    ztiltTriangle.setTop(130 - 10 * position.z);
    ztiltTriangle.set('angle', 90 + position.tilt);
    ztiltTriangle.setCoords();
    ztiltCanvas.renderAll();
}

function show_files(files)
{
    var list = document.getElementById("filelist");
    while (list.hasChildNodes()) {
        list.removeChild(list.firstChild);
    }
    for (var i = 0; i < files.length; i++) {
        var a = document.createElement("A");
        a.setAttribute("href", files[i].href);
        a.innerHTML = files[i].name;
        list.appendChild(a);
        list.appendChild(document.createElement("BR"));
    }
}

function stop()
{
    $.get("/lettucescan/stop");
}

function moveTo() {
    var coord = { x: parseFloat(document.getElementById("x").value),
                  y: parseFloat(document.getElementById("y").value),
                  z: parseFloat(document.getElementById("z").value),
                  pan: parseFloat(document.getElementById("pan").value),
                  tilt: parseFloat(document.getElementById("tilt").value) };
    $.post("/lettucescan/moveto", coord, function(result){
        set_position(result);
    });
}

function move(dx, dy, dz) {
    var coord = { "dx": dx, "dy": dy, "dz": dz }
    $.post("/lettucescan/move", coord, function(result){
        set_position(result);
    });
}

function circularScan()
{
    var params = { xc: parseFloat(document.getElementById("xc").value),
                   yc: parseFloat(document.getElementById("yc").value),
                   zc: parseFloat(document.getElementById("zc").value),
                   r: parseFloat(document.getElementById("r").value),
                   nc: parseInt(document.getElementById("nc").value) };
    $.post("/lettucescan/circularscan", params, function (result) {
        if (result.error) alert(result.message);
        else {
            alert("scan finished");
            set_position(result.position);
            show_files(result.files);
        }
    });
}

function squareScan()
{
    var params = { xs: parseFloat(document.getElementById("xs").value),
                   ys: parseFloat(document.getElementById("ys").value),
                   zs: parseFloat(document.getElementById("zs").value),
                   d: parseFloat(document.getElementById("d").value),
                   ns: parseInt(document.getElementById("ns").value) };
    $.post("/lettucescan/squarescan", params, function (result) {
        if (result.error) alert(result.message);
        else {
            alert("scan finished");
            set_position(result.position);
            show_files(result.files);
        }
    });
}

function homing()
{
    $.get("/lettucescan/homing");
}

function xyChangingHandler(evt)
{
    var movingObject = evt.target;
    var pt = movingObject.getCenterPoint();
    set_position2({'x': 80 - pt.x / 2,
                   'y': 80 - pt.y / 2,
                   'z': position.z,
                   'pan': position.pan,
                   'tilt': position.tilt });
};

function panChangingHandler(evt)
{
    var movingObject = evt.target;
    set_position2({'x': position.x,
                   'y': position.y,
                   'z': position.z,
                   'pan': movingObject.get('angle') - 180,
                   'tilt': position.tilt });
}

function xypanChangedHandler(evt)
{
    var movingObject = evt.target;
    var pt = movingObject.getCenterPoint();
    set_position2({'x': 80 - pt.x / 2,
                  'y': 80 - pt.y / 2,
                   'z': position.z,
                   'pan': movingObject.get('angle') - 180,
                   'tilt': position.tilt });
    moveTo();
    grabImages();
}

function zChangingHandler(evt)
{
    var movingObject = evt.target;
    var pt = movingObject.getCenterPoint();
    set_position2({'x': position.x,
                   'y': position.y,
                   'z': (130 - pt.y) / 10,
                   'pan': position.pan,
                   'tilt': position.tilt });
};

function tiltChangingHandler(evt)
{
    var movingObject = evt.target;
    set_position2({'x': position.x,
                   'y': position.y,
                   'z': position.z,
                   'pan': position.pan,
                   'tilt': movingObject.get('angle') - 90 });
}

function ztiltChangedHandler(evt)
{
    var movingObject = evt.target;
    var pt = movingObject.getCenterPoint();
    set_position2({'x': position.x,
                   'y': position.y,
                   'z': (130 - pt.y) / 10,
                   'pan': position.pan,
                   'tilt': movingObject.get('angle') - 90 });
    moveTo();
    grabImages();
}

function grabImages()
{
    $.get("/lettucescan/grab", function(result){
        document.getElementById("RGBImage").src = "/lettucescan/rgb.png?d=" + new Date().toISOString();
        document.getElementById("DepthImage").src = "/lettucescan/depth.png?d=" + new Date().toISOString();
    });
}

function initControllerButton(svg, id, dx, dy, dz)
{
    var b = svg.getElementById(id);
    b.addEventListener("mouseup",
                       function() {
                           move(dx, dy, dz);
                           grabImages(); },
                       false);
}

function initController()
{
    var a = document.getElementById("controllerImg");
    var svg = a.contentDocument;
    initControllerButton(svg, "controllerXp1", 0.1, 0, 0);
    initControllerButton(svg, "controllerXp10", 1, 0, 0);
    initControllerButton(svg, "controllerXp100", 10, 0, 0);
    initControllerButton(svg, "controllerXm1", -0.1, 0, 0);
    initControllerButton(svg, "controllerXm10", -1, 0, 0);
    initControllerButton(svg, "controllerXm100", -10, 0, 0);
    initControllerButton(svg, "controllerYp1", 0, 0.1, 0);
    initControllerButton(svg, "controllerYp10", 0, 1, 0);
    initControllerButton(svg, "controllerYp100", 0, 10, 0);
    initControllerButton(svg, "controllerYm1", 0, -0.1, 0);
    initControllerButton(svg, "controllerYm10", 0, -1, 0);
    initControllerButton(svg, "controllerYm100", 0, -10, 0);
    initControllerButton(svg, "controllerZp1", 0, 0, 0.1);
    initControllerButton(svg, "controllerZp10", 0, 0, 1);
    initControllerButton(svg, "controllerZp100", 0, 0, 10);
    initControllerButton(svg, "controllerZm1", 0, 0, -0.1);
    initControllerButton(svg, "controllerZm10", 0, 0, -1);
    initControllerButton(svg, "controllerZm100", 0, 0, -10);
}

function initApp()
{
    $('#CircularScan').on('click', circularScan);
    $('#SquareScan').on('click', squareScan);
    $('#Homing').on('click', homing);
    $('#Stop').on('click', stop);
    $('#MoveTo').on('click', moveTo);
    $('#Move').on('click', move);
    $('#Grab').on('click', grabImages);

    $('#controllerMap_z1').on('click', function() { alert("z1"); });

    //var a = document.getElementById("controllerImg");
    //a.addEventListener("load", initController, false);
    initController();
    
    $.get("/lettucescan/position", function(result){
        set_position(result);
    });
    
    xypanCanvas = new fabric.Canvas('XYPanView');
    xypanTriangle = new fabric.Triangle({
    width: 16, height: 32, fill: 'blue',
        left: 80, top: 80,
        originX: "center",
        originY: "center",
        hasBorders: true,
        hasControls: true,
        hasRotatingPoint: true
    });
    xypanTriangle.setControlsVisibility({
        mt: false,
        mb: false,
        ml: false,
        mr: false,
        tr: false,
        tl: false,
        br: false,
        bl: false
    });
    xypanCanvas.add(xypanTriangle);
    xypanCanvas.add(new fabric.Text('XY and Pan', { 
        left: 4, top: 4, hasControls: false, hasBorders: false, evented: false, fontSize: 12
    }));
    xypanCanvas.on('object:moving', xyChangingHandler);
    xypanCanvas.on('object:rotating', panChangingHandler);
    xypanCanvas.on('object:modified', xypanChangedHandler);

    ztiltCanvas = new fabric.Canvas('ZTiltView');
    ztiltTriangle = new fabric.Triangle({
    width: 16, height: 32, fill: 'blue',
        left: 20, top: 80,
        originX: "center",
        originY: "center",
        hasBorders: true,
        hasControls: true,
        hasRotatingPoint: true
    });
    ztiltTriangle.setControlsVisibility({
        mt: false,
        mb: false,
        ml: false,
        mr: false,
        tr: false,
        tl: false,
        br: false,
        bl: false
    });
    ztiltTriangle.set('angle', 90);
    ztiltCanvas.add(ztiltTriangle);
    ztiltCanvas.add(new fabric.Text('Z and Tilt', { 
        left: 4, top: 4, hasControls: false, hasBorders: false, evented: false, fontSize: 12
    }));
    ztiltCanvas.on('object:moving', zChangingHandler);
    ztiltCanvas.on('object:rotating', tiltChangingHandler);
    ztiltCanvas.on('object:modified', ztiltChangedHandler);

}

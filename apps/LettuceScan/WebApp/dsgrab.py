# dsgrab.py
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

import DepthSense as DS
import cv2
import numpy as np
import os

ds = DS.initDepthSense()
imdir = "static/img"

def grab_images():
    im = DS.getColourMap()
    cv2.imwrite("%s/rgb.png"%(imdir), im)   
    
    im = DS.getDepthMap()
    cv2.imwrite("%s/depth.png"%(imdir), im)   

    im = DS.getConfidenceMap()
    cv2.imwrite("%s/confidence.png"%(imdir), im)   
    
    im = DS.getDepthColouredMap()
    cv2.imwrite("%s/rgbd.png"%(imdir), im)   
    
    im = DS.getGreyScaleMap()
    cv2.imwrite("%s/gscale.png"%(imdir), im)   
    
    im = DS.getSyncMap()
    np.save("%s/sync"%(imdir), im)   
    
    im = DS.getUVMap()
    np.save("%s/uv"%(imdir), im)   
    
    im = DS.getVertices()
    np.save("%s/vert"%(imdir), im)   
    return

grab_images()

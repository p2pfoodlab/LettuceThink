"""
    Copyright 2016-2017 Sony Computer Science Laboratories 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import lettucehoe as lh

fname="data/pics/OH.jpg"
im=lh.cv2.imread(fname)

#Workspace parameters [x0, y0, dx, dy]
ws_par=[970, 140, 700,500]
tool_size=50

omask=lh.plantmask(im, ws_par, tool_size)
toolPath=lh.mod_boustrophedon(omask, im, tool_size, ws_par)
lh.np.savetxt("data/toolPath.txt", toolPath)

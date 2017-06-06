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

    Modified boustrophedon path for the tool to cover ground around segmented plants
"""

import cv2
import numpy as np

def exgreen(im_BGR):
   Ms=np.max(im_BGR,axis=(0,1)).astype(np.float) 
   im_Norm=im_BGR/Ms
   L=im_Norm.sum(axis=2)
   return 3*im_Norm[:,:,1]/L-1

def plantcont(plants_mask, svg, bg=0):
   im,c,h=cv2.findContours(plants_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
   cont=[np.vstack([ci[:,0],ci[:,0][0]]) for ci in c if (len(ci)>10)]
   return cont

def plantmask(im, ts, bilf=[11, 5, 17], morpho_it=[5,5]):
   cidx=np.nan_to_num(exgreen(im))
   M=cidx.max()
   m=cidx.min()
   
   cidx= (255*(cidx-m)/(M-m)).astype(np.uint8)
   cidx=cv2.bilateralFilter(cidx, bilf[0], bilf[1], bilf[2])
   th, mask=cv2.threshold(cidx,0,255,cv2.THRESH_OTSU)
   kr=np.ones((3,3)).astype(np.uint8)
   kr[[0,0,2,2],[0,2,2,0]]=0

   omask=cv2.morphologyEx(mask, cv2.MORPH_OPEN, kr, iterations=morpho_it[0])
   omask=cv2.dilate(omask,kernel=kr,iterations=morpho_it[1])
   
   d=cv2.DIST_MASK_PRECISE
   dist=cv2.distanceTransform(255-(omask.astype(np.uint8)), cv2.DIST_L2, d)
   omask=255*(1-(dist>ts/2)).astype(np.uint8)
   return omask

def fillNpoints(xy,Np):
   ts=np.linspace(0,len(xy[0]),num=len(xy[0]),endpoint=True)
   nts=np.linspace(0,len(xy[0]),num=Np,endpoint=True)
   fx = np.interp(nts,ts, xy[0])
   fy = np.interp(nts,ts, xy[1])
   return np.array([fx,fy])

def point_line_distance(point, start, end):
    if (start == end).all():
        return np.linalg.norm(point-start)
    else:
        n = np.linalg.norm(np.linalg.det([end - start, start - point]))
        d = np.linalg.norm(end-start)
        return n/d

def rdp(points, epsilon):
    """
    Cartographic generalization is achieved with the Ramer-Douglas-Peucker algorithm
    pseudo-code: http://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm
    python port: http://github.com/sebleier/RDP
    """
    dmax = 0.0
    index = -1
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d
    if dmax >= epsilon:
        res1 = rdp(points[:index+1], epsilon)
        res2 = rdp(points[index:], epsilon)
        return np.vstack([res1[:-1],res2])
    else:
        return np.vstack([points[0], points[-1]])

def plain_boustrophedon(Ns, dx, dy, x0, y0):
    x=[x0]
    y=[y0]
    for i in range(Ns/2):
       x.append(x[-1]+dx)
       y.append(y[-1])
       x.append(x[-1])
       y.append(y[-1]+dy)
       x.append(x[-1]-dx)
       y.append(y[-1])
       if (i!=Ns/2-1): 
          x.append(x[-1])
          y.append(y[-1]+dy)
    return np.array([x,y])

def corrected_path(pi,po,tr,Nfp=200):
   """
   Substitute path passing through plants by shortest contour connecting i/o points 
   """
   longtr=fillNpoints(tr.T,Nfp) 
   pi_idx=((pi[:,np.newaxis]-longtr)**2).sum(axis=0).argmin()
   po_idx=((po[:,np.newaxis]-longtr)**2).sum(axis=0).argmin()

   if (pi_idx<po_idx):
      p1=longtr[:,pi_idx:po_idx]
      p2=longtr.take(range(-(Nfp-po_idx),pi_idx),axis=1,mode="wrap")[:,::-1]
   else:
      p1=longtr[:,::-1][:,Nfp-pi_idx:Nfp-po_idx]
      p2=longtr.take(range(-(Nfp-pi_idx),po_idx),axis=1,mode="wrap")

   d1=(np.diff(p1,axis=1)**2).sum()
   d2=(np.diff(p2,axis=1)**2).sum()
   if (d1<=d2): return p1
   else: return p2

def mod_boustrophedon(omask, ts, ws_par, eps_contours=1, eps_toolpath=1, Nfp=5000):
   #Compute boustrophedon ignoring the plants and transform to workspace coordinates
   boustro=plain_boustrophedon(ws_par[3]/ts+1, ws_par[2], ts, ts/2., ts/2.)
   boustro[0]*=-1
   boustro[0]+=omask.shape[1]

   #Detect i/o points of paths passing through plants
   dense_boustro=fillNpoints(boustro,Nfp)
   pval=omask[(dense_boustro[1]).astype(int),(dense_boustro[0]).astype(int)]

   if pval[0]: 
      fpath=np.where(pval==0)[0]  
      dense_boustro=dense_boustro[:,fpath[0]:]
      pval=pval[fpath[0]:]
   if pval[-1]: 
      fpath=np.where(pval==0)[0]  
      dense_boustro=dense_boustro[:,:fpath[-1]]
      pval=pval[:fpath[-1]]

   idxs=np.where(np.diff(pval)>0)[0]
   io_points=dense_boustro[:,idxs]

   #extract, downsample and compute center of plant contours 
   conts=plantcont(omask.copy(), {})
   s_tr=[]
   trc=[]

   for tri in conts:
      s_tr.append(rdp(tri, eps_contours))
      if len(trc): trc=np.vstack([trc,s_tr[-1].mean(axis=0)])
      else: trc=s_tr[-1].mean(axis=0)

   #Generate the mofified boustrophedon
   toolPath=np.array([dense_boustro[:,0]]).T
   toolPath=np.hstack([toolPath,dense_boustro[:,:idxs[0]]])
   for k in range(len(io_points[0])/2):
      pi=io_points[:,2*k]   #in point
      po=io_points[:,2*k+1] #out point
      plant=((.5*(pi+po)-trc)**2).sum(axis=1).argmin() #plant attached to i/o points
      cor_path=corrected_path(pi,po,s_tr[plant])      
      toolPath=np.hstack([toolPath,cor_path])
      if k<(len(io_points[0])/2-1): toolPath=np.hstack([toolPath,dense_boustro[:,idxs[2*k+1]:idxs[2*k+2]]])
   toolPath=np.hstack([toolPath,dense_boustro[:,idxs[2*k+1]:]])
   toolPath=rdp(toolPath.T, 1)
   return toolPath.T

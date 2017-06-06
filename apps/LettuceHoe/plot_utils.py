import cv2
import numpy as np

def corners(im, Cmask, path="./", alpha=.5):
   res=im.copy()
   cv2.addWeighted(cv2.merge((Cmask,Cmask,Cmask)), alpha, res, 1 - alpha, 0, res)
   cv2.imwrite(path+"cmask.jpg",res)

def workspace(im, c0, dx, dy, path="./", margin=0.05):
   imc=im.copy()
   cv2.rectangle(imc,(int(c0[1]+margin*dx),int(c0[0]+margin*dy)),(int(c0[1]+(1-margin)*dx),int(c0[0]+(1-margin)*dy)),(0,128,0),3)
   cv2.circle(imc, (int(c0[1]),int(c0[0])), 15, (255,0,0), 2)
   cv2.circle(imc, (int(c0[1]+dx),int(c0[0])), 15, (0,255,0), 2)
   cv2.circle(imc, (int(c0[1]),int(c0[0]+dy)), 15, (0,0,255), 2)
   cv2.circle(imc, (int(c0[1]+dx),int(c0[0]+dy)), 15, (255,255,255), 2)
   cv2.imwrite(path+"corners.jpg",imc)
   return imc

def plant_mask(imc, Pmask, c0, dx, dy, path="./", margin=0.05, alpha=.5):
   mP=np.zeros_like(imc)
   mP[c0[0]+margin*dy:c0[0]+(1-margin)*dy,c0[1]+margin*dx:c0[1]+(1-margin)*dx]=Pmask[:,:,np.newaxis]
   res=imc.copy()
   imP=cv2.addWeighted(mP, alpha, res, 1 - alpha, 0, res)
   cv2.imwrite(path+"pmask.jpg",imP)
   return res

def tpath(res, stp, c0, dx, dy, path="./", margin=0.05):
   pim=res[c0[0]+margin*dy:c0[0]+(1-margin)*dy,c0[1]+margin*dx:c0[1]+(1-margin)*dx]
   cv2.polylines(pim,[stp],False,[145,235,229],8)

   res[c0[0]+margin*dy:c0[0]+(1-margin)*dy,c0[1]+margin*dx:c0[1]+(1-margin)*dx]=pim
   cv2.imwrite(path+"tpath.jpg", res)      


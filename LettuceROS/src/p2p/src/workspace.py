import numpy as np
import cv2

def getWS(im):
   exR= getExR(im)
   idxs=np.array(np.where(exR>90)).T.astype(np.float32)
   term_crit = (cv2.TERM_CRITERIA_EPS, 30, 0.1)
   ret, labels, centers = cv2.kmeans(idxs, 4, None, term_crit, 10, 0)
   idxs=np.lexsort(centers.T.astype(np.int)/100)
   centers=centers[idxs]
   c_NW=centers[0]
   c_SW=centers[1]
   c_SE=centers[2]
   c_NE=centers[3]
   dx=.5*(c_NE[1]-c_NW[1])+0.5*(c_NE[1]-c_NW[1])
   dy=.5*(c_SW[0]-c_NW[0])+.5*(c_SW[0]-c_NW[0])
   return centers[:4], dx, dy

def getCMask(im, th=None,morpho_it=[5,5]):
   exR= getExR(im)
   if not(th): th=np.mean(exR)+5*np.std(exR)
   mask=255*(exR>th).astype(np.uint8)
   kr=np.ones((3,3)).astype(np.uint8)
   kr[[0,0,2,2],[0,2,2,0]]=0
   omask=cv2.morphologyEx(mask, cv2.MORPH_OPEN, kr, iterations=morpho_it[0])
   mask=cv2.dilate(omask,kernel=kr,iterations=morpho_it[1])
   return mask

def getCorners(im, th=None,morpho_it=[5,5]):
  mask=getCMask(im, th=None,morpho_it=[5,5])
  ret,l=cv2.connectedComponents(mask)
  K=len(np.unique(l))-1
  print K," corners found"

  idxs=np.array(np.where(mask)).T.astype(np.float32)
  term_crit = (cv2.TERM_CRITERIA_EPS, 30, 0.1)
  ret, labels, centers = cv2.kmeans(idxs, K, None, term_crit, 10, 0)

  if (len(centers)==3):
     print "completing to 4"
     k=np.argmin([np.linalg.norm(centers[0]-centers[1]), np.linalg.norm(centers[1]-centers[2]), np.linalg.norm(centers[2]-centers[0])])
     csup=np.array([centers[(k+2)%3]+(centers[k]-centers[(k+1)%3]), centers[(k+2)%3]-(centers[k]-centers[(k+1)%3])])
     l=np.argmin([np.linalg.norm(centers[k]-csup, axis=1)])
     centers=np.vstack([centers,csup[l]])

  idxs=np.lexsort(np.round(centers[:,::-1].T.astype(np.int)/100.,0))
  corners=centers[idxs]

  if (len(corners)==4):
     cN=corners[:2].copy()
     cN.sort(axis=0)
     cS=corners[2:].copy()
     cS.sort(axis=0)
     c0=[.5*(cN[1,0]+cN[0,0]),.5*(cN[0,1]+cS[0,1])]
     dx=.5*(cN[1,1]-cN[0,1])+0.5*(cS[1,1]-cS[0,1])
     dy=.5*(cS[0,0]-cN[0,0])+.5*(cS[1,0]-cN[1,0])

  if (len(corners)==6):
     cN=corners[:3].copy()
     cN.sort(axis=0)
     cS=corners[3:].copy()
     cS.sort(axis=0)
     outlier=np.argmin(np.diff(cN[:,1]))

     if outlier==1:
        c0=[.5*(cN[1,0]+cN[0,0]),.5*(cN[0,1]+cS[0,1])]
        dx=.5*(cN[1,1]-cN[0,1])+0.5*(cS[1,1]-cS[0,1])
        dy=.5*(cS[0,0]-cN[0,0])+.5*(cS[1,0]-cN[1,0])

     if outlier==0:
        c0=[.5*(cN[2,0]+cN[1,0]),.5*(cN[1,1]+cS[1,1])]
        dx=.5*(cN[2,1]-cN[1,1])+0.5*(cS[2,1]-cS[1,1])
        dy=.5*(cS[1,0]-cN[1,0])+.5*(cS[2,0]-cN[2,0])
  return c0,dx,dy, mask

def getExR(im_BGR):
   return 1.3*im_BGR[:,:,2]-im_BGR[:,:,1]



import os
import sys
from CeleryPy import log
from CeleryPy import send_message
from DB import DB
from Image import Image
import json
from Parameters import Parameters
import requests
import cv2
from Capture import Capture
import numpy as np
from PlantDetection import PlantDetection
from farmware_tools import device
import CeleryPy

def create_mask(image,lowergreen,uppergreen):##función para crear máscara a partir de valores máximos y minimos de HSV
  imghsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV_FULL)
  mask=cv2.inRange(imghsv,lowergreen,uppergreen)
  return mask
def colorize(image):##función para cambiar el brillo y el contraste de imagen
 n_image = np.zeros(image.shape, image.dtype)
 alpha=2.4
 beta=-280
 n_image = np.clip(np.multiply(alpha,image)+beta, 0, 255)
 return n_image.astype(np.uint8) 
def invert(img):
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = 255-img
    img2 = cv2.medianBlur(img2,17)
    return img2
def array_shape(selected):
    a=sorted(selected,key=lambda x:x[0])
    rows=[]
    counter=0
    print(len(a))
    for i in range(len(a)-1):
        if abs(a[i][0]-a[i+1][0])<30:
            counter+=1
        else:
            counter += 1
            rows.append(counter)
            counter=0
    counter = 0
    b=sorted(selected,key=lambda x:x[1])
    cols=[]
    for i in range(len(a)-1):
        if abs(b[i][1]-b[i+1][1])<30:
            counter+=1
        else:
            counter += 1
            cols.append(counter)
            counter=0
    print(rows)
    print(cols)
    rows=int(np.mean(rows))
    cols=int(np.mean(cols))
    return rows,cols
  
def fill_array(matrix,list):
    sortedlistx=sorted(list,key=lambda x:x[0])
    rows=matrix.shape[0]
    cols=matrix.shape[1]
    for i in range(cols):
        sortedlisti=sortedlistx[i*rows:(i+1)*rows]
        sortedlistij=sorted(sortedlisti, key=lambda x: x[1])
        for j in range(rows):
            print(sortedlistij[j])
            matrix[j,i]=sortedlistij[j]
    return matrix
def mergearrays(matrix1,matrix2):
    res_matrix=matrix1
    row2=matrix2[0,:,:]
    for i in range(matrix1.shape[0]):
        row1=matrix1[i,:,:]
        res=sum(abs(row2[0]-row1[0])+abs(row2[1]-row1[1]))/row1.shape[0]
        log(str(res))
        if res<4 :
            subindex=i
            break
    counter=matrix1.shape[0]-subindex
    log(str(counter))
    res_matrix=np.concatenate((res_matrix[:,:,:],matrix2[counter:,:,:]),axis=0)
    log(str(res_matrix.shape))
    return res_matrix
      
#######________________SEGUNDA MATRIZ___________________________________-####################################
########SETEAMOS VALORES MÍNIMOS Y MÁXIMOS DE HSV##################
HL=52
SL=95
VL=50
HH=110
SH=255
VH=255
###################################################################
CeleryPy.move_absolute((845,290,0),(0,0,0),150)
CeleryPy.wait(5000)
file=Capture().capture()
img2 = cv2.imread(file,1)
image_gray=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
circles=cv2.HoughCircles(image_gray,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=15,maxRadius=34)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
 cv2.circle(img2,(i[0],i[1]),15,(0,255,0),cv2.FILLED)
new_image=img2
cv2.imwrite('/tmp/images/1549138022.jpg',new_image)
mask=create_mask(new_image,np.array([HL,SL,VL]),np.array([HH,SH,VH]))###Creamos la máscara
image3=cv2.bitwise_and(new_image,new_image,mask=mask)##aplicamos la máscara
image3=cv2.medianBlur(image3,5)
cv2.imwrite('/tmp/images/1549138027.jpg',image3)

PD = PlantDetection(
             image='/tmp/images/1549138027.jpg',
             blur=2, morph=2, iterations=3, from_env_var=True, coordinates=True,
             array=[{"size": 5, "kernel": 'ellipse', "type": 'erode', "iters": 1}],
             HSV_min=[49,95,50],HSV_max=[110,255,255]
             )
PD.detect_plants() # detect coordinates and sizes of weeds and plants
if len(PD.plant_db.coordinate_locations) >= 1:
  holes=[]
  for coordinate_location in PD.plant_db.coordinate_locations:
    if 19>coordinate_location[2]>7 and coordinate_location[0]<950:
     holes.append([coordinate_location[0],coordinate_location[1]])  
  rows,cols=array_shape(holes)
  matrix10=np.zeros((rows,cols,2))
  matrix10=fill_array(matrix10,holes) 
  matrix10=matrix10[:,0:6,:]
  log(str(matrix10.shape))

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
import time

#x=DB()
#y=x.get_image(95)
device.set_pin_io_mode(1,4)
weeder=(20,553,-402)
CeleryPy.move_absolute((500,440,0),(0,0,0),150)
#send_message(message=str(os.environ), message_type='success', channel='toast')
file=Capture().capture()
start=time.time()
img2 = cv2.imread(file,1)
def create_mask(image,lowergreen,uppergreen):##función para crear máscara a partir de valores máximos y minimos de HSV
  imghsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV_FULL)
  mask=cv2.inRange(imghsv,lowergreen,uppergreen)
  return mask
def normalize(array):
    b, g, r = cv2.split(array)
    minimum=np.min(b)
    maximum=np.max(b)
    b_n=np.clip((b-minimum)*(255/maximum),0,255).astype(np.uint8)
    minimum=np.min(g)
    maximum=np.max(g)
    g_n=np.clip((g-minimum)*(255/maximum),0,255).astype(np.uint8)
    minimum=np.min(r)
    maximum=np.max(r)
    r_n=np.clip((r-minimum)*(255/maximum),0,255).astype(np.uint8)
    array=cv2.merge([b_n, g_n, r_n])
    return array
def colorize(image,alpha,beta,theta):##función para cambiar el brillo y el contraste de imagen
   #alpha = 1.32
   #beta=60
   #theta=1.8
   n_image = alpha**(image/beta+theta)#+theta
   n_image=normalize(n_image)
   b,g,r=cv2.split(n_image)
   kernel=(1/16)*np.ones([4,4],dtype=np.uint8)
   b_n=cv2.filter2D(b,-1,kernel)
   g_n=cv2.filter2D(g,-1,kernel)
   r_n=cv2.filter2D(r,-1,kernel)
   f=0.6
   B=b-f*b_n
   G=g-f*g_n
   R=r-f*r_n
   n_image=cv2.merge([B,G,R])+20
   return n_image.astype(np.uint8)
def invert(imagem):
 imagem = (255-imagem)
 return imagem


new_image=colorize(img2)##obtenemos imagen con brillo y contraste modificados
cv2.imwrite('/tmp/images/1549138022.jpg',new_image)
kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4))
mask = create_mask(new_image, np.array([45, 85, 50]), np.array([90, 255, 255]))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
mask = cv2.dilate(mask,kernel,iterations=2)
image3=cv2.bitwise_and(new_image,new_image,mask=mask)##aplicamos la máscara
image3=cv2.medianBlur(image3,5)
cv2.imwrite('/tmp/images/1549138027.jpg',image3)

PD = PlantDetection(
            image='/tmp/images/1549138027.jpg',
            blur=0, morph=2, iterations=1, from_env_var=True, coordinates=True,
            array=[{"size": 3, "kernel": 'ellipse', "type": 'dilate',  "iters": 3},
                   {"size": 3, "kernel": 'ellipse', "type": 'erode', "iters": 3}],
            HSV_min=[50,65,45],HSV_max=[90,255,255]
            )
PD.detect_plants()

if len(PD.plant_db.coordinate_locations) >= 1:
  #O=len(PD.plant_db.coordinate_locations)
  dir_path='/root/farmware'
  matrix=np.load(dir_path+'/'+'array.npy')
  matrix2=np.load(dir_path+'/'+'array2.npy')
  matrix3=np.load(dir_path+'/'+'array3.npy')
  matrix4=np.load(dir_path+'/'+'array4.npy')
  for coordinate_location in PD.plant_db.coordinate_locations:
        log("Plant detected at X = {:5.0f} mm, Y = {:5.0f} mm with R = {:.1f} mm".format(
                    coordinate_location[0],
                    coordinate_location[1],
                    coordinate_location[2]))
  send_message(message='TUDO BEM', message_type='success', channel='toast')
  CeleryPy.move_absolute(weeder,(0,0,0),150)
  CeleryPy.move_absolute(weeder,(100,0,0),150)
  CeleryPy.move_absolute(weeder,(100,0,100),150)
  CeleryPy.move_absolute(weeder,(100,0,200),150)
  CeleryPy.write_pin(number=4, value=1, mode=0)
  CeleryPy.wait(100)
  CeleryPy.write_pin(number=4, value=0, mode=0)
  CeleryPy.wait(200)
  CeleryPy.write_pin(number=4, value=1, mode=0)
  
  for i,coordinate_location in enumerate(PD.plant_db.coordinate_locations):
    if coordinate_location[2] > 13.5:
          aux=np.abs(coordinate_location[0]-matrix[:,:,0])+np.abs(coordinate_location[1]-matrix[:,:,1])
          (min,_,minloc,_)=cv2.minMaxLoc(aux,None)
          log(str(min))
          xmat=minloc[0]
          ymat=minloc[1]
          xmatsig=int(np.clip(i%2,0,10))
          ymatsig=int(np.clip((i-xmatsig)/2,0,10))
          x,y=matrix[ymat,xmat]
          if i%3==0:
            xsig,ysig=matrix2[ymatsig,xmatsig]
            xsig=xsig-7
            ysig=ysig+7
          elif i%3==1:
            xsig,ysig=matrix3[ymatsig,xmatsig]
            xsig=xsig-7
            ysig=ysig+7
          elif i%3==2:
            xsig,ysig=matrix4[ymatsig,xmatsig]
            xsig=xsig-7
            ysig=ysig+7 
          x=x-7
          y=y+7
          CeleryPy.move_absolute((x,y,-205),(0,0,0),100)
          CeleryPy.move_absolute((x,y,-282),(0,0,0),100)
          CeleryPy.wait(500)
          CeleryPy.write_pin(number=4, value=0, mode=0)
          CeleryPy.wait(2000)
          CeleryPy.move_absolute((x,y,-215),(0,0,0),100)
          CeleryPy.wait(500)
          CeleryPy.move_absolute((xsig,ysig,-200),(0,0,0),100)
          CeleryPy.move_absolute((xsig,ysig,-278),(0,0,0),100)
          CeleryPy.write_pin(number=4, value=1, mode=0)
          CeleryPy.wait(400)
          CeleryPy.write_pin(number=4, value=0, mode=0)
          CeleryPy.wait(400)
          CeleryPy.write_pin(number=4, value=1, mode=0)
          CeleryPy.wait(400)
          CeleryPy.write_pin(number=4, value=0, mode=0)
          CeleryPy.wait(400)
          CeleryPy.write_pin(number=4, value=1, mode=0)
          CeleryPy.move_absolute((xsig,ysig,-205),(0,0,0),100)
          CeleryPy.write_pin(number=4, value=0, mode=0)
          CeleryPy.wait(200)
          CeleryPy.write_pin(number=4, value=1, mode=0)
          CeleryPy.wait(200)
          CeleryPy.write_pin(number=4, value=0, mode=0)
          CeleryPy.wait(200)
          CeleryPy.write_pin(number=4, value=1, mode=0)
          CeleryPy.wait(500)
  CeleryPy.move_absolute(weeder,(120,0,200),150)
  CeleryPy.move_absolute(weeder,(120,0,0),150)
  CeleryPy.move_absolute(weeder,(0,0,0),150)
  CeleryPy.move_absolute(weeder,(0,0,200),150)
if len(PD.plant_db.coordinate_locations) == 0:
  send_message(message='NINGUN PLANTIN DETECTADO', message_type='error', channel='toast')
CeleryPy.move_absolute((0,0,0),(0,0,0),250)
  #CeleryPy.move_absolute((500,500,0),(0,0,0),100)
  #CeleryPy.move_absolute((0,0,0),(0,0,0),100)







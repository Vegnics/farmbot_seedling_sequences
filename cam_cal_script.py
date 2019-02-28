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

#x=DB()
#y=x.get_image(95)
device.set_pin_io_mode(1,4)
weeder=(20,553,-402)
CeleryPy.move_absolute((500,500,0),(0,0,0),150)
#send_message(message=str(os.environ), message_type='success', channel='toast')
file=Capture().capture()
print(file)
img2 = cv2.imread(file,1)
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
def invert(imagem):
 imagem = (255-imagem)
 return imagem


new_image=colorize(img2)##obtenemos imagen con brillo y contraste modificados
cv2.imwrite('/tmp/images/1549138022.jpg',new_image)
########SETEAMOS VALORES MÍNIMOS Y MÁXIMOS DE HSV##################
HL=52
SL=95
VL=50
HH=110
SH=255
VH=255
###################################################################
mask=create_mask(new_image,np.array([HL,SL,VL]),np.array([HH,SH,VH]))###Creamos la máscara
image3=cv2.bitwise_and(new_image,new_image,mask=mask)##aplicamos la máscara
image3=cv2.medianBlur(image3,5)
cv2.imwrite('/tmp/images/1549138027.jpg',image3)

PD = PlantDetection(
            image='/tmp/images/1549138027.jpg',
            blur=5, morph=2, iterations=5, from_env_var=True, coordinates=True,
            array=[{"size": 3, "kernel": 'ellipse', "type": 'dilate',  "iters": 3},
                   {"size": 5, "kernel": 'ellipse', "type": 'erode', "iters": 3}],
            HSV_min=[49,95,50],HSV_max=[110,255,255]
            )
PD.detect_plants() # detect coordinates and sizes of weeds and plants
if len(PD.plant_db.coordinate_locations) >= 1:
  dir_path='/root/farmware'
  matrix=np.load(dir_path+'/'+'array.npy')
  for coordinate_location in PD.plant_db.coordinate_locations:
        log("Plant detected at X = {:5.0f} mm, Y = {:5.0f} mm with R = {:.1f} mm".format(
                    coordinate_location[0],
                    coordinate_location[1],
                    coordinate_location[2]))
  send_message(message='TUDO BEM', message_type='success', channel='toast')
#CeleryPy.move_absolute((500,500,-400),(0,0,0),100)
  CeleryPy.move_absolute(weeder,(0,0,0),150)
  CeleryPy.move_absolute(weeder,(100,0,0),150)
  CeleryPy.move_absolute(weeder,(100,0,100),150)
  CeleryPy.move_absolute(weeder,(100,0,200),150)
  CeleryPy.write_pin(number=4, value=0, mode=0)
  for coordinate_location in PD.plant_db.coordinate_locations:
    if coordinate_location[2] > 14:
          aux=abs(coordinate_location[0]-matrix[:,:,0])+abs(coordinate_location[1]-matrix[:,:,1])
          _,_,minloc,_=cv2.minMaxLoc(aux,None)
          x,y=matrix[minloc]
          CeleryPy.move_absolute((x,y,-235),(0,0,0),100)
          CeleryPy.move_absolute((x,y,-276),(0,0,0),100)
          #CeleryPy.wait(500)
          CeleryPy.write_pin(number=4, value=1, mode=0)
          CeleryPy.wait(500)
          CeleryPy.move_absolute((x,y,-180),(0,0,0),100)
          CeleryPy.wait(500)
          CeleryPy.move_absolute((x+300,y,-180),(0,0,0),200)
          CeleryPy.move_absolute((x+300,y,-235),(0,0,0),200)
          CeleryPy.wait(500)
          CeleryPy.write_pin(number=4, value=0, mode=0)
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







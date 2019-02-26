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

CeleryPy.move_absolute((500,450,0),(0,0,0),150)
file=Capture().capture()
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
def circles(template):
  selected = []
  template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
  template_gray = cv2.adaptiveThreshold(template_gray, 128, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 111, 2)
  board=np.zeros(template_gray.shape)
  cv2.circle(board,(200,200),30,255,2)
  _,circle, hie = cv2.findContours(board.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
  _,contours, hie = cv2.findContours(template_gray.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
  for i in range(len(contours)):
      a=cv2.matchShapes(contours[i],circle[1],cv2.CONTOURS_MATCH_I2,0)
      (x, y), r = cv2.minEnclosingCircle(contours[i])
      print(a)
      if 10<r<30 and a<0.14:
          selected.append([x, y, r])
          cv2.circle(template,(int(x),int(y)),int(r),(0,255,0),cv2.FILLED)
  return 

circles(img2)##obtenemos circulos
new_image=img2
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
            blur=1, morph=1, iterations=1, from_env_var=True, coordinates=True,
            array=[{"size": 5, "kernel": 'ellipse', "type": 'erode', "iters": 4}],
            HSV_min=[49,95,50],HSV_max=[110,255,255]
            )
PD.detect_plants() # detect coordinates and sizes of weeds and plants
if len(PD.plant_db.coordinate_locations) >= 1:
  for coordinate_location in PD.plant_db.coordinate_locations:
        log("Plant detected at X = {:5.0f} mm, Y = {:5.0f} mm with R = {:.1f} mm".format(
                    coordinate_location[0],
                    coordinate_location[1],
                    coordinate_location[2]))
  send_message(message='TUDO BEM', message_type='success', channel='toast')
  #for coordinate_location in PD.plant_db.coordinate_locations:
  #     x=coordinate_location[0]
  #     y=coordinate_location[1]
   #    CeleryPy.move_absolute((x,y,-435),(0,0,0),100)
    #   CeleryPy.wait(500)
if len(PD.plant_db.coordinate_locations) == 0:
  send_message(message='NO HOLES', message_type='error', channel='toast')
#CeleryPy.move_absolute((0,0,0),(0,0,0),250)
  #CeleryPy.move_absolute((500,500,0),(0,0,0),100)
#CeleryPy.move_absolute((0,0,0),(0,0,0),100)


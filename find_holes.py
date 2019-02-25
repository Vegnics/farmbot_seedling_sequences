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

CeleryPy.move_absolute((500,500,0),(0,0,0),150)
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
  _, contours, _ = cv2.findContours(template_gray.astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
  for i in range(len(contours)):
      (x, y), r = cv2.minEnclosingCircle(contours[i])
      if 25< r < 40:
          selected.append([x, y, r])
          cv2.circle(template,(int(x),int(y)),int(r),(0,255,0),cv2.FILLED)
  return 

circles(img2)##obtenemos circulos
new_image=img2
cv2.imwrite('/tmp/images/1549138022.jpg',new_image)



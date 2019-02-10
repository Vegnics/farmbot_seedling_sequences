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

#x=DB()
#y=x.get_image(95)
file=Capture().capture()
print(file)
img2 = cv2.imread(file,1)
def create_mask(image,lowergreen,uppergreen):##función para crear máscara a partir de valores máximos y minimos de HSV
  imghsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV_FULL)
  mask=cv2.inRange(imghsv,lowergreen,uppergreen)
  return mask
def colorize(image):##función para cambiar el brillo y el contraste de imagen
 n_image = np.zeros(image.shape, image.dtype)
 alpha=2.3
 beta=-135
 for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        for c in range(image.shape[2]):
             n_image[y, x, c] = np.clip(np.multiply(alpha,image[y, x, c])+beta, 0, 255)
 return n_image

new_image=colorize(img2)##obtenemos imagen con brillo y contraste modificados
cv2.imwrite('/tmp/images/1549138022.jpg',new_image)
########SETEAMOS VALORES MÍNIMOS Y MÁXIMOS DE HSV##################
HL=80
SL=85
VL=10
HH=160
SH=255
VH=255
###################################################################
mask=create_mask(new_image,np.array([HL,SL,VL]),np.array([HH,SH,VH]))###Creamos la máscara
image3=cv2.bitwise_and(new_image,new_image,mask=mask)##aplicamos la máscara
image3=cv2.medianBlur(image3,7)
cv2.imwrite('/tmp/images/1549138027.jpg',image3)
send_message(message='TUDO BEM', message_type='success', channel='toast')





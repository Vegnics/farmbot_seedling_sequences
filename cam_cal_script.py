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
from subprocess import call
import numpy as np

#x=DB()
#y=x.get_image(52)
#parms=Parameters()
#z=Image(parms,x)
#z.load(y)
#print(cv2.__version__)
img2 = cv2.imread('/tmp/images/1549133011.jpg',1)
print(img2)
def create_mask(image,lowergreen,uppergreen):##función para crear máscara a partir de valores máximos y minimos de HSV
  imghsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV_FULL)
  mask=cv2.inRange(imghsv,lowergreen,uppergreen)
  return mask
def integrate(hist,bounds):#función para integrar un histograma
    aux=0
    for i in range(bounds[0],bounds[1]+1,1):
        aux=aux+hist[i]
    return aux
def colorize(image):##función para cambiar el brillo y el contraste de imagen
 n_image = np.zeros(image.shape, image.dtype)
 image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 histo = cv2.calcHist([image_gray], [0], None, [256], [0, 256])
 histo_itg=integrate(histo,[249,255])
 print(histo_itg)
 alpha=2.21046+(2.519272e-06)*histo_itg
 beta=-155+-0.001259636217060513*histo_itg
 for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        for c in range(image.shape[2]):
            n_image[y, x, c] = np.clip(np.multiply(alpha,image[y, x, c])+beta, 0, 255)
 return n_image

new_image=colorize(img2)##obtenemos imagen con brillo y contraste modificados
########SETEAMOS VALORES MÍNIMOS Y MÁXIMOS DE HSV##################
HL=51
SL=90
VL=140
HH=112
SH=255
VH=255
###################################################################
mask=create_mask(new_image,np.array([HL,SL,VL]),np.array([HH,SH,VH]))###Creamos la máscara
image3=cv2.bitwise_and(new_image,new_image,mask=mask)##aplicamos la máscara
image3=cv2.medianBlur(image3,7)
send_message(message=str(cv2.__version__), message_type='success', channel='toast')





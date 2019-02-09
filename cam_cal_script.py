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
img2 = cv2.imread('/tmp/images/1549669210.jpg',1)
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
 alpha=2.21046+(2.519272e-06)*histo_itg
 beta=-155+-0.001259636217060513*histo_itg
 for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        for c in range(image.shape[2]):
            n_image[y, x, c] = np.clip(np.multiply(alpha,image[y, x, c])+beta, 0, 255)
 return n_image

send_message(message='Hello World!', message_type='success', channel='toast')





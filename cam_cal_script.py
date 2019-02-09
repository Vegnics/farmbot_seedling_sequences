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

send_message(message='Hello World!', message_type='success', channel='toast')





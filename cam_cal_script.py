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
img1 = cv2.imread('/tmp/images/1549133011.jpg',1)
img2=cv2.resize(img1,(640,480),interpolation = cv2.INTER_AREA)

send_message(message=str(cv2.__version__), message_type='success', channel='toast')





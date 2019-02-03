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

x=DB()
y=x.get_image(52)
parms=Parameters()
z=Image(parms,x)
z.load(y)
#print(cv2.__version__)
#img = cv2.imread(y,0)
print(str(img))
print(sys.version)
#cv2.imshow('image',img)
#z.show()
retcode = call(
["raspistill", "-w", "640", "-h", "480", "-o", y])
#help(cv2.imshow)


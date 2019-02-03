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

x=DB()
y=x.get_image(52)
parms=Parameters()
z=Image(parms,x)
z.load(y)
print(cv2.__version__)
img = cv2.imread(y,0)
print(str(img))
#cv2.imshow('image',img)
#z.show()
help(cv2)


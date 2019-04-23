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
import time

#x=DB()
#y=x.get_image(95)
device.set_pin_io_mode(1,4)
weeder=(20,553,-402)
CeleryPy.move_absolute((500,500,0),(0,0,0),150)
dir_path='/root/farmware'
matrix=np.load(dir_path+'/'+'array.npy')
matrix2=np.load(dir_path+'/'+'array2.npy')
matrix3=np.load(dir_path+'/'+'array3.npy')
matrix4=np.load(dir_path+'/'+'array4.npy')
CeleryPy.move_absolute(weeder,(0,0,0),150)
CeleryPy.move_absolute(weeder,(100,0,0),150)
CeleryPy.move_absolute(weeder,(100,0,100),150)
CeleryPy.move_absolute(weeder,(100,0,200),150)
CeleryPy.write_pin(number=4, value=1, mode=0)
CeleryPy.wait(100)
CeleryPy.write_pin(number=4, value=0, mode=0)
CeleryPy.wait(200)
CeleryPy.write_pin(number=4, value=1, mode=0)
 
x,y=matrix[0,1]
xsig,ysig=matrix2[0,0]
xsig=xsig-6
ysig=ysig+9 
x=x-9
y=y+9
CeleryPy.move_absolute((x,y,-205),(0,0,0),100)
CeleryPy.move_absolute((x,y,-302),(0,0,0),100)
CeleryPy.wait(500)
CeleryPy.write_pin(number=4, value=0, mode=0)
CeleryPy.wait(500)
CeleryPy.move_absolute((x,y,-195),(0,0,0),100)
CeleryPy.wait(500)
CeleryPy.move_absolute((xsig,ysig,-195),(0,0,0),100)
CeleryPy.move_absolute((xsig,ysig,-278),(0,0,0),100)
CeleryPy.write_pin(number=4, value=1, mode=0)
CeleryPy.wait(400)
CeleryPy.write_pin(number=4, value=0, mode=0)
CeleryPy.wait(400)
CeleryPy.write_pin(number=4, value=1, mode=0)
CeleryPy.wait(400)
CeleryPy.write_pin(number=4, value=0, mode=0)
CeleryPy.wait(400)
CeleryPy.write_pin(number=4, value=1, mode=0)
CeleryPy.move_absolute((xsig,ysig,-205),(0,0,0),100)
CeleryPy.write_pin(number=4, value=0, mode=0)
CeleryPy.wait(200)
CeleryPy.write_pin(number=4, value=1, mode=0)
CeleryPy.wait(200)
CeleryPy.write_pin(number=4, value=0, mode=0)
CeleryPy.wait(200)
CeleryPy.write_pin(number=4, value=1, mode=0)
CeleryPy.wait(500)
CeleryPy.move_absolute(weeder,(120,0,200),150)
CeleryPy.move_absolute(weeder,(120,0,0),150)
CeleryPy.move_absolute(weeder,(0,0,0),150)
CeleryPy.move_absolute(weeder,(0,0,200),150)
CeleryPy.move_absolute((0,0,0),(0,0,0),250)


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
from farmware_tools import get_config_value
import CeleryPy
import time
farmware_name = "Movements calibration"
valueM1p=get_config_value(farmware_name,'row1',int)
valueM1q=get_config_value(farmware_name,'col1',int)
valueM2p=get_config_value(farmware_name,'row2',int)
valueM2q=get_config_value(farmware_name,'col2',int)
weeder=(20,553,-402)
send_message(message='TUDO BEM', message_type='success', channel='toast')                          
dir_path='/root/farmware'
matrix=np.load(dir_path+'/'+'array.npy')
matrix2=np.load(dir_path+'/'+'array2.npy')
matrix3=np.load(dir_path+'/'+'array3.npy')
matrix4=np.load(dir_path+'/'+'array4.npy')
send_message(message='TUDO BEM', message_type='success', channel='toast')
CeleryPy.move_absolute(weeder,(0,0,0),150)
CeleryPy.move_absolute(weeder,(100,0,0),150)
CeleryPy.move_absolute(weeder,(100,0,100),150)
CeleryPy.move_absolute(weeder,(100,0,200),150)
CeleryPy.write_pin(number=4, value=1, mode=0)
CeleryPy.wait(100)
CeleryPy.write_pin(number=4, value=0, mode=0)
CeleryPy.wait(200)
CeleryPy.write_pin(number=4, value=1, mode=0)
  
xmat=valueM1p
ymat=valueM1q
xmatsig=valueM2p
ymatsig=valueM2q
x,y=matrix[ymat,xmat]
xsig,ysig=matrix2[ymatsig,xmatsig]
xsig=xsig-4
ysig=ysig+4
x=x-7
y=y+7
CeleryPy.move_absolute((x,y,-205),(0,0,0),100)
CeleryPy.move_absolute((x,y,-279),(0,0,0),100)
CeleryPy.wait(500)
CeleryPy.write_pin(number=4, value=0, mode=0)
CeleryPy.wait(2000)
CeleryPy.move_absolute((x,y,-215),(0,0,0),100)
CeleryPy.wait(500)
CeleryPy.move_absolute((xsig,ysig,-200),(0,0,0),100)
CeleryPy.move_absolute((xsig,ysig,-278),(0,0,0),100)
CeleryPy.write_pin(number=4, value=1, mode=0)
eleryPy.wait(400)
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
CeleryPy.wait(00)
CeleryPy.write_pin(number=4, value=0, mode=0)
CeleryPy.wait(200)
CeleryPy.write_pin(number=4, value=1, mode=0)
CeleryPy.wait(500)
CeleryPy.move_absolute(weeder,(120,0,200),150)
CeleryPy.move_absolute(weeder,(120,0,0),150)
CeleryPy.move_absolute(weeder,(0,0,0),150)
CeleryPy.move_absolute(weeder,(0,0,200),150
CeleryPy.move_absolute((0,0,0),(0,0,0),250)


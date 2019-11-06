import os
import sys
from CeleryPy import log
from CeleryPy import send_message
import numpy as np
from farmware_tools import device
import CeleryPy


device.set_pin_io_mode(1,4)
weeder=(20,553,-402)
herramienta_2=(20,453,-402)
herramienta_3=(20,353,-402)
central_position=(500,440,-270)
send_message(message='Iniciando secuencia de cambio de herramientas', message_type='warn', channel='toast')
CeleryPy.move_absolute(weeder,(0,0,0),150)
CeleryPy.move_absolute(weeder,(100,0,0),150)
CeleryPy.move_absolute(weeder,(100,0,100),150)
CeleryPy.move_absolute(weeder,(100,0,200),150)
CeleryPy.write_pin(number=4, value=1, mode=0)
CeleryPy.wait(300)
CeleryPy.write_pin(number=4, value=0, mode=0)
CeleryPy.wait(300)
CeleryPy.write_pin(number=4, value=1, mode=0)
CeleryPy.move_absolute(central_position,(0,0,0),100)
CeleryPy.write_pin(number=4, value=0, mode=0)
CeleryPy.wait(400)
CeleryPy.write_pin(number=4, value=1, mode=0)
CeleryPy.wait(400)
CeleryPy.write_pin(number=4, value=0, mode=0)
CeleryPy.wait(400)
CeleryPy.write_pin(number=4, value=1, mode=0)
CeleryPy.wait(400)
CeleryPy.write_pin(number=4, value=0, mode=0)
CeleryPy.wait(2000)
CeleryPy.move_absolute(weeder,(120,0,200),150)
CeleryPy.move_absolute(weeder,(120,0,0),150)
CeleryPy.move_absolute(weeder,(0,0,0),150)
CeleryPy.move_absolute(weeder,(0,0,200),150)

CeleryPy.move_absolute(herramienta_2,(0,0,0),150)
CeleryPy.move_absolute(herramienta_2,(100,0,0),150)
CeleryPy.move_absolute(herramienta_2,(100,0,100),150)
CeleryPy.move_absolute(herramienta_2,(100,0,200),150)
CeleryPy.move_absolute(central_position,(0,0,0),100)
CeleryPy.wait(2500)
CeleryPy.move_absolute(herramienta_2,(120,0,200),150)
CeleryPy.move_absolute(herramienta_2,(120,0,0),150)
CeleryPy.move_absolute(herramienta_2,(0,0,0),150)
CeleryPy.move_absolute(herramienta_2,(0,0,200),150)

CeleryPy.move_absolute(herramienta_3,(0,0,0),150)
CeleryPy.move_absolute(herramienta_3,(100,0,0),150)
CeleryPy.move_absolute(herramienta_3,(100,0,100),150)
CeleryPy.move_absolute(herramienta_3,(100,0,200),150)
CeleryPy.move_absolute(central_position,(0,0,0),100)
CeleryPy.wait(2500)
CeleryPy.move_absolute(herramienta_3,(120,0,200),150)
CeleryPy.move_absolute(herramienta_3,(120,0,0),150)
CeleryPy.move_absolute(herramienta_3,(0,0,0),150)
CeleryPy.move_absolute(herramienta_3,(0,0,200),150)
CeleryPy.move_absolute((0,0,0),(0,0,0),250)
send_message(message='Secuencia de cambio de herramientas satisfactoria', message_type='success', channel='toast')


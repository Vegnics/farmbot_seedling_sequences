import os
import sys
from CeleryPy import log
from CeleryPy import send_message
import numpy as np
from farmware_tools import device
import CeleryPy


device.set_pin_io_mode(1,4)
weeder=(20,553,-402)
herramienta_2=()#modificar posición de herramienta 2
CeleryPy.move_absolute((500,440,0),(0,0,0),150)

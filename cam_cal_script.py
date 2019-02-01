import os
import sys
from CeleryPy import log
from DB import DB
import Capture 
import Image
x=DB.getcoordinates()
y=str(object=x,encoding='ascii', errors='ignore')
log(y, message_type='error', title='FUNCO')
#log_message = '[{y}]'.format(y=y)
#send_message(log_message,'error')


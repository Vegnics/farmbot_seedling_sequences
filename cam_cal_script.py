import os
import sys
from CeleryPy import log
from DB import DB
import Capture 
import Image
x=DB.getcoordinates()
#log('ya', message_type='error', title='FUNCO')
log_message = '[{x}]'.format(x=x)
send_message(log_message,'error')


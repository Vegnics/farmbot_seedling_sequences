import os
import sys
from CeleryPy import log
from CeleryPy import send_message
from DB import DB
import Capture
import Image
import requests
x=DB()
#y=x.api_get('peripherals/')
y=x._get_bot_state()
y=str(y)
#log(print(os.environ['API_TOKEN']), message_type='error', title='FUNCO')
send_message(message=y, message_type='success', channel='toast')

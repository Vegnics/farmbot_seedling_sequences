import os
import sys
from CeleryPy import log
from DB import DB
import Capture
import Image
import requests
x=DB()
#y=x.api_get('peripherals/')
y=x._get_bot_state()
log(print(y), message_type='error', title='FUNCO')

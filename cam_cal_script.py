import os
import sys
from CeleryPy import log
from DB import DB
import Capture
import Image
import requests
x=DB()
#y=x.api_get('peripherals/')
y=x._api_info('app')
log(print(os.environ['API_TOKEN']), message_type='error', title='FUNCO')

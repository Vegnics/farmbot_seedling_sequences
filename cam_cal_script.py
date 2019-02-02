import os
import sys
from CeleryPy import log
from CeleryPy import send_message
from DB import DB
import Capture
import Image
import requests
x=DB()
y=x.api_get('images')
#y=x._get_bot_state()
#y=dict(y)['user_env']['camera']
#log(print(os.environ['API_TOKEN']), message_type='error', title='FUNCO')
y=str(y)
send_message(message=y, message_type='success', channel='toast')

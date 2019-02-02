import os
import sys
from CeleryPy import log
from CeleryPy import send_message
from DB import DB
import json
import requests

x=DB()
response = x.api_get('images/' + str(52))
img_json=response.json()
#filename_path = upload_path(y)
#retcode = call(["raspistill", "-w", "640", "-h", "480", "-o", filename_path])
#y=x._get_bot_state()
#y=dict(y)['user_env']['camera']
#log(print(os.environ['API_TOKEN']), message_type='error', title='FUNCO')
#z=str(z)
send_message(message=str(img_json), message_type='success', channel='toast')
#z=os.path.dirname(os.path.realpath(__file__)) + os.sep
#send_message(message=z, message_type='success', channel='toast')
image_url = 'smb://192.168.1.106'+img_json['attachment_url']
send_message(message=str(image_url), message_type='success', channel='toast')
y = requests.get(image_url, stream=True)
#y=x.get_image(52)


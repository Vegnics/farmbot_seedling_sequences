import CeleryPy
import cv2
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
cmd='ls {}'.format(dir_path)
f=os.popen(cmd)
out=f.read()
CeleryPy.send_message(message=str(out), message_type='warn', channel='toast'):



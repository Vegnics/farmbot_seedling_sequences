from farmware_tools import get_config_value
from CeleryPy import send_message
from time import time,sleep
import cv2

send_message(message='libraries ok', message_type='success', channel='toast')
fw_name="Taking_photo"
try:
    width = get_config_value(fw_name,config_name="width")
    height = get_config_value(fw_name,config_name="height")
    bright = get_config_value(fw_name,config_name="bright")
    contrast = get_config_value(fw_name,config_name="contrast")
    saturation = get_config_value(fw_name,config_name="sat")
    hue = get_config_value(fw_name,config_name="hue")
except:
    send_message(message='reading bad', message_type='error', channel='toast')

def usb_camera_photo():
    #'Take a photo using a USB camera.'#
    camera_port = 0      # default USB camera port
    max_port_num = 1     # highest port to try if not detected on port
    discard_frames = 10  # number of frames to discard for auto-adjust
    max_attempts = 5     # number of failed discard frames before quit
    send_message(message='reading ok', message_type='success', channel='toast')
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,640)#640
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,480)#480
    cam.set(cv2.CAP_PROP_BRIGHTNESS,0.5#0.5
    cam.set(cv2.CAP_PROP_CONTRAST,0.73333)#0.733333
    cam.set(cv2.CAP_PROP_SATURATION,0.3543)#0.3543
    cam.set(cv2.CAP_PROP_HUE,0.5)#0.5
    send_message(message='setting ok', message_type='success', channel='toast')
    #send_message(message='{}'.format(cam.get(cv2.CAP_PROP_FRAME_WIDTH)), message_type='success', channel='toast')
    #send_message(message='{}'.format(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)), message_type='success', channel='toast')
    #send_message(message='{}'.format(cam.get(cv2.CAP_PROP_BRIGHTNESS)), message_type='success', channel='toast')
    #send_message(message='{}'.format(cam.get(cv2.CAP_PROP_CONTRAST)), message_type='success', channel='toast')
    #send_message(message='{}'.format(cam.get(cv2.CAP_PROP_SATURATION)), message_type='success', channel='toast')
    #send_message(message='{}'.format(cam.get(cv2.CAP_PROP_HUE)), message_type='success', channel='toast')
    failed_attempts = 0
    max_attempts = 5
    
    for a in range(20):
        ret,image = cam.read()
        if not cam.grab():
            #verbose_log('Could not get frame.')
            failed_attempts += 1
        if failed_attempts >= max_attempts:
            break
        sleep(0.1)
    # Take a photo
    ret, image = cam.read()
    directory = '/tmp/images/'
    image_filename = directory +  '{timestamp}.jpg'.format(timestamp=int(time()))
    cv2.imwrite(image_filename,image)
    # Close the camera
    cam.release()

usb_camera_photo()
send_message(message='finish ok', message_type='success', channel='toast')

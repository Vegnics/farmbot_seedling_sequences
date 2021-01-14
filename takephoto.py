from farmware_tools import get_config_value
from CeleryPy import send_message
from time import time,sleep
import cv2
send_message(message='libraries ok', message_type='success', channel='toast')
fw_name="Taking_photo"

def usb_camera_photo():
    #'Take a photo using a USB camera.'#
    camera_port = 0      # default USB camera port
    max_port_num = 1     # highest port to try if not detected on port
    discard_frames = 10  # number of frames to discard for auto-adjust
    max_attempts = 5     # number of failed discard frames before quit
    image_width = int(1600)
    image_height = int(1200)
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,get_config_value(fw_name,config_name="width"))#640
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,get_config_value(fw_name,config_name="height"))#480
    cam.set(cv2.CAP_PROP_BRIGHTNESS,get_config_value(fw_name,config_name="bright"))#0.5
    cam.set(cv2.CAP_PROP_CONTRAST,get_config_value(fw_name,config_name="contrast"))#0.733333
    cam.set(cv2.CAP_PROP_SATURATION,get_config_value(fw_name,config_name="sat"))#0.3543
    cam.set(cv2.CAP_PROP_HUE,get_config_value(fw_name,config_name="hue"))#0.5
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

from CeleryPy import send_message
from time import time,sleep
import cv2
send_message(message='libraries ok', message_type='success', channel='toast')

def usb_camera_photo():
    #'Take a photo using a USB camera.'#
    camera_port = 0      # default USB camera port
    max_port_num = 1     # highest port to try if not detected on port
    discard_frames = 10  # number of frames to discard for auto-adjust
    max_attempts = 5     # number of failed discard frames before quit
    image_width = int(1600)
    image_height = int(1200)
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,1600)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,1200)
    cam.set(cv2.CAP_PROP_BRIGHTNESS,0)#-8
    cam.set(cv2.CAP_PROP_CONTRAST,0)#-3
    cam.set(cv2.CAP_PROP_SATURATION,0)#7
    cam.set(cv2.CAP_PROP_HUE,0)#-100
    send_message(message='point1_ok', message_type='success', channel='toast')
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
        
    send_message(message='point2_ok', message_type='success', channel='toast')
    # Take a photo
    ret, image = cam.read()
    directory = '/tmp/images/'
    image_filename = directory +  '{timestamp}.jpg'.format(timestamp=int(time()))
    cv2.imwrite(image_filename,image)
    # Close the camera
    cam.release()

usb_camera_photo()
send_message(message='finish ok', message_type='success', channel='toast')

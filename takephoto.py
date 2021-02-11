#from CeleryPy import send_message,device
from time import time,sleep
from farmware_tools import get_config_value,device
import cv2
from cv2 import floodFill
import numpy as np
from numpy.fft import fft2,fftshift,ifft2,ifftshift
import os

device.log(message='libraries ok', message_type='success')
fw_name="Taking_photo"
dir_path = os.path.dirname(os.path.realpath(__file__))
gauss_kernel = np.load(dir_path+'/'+'gauss_kernel.npy')


def highpass_gaussian_kernel(size0,size1,sigma):
    kernel = np.zeros((size0,size1))
    for i in range(size0):
        for j in range(size1):
            kernel[i,j] = 1 - np.exp(-((i-int(size0/2))**2 + (j-int(size1/2))**2)/(2*sigma**2))
    return kernel

def lowpass_gaussian_kernel(size0,size1,sigma):
    kernel = np.zeros((size0,size1))
    for i in range(size0):
        for j in range(size1):
            kernel[i,j] = np.exp(-((i-int(size0/2))**2 + (j-int(size1/2))**2)/(2*sigma**2))
    return kernel

def remap(src,min,max):
    max=np.max(src)
    min=np.min(src)
    output_img=(255/(max-min))*(src-min)
    output_img=output_img
    output_img = np.clip(output_img,0,255)
    output_img = output_img.astype(np.uint8)
    return output_img

def homomorph_filter_N1(src,sigma):
    src = src.astype(np.float32)
    Ln_I = np.log(src + 1)
    I_fft = fft2(Ln_I)
    I_fft = fftshift(I_fft)
    #kernel = highpass_gaussian_kernel(I_fft.shape[0], I_fft.shape[1], sigma)
    kernel = gauss_kernel
    I_filt_fft = I_fft * kernel
    I_filt_fft_uns = ifftshift(I_filt_fft)
    I_filtered = np.real(ifft2(I_filt_fft_uns))
    I_filtered = np.exp(I_filtered)
    return I_filtered,np.min(I_filtered),np.max(I_filtered)

def homomorph_filter_N3(src,sigma):
    B, G, R = cv2.split(src)
    nB,minB,maxB = homomorph_filter_N1(B, sigma)
    nG,minG,maxG = homomorph_filter_N1(G, sigma)
    nR,minR,maxR = homomorph_filter_N1(R, sigma)
    max=np.max([maxB,maxG,maxR])
    min=np.min([minB,minG,minR])
    nB=remap(nB,min,max)
    nG = remap(nG, min, max)
    nR = remap(nR, min, max)
    return cv2.merge((nB,nG,nR))

width = get_config_value(fw_name,config_name="width",value_type=int)
height = get_config_value(fw_name,config_name="height",value_type=int)
bright = get_config_value(fw_name,config_name="bright",value_type=int)
contrast = get_config_value(fw_name,config_name="contrast",value_type=int)
saturation = get_config_value(fw_name,config_name="sat",value_type=int)
hue = get_config_value(fw_name,config_name="hue",value_type=int)
device.log(message='reading ok', message_type='success')

def usb_camera_photo():
    #'Take a photo using a USB camera.'#
    camera_port = 0      # default USB camera port
    max_port_num = 1     # highest port to try if not detected on port
    discard_frames = 10  # number of frames to discard for auto-adjust
    max_attempts = 5     # number of failed discard frames before quit
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)#640
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)#480
    cam.set(cv2.CAP_PROP_BRIGHTNESS,bright*0.01)#0.5
    cam.set(cv2.CAP_PROP_CONTRAST,contrast*0.01)#0.733333
    cam.set(cv2.CAP_PROP_SATURATION,saturation*0.01)#0.3543
    cam.set(cv2.CAP_PROP_HUE,hue*0.01)#0.5
    device.log(message='setting ok', message_type='success')
    #send_message(message='{}'.format(cam.get(cv2.CAP_PROP_FRAME_WIDTH)), message_type='success', channel='toast')
    #send_message(message='{}'.format(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)), message_type='success', channel='toast')
    #send_message(message='{}'.format(cam.get(cv2.CAP_PROP_BRIGHTNESS)), message_type='success', channel='toast')
    #send_message(message='{}'.format(cam.get(cv2.CAP_PROP_CONTRAST)), message_type='success', channel='toast')
    #send_message(message='{}'.format(cam.get(cv2.CAP_PROP_SATURATION)), message_type='success', channel='toast')
    #send_message(message='{}'.format(cam.get(cv2.CAP_PROP_HUE)), message_type='success', channel='toast')
    failed_attempts = 0
    max_attempts = 5
    
    for a in range(10):
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
    return image


img=usb_camera_photo()
directory = '/tmp/images/'
image_filename = directory +  '{timestamp}.jpg'.format(timestamp=int(time()))
#img_filter= homomorph_filter_N3(img,1.1)
#img_filter_hsv = cv2.cvtColor(img_filter,cv2.COLOR_BGR2HSV)
#H=[27,100]
#S=[50,255]
#V=[32,255]
#mask = cv2.inRange(img_filter_hsv ,np.array([H[0],S[0],V[0]]),np.array([H[1],S[1],V[1]]))
#num_labels, labeled = cv2.connectedComponents(mask)


#cv2.imwrite(image_filename,img_filter)

device.log(message='finish ok', message_type='success')

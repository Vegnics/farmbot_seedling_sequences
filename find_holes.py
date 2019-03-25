import os
import sys
from CeleryPy import log
from CeleryPy import send_message
from DB import DB
from Image import Image
import json
from Parameters import Parameters
import requests
import cv2
from Capture import Capture
import numpy as np
from PlantDetection import PlantDetection
from farmware_tools import device
import CeleryPy

def create_mask(image,lowergreen,uppergreen):##función para crear máscara a partir de valores máximos y minimos de HSV
  imghsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV_FULL)
  mask=cv2.inRange(imghsv,lowergreen,uppergreen)
  return mask
def colorize(image):##función para cambiar el brillo y el contraste de imagen
 n_image = np.zeros(image.shape, image.dtype)
 alpha=2.4
 beta=-280
 n_image = np.clip(np.multiply(alpha,image)+beta, 0, 255)
 return n_image.astype(np.uint8) 
def invert(img):
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = 255-img
    img2 = cv2.medianBlur(img2,17)
    return img2
def array_shape(selected):
    a=sorted(selected,key=lambda x:x[0])
    rows=[]
    counter=0
    print(len(a))
    for i in range(len(a)-1):
        if abs(a[i][0]-a[i+1][0])<30:
            counter+=1
        else:
            counter += 1
            rows.append(counter)
            counter=0
    counter = 0
    b=sorted(selected,key=lambda x:x[1])
    cols=[]
    for i in range(len(a)-1):
        if abs(b[i][1]-b[i+1][1])<30:
            counter+=1
        else:
            counter += 1
            cols.append(counter)
            counter=0
    print(rows)
    print(cols)
    rows=int(np.mean(rows))
    cols=int(np.mean(cols))
    return rows,cols
  
def fill_array(matrix,list):
    sortedlistx=sorted(list,key=lambda x:x[0])
    rows=matrix.shape[0]
    cols=matrix.shape[1]
    for i in range(cols):
        sortedlisti=sortedlistx[i*rows:(i+1)*rows]
        sortedlistij=sorted(sortedlisti, key=lambda x: x[1])
        for j in range(rows):
            print(sortedlistij[j])
            matrix[j,i]=sortedlistij[j]
    return matrix
def mergearrays(matrix1,matrix2):
    res_matrix=matrix1
    row2=matrix2[0,:,:]
    for i in range(matrix1.shape[0]):
        row1=matrix1[i,:,:]
        res=sum(abs(row2[0]-row1[0])+abs(row2[1]-row1[1]))/row1.shape[0]
        log(str(res))
        if res<4 :
            subindex=i
            break
    counter=matrix1.shape[0]-subindex
    log(str(counter))
    res_matrix=np.concatenate((res_matrix[:,:,:],matrix2[counter:,:,:]),axis=0)
    log(str(res_matrix.shape))
    return res_matrix
  
#######################################PRIMERA MATRIZ##########################################################################################
number=1
for num in range(number):
      CeleryPy.move_absolute((500,330,0),(0,0,0),150)
      CeleryPy.wait(5000)
      dir_path = os.path.dirname(os.path.realpath(__file__))
      template=cv2.imread(dir_path+'/'+'template.jpg',1)
      template=cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
      w, h = template.shape[::-1]

      file=Capture().capture()
      img2 = cv2.imread(file,1)
      image=invert(img2)
      image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

      res = cv2.matchTemplate(image_gray,template,cv2.TM_CCOEFF_NORMED)
      threshold = 0.8
      loc = np.where( res >= threshold)
      for pt in zip(*loc[::-1]):
          cv2.circle(img2,(int(pt[0]+w/2),int(pt[1]+h/2)),15,(0,255,0),cv2.FILLED)
      new_image=img2
      cv2.imwrite('/tmp/images/1549138022.jpg',new_image)
      ########SETEAMOS VALORES MÍNIMOS Y MÁXIMOS DE HSV##################
      HL=52
      SL=95
      VL=50
      HH=110
      SH=255
      VH=255
      ###################################################################
      mask=create_mask(new_image,np.array([HL,SL,VL]),np.array([HH,SH,VH]))###Creamos la máscara
      image3=cv2.bitwise_and(new_image,new_image,mask=mask)##aplicamos la máscara
      image3=cv2.medianBlur(image3,5)
      cv2.imwrite('/tmp/images/1549138027.jpg',image3)

      PD = PlantDetection(
                  image='/tmp/images/1549138027.jpg',
                  blur=2, morph=2, iterations=3, from_env_var=True, coordinates=True,
                  array=[{"size": 5, "kernel": 'ellipse', "type": 'erode', "iters": 1}],
                  HSV_min=[49,95,50],HSV_max=[110,255,255]
                  )
      PD.detect_plants() # detect coordinates and sizes of weeds and plants
      if len(PD.plant_db.coordinate_locations) >= 1:
        holes=[]
        for coordinate_location in PD.plant_db.coordinate_locations:
              if coordinate_location[2]>10.5:
                holes.append([coordinate_location[0],coordinate_location[1]])  
        rows,cols=array_shape(holes)
        matrix00=np.zeros((rows,cols,2))
        matrix00=fill_array(matrix00,holes) 
        log(str(matrix00.shape))
#######___________________________________________________-####################################
      CeleryPy.move_absolute((500,600,0),(0,0,0),150)
      CeleryPy.wait(5000)
      file=Capture().capture()
      img2 = cv2.imread(file,1)
      image=invert(img2)
      image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
      res = cv2.matchTemplate(image_gray,template,cv2.TM_CCOEFF_NORMED)
      loc = np.where( res >= threshold)
      for pt in zip(*loc[::-1]):
          cv2.circle(img2,(int(pt[0]+w/2),int(pt[1]+h/2)),15,(0,255,0),cv2.FILLED)
      new_image=img2
      cv2.imwrite('/tmp/images/1549138022.jpg',new_image)
      mask=create_mask(new_image,np.array([HL,SL,VL]),np.array([HH,SH,VH]))###Creamos la máscara
      image3=cv2.bitwise_and(new_image,new_image,mask=mask)##aplicamos la máscara
      image3=cv2.medianBlur(image3,5)
      cv2.imwrite('/tmp/images/1549138027.jpg',image3)

      PD = PlantDetection(
                  image='/tmp/images/1549138027.jpg',
                  blur=2, morph=2, iterations=3, from_env_var=True, coordinates=True,
                  array=[{"size": 5, "kernel": 'ellipse', "type": 'erode', "iters": 1}],
                  HSV_min=[49,95,50],HSV_max=[110,255,255]
                  )
      PD.detect_plants() # detect coordinates and sizes of weeds and plants
      if len(PD.plant_db.coordinate_locations) >= 1:
        holes=[]
        for coordinate_location in PD.plant_db.coordinate_locations:
              if coordinate_location[2]>10.5:
                holes.append([coordinate_location[0],coordinate_location[1]])  
        rows,cols=array_shape(holes)
        matrix01=np.zeros((rows,cols,2))
        matrix01=fill_array(matrix01,holes) 
        log(str(matrix01.shape))
      matrix=mergearrays(matrix00,matrix01)
      np.save('/root/farmware/array',matrix)
      #######________________SEGUNDA MATRIZ___________________________________-####################################
      CeleryPy.move_absolute((845,300,0),(0,0,0),150)
      CeleryPy.wait(5000)
      file=Capture().capture()
      img2 = cv2.imread(file,1)
      image=invert(img2)
      image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
      res = cv2.matchTemplate(image_gray,template,cv2.TM_CCOEFF_NORMED)
      loc = np.where( res >= 0.55)
      for pt in zip(*loc[::-1]):
          cv2.circle(img2,(int(pt[0]+w/2),int(pt[1]+h/2)),15,(0,255,0),cv2.FILLED)
      new_image=img2
      cv2.imwrite('/tmp/images/1549138022.jpg',new_image)
      mask=create_mask(new_image,np.array([HL,SL,VL]),np.array([HH,SH,VH]))###Creamos la máscara
      image3=cv2.bitwise_and(new_image,new_image,mask=mask)##aplicamos la máscara
      image3=cv2.medianBlur(image3,5)
      cv2.imwrite('/tmp/images/1549138027.jpg',image3)

      PD = PlantDetection(
                  image='/tmp/images/1549138027.jpg',
                  blur=2, morph=2, iterations=3, from_env_var=True, coordinates=True,
                  array=[{"size": 5, "kernel": 'ellipse', "type": 'erode', "iters": 1}],
                  HSV_min=[49,95,50],HSV_max=[110,255,255]
                  )
      PD.detect_plants() # detect coordinates and sizes of weeds and plants
      if len(PD.plant_db.coordinate_locations) >= 1:
        holes=[]
        for coordinate_location in PD.plant_db.coordinate_locations:
              if 15>coordinate_location[2]>10.5:
                holes.append([coordinate_location[0],coordinate_location[1]])  
        rows,cols=array_shape(holes)
        matrix10=np.zeros((rows,cols,2))
        matrix10=fill_array(matrix10,holes) 
        matrix10=matrix10[:,0:5,:]
        log(str(matrix10.shape))
      #######___________________________________________________-####################################
      CeleryPy.move_absolute((845,600,0),(0,0,0),150)
      CeleryPy.wait(5000)
      file=Capture().capture()
      img2 = cv2.imread(file,1)
      image=invert(img2)
      image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
      res = cv2.matchTemplate(image_gray,template,cv2.TM_CCOEFF_NORMED)
      loc = np.where( res >= 0.55)
      for pt in zip(*loc[::-1]):
          cv2.circle(img2,(int(pt[0]+w/2),int(pt[1]+h/2)),15,(0,255,0),cv2.FILLED)
      new_image=img2
      cv2.imwrite('/tmp/images/1549138022.jpg',new_image)
      mask=create_mask(new_image,np.array([HL,SL,VL]),np.array([HH,SH,VH]))###Creamos la máscara
      image3=cv2.bitwise_and(new_image,new_image,mask=mask)##aplicamos la máscara
      image3=cv2.medianBlur(image3,5)
      cv2.imwrite('/tmp/images/1549138027.jpg',image3)

      PD = PlantDetection(
                  image='/tmp/images/1549138027.jpg',
                  blur=2, morph=2, iterations=3, from_env_var=True, coordinates=True,
                  array=[{"size": 5, "kernel": 'ellipse', "type": 'erode', "iters": 1}],
                  HSV_min=[49,95,50],HSV_max=[110,255,255]
                  )
      PD.detect_plants() # detect coordinates and sizes of weeds and plants
      if len(PD.plant_db.coordinate_locations) >= 1:
        holes=[]
        for coordinate_location in PD.plant_db.coordinate_locations:
              if 15>coordinate_location[2]>10.5:
                holes.append([coordinate_location[0],coordinate_location[1]])  
        rows,cols=array_shape(holes)
        matrix11=np.zeros((rows,cols,2))
        matrix11=fill_array(matrix11,holes) 
        matrix11=matrix11[:,0:5,:]
        log(str(matrix11.shape))
      matrix=mergearrays(matrix10,matrix11)
      log(str(matrix.shape))
      np.save('/root/farmware/array2',matrix)
      if len(PD.plant_db.coordinate_locations) == 0:
        send_message(message='NO HOLES', message_type='error', channel='toast')
      CeleryPy.move_absolute((0,0,0),(0,0,0),200)
      
send_message(message='TUDO BEM', message_type='success', channel='toast')


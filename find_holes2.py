      
      
      
      
      #######________________SEGUNDA MATRIZ___________________________________-####################################
      CeleryPy.move_absolute((845,290,0),(0,0,0),150)
      CeleryPy.wait(5000)
      file=Capture().capture()
      img2 = cv2.imread(file,1)
      image_gray=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
      circles=cv2.HoughCircles(image_gray,cv2.HOUGH_GRADIENT,1,11,param1=65,param2=30,minRadius=15,maxRadius=34)
      circles = np.uint16(np.around(circles))
      for i in circles[0,:]:
        cv2.circle(img2,(i[0],i[1]),15,(0,255,0),cv2.FILLED)
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
              if 19>coordinate_location[2]>7:
                holes.append([coordinate_location[0],coordinate_location[1]])  
        rows,cols=array_shape(holes)
        matrix10=np.zeros((rows,cols,2))
        matrix10=fill_array(matrix10,holes) 
        matrix10=matrix10[:,0:6,:]
        log(str(matrix10.shape))
      #######___________________________________________________-####################################
      CeleryPy.move_absolute((845,600,0),(0,0,0),150)
      CeleryPy.wait(5000)
      file=Capture().capture()
      img2 = cv2.imread(file,1)
      image=invert(img2)
      image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
      res = cv2.matchTemplate(image_gray,template2,cv2.TM_CCOEFF_NORMED)
      loc = np.where( res >= 0.635)
      for pt in zip(*loc[::-1]):
          cv2.circle(img2,(int(pt[0]+w/2),int(pt[1]+h/2)),15,(0,255,0),cv2.FILLED)
      
      res = cv2.matchTemplate(image_gray,template3,cv2.TM_CCOEFF_NORMED)
      loc = np.where( res >= 0.635)
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
                  array=[{"size": 5, "kernel": 'ellipse', "type": 'erode', "iters": 4}],
                  HSV_min=[49,95,50],HSV_max=[110,255,255]
                  )
      PD.detect_plants() # detect coordinates and sizes of weeds and plants
      if len(PD.plant_db.coordinate_locations) >= 1:
        holes=[]
        for coordinate_location in PD.plant_db.coordinate_locations:
              if 19>coordinate_location[2]>10.5:
                holes.append([coordinate_location[0],coordinate_location[1]])  
        rows,cols=array_shape(holes)
        matrix11=np.zeros((rows,cols,2))
        matrix11=fill_array(matrix11,holes) 
        matrix11=matrix11[:,0:6,:]
        log(str(matrix11.shape))
      matrix=mergearrays(matrix10,matrix11)
      log(str(matrix.shape))
      np.save('/root/farmware/array2',matrix)

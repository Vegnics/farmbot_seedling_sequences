import cv2
import numpy as np
img=cv2.imread('checkerboard.jpg',1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Find the chess board corners
ret, corners = cv2.findChessboardCorners(gray, (7,7), None)
# If found, add object points, image points (after refining them)
objpoints=[]
imgpoints=[]
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)
img_aux=img
if ret == True:
    # Draw and display the corners
    cv2.drawChessboardCorners(img_aux, (7,7), corners, ret)
    objpoints.append(objp)
    imgpoints.append(corners)
    cv2.imshow('img', img_aux)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
h, w = img.shape[:2]
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
cv2.imshow('img2', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

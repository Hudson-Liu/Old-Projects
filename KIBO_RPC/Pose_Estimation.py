# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 08:26:32 2022

https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html
https://aliyasineser.medium.com/aruco-marker-tracking-with-opencv-8cb844c26628
Find distortion by using ar tags themselves
 
@author: hudso
"""

import numpy as np
import cv2
import cv2.aruco as aruco

cap = cv2.VideoCapture(0)

path = r"\Camera_Calibration\calibration_aruco.yml"
cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
mtx = cv_file.getNode('K').mat()
dist = cv_file.getNode('D').mat()
cv_file.release()

#Everything is in centimeters
def motion_tracking(mtx, dist):
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)  # Use 5x5 dictionary to find markers
    marker_size = 5 #centimeters
    axis_size = marker_size/2 #just for the visualization, can be any value
    while True:
        #Escape program
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        
        #Get frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        parameters = aruco.DetectorParameters_create()  # Marker detection parameters
        corners, ids, rejected_img_points = aruco.detectMarkers(
            gray, 
            aruco_dict, 
            parameters=parameters, 
            cameraMatrix=mtx, 
            distCoeff=dist
        )
        
        if np.all(ids is not None):
            for i in range(0, len(ids)):
                rvec, tvec, markerPoints = aruco.estimatePoseSingleMarkers(
                    corners[i], 
                    marker_size, 
                    mtx,
                    dist
                )
                (rvec - tvec).any() #no idea what this does lol i just saw it in the tutorial
                aruco.drawDetectedMarkers(frame, corners)  # Draw A square around the markers
                aruco.drawAxis(frame, mtx, dist, rvec, tvec, axis_size)  # Draw Axis
        
        cv2.imshow('frame', frame)
    cap.release()
    cv2.destroyAllWindows()

motion_tracking(mtx, dist)

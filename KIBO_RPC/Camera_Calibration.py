# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 12:26:08 2022

ArUco OpenCV Calibration
Only needs to be ran once
Run calibration only after Astrobee is at Target 1

@author: hudso
"""
import cv2
import cv2.aruco as aruco
import numpy as np
import glob
import os

def create_ArUco_board_format():
    """Defines constants and the general format of the ArUco Tags"""
    
    #These are the only changable variables
    num_markers_row = 2 #number of rows
    num_markers_column = 2 #numbers of columns
    side_length = 5 #side length of ar tags in cm
    
    #Calculates the marker separation as if in a grid
    dist_to_circle = 3.75
    dist_between_centers = 2 * dist_to_circle
    marker_separation = dist_between_centers - side_length
    
    dist_to_circle_x = 10
    dist_between_centers_x = 2 * dist_to_circle_x
    marker_separation_x = dist_between_centers_x - side_length
    
    #Downloads ArUco 5x5 250 Tag Dictionary
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    
    #Creates custom ArUco Board type object "board"
    tag_corners = []
    sep_array_y = [0, marker_separation + side_length, marker_separation + side_length, 0]
    sep_array_x = [0, 0, marker_separation_x + side_length, marker_separation_x + side_length]
    for i in range(num_markers_column*num_markers_row):
        top_left = np.array([sep_array_x[i], side_length + sep_array_y[i], 0], dtype = np.float32)
        top_right = np.array([side_length + sep_array_x[i], side_length + sep_array_y[i], 0], dtype = np.float32)
        bottom_right = np.array([side_length + sep_array_x[i], sep_array_y[i], 0], dtype = np.float32)
        bottom_left = np.array([sep_array_x[i], sep_array_y[i], 0], dtype = np.float32)
        tag_corners.append(np.array([top_left, top_right, bottom_right, bottom_left]))
    
    #Assigns the respective "board_ids" of the ArUco tags
    board_ids = np.array([[0],[1],[2],[3]], dtype=np.int32)
    
    #Creates board
    board = aruco.Board_create(tag_corners, aruco_dict, board_ids)
    
    return board, aruco_dict
    
def calibrate_aruco(board, aruco_dict):
    """Calibrates Camera Using ArUco Tags"""
    
    #Search through directory of Calibration Images
    cwd = os.getcwd()
    path = r"\Calibration_Images"
    os.chdir(cwd + path)
    files = glob.glob('*.{}'.format("jpg"))
    
    arucoParams = aruco.DetectorParameters_create()
    
    #Iterate over each calibration image and find markers
    all_corners = np.array([])
    all_ids = np.array([])
    num_detected_markers = []
    for file in files:
        #Open File
        image = cv2.imread(file)
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("obama", img_gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        #Detect markers
        corners, ids, rejected = aruco.detectMarkers(
            img_gray, 
            aruco_dict, 
            parameters=arucoParams
        )
        
        #Append marker data
        if np.size(all_corners) == 0:
            all_corners = corners
            all_ids = ids
        else:
            all_corners = np.append(all_corners, corners, axis=0)
            all_ids = np.append(all_ids, ids, axis=0)
        num_detected_markers.append(len(ids))
        
    num_detected_markers = np.array(num_detected_markers)

    #Uses markers to calibrate camera
    ret, mtx, dist, rvecs, tvecs = aruco.calibrateCameraAruco(
        all_corners, 
        all_ids, 
        num_detected_markers, 
        board, 
        img_gray.shape, 
        None, 
        None 
    )
    return ret, mtx, dist, rvecs, tvecs

#The actual execution of the methods
board, aruco_dict = create_ArUco_board_format()
ret, mtx, dist, rvecs, tvecs = calibrate_aruco(board, aruco_dict)
print(mtx) #Camera Matrix
print(dist) #Distortion Coefficients

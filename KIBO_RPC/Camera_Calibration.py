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

num_markers_row = 2 #number of rows
num_markers_column = 2 #numbers of columns

side_length = 5 #side length of ar tags in cm

dist_to_circle = 3.75 #distance between the y coordinate of ar tag and the y coordinate of circle
dist_between_centers = 2 * dist_to_circle
marker_separation = dist_between_centers - side_length

dist_to_circle_x = 10
dist_between_centers_x = 2 * dist_to_circle_x
marker_separation_x = dist_between_centers_x - side_length

print(marker_separation)
print(marker_separation_x)
    
def calibrate_aruco(num_markers_row, num_markers_column, side_length, marker_separation, marker_separation_x):
    """Calibrates Camera Using ArUco Tags"""
    
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    arucoParams = aruco.DetectorParameters_create()
    
    tag_corners = []
    sep_array_y = [0, marker_separation + side_length, marker_separation + side_length, 0]
    sep_array_x = [0, 0, marker_separation_x + side_length, marker_separation_x + side_length]
    for i in range(num_markers_column*num_markers_row):
        top_left = np.array([sep_array_x[i], side_length + sep_array_y[i], 0], dtype = np.float32)
        top_right = np.array([side_length + sep_array_x[i], side_length + sep_array_y[i], 0], dtype = np.float32)
        bottom_right = np.array([side_length + sep_array_x[i], sep_array_y[i], 0], dtype = np.float32)
        bottom_left = np.array([sep_array_x[i], sep_array_y[i], 0], dtype = np.float32)
        tag_corners.append(np.array([top_left, top_right, bottom_right, bottom_left]))
    
    board_ids = np.array( [[0],[1],[2],[3]], dtype=np.int32)
    
    board = aruco.Board_create(tag_corners, aruco_dict, board_ids)
    
# =============================================================================
#     board = aruco.GridBoard_create(
#         num_markers_column, 
#         num_markers_row,
#         side_length, 
#         marker_separation, 
#         aruco_dict
#     )
#     board.draw((1920, 1080))
# =============================================================================
    
    # Find the ArUco markers inside target image
    image = cv2.imread(r"D:\Downloads\target_1.png")
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    #cv2.imshow("obama", img_gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    corners, ids, rejected = aruco.detectMarkers(
        img_gray, 
        aruco_dict, 
        parameters=arucoParams
    )
    return corners, ids, rejected
    """
    # Actual calibration
    ret, mtx, dist, rvecs, tvecs = aruco.calibrateCameraAruco(corners, 
        ids, 
        num_markers_row*num_markers_column, 
        board, 
        img_gray.shape, 
        None, 
        None 
    )
    return [ret, mtx, dist, rvecs, tvecs]
    """

corners, ids, rejected = calibrate_aruco(num_markers_row, num_markers_column, side_length, marker_separation)
#tag_corners = calibrate_aruco(num_markers_row, num_markers_column, side_length, marker_separation, marker_separation_x)

# =============================================================================
# #This was commented out because ArUco Grid does not support different x and y separations
# 
# num_markers_row = 2 #number of rows
# num_markers_column = 2 #numbers of columns
# 
# side_length = 5 #side length of ar tags in cm
# 
# dist_to_circle_x = 3.75 #distance between the x coordinate of ar tag and the x coordinate of circle
# dist_between_centers_x = 2 * dist_to_circle_x
# marker_separation_x = dist_between_centers_x - side_length
# 
# dist_to_circle_y = 10 #distance between the x coordinate of ar tag and the x coordinate of circle
# dist_between_centers_y = 2 * dist_to_circle_y
# marker_separation_y = dist_between_centers_y - side_length
# 
# print(marker_separation_x)
# print(marker_separation_y)
# 
# =============================================================================


# =============================================================================
# 
# #This was commented out due to a misinterpretation of the KIBO Programming Guide
# #I thought that "5 cm square" referred to a square with an area of 5 cm^2
# #Instead, they were referring to a square with sides of 5 cms
# 
# import math
# 
# dist_to_circle_x = 3.75 #distance between the x coordinate of ar tag and the x coordinate of circle
# area = 5 #5 cm^2
# dist_between_centers = dist_to_circle_x * 2
# side_length = math.sqrt(area)
# marker_separation_x = dist_between_centers - side_length #in cm
# print(marker_separation_x)
# 
# =============================================================================

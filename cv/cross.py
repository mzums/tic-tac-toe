import cv2
import numpy as np
from main import *
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def draw_lines(image, lines, color=(0, 255, 0), thickness=2):
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), color, thickness)
    return image


def detect_cross(cell):
    if len(cell.shape) == 3:
        gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
    else:
        gray = cell.copy()
    
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    
    edges = cv2.Canny(thresh, 50, 150)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=10, 
                          minLineLength=10, maxLineGap=10)
    
    
    if lines is not None:
        line_image = cell.copy()
        line_image = draw_lines(line_image, lines)
        
        """cv2.imshow("Original", cell)
        cv2.imshow("Edges", edges)
        cv2.imshow("Detected Lines", line_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()"""
    #else:
        #print("Nie znaleziono linii")
    
    #show_image("", edges)
    
    if lines is None:
        return False

    h, w = gray.shape
    center = (w//2, h//2)
    angle_tolerance = 25
    min_intersection_distance = max(w, h)//3

    diagonal_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.degrees(np.arctan2(y2-y1, x2-x1))
        
        if angle < 0:
            angle += 180
        
        if (45-angle_tolerance < angle < 45+angle_tolerance) or \
           (135-angle_tolerance < angle < 135+angle_tolerance):
            diagonal_lines.append(line[0])

    for i in range(len(diagonal_lines)):
        for j in range(i+1, len(diagonal_lines)):
            line1 = diagonal_lines[i]
            line2 = diagonal_lines[j]
            
            #print(line_intersection(line1, line2))
            intersect = line_intersection(line1, line2)
            if intersect is None:
                continue
                
            distance = np.hypot(intersect[0]-center[0], intersect[1]-center[1])
            angle_diff = abs(get_angle(line1) - get_angle(line2))

            #print(distance, min_intersection_distance)
            #print(angle_diff)
            
            if 70 < angle_diff < 100:
                return True
    return False

def line_intersection(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if den == 0:
        return None
        
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / den
    u = -((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)) / den
    
    if 0 <= t <= 1 and 0 <= u <= 1:
        x = x1 + t*(x2-x1)
        y = y1 + t*(y2-y1)
        return (int(x), int(y))
    return None

def get_angle(line):
    x1, y1, x2, y2 = line
    return np.degrees(np.arctan2(y2-y1, x2-x1))
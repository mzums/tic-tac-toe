import cv2
import numpy as np
from cross import *


def show_image(title, image):
    cv2.imshow(title, image)
    cv2.waitKey(0)


def preprocess(image_path, draw = False):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Couldn't load the image")
        return
    
    show_image("1. Original", image) if draw else None
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    show_image('2. Thresholded Image', thresh) if draw else None

    edges = cv2.Canny(thresh, 5, 50)
    show_image('3. Edge Detection', edges) if draw else None

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    show_image('4. Closed Edges', closed_edges) if draw else None

    filled = np.zeros_like(gray)
    contours, _ = cv2.findContours(closed_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(filled, contours, -1, 255, thickness=cv2.FILLED)
    show_image('5. Filled Contours', filled) if draw else None

    return image, closed_edges, contours, filled


def detect_grid_center(image, closed_edges, contours, filled, draw=False):
    center_point = (image.shape[1]//2, image.shape[0]//2)
    best_contour = None
    min_distance = float('inf')

    all_contours_img = image.copy()
    cv2.drawContours(all_contours_img, contours, -1, (0,255,0), 2)
    show_image('6. All Contours', all_contours_img) if draw else None

    for cnt in contours:
        M = cv2.moments(cnt)
        if M["m00"] == 0:
            continue
            
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        distance = np.sqrt((cx - center_point[0])**2 + (cy - center_point[1])**2)
        
        area = cv2.contourArea(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        aspect_ratio = float(w)/h
        
        if area > 2000 and 0.7 < aspect_ratio < 1.3 and distance < min_distance:
            min_distance = distance
            best_contour = cnt

    result = image.copy()
    if best_contour is not None:
        M = cv2.moments(best_contour)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        cv2.drawContours(result, [best_contour], -1, (0,255,0), 3)
        cv2.circle(result, (cx, cy), 10, (0,0,255), -1)
        print(f"Center of middle cell: ({cx}, {cy})")
    else:
        print("Middle cell not found")

    get_center_size(cx, cy, filled, closed_edges, image)

    show_image('7. Final Result', result) if draw else None
    cv2.destroyAllWindows()


def extract_cells(filled, left, top, right, bottom, original_image):
    cell_w = right - left
    cell_h = bottom - top
    spacing = 7
    
    cells = []
    board = []
    
    debug_image = original_image.copy()
    
    for row_offset in (-1, 0, 1):
        for col_offset in (-1, 0, 1):
            x1 = max(left + col_offset * (cell_w + spacing), 0)
            y1 = max(top + row_offset * (cell_h + spacing), 0)
            x2 = min(x1 + cell_w, original_image.shape[1])
            y2 = min(y1 + cell_h, original_image.shape[0])
            
            cell = original_image[y1:y2, x1:x2]
            
            if cell.size == 0:
                cell = np.zeros((cell_h, cell_w, 3), dtype=np.uint8)
            
            cells.append(cell)
            
            cv2.rectangle(debug_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    #show_image("title", debug_image)
    
    for idx, cell in enumerate(cells):
        label = predict_cell(cell)

        if label == "circle":
            board.append("| O")
        elif label == "cross":
            board.append("| X")
        else:
            board.append("|  ")
        #show_image(f'Cell {idx+1, label}', cell)

    for (idx, i) in enumerate(board):
        print(i, end=" ")
        if (idx+1) % 3 == 0:
            print("|", end="")
            print()


def check_circle(cell):
    detected_circles = cv2.HoughCircles(cell,  
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 60, 
               param2 = 20, minRadius = 1, maxRadius = 40)
    
    if detected_circles is not None: 
        detected_circles = np.uint16(np.around(detected_circles)) 
    
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
            cv2.circle(cell, (a, b), r, (0, 255, 0), 2) 
            cv2.circle(cell, (a, b), 1, (0, 0, 255), 3) 

        return True


def predict_cell(cell):
    if cell is None or cell.size == 0:
        print("Empty cell received")
        return "unknown"
    
    if len(cell.shape) == 3:
        gray_cell = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
    else:
        gray_cell = cell.copy()

    if check_circle(gray_cell):
        return "circle"
    elif detect_cross(cell):
        return "cross"
    


def get_center_size(cx, cy, filled, closed_edges, image):
    h, w = filled.shape

    left = cx
    while left > 0 and filled[cy, left] == 255:
        left -= 1
    left += 7
    
    right = cx
    while right < w-1 and filled[cy, right] == 255:
        right += 1
    right -= 7
    
    top = cy
    while top > 0 and filled[top, cx] == 255:
        top -= 1
    top += 7
    
    bottom = cy
    while bottom < h-1 and filled[bottom, cx] == 255:
        bottom += 1
    bottom -= 7
    
    result = cv2.cvtColor(filled, cv2.COLOR_GRAY2BGR)
    
    cv2.line(result, (left, cy), (right, cy), (0,0,255), 1)
    cv2.line(result, (cx, top), (cx, bottom), (0,0,255), 1)
    
    cv2.rectangle(result, (left, top), (right, bottom), (0,0,255), 2)

    #show_image("title", result)

    extract_cells(filled, left, top, right, bottom, image)


if __name__ == '__main__':
    image, closed_edges, contours, filled = preprocess('image3.jpg')
    detect_grid_center(image, closed_edges, contours, filled)
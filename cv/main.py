import cv2 
import numpy as np 


def detect_grid_lines(edges, image, draw):
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=10, minLineLength=100, maxLineGap=20)

    horizontal = []
    vertical = []
    img_with_lines = image.copy()

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            
            if abs(angle) < 25:
                color = (0, 0, 255)
                horizontal.append((y1 + y2) / 2)
            elif abs(angle - 90) < 25:
                color = (0, 255, 0)
                vertical.append((x1 + x2) / 2)
            else:
                continue
            
            cv2.line(img_with_lines, (x1, y1), (x2, y2), color, 10) if draw else None
        
        if draw:
            cv2.imshow('Line detection', img_with_lines)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        print("Lines not found")

    return lines


if __name__ == '__main__':
    image = cv2.imread('unnamed.png')
    if image is None:
        print("Error: couldn't load the image")
        exit()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, 5, 50)

    cv2.imshow('Line detection', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    detect_grid_lines(edges, image, True)


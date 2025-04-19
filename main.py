import cv2
import sys
import numpy as np
import argparse
from cv.main import *
from minimax.main import *

def draw_symbol(image, coordinates, symbol):
    x1, y1, x2, y2 = coordinates
    center = ((x1 + x2) // 2, (y1 + y2) // 2)
    radius = int(min(x2 - x1, y2 - y1)) // 4
    thickness = 3
    
    if symbol.lower() == 'x':
        padding = radius
        cv2.line(image, (x1 + padding, y1 + padding), 
                 (x2 - padding, y2 - padding), (0, 0, 255), thickness)
        cv2.line(image, (x1 + padding, y2 - padding), 
                 (x2 - padding, y1 + padding), (0, 0, 255), thickness)
    else:
        cv2.circle(image, center, radius, (0, 255, 0), thickness)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Tic-Tac-Toe Image Processor")
    parser.add_argument("-s", "--show_steps", help="shows processing steps", action="store_true")
    parser.add_argument('image_path', help='Path to input image file')
    argument = parser.parse_args()

    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp'}

    if len(sys.argv) < 2:
        print("Usage: python -m cv.main <path_to_image>")
        sys.exit(1)
        
    image_path = sys.argv[1]
    
    if not any(image_path.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        print("Unsupported file format")
        sys.exit(1)

    image = cv2.imread(image_path)
    h, w = image.shape[:2]
    new_width = 200
    new_height = int(h * (new_width / w))
    image = cv2.resize(image, (new_width, new_height))

    if argument.show_steps:
        draw = True
    else:
        draw = False

    center_coordinates, board = preprocess(image_path, draw)
    _, cell_coordinates = divide_cells(*center_coordinates, image, False)
    
    player = input("Whose turn is it? [X/O]: ").lower()
    while player not in {'x', 'o'}:
        print("Invalid input! Please enter X or O")
        player = input("Whose turn is it? [X/O]: ").lower()
    
    pl = -1 if player == "x" else 1
    move, _ = minimax(board, 9, pl, -1000, 1000)
    x, y = move
    print(move)
    
    cell_index = x * 3 + y
    cell_coords = cell_coordinates[cell_index]
    
    draw_symbol(image, cell_coords, player.upper())
    
    cv2.imshow("Result", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
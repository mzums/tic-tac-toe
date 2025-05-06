import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from main import preprocess, divide_cells
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'minimax')))
from minimax.main import get_ai_move

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'bmp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def resize_image(image):
    h, w = image.shape[:2]
    new_width = 200
    new_height = int(h * (new_width / w))
    return cv2.resize(image, (new_width, new_height))

def draw_symbol(image, cell_coords, symbol):
    x1, y1, x2, y2 = cell_coords
    cell_w = x2 - x1
    cell_h = y2 - y1
    
    size = int(min(cell_w, cell_h) * 0.3)
    thickness = int(max(1, size // 5))
    
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    if symbol == 'X':
        cv2.line(image, 
                (center_x - size, center_y - size),
                (center_x + size, center_y + size),
                (0, 0, 255), thickness)
        cv2.line(image, 
                (center_x - size, center_y + size),
                (center_x + size, center_y - size),
                (0, 0, 255), thickness)
    elif symbol == 'O':
        cv2.circle(image, 
                  (center_x, center_y), 
                  size, 
                  (0, 0, 255), 
                  thickness)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if not file or not allowed_file(file.filename):
        return "Invalid file"

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    original_filename = f"{timestamp}_original.jpg"
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    file.save(original_path)

    try:
        grid_coords, board = preprocess(original_path)
    except Exception as e:
        return f"Error processing: {str(e)}"

    current_state = np.array(board, dtype=int)
    player = -1 if request.form.get('player') == 'X' else 1

    try:
        best_move = get_ai_move(current_state)
        row, col = best_move
    except Exception as e:
        return f"Błąd AI: {str(e)}"

    image = cv2.imread(original_path)
    image = resize_image(image)
    
    _, cell_coords = divide_cells(*grid_coords, image, draw=False)
    
    cell_index = row * 3 + col
    symbol = 'O' if player == 1 else 'X'
    draw_symbol(image, cell_coords[cell_index], symbol)

    result_filename = f"{timestamp}_result.jpg"
    result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
    cv2.imwrite(result_path, image)

    return render_template('result.html',
                         original=original_filename,
                         result=result_filename,
                         move=(row+1, col+1),
                         player=symbol)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
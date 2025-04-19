from cv.main import *
from minimax.main import *


if __name__ == '__main__':
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp'}

    if len(sys.argv) < 2:
        print("Usage: python -m cv.main <path_to_image>")
        sys.exit(1)
        
    image_path = sys.argv[1]
    if not any(image_path.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        print("Unsupported file format")
        sys.exit(1)
        
    board = preprocess(image_path)

    player = input("Whose turn is it? [X/O]: ").lower()
    pl = -1 if player == "x" else 1
    move, _ = minimax(board, 9, pl, -1000, 1000)
    x, y = move
    print(move)

import argparse
from ascc import ascii_display  # 換成您模組中負責執行 ASCII 顯示的函數

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display ASCII art animation.")
    parser.add_argument('--path', type=str, required=True, help="The path to the GIF or MP4 file.")
    parser.add_argument('--width', type=int, default=100, help="The width of the ASCII art.")
    parser.add_argument('--sec', type=float, default=0.1, help="The delay between frames in seconds.")

    args = parser.parse_args()
ascii_display(args.path, args.width, args.sec)

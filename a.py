import os
import cv2
from time import sleep


def move (y, x):
    print("\033[%d;%dH" % (y, x))

def print_frame(vid):
    success, frame = vid.read()
    terminal_window_size = (
        os.get_terminal_size().columns,
        os.get_terminal_size().lines,
    )

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_resize = cv2.resize(
        frame,
        (
            int(terminal_window_size[1] * frame.shape[1] / frame.shape[0]),
            terminal_window_size[1],
        ),
    )
    _, frame_resize = cv2.threshold(frame_resize, 20, 255, cv2.THRESH_BINARY)
    frame_symbols = ""

    for i in range(frame_resize.shape[0]):
        frame_symbols += " " * int(
            (terminal_window_size[0] - frame_resize.shape[1]) / 4
        )
        for j in range(frame_resize.shape[1]):
            if frame_resize[i, j] != 0:
                frame_symbols += "WW"
            else:
                frame_symbols += "  "
        frame_symbols += "\n"
    print(frame_symbols, end='\r', flush=True)
    move(0, 0)
    return success


if __name__ == "__main__":
    vid = cv2.VideoCapture("bad_apple.mp4")
    success = print_frame(vid)
    while success:
        sleep(0.018)
        success = print_frame(vid)

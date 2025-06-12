"""
===============================================================================
File: calibrate.py
Author: Joel Jojo Painuthara <joeljojop@gmail.com>
Created: 11 June 2025
Description: Minesweeper game window calibration tool
===============================================================================
"""

import pyautogui
import cv2
import numpy as np
import time
import json

rows = 16
cols = 16
tile_gap = 24
start_x = 255
start_y = 216
face = [440, 179]
mines = 99

def change_rows(x):
    global rows
    rows = x

def change_cols(x):
    global cols
    cols = x

def change_start_x(x):
    global start_x
    start_x = x

def change_start_y(x):
    global start_y
    start_y = x

def change_face_x(x):
    global face
    face[0] = x

def change_face_y(x):
    global face
    face[1] = x

def change_mines(x):
    global mines
    mines = x

try:
    cal_data = None
    with open('calibration_data.json', 'r') as f:
        cal_data = json.load(f)
    rows = cal_data['rows']
    cols = cal_data['cols']
    start_x = cal_data['start_x']
    start_y = cal_data['start_y']
    face[0] = cal_data['face_x']
    face[1] = cal_data['face_y']
    mines = cal_data['mines']
except:
    pass

# Allow time to switch to the Minesweeper window
print("\nTo save calibration data press 's'")
print("To exit without saving press 'q'")
input("Press enter and switch to the Minesweeper window within 5 seconds...\n")
time.sleep(5)

# Take a screenshot of the Minesweeper game
screenshot = pyautogui.screenshot()

cv2.namedWindow("Calibration", cv2.WINDOW_NORMAL)
cv2.createTrackbar("Rows", "Calibration", rows, 20, change_rows)
cv2.createTrackbar("Columnss", "Calibration", cols, 45, change_cols)
cv2.createTrackbar("Start X", "Calibration", start_x, 500, change_start_x)
cv2.createTrackbar("Start Y", "Calibration", start_y, 500, change_start_y)
cv2.createTrackbar("Face X", "Calibration", face[0], 1000, change_face_x)
cv2.createTrackbar("Face Y", "Calibration", face[1], 1000, change_face_y)
cv2.createTrackbar("Mines", "Calibration", mines, 100, change_mines)

try:
    while True:
        image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        for i in range(rows):
            for j in range(cols):
                x = start_x + (tile_gap * j)
                y = start_y + (tile_gap * i)
                if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
                    image[y][x] = [0, 255, 0]
        image[face[1]][face[0]] = [0, 0, 255]
        cv2.imshow("Image", image)
        keypress = cv2.waitKey(1)
        if keypress & 0xFF == ord('s'):
            calibration_data = {
                "rows": rows,
                "cols": cols,
                "start_x": start_x,
                "start_y": start_y,
                "face_x": face[0],
                "face_y": face[1],
                "mines": mines
            }
            with open("calibration_data.json", "w") as f:
                json.dump(calibration_data, f, indent=4)
            print("\033[92mCalibration data saved to 'calibration_data.json'\033[00m\n")
            break
        elif keypress & 0xFF == ord('q'):
            print("\033[93mCalibration cancelled...\033[00m\n")
            break
    cv2.destroyAllWindows()
except KeyboardInterrupt:
    print("\033[91mCalibration interrupted...\033[00m\n")
    cv2.destroyAllWindows()
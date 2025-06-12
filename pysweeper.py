"""
===============================================================================
File: pysweeper.py
Author: Joel Jojo Painuthara <joeljojop@gmail.com>
Created: 11 June 2025
Description: Automated Minesweeper solver using pyautogui and OpenCV.
===============================================================================
"""

import pyautogui
import cv2
import numpy as np
import time
import json
import sys

rows = 16
cols = 30
mines = 99
tile_gap = 24
start_x = 255
start_y = 216
char_pixel_gap_x = 13
char_pixel_gap_y = 18
face = [608, 179]

# Initialize minefield matrix
# The minefield is a 2D list where each cell represents a tile in the
# Minesweeper game:
# 1-8 represent numbers on the tiles,
# 0 represents unrevealed tiles,
# -1 represents revealed tiles (or numbered tiles that have been processed),
# -2 represents marked tiles.
minefield = [[0 for _ in range(cols)] for _ in range(rows)]

# Color code for the Minesweeper characters (BGR Format)
one = [255, 0, 0]
two = [0, 128, 0]
three = [0, 0, 255]
four = [128, 0, 0]
five = [0, 0, 128]
six = [128, 128, 0]
seven = [0, 0, 0]
eight = [128, 128, 128]
revealed = [128, 128, 128]

game_over = False
marked_tiles = 0
image = None
show_log = False

# Function to get the current state of the minefield from the screenshot
def get_minefield_data():
    global minefield, game_over
    for i in range(cols):
        for j in range(rows):
            if minefield[j][i] != 0:
                continue
            x = start_x + (tile_gap * i)
            y = start_y + (tile_gap * j)
            char_x = x + char_pixel_gap_x
            char_y = y + char_pixel_gap_y
            char_color = list(image[char_y][char_x])
            tile_color = list(image[y][x])
            if char_color == one:
                minefield[j][i] = 1
            elif char_color == two:
                minefield[j][i] = 2
            elif char_color == three:
                minefield[j][i] = 3
            elif char_color == four:
                minefield[j][i] = 4
            elif char_color == five:
                minefield[j][i] = 5
            elif char_color == six:
                minefield[j][i] = 6
            elif char_color == seven:
                if tile_color == [255, 255, 255]:
                    minefield[j][i] = -2
                else:
                    minefield[j][i] = 7
            elif char_color == eight:
                minefield[j][i] = 8
            elif tile_color == revealed:
                minefield[j][i] = -1
    if list(image[face[1]][face[0]]) != [0, 0, 0]:
        game_over = True

# Function to find and reveal tiles based on the current state of the minefield
def find_mine():
    global minefield, marked_tiles
    run_loop = True
    is_clicked = False
    probability_field = [[0 for _ in range(cols)] for _ in range(rows)]
    while run_loop:
        probability_field = [[0 for _ in range(cols)] for _ in range(rows)]
        run_loop = False
        for i in range(cols):
            for j in range(rows):
                if minefield[j][i] <= 0:
                    continue
                marker_count = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if x == 0 and y == 0:
                            continue
                        if 0 <= i + x < cols and 0 <= j + y < rows:
                            if minefield[j + y][i + x] == -2:
                                marker_count += 1
                if marker_count == minefield[j][i]:
                    minefield[j][i] = -1
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if x == 0 and y == 0:
                                continue
                            if 0 <= i + x < cols and 0 <= j + y < rows:
                                if minefield[j + y][i + x] == 0:
                                    pyautogui.leftClick(start_x + char_pixel_gap_x + (tile_gap * (i + x)), start_y + (tile_gap * (j + y)))
                                    is_clicked = True
                                    if show_log:
                                        print("Revealing tile at:", (i + x, j + y))
                    run_loop = True
                else:
                    options = []
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if x == 0 and y == 0:
                                continue
                            if 0 <= i + x < cols and 0 <= j + y < rows:
                                if minefield[j + y][i + x] == 0:
                                    options.append((i + x, j + y))
                    if len(options) == minefield[j][i] - marker_count:
                        for option in options:
                            minefield[option[1]][option[0]] = -2
                            pyautogui.rightClick(start_x + char_pixel_gap_x + (tile_gap * option[0]), start_y + (tile_gap * option[1]))
                            marked_tiles += 1
                            if show_log:
                                print("Marking tile at:", option)
                        is_clicked = True
                        run_loop = True
                    else:
                        for option in options:
                            probability_field[option[1]][option[0]] += 1
    if not is_clicked:
        min_probability = 10
        min_tile = None
        for i in range(cols):
            for j in range(rows):
                if minefield[j][i] == 0 and probability_field[j][i] < min_probability and probability_field[j][i] > 0:
                    min_probability = probability_field[j][i]
                    min_tile = (i, j)
        if min_tile is not None:
            pyautogui.leftClick(start_x + char_pixel_gap_x + (tile_gap * min_tile[0]), start_y + (tile_gap * min_tile[1]))
            if show_log:
                print("Revealing tile (prob) at:", min_tile)

# Function to reset the minefield and game state
def reset_minefield():
    global minefield, marked_tiles, game_over
    minefield = [[0 for _ in range(cols)] for _ in range(rows)]
    marked_tiles = 0
    game_over = False

# Import calibration data
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
    print("\033[91mFailed to fetch calibration data...Run calibrate.py\033[00m")
    exit()

if len(sys.argv) > 1 and sys.argv[1] == '-v':
    show_log = True
    print("\033[93mVerbose mode enabled. Logging actions...\033[00m")

input("\nPress enter and switch to Minesweeper window within 5 seconds...")

# Allow time to switch to the Minesweeper window
time.sleep(5)

# Start the game by clicking the first tile
pyautogui.leftClick(start_x + char_pixel_gap_x, start_y)

# Main loop to continuously check the minefield and perform actions
try:
    while True:
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        get_minefield_data()
        if game_over:
            print("\033[93mGame Over! Retrying...\033[00m")
            time.sleep(1)
            pyautogui.click(face[0], face[1])
            reset_minefield()
            pyautogui.leftClick(start_x + char_pixel_gap_x, start_y)
            continue
        find_mine()
        if marked_tiles >= mines:
            print("\033[92mAll mines marked!\033[00m\n")
            break
        pyautogui.moveTo(100, 300)
except:
    print("\033[91mFailsafe triggered! Exiting...\033[00m\n")
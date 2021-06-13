import socket
import threading
import pygame as pg
import math
import sys
import numpy as np

TOTAL_ROWS = 6
TOTAL_COLUMN = 7
plum = (221, 160, 221)
black = (0, 0, 0)
red = (240, 0, 0)
green = (0, 240, 0)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 2049))  # change port number if already occupied

def create_board():
    board = np.zeros((TOTAL_ROWS, TOTAL_COLUMN))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def get_open_row(board, col):
    for row in range(TOTAL_ROWS):
        if board[row][col] == 0:
            return row


def draw_bord():
    draw_board(board)
    pg.display.update()


def twofour():
    game_over = False
    turn = 0

    while not game_over:
        isvalid = False
        input1 = sock.recv(100)
        input1 = input1.decode().strip()
        print(input1)
        if "player 1" in input1:
            turn = 0
        elif "player 2" in input1:
            turn = 1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                # player 1 input
                if turn == 0:
                    posi = event.pos[0]
                    col = int(math.floor(posi / Square))
                    sock.sendall(str(col).encode())

                    input = sock.recv(100)

                    input = input.decode().strip()
                    print(input)
                    if "accept" in input:
                        isvalid = True
                    elif "reject" in input:
                        isvalid = False

                    elif "win player 1" in input:
                        print(input)
                        game_over = True

                    elif "Player 2 wins!" in input:
                        print(input)
                        game_over = True

                    if isvalid:
                        row = get_open_row(board, col)
                        drop_piece(board, row, col, 1)

                # player 2 input
                else:
                    posi = event.pos[0]
                    col = int(math.floor(posi / Square))
                    sock.sendall(str(col).encode())
                    input = sock.recv(100)
                    input = input.decode().strip()
                    print(input)
                    if "accept" in input:
                        isvalid = True
                    elif "reject" in input:
                        isvalid = False

                    elif "win player 2" in input:
                        print(input)
                        game_over = True

                    elif "Player 1 wins!" in input:
                        print(input)
                        game_over = True

                    if isvalid:
                        row = get_open_row(board, col)
                        drop_piece(board, row, col, 2)

                draw_board(board)
                turn += 1
                turn = turn % 2


def connect_clients():
    while True:
        threading.Thread(target=twofour).start()

# The follwoing fuction actually draws the board on out pygame GUI
def draw_board(board):
    for col in range(TOTAL_COLUMN):
        for row in range(TOTAL_ROWS):
            pg.draw.rect(screen, plum, (col * Square, row * Square + Square, Square, Square))
            pg.draw.circle(screen, black, (
                int(col * Square + Square / 2), int(row * Square + Square + Square / 2)), RADIUS)

    for col in range(TOTAL_COLUMN):
        for row in range(TOTAL_ROWS):
            if board[row][col] == 1:
                pg.draw.circle(screen, red, (
                    int(col * Square + Square / 2), Height - int(row * Square + Square / 2)), RADIUS)
            elif board[row][col] == 2:
                pg.draw.circle(screen, green, (
                    int(col * Square + Square / 2), Height - int(row * Square + Square / 2)), RADIUS)
    pg.display.update()

board = create_board()
pg.init()

Square = 100
Width = TOTAL_COLUMN * Square
Height = (TOTAL_ROWS + 1) * Square # We will need ROWS + 1 for displaying 6 rows
Size = (Width, Height)
RADIUS = int(Square / 2 - 4)

screen = pg.display.set_mode(Size)  # setting the size of the display
draw_board(board)                   # calling the function to draw the board
pg.display.update()                 # updating the board
connect_clients()                   # calling the function to connect the clients

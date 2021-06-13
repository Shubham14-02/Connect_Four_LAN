import socket
import threading
import numpy as np

TOTAL_ROWS = 6  # number of total rows
TOTAL_COLUMN = 7  # number of total columns

# Here, we will make the socket named 'server' for convenience of using it
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 2049)) # change port number if already occupied
server.listen(5)  # Allow up to 5 queued connections


# Below written is the main fucntion which will deal with inputs, value checking, stripping, etc
def two_four(client_one, client_two):
    game_over = False  # game_over is the indicator of the game's status and by default, game_over will be false
    turn = 0  # turn is the indicator of whose turn there is, and it will be zero by default

    while not game_over:
        # player 1 input
        if turn == 0:

            str1 = "Enter your choice, player 1: "
            client_one.sendall(str1.encode())
            input1 = client_one.recv(100)
            # Checking for input validation
            if len(input1.decode().strip()) == 0:
                continue
            col = int(input1.decode().strip())
            input1 = ''

            if is_valid_pos(board, col):
                row = get_open_row(board, col)
                drop_piece(board, row, col, 1)

                if wins(board, 1):
                    str = "You win player 1! "
                    client_one.sendall(str.encode())
                    client_two.sendall(("Player 1 wins!").encode())
                    game_over = True
            else:
                continue

        # player 2 input
        else:

            str2 = "Enter your choice, player 2: "
            client_two.sendall(str2.encode())
            input2 = client_two.recv(100)
            # Checking for input validation
            if len(input2.decode().strip()) == 0:
                continue

            col = int(input2.decode().strip())
            input2 = ''
            if is_valid_pos(board, col):
                row = get_open_row(board, col)
                drop_piece(board, row, col, 2)

                if wins(board, 2):
                    client_two.sendall(("You win player 2! ").encode())
                    client_one.sendall(("Player 2 wins! ").encode())
                    game_over = True
            else:
                continue

        print(print_board(board))
        turn += 1
        turn = turn % 2


# function connect_clients() will connect two clients with the server
# we will use the thread in this function for two_four(client_one, client_two) with it's arguments
def connect_clients():
    while True:  # Just keep accepting pairs of connections!
        (client_one, add_one) = server.accept()
        print("Accepted client A:" + str(add_one))
        (client_two, add_two) = server.accept()
        print("Accepted client B:" + str(add_two))
        threading.Thread(target=two_four, args=(client_one, client_two)).start()


# the following function creates the board as we see
def create_board():
    board = np.zeros((TOTAL_ROWS, TOTAL_COLUMN))
    return board

# the following function updates the board after every valid/successful input
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# the function is_valid_pos(board, col) checks if the position (col) entered is valid
def is_valid_pos(board, col):
    if (col < 0 or col > 6):
        return False
    else:
        return board[TOTAL_ROWS - 1][col] == 0


# the function get_open_row(board, col) will give the next available row
def get_open_row(board, col):
    for row in range(TOTAL_ROWS):
        if board[row][col] == 0:
            return row


# the function print_board(board) will return a flipped board we can see.
# We use 'flip' as in connect four, direction is bottom to top
def print_board(board):
    return np.flip(board, 0)


# the function wins(board, piece) will check if either of the players are winning
def wins(board, piece):
    # check horizontal series for winner
    for col in range(TOTAL_COLUMN - 3):
        for row in range(TOTAL_ROWS):
            if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and board[row][
                col + 3] == piece:
                return True

    # check vertical series for winner
    for col in range(TOTAL_COLUMN):
        for row in range(TOTAL_ROWS - 3):
            if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and board[row + 3][
                col] == piece:
                return True

    # check ascending diagonals for win
    for col in range(TOTAL_COLUMN - 3):
        for row in range(3, TOTAL_ROWS):
            if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and board[row - 3][
                col + 3] == piece:
                return True

    # check descending diagonals for winner
    for col in range(TOTAL_COLUMN - 3):
        for row in range(TOTAL_ROWS - 3):
            if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece and board[row + 3][
                col + 3] == piece:
                return True


board = create_board()
connect_clients()
print(print_board(board))

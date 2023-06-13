import numpy as np
import time
from alphaBeta import Alphabeta

# print out the array in the required format 
def print_board(board):
    print("  ", end="")
    for x in range(1, 9):
        print(x, end=" ")
    print()

    for x, row in enumerate(board):
        print(chr(65 +  x), " ".join(row))


# given a letter and a number, it will return the matching array coords 
def get_coord(user_input):
    if len(user_input) != 2:
        return (-1,-1)
    if user_input[0] < 'a' or user_input[0] > 'h' or user_input[1] < '1' or user_input[1] > '8':
        return (-1,-1)
    r = ord(user_input[0]) - ord('a')
    c = int(user_input[1]) - 1
    return (r, c)


# will prompt the user for a move and has error handling
def get_input(board):
    while True:
        user_input = input("Choose your next move: ")
        coord = get_coord(user_input.lower())
        if coord[0] == -1:
            print("Not a legal move!")

        elif board[coord[0]][coord[1]] != '-':
            print("Move already taken!")
        else:
            return coord

# if there is a winner, will return the the piece of the winner. 
def check_winner(board):

    # check for a horizontal 4 in a line
    for r in board:
        for c in range(len(r) - 3):
            if r[c] == r[c + 1] == r[c + 2] == r[c + 3] and r[c] != '-':
                return r[c]

    # check for vertical 4 in a line
    for c in range(len(board[0])):
        for r in range(len(board) - 3):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] and board[r][c] != '-':
                return board[r][c]
    
    # check if the board is full 
    spots_left = False
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == '-':
                spots_left = True
    if spots_left == False:
        return "full"

# prompts the user it they want to go first
def intro():
    while True:
        user_input = input("Would you like to go first? (y/n) : ")
        if user_input.lower() == 'y':
            print()
            return 1
        elif user_input.lower() == 'n':
            print()
            return 2
        else:
            print("Invalid reponse")

# prompts the user for how long the alpha-beta algorithm should run for
def time_question():
     while True:
        try:
            evaluation_time = float(input("How long should the computer think about its move (in seconds)? : "))
        except ValueError:
            print("You must enter a valid number.")
        else: 
            if evaluation_time > 0:
                print()
                return evaluation_time
            else:
                print("The number must be greater than 0")

# runs the game
def play():

    # asks the starting question 
    turn = intro()
    et = time_question()
    
    # stores the values needed to determine who is going first
    original = False
    user_piece = 'X'
    if turn == 2:
        original = True
        user_piece = 'O'

    # initialized an empty board
    initial_board = np.full((8,8), "-")
    print_board(initial_board)

    while True:
        
        # checks if a player has won or if the board is full 
        winner = check_winner(initial_board)
        if winner == "full":
            print()
            print("You tied!")
            break
        if winner != None:
            if user_piece == winner:
                print()
                print("You won!")
            else:
                print()
                print("You lost!")
            break


        if turn == 1:

            # asks the user for a move and updates the board accordingly 
            coord = get_input(initial_board)
            initial_board[coord[0]][coord[1]] = user_piece
            print()
            print_board(initial_board)

            # changes the turn for the next loop
            turn = 2

        elif turn == 2:   
            # sets the inital values needed for the algorithm
            depth = 4
            alpha =float("-inf")
            beta = float("inf")
            maximizing_player = original
            timer = time.time() 
            time_limit = et
        
            # finds the best move and updates the board accordingly
            best_move = Alphabeta().alpha_beta_pruning(initial_board, depth, alpha, beta, maximizing_player, timer, time_limit)
            initial_board = best_move[1]

            print()
            print_board(initial_board)

            # changes the turn for the next loop
            turn = 1


def main():
    play()

if __name__=="__main__":
    main()



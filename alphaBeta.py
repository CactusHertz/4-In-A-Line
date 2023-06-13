import numpy as np
import time


class Alphabeta():
    def __init__(self):
        pass
    
    # get the possible board for each valid move
    def possible_boards(self, board, maximizing_player):
        boards = []
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] == '-':
                    new_board = np.copy(board)
                    if maximizing_player:
                        new_board[r][c] = 'X'
                    else:
                        new_board[r][c] = 'O'
                    boards.append(new_board)
        boards = np.array(boards)
        return boards

    # checks if a terminal state has been reached 
    def check_terminal(self, board):
        # horizontal check
        for r in board:
            for c in range(len(r) - 3):
                if r[c] == r[c + 1] == r[c + 2] == r[c + 3] and r[c] != '-':
                    return True
        # vertical check 
        for c in range(len(board[0])):
            for r in range(len(board) - 3):
                if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] and board[r][c] != '-':
                    return True

        # board full check
        spots_left = False
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] == '-':
                    spots_left = True
        if spots_left == False:
            return True
        
        return False

    # judges the score of a given board 
    def evaluate(self, board):
        score = 0
        for r in range(len(board)):
            for c in range(len(board[0])-3):
                # creates a horizontal 4 cell area
                box = board[r][c:c+4]

                # counts the number of Xs and Os in a box
                count_o = 0
                count_x = 0
                for cell in box:
                    if cell == 'X':
                        count_x += 1
                    if cell == 'O':
                        count_o += 1
                
                # there is no mix of pieces, will give more points for each piece
                if count_o == 0:
                    if count_x == 1:
                        score += 1
                    elif count_x == 2:
                        score += 100
                    elif count_x == 3:
                        score += 1000
                    elif count_x == 4:
                        score += 10000000
                if count_x == 0:
                    if count_o == 1:
                        score -= 1
                    elif count_o == 2:
                        score -= 100
                    elif count_o == 3:
                        score -= 1000
                    elif count_o == 4:
                        score -= 10000000

                # give priority to defense by giving more score if the minority in a box.
                if count_x == 1 and count_o > 1:
                        score += 1001
                        if count_o == 3:
                            score += 100000
                if count_o == 1 and count_x > 1:
                        score -= 1001
                        if count_x == 3:
                            score -= 100000
    
        for r in range(len(board)-3):
            for c in range(len(board[0])):
                # creates a vertical 4 cell area
                box = [board[r+i][c] for i in range(4)]

                # counts the number of Xs and Os in a box
                count_o = 0
                count_x = 0
                for cell in box:
                    if cell == 'X':
                        count_x += 1
                    if cell == 'O':
                        count_o += 1
                
                 # there is no mix of pieces, will give more points for each piece
                if count_o == 0:
                    if count_x == 1:
                        score += 1
                    elif count_x == 2:
                        score += 100
                    elif count_x == 3:
                        score += 1000
                    elif count_x == 4:
                        score += 10000000
                if count_x == 0:
                    if count_o == 1:
                        score -= 1
                    elif count_o == 2:
                        score -= 100
                    elif count_o == 3:
                        score -= 1000
                    elif count_o == 4:
                        score -= 10000000

                # give priority to defense by giving more score if the minority in a box.
                if count_x == 1 and count_o > 1:
                    score += 1001
                    if count_o == 3:
                        score += 100000
                if count_o == 1 and count_x > 1:
                    score -= 1001
                    if count_x == 3:
                        score -= 100000
        return score

    # implementation fo the alpha beta pruning algorithm
    def alpha_beta_pruning(self, board, depth, alpha, beta, maximizing_player, timer, time_limit):
        # checks if a base case has been reached and return the evaluation of the board
        if depth == 0 or self.check_terminal(board) or time.time() - timer >= time_limit:
            return self.evaluate(board), None
        
        # max player will search for the highest score and will prune branches
        if maximizing_player:
            maxEval = float("-inf")
            best_board = None
            for b in self.possible_boards(board, True):
                eval, _ = self.alpha_beta_pruning(b, depth - 1, alpha, beta, False, timer, time_limit)
                # stores the current board in the serach, if the highest evalutation if found
                if maxEval < eval:
                    maxEval = eval 
                    best_board = b
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, best_board

        # min player will search for the lowest score and will prune branches
        else:
            minEval = float("inf")
            best_board = None
            for b in self.possible_boards(board, False):
                eval, _ = self.alpha_beta_pruning(b, depth - 1, alpha, beta, True, timer, time_limit)
                # stores the current board in the serach, if the lowest evalutation if found 
                if minEval > eval:
                    minEval = eval
                    best_board = b
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval, best_board
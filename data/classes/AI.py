import random
from classes.Const import ROWS, COLS
from classes.Game import Game


class AI:
    '''
     AI class
     contains the AI logic for the game
    '''    
    def __init__(self, game: Game, color):
        '''
        __init__ _summary_

        Args:
            game (Game): the game object that this AI is playing
            color (_type_): the color of the game object that this AI is playing
        '''        
        self.game = game
        self.color = color

    # Get list of valid moves from Game class
    def get_all_valid_moves(self):
        '''
        get_all_valid_moves 

        Returns:
            _type_: list of valid moves from Game class.
        '''        
        valid_moves = []
        check_avoiding_moves = []

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.game.squares[row][col].piece
                if piece and piece.color == self.color:
                    self.game.calc_moves(piece, row, col, bool=True)
                    for move in piece.moves:
                        if self.game.valid_move(piece, move):
                            if self.game.in_check(piece, move):
                                check_avoiding_moves.append((piece, move))
                            else:
                                valid_moves.append((piece, move))

        return check_avoiding_moves, valid_moves

    # Dumb AI 
    # Makes a random move from the valid move list
    def make_random_move(self):
        '''
        make_random_move 

        Returns:
            _type_: random move from the valid move list.
        '''        
        check_avoiding_moves, valid_moves = self.get_all_valid_moves()

        if check_avoiding_moves:
            piece, move = random.choice(check_avoiding_moves)
        elif valid_moves:
            piece, move = random.choice(valid_moves)
        else:
            return False

        self.game.move(piece, move)

        return True

    # Smarter AI
    # Minimax with Alpha-Beta Pruning
    def minimax(self, depth, alpha, beta, maximizing_player):
        '''
        minimax

        Args:
            depth (_type_): The depth of the minimax object to be used for minimax calculations.
            alpha (_type_): The alpha of the minimax object to be used for minimax calculations.
            beta (_type_): The beta of the minimax object to be used for minimax calculations.
            maximizing_player (_type_): The maximum number of players to be minimaxed for minimax calculations.

        Returns:
            _type_: The type of minimax object to be used for minimax calculations based on the depth. The type is determined by the maximizing_player parameter. 
        '''        
        if depth == 0:
            return evaluate_board()

        if maximizing_player:
            max_eval = float("-inf")
            for move in self.get_all_valid_moves()[1]:
                piece, move = move
                self.game.move(piece, move)
                score = self.minimax(depth - 1, alpha, beta, False)
                if score is not None:
                    max_eval = max(max_eval, score)
                    if max_eval >= beta:
                        break
            return max_eval if max_eval != float("-inf") else None
        
        else:   # Minimizing player
            min_eval = float("inf")
            for move in self.get_all_valid_moves()[0]:
                piece, move = move
                self.game.move(piece, move)
                score = self.minimax(depth - 1, alpha, beta, True)
                if score is not None:
                    min_eval = min(min_eval, score)
                    if min_eval <= alpha:
                        break
            return min_eval if min_eval != float("inf") else None
            
    def evaluate_board(self):
        '''
        evaluate_board 
        This function is called when to evaluate the board. 
        All the pieces have a specific score and the move determines the score based on the current state of the board.
        
        Returns:
            _type_: The value of the board after minimax calculations. The value is determined by the maximizing_player parameter. 
        '''        
        ai_score = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.game.squares[row][col].piece
                if piece and piece.color == self.color:
                    ai_score += piece.value

        return ai_score


    def make_smart_move(self, depth):
        '''
        make_smart_move

        Args:
            depth (_type_): The depth to make the move from (integer or float or None for default value of depth value in seconds to make the move from the best possible move).
        '''        
        best_move = None
        best_score = float("-inf")

        for move in self.get_all_valid_moves()[1]:
            piece, move = move
            self.game.move(piece, move)
            score = self.minimax(depth - 1, float("-inf"), float("inf"), True)
            if score > best_score:
                best_score = score
                best_move = move

        if best_move is not None:
            self.game.move(piece, best_move)

import copy

from classes.Const import *
from classes.Square import Square
from classes.Piece import *
from classes.Move import Move


class Game:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.turn = 'white'
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        
    def move(self, piece, move, testing=False):
        '''
        move _summary_
        This function is used to move a piece to a new square and returns the move. The move should be an instance of Move.

        Args:
            piece (_type_):  The piece to move to the new square and return the move.
            move (_type_): The move to make with the piece to the new square
            testing (bool, optional): _description_. Defaults to False.
        '''        
        initial = move.initial
        final = move.final

        # check if the piece is already in the square and if it is not then return False.
        en_passant_empty = self.squares[final.row][final.col].isempty()

        # console game move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if piece.name == 'pawn':
            # en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console game move update          
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece

            # pawn promotion
            self.check_promotion(piece, final)

        # king castling
        if piece.name == 'king':
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # last move
        self.last_move = move

    def valid_move(self, piece, move):
        '''
        valid_move 

        This function is called to check if a piece is valid and if it is not then return False.

        Args:
            piece (_type_): The piece to check against the piece list.
            move (_type_): The move to check against the piece list

        Returns:
            _type_: The square where the piece is valid and the piece list is valid.
        '''        
        dest_piece = self.squares[move.final.row][move.final.col].piece
        # If the destination square is empty or contains an opponent's piece, the move is valid
        if dest_piece is None or dest_piece.color != piece.color:
            return move in piece.moves
        # If the destination square contains a piece of the same color, the move is invalid
        return False

    def check_promotion(self, piece, final):
        '''
        check_promotion 
        This function checks the promotion of a pawn against the destination square and returns True if the promotion is valid.

        Args:
            piece (_type_): The piece to check
            final (_type_): The promotion of the piece against the destination square and returns True if the promotion is valid.
        '''        
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        '''
        castling

        Args:
            initial (_type_): The initial check for castling of the king and rooks.
            final (_type_): the final check for castling of the king and rooks.

        Returns:
            _type_: The type of the castling of the king and rooks.
        '''        
        return abs(initial.col - final.col) == 2
    
    def set_true_en_passant(self, piece):
        '''
        set_true_en_passant

        This function is called by pawn to set the true value of the piece on the board and return the piece value of the piece.

        Args:
            piece (_type_): The piece to set true for.
        '''        

        if piece.name != 'pawn':
            return
        
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False

        piece.en_passant = True

    def in_check(self, piece, move, print_message=False):
        '''
        in_check

        This function is called when the piece has been moved to a new position.
        It checks if the piece had put the enemy king in check.

        Args:
            piece (_type_): The piece to check against the enemy king.
            move (_type_): The move to check against the enemy king
            print_message (bool, optional): Message that is being printed only whn a king is in check. Defaults to False.

        Returns:
            _type_: The type of piece to 
        '''        
        temp_piece = copy.deepcopy(piece)
        temp_game = copy.deepcopy(self)
        temp_game.move(temp_piece, move, testing=True)
        for row in range(ROWS):
            for col in range(COLS):
                if temp_game.squares[row][col].has_rival_piece(piece.color):
                    p = temp_game.squares[row][col].piece
                    temp_game.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            if print_message:
                                print(f'{p.color} is in check')
                            return True            
        return False
    
    def is_checkmate(self, color):
        '''
        is_checkmate 

        This function returns True if the given color is checkmate.

        Args:
            color (_type_): The color to check if it is a checkmate.

        Returns:
            _type_: Returns True if the given color is a checkmate. False otherwise.
        '''        
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.squares[row][col].piece
                    if piece and piece.color == color:
                        self.calc_moves(piece, row, col, bool=True)
                        if piece.moves:
                            return False
            return True

    def calc_moves(self, piece, row, col, bool=True):
        '''
        Calculates all possible moves for a piece.
        '''
        def pawn_moves():
            # steps of pawn movement
            if piece.moved:
                steps = 1
            else:
                steps = 2

            # vertical movement
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final moves
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)

                        # create new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)
                    # blocked
                    else:
                        break
                # not in range
                else:
                    break

            # diagonal movement
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color): # noqa
                        # create initial and final moves
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece # noqa
                        final = Square(possible_move_row, possible_move_col, final_piece) # noqa
                        # create new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)

            # left en passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            if Square.in_range(col - 1) and row == r:
                if self.squares[row][col - 1].has_rival_piece(piece.color):
                    p = self.squares[row][col - 1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final moves
                            initial = Square(row, col)
                            final = Square(fr, col - 1, p)
                            # create new move
                            move = Move(initial, final)

                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
            
            # right en passant moves
            if Square.in_range(col + 1) and row == r:
                if self.squares[row][col + 1].has_rival_piece(piece.color):
                    p = self.squares[row][col + 1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final moves
                            initial = Square(row, col)
                            final = Square(fr, col + 1, p)
                            # create new move
                            move = Move(initial, final)

                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

        def knight_moves():
            possible_moves = [
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row + 1, col + 2),
                (row + 1, col - 2),
                (row - 1, col + 2),
                (row - 1, col - 2)
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color): # noqa
                        # create squares of the new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece # noqa
                        final = Square(possible_move_row, possible_move_col, final_piece) # noqa
                        # create a new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        # create squares of the new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece # noqa
                        final = Square(possible_move_row, possible_move_col, final_piece) # noqa
                        # create a new move
                        move = Move(initial, final)
                        
                        # empty squares of the new move
                        if self.squares[possible_move_row][possible_move_col].isempty(): # noqa
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

                        # has rival piece
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
                            break

                        # has team piece
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    # not in range
                    else:
                        break

                    # incrementing the row and col
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row - 1, col - 0),
                (row - 1, col + 1),
                (row + 0, col + 1),
                (row + 1, col + 1),
                (row + 1, col + 0),
                (row + 1, col - 1),
                (row + 0, col - 1),
                (row - 1, col - 1)
            ]
            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color): # noqa
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create a new move
                        move = Move(initial, final)
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)

            # castling moves
            if not piece.moved:
                # queen castling moves
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # castling not possible when pieces are inbetween the rook and the queen
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                # add left rook to the king square
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                # check potential checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR): # noqa
                                        # append new move to rook
                                        left_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    left_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

                # king castling moves
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling not possible when pieces are inbetween the rook and the queen # noqa
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                # add right rook to the king square
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                # check potential checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR): # noqa
                                        # append new move to rook
                                        right_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    right_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)
                
        if piece.name == 'pawn':
            pawn_moves()

        elif piece.name == 'knight':
            knight_moves()

        elif piece.name == 'bishop':
            straightline_moves([
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1)
            ])   

        elif piece.name == 'rook':
            straightline_moves([
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1)
            ]) 

        elif piece.name == 'queen':
            straightline_moves([
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1)
            ]) 

        elif piece.name == 'king':
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        if color == 'white':
            row_pawn, row_other = (6, 7)
        else:
            row_pawn, row_other = (1, 0)

        # Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
      
        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color))
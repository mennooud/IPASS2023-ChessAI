import pygame

from classes.Const import *
from classes.Game import Game
from classes.Dragger import Dragger
from classes.AI import AI


class Board:    

    def __init__(self):
        '''
        contains all the methods for the game board.
        '''        
        self.next_player = 'white'
        self.game = Game()
        self.dragger = Dragger()

        self.game_mode = input("Choose game mode\n1: Player vs Player\n2: Player vs Dumb AI\n3: Dumb AI vs Dumb AI\n4: Player vs AI\n5: AI vs AI\n")


    # blit methods

    def show_bg(self, surface):
        '''
        show_bg 

        Args:
            surface (_type_): the surface to blit the background to.
        '''        
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (128, 128, 128)
                else:
                    color = (96, 96, 96)

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        '''
        show_pieces

        Args:
            surface (_type_): the surface to blit the pieces to.
        '''        
        for row in range(ROWS):
            for col in range(COLS):
                if self.game.squares[row][col].has_piece():
                    piece = self.game.squares[row][col].piece
                    # all pieces except the last one
                    if piece is not self.dragger.piece:

                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        '''
        show_moves
        Args:
            surface (_type_): The surface to display the moves from.
        '''        
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                # color
                color = (200, 100, 100) if (move.final.row + move.final.col) % 2 == 0 else (200, 70, 70)
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    # other methods
    # player vs player
    def player_vs_player_turn(self):
        '''
        player_vs_player_turn

        Initializes the player versus player game mode.
        '''        
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    # player vs dumb ai
    def player_vs_dumb_ai_turn(self):
        '''
        player_vs_dumb_ai_turn 

        initializes the player versus dumb ai game mode.
        '''        
        if self.next_player == 'white':
            self.next_player = 'black'
            ai = AI(self.game, self.next_player)
            ai.make_random_move()
            self.next_player = 'white'

    # dumb ai vs dumb ai
    def dumb_ai_vs_dumb_ai_turn(self):
        '''
        dumb_ai_vs_dumb_ai_turn 

        initializes the dumb ai versus dumb ai game mode.
        '''        

        # Create AI for the current player
        ai = AI(self.game, self.next_player)
        # Make a move with the AI
        ai.make_random_move()
        # Check if the game is a checkmate
        if self.game.is_checkmate(self.next_player):
            winner = 'white' if self.next_player == 'black' else 'black'
            print(f'Checkmate! {winner} wins in {self.game.turn} turns.')
            return
        # Switch to the other player
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        # Add a delay so you can watch the game
        pygame.time.wait(250)  # delay for 1000 milliseconds (1 second)

    # player vs smarter ai
    def player_vs_smarter_ai_turn(self):
        '''
        player_vs_smarter_ai_turn

        Initializes the player versus smarter ai game mode.
        This game mode is using minimax with alpha-beta pruning. 
        '''        
        if self.next_player == 'white':
            self.next_player = 'black'
            ai = AI(self.game, self.next_player)
            ai.make_smart_move(depth=3)
            self.next_player = 'white'

    def ai_vs_ai_turn(self):
        '''
        ai_vs_ai_turn 

        Initializes the ai versus ai game mode.
        This game mode is using minimax with alpha-beta pruning.        
        '''        
        # Create AI for the current player
        ai = AI(self.game, self.next_player)
        # Make a move with the AI
        ai.make_smart_move(depth=3)
        # Check if the game is a checkmate
        if self.game.is_checkmate(self.next_player):
            winner = 'white' if self.next_player == 'black' else 'black'
            print(f'Checkmate! {winner} wins in {self.game.turn} turns.')
            return
        # Switch to the other player
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        # Add a delay so you can watch the game
        pygame.time.wait(250)  # delay for 250 milliseconds (0.25 second)
import pygame
import sys

from classes.Const import *
from classes.Board import Board
from classes.Square import Square
from classes.Move import Move
from classes.AI import AI


class Main:
    '''
     Main class
     contains the main loop
     

    '''    
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.board = Board()
        
        
    def mainloop(self):
        '''
        
        '''    
          
        screen = self.screen
        board = self.board
        game = self.board.game
        dragger = self.board.dragger
        game_mode = board.game_mode

        # to start the AI vs AI game
        if game_mode == '3':
            board.dumb_ai_vs_dumb_ai_turn()
        

        while True:
            board.show_bg(screen)
            board.show_moves(screen)
            board.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            if game_mode == '3':
                board.dumb_ai_vs_dumb_ai_turn()
            

            for event in pygame.event.get():

                # clicking on the pieces
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    
                    clicked_row = dragger.MouseY // SQSIZE
                    clicked_col = dragger.MouseX // SQSIZE

                    # clicked on a square if has a piece
                    if game.squares[clicked_row][clicked_col].has_piece():
                        piece = game.squares[clicked_row][clicked_col].piece
                        # valid color piece?
                        if piece.color == board.next_player:

                            game.calc_moves(piece, clicked_row, clicked_col, bool=True) # noqa
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods
                            board.show_bg(screen)
                            board.show_moves(screen)
                            board.show_pieces(screen)

                # mousemotion of the pieces
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        board.show_bg(screen)
                        board.show_moves(screen)
                        board.show_pieces(screen)
                        dragger.update_blit(screen)
                
                # click release of the pieces
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        released_row = dragger.MouseY // SQSIZE
                        returned_col = dragger.MouseX // SQSIZE

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, returned_col)
                        move = Move(initial, final) 
                        # check if move is valid
                        if game.valid_move(dragger.piece, move):
                            # normal move
                            game.move(dragger.piece, move)

                            game.set_true_en_passant(dragger.piece)
                            # show methods
                            board.show_bg(screen)
                            board.show_moves(screen)
                            board.show_pieces(screen)

                            # next turn
                            if game_mode == '1':
                                board.player_vs_player_turn()
                            elif game_mode == '2':
                                board.player_vs_dumb_ai_turn()
                            elif game_mode == '4':
                                board.player_vs_smarter_ai_turn()
                            elif game_mode == '5':
                                board.ai_vs_ai_turn()
                            

                            # check for checkmate
                            if game.in_check(dragger.piece, move, print_message=True):
                                if game.checkmate(dragger.piece.color):
                                    print(f'{dragger.piece.color} is in checkmate.')
                                    pygame.quit()
                                    sys.exit()

                    dragger.undrag_piece()

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()


main = Main()
main.mainloop()

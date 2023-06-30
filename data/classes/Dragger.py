import pygame

from classes.Const import *

class Dragger:
    '''
    This class is used to handle the dragging of the piece.
    '''    

    def __init__(self):
        '''
        __init__ 

        This function contains the initialization of the class.
        '''        
        self.piece = None
        self.dragging = False
        self.MouseX = 0
        self.MouseY = 0
        self.initial_row = 0
        self.initial_col = 0
    
    # blit method
    def update_blit(self, surface):
        '''
        update_blit 
        This function is used to update the blit.

        Args:
            surface (_type_): The surface to update the blit to. This should be a pygame surface.
        '''        
        # texture
        self.piece.set_texture()
        texture = self.piece.texture

        # image
        img = pygame.image.load(texture)

        # rect
        img_center = (self.MouseX, self.MouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)

        # blit
        surface.blit(img, self.piece.texture_rect)

    # other methods
    def update_mouse(self, pos):
        '''
        update_mouse
        This function is used to update the position of the mouse.

        Args:
            pos (_type_): The position of the mouse. The position should be a tuple of the form (x, y).
        '''        
        self.MouseX, self.MouseY = pos

    def save_initial(self, pos):
        '''
        save_initiall
        This function is used to save the initial position of the piece.

        Args:
            pos (_type_): The position of the mouse. The position should be a tuple of the form (x, y).
        '''        
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def drag_piece(self, piece):
        '''
        drag_piece
        This function is used to drag the piece.

        Args:
            piece (_type_): The piece to drag. This should be a Piece object.
        '''        
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        '''
        undrag_piece

        This function is used to undrag the piece.
        '''        
        self.piece = None
        self.dragging = False

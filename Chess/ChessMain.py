"""
This is our main driver file. Handles user input
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''


def LoadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        # We can access an images by now saying IMAGES['wp']


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag varible for when a move is made
    LoadImages()
    running = True
    sqSelected = ()  #no square is selected, keep track of the last click of the user( tuple: (row, column)
    playerClicks = []  #keep track of the player clicks (two tuples: [(6,4) , (4, 4)])


    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
               location = p.mouse.get_pos() #(x,y) location of mouse
               col = location[0] // SQ_SIZE
               row = location[1] // SQ_SIZE
               if sqSelected == (row, col): # when the user clicks twice means undo
                   sqSelected = () #deselcted
                   playerClicks = [] # clear player click
               else:
                   sqSelected =(row, col)
                   playerClicks.append(sqSelected) #append for both 1st and second click
               if len(playerClicks) == 2: # after 2nd click
                   move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                   print(move.getChessNotation())
                   if move in validMoves:
                       gs.makeMove(move)
                       moveMade =True
                   sqSelected = ()
                   playerClicks = []
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # UNDO WHEN Z IS PRESSEDE
                   gs.undoMove()
                   moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False




        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


# draw the squares on the board
def drawBoard(screen):
    colors = [p.Color("gray"), p.Color("light blue")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()

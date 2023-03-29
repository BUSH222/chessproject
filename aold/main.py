import numpy as np
import pygame
pygame.init()

display = pygame.display.set_mode((800, 800)) #w, h
click = pygame.time.Clock()
FPS = 50

pchars = {'K': '\u2654', 'Q': '\u2655', 'R': '\u2656', 'B': '\u2657', 'N': '\u2658', 'P': '\u2659', 'k': '\u265A', 'q': '\u265B', 'r': '\u265C', 'b': '\u265D', 'n': '\u265E', 'p': '\u265F'}
startfen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
position = np.array([['']*8]*8)


def draw_board(surface, colorlight=(232, 235, 235), colordark=(125, 135, 150), dfill=(0, 0, 0)):
    '''draws the board'''
    display.fill(dfill)
    for i in range(8):
        for j in range(8):
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                pygame.draw.rect(surface, colorlight, (i*100, j*100, 100, 100))
            else:
                pygame.draw.rect(surface, colordark, (i*100, j*100, 100, 100))

def fen_to_pos(fen):
    '''converts the inputted fen to a numpy array of the chess board; CAPITAL letters for white'''
    pos = np.array([['']*8]*8)
    _pieces = {'K': [], 'Q': [], 'R': [], 'B': [], 'N': [], 'P': [], 'k': [], 'q': [], 'r': [], 'b': [], 'n': [], 'p': []}
    fen = fen.split('/')
    for i in range(8):
        cpos = 0
        for s in fen[i]:
            if not s.isnumeric():
                pos[i, cpos] = s
                cpos += 1
                _pieces[s].append([cpos, 8-i])
            else:
                cpos += int(s)
    
    return pos

def highlight(surface, poslst, hcolor=(40, 50, 194)):
    if len(poslst) == 2:
        pygame.draw.rect(surface, hcolor, (poslst[0]*100, poslst[1]*100, 100, 100), 5)

def get_possible_moves(p, ppos, plist):
    glist = []
    if p.lower() == 'k':
        for i in range(3):
            for j in range(3):
                glist.append([i-1, j-1])
    if p.lower() == 'b':
        for i in range(7):
            glist.append([i-7, i-7])
            glist.append([-(i-7), i-7])
            glist.append([i-7, -(i-7)])
            glist.append([-(i-7), -(i-7)])
    if p.lower() == 'r':
        for i in range(7):
            glist.append([i-7, 0])
            glist.append([0, i-7])
            glist.append([-(i-7), 0])
            glist.append([0, -(i-7)])
    if p.lower() == 'q':
        for i in range(7):
            glist.append([i-7, i-7])
            glist.append([-(i-7), i-7])
            
            glist.append([i-7, -(i-7)])
            glist.append([-(i-7), -(i-7)])
            glist.append([i-7, 0])
            glist.append([0, i-7])
            glist.append([-(i-7), 0])
            glist.append([0, -(i-7)])
    if p.lower == 'n':
        glist.append(2, 1)
        glist.append(-1, 2)
        glist.append(-2, 1)
        glist.append(1, -2)
        glist.append(2, -1)
        glist.append(-1, -2)
        glist.append(-2, -1)
    if p.lower == 'p':
        if plist[ppos[0] + 1, ppos[1] + 1] != '':
            glist.append([1, 1])
        if plist[ppos[0] - 1, ppos[1] + 1] != '':
            glist.append([-1, 1])
        if plist[ppos[0], ppos[1] + 1] == '':
            glist.append([0, 1])
        if plist[ppos[0], ppos[1] + 1] == '' and plist[ppos[0], ppos[1] + 1] == '':
            glist.append([0, 2])
    





    return glist
position = fen_to_pos(startfen)


        




def game():
    wturn = True
    mpos1 = []
    mpos2 = []
    highlight1, highlight2 = False, False
    while True:
        draw_board(display)
        if highlight1: highlight(display, mpos1)
        if highlight2: highlight(display, mpos2, hcolor=(255, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == 1:
                    temp1 = pygame.mouse.get_pos()
                    mpos1 = [temp1[0]//100, temp1[1]//100]
                    highlight1 = True
                    highlight2 = False
                elif event.type == 2:
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.type == 1:
                    temp2 = pygame.mouse.get_pos()
                    mpos2 = [temp2[0]//100, temp2[1]//100]
                    highlight2 = True
                    highlight1 = False
                    if position[mpos1[1], mpos1[0]] != '' and position[mpos2[1], mpos2[0]] != position[mpos1[1], mpos1[0]]:
                        if (position[mpos1[1], mpos1[0]].isupper() and wturn) or (position[mpos1[1], mpos1[0]].islower() and not wturn):
                            position[mpos2[1], mpos2[0]] = position[mpos1[1], mpos1[0]]
                            position[mpos1[1], mpos1[0]] = ''
                            wturn = not wturn
                elif event.type == 2:
                    pass
        
        customfont = pygame.font.SysFont('segoeuisymbol', 75)

        for i in range(8):
            for j in range(8):
                if position[i, j] != '':
                    srf = customfont.render(position[i, j], False, (0, 0, 0))
                    display.blit(srf, (j*100+25, i*100+25))
                    
        
        


        


        
        pygame.display.update()
        click.tick(FPS)
game()
pygame.quit()
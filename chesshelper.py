from chess import Board
import pygame 
import os
import time
import pprint

FPS = 50
imglist = {'K': 'wKing.png', 'Q': 'wQueen.png', 'R': 'wRook.png', 'B': 'wBishop.png', 'N': 'wHorse.png', 'P': 'wPawn.png', 'k': 'bKing.png', 'q': 'bQueen.png', 'r': 'bRook.png', 'b': 'bBishop.png', 'n': 'bHorse.png', 'p': 'bPawn.png'}


class Piece():
    def __init__(self, x, y, ptype):
        self.x = x
        self.y = y
        self.ptype = ptype
        self.impostor = False
        if self.ptype.isupper():
            self.color = 'w'
        else:
            self.color = 'b'
    def truepos(self, fordrawing=False):
        if fordrawing:
            return (self.x*100+50, 800-self.y*100+50)
        return [self.x*100, 800-self.y*100]
    def draw(self, display):
        img = pygame.image.load(os.path.join(os.getcwd(), 'new', 'assets', f'{imglist[self.ptype]}'))
        img.convert()
        img = pygame.transform.scale(img, (100, 100))
        display.blit(img, self.truepos(fordrawing=False))

class ChessBoard():
    def __init__(self, display):
        self.display = display
        self.board = [[' ' for _ in range(8)] for _ in range(8)] 
        self.castling_rights = ['K', 'Q', 'k', 'q']
        self.last_pawn_move = [[0, 0],[0, 0]]
        self.wmove = True
        self.movecount = 1
        self.impostormove = 5
        self.timew = 120000
        self.timeb = 120000
        self.gameended = False
        self.impostorselected = [False, False]
    def selectimpostors(self, pcoord):
        if self.board[pcoord[1]][pcoord[0]] != ' ':
            if self.board[pcoord[1]][pcoord[0]].ptype.lower() == 'n' or self.board[pcoord[1]][pcoord[0]].ptype.lower() == 'b':
                if (self.board[pcoord[1]][pcoord[0]].color == 'w' and not self.impostorselected[0]):
                    self.board[pcoord[1]][pcoord[0]].impostor = True
                    self.impostorselected[0] = True
                if (self.board[pcoord[1]][pcoord[0]].color != 'w' and not self.impostorselected[1]):
                    self.board[pcoord[1]][pcoord[0]].impostor = True
                    self.impostorselected[1] = True
    def print_board(self):
        for s in self.board:
            for j in s:
                if j != ' ':
                    print(j.ptype, end='')
                else:
                    print(' ', end='')
            print()
        print()
    def exportfen(self, pos):
        fen = ''
        cnt = 0
        for s in pos:
            for m in s:
                if m != ' ':
                    if cnt != 0:
                        fen += str(cnt)
                        cnt = 0
                    fen += m
                else:
                    cnt += 1
            if cnt != 0:
                fen += str(cnt)
                cnt = 0
            fen += '/'
        fen = fen[:-1]
        return fen
    def importfen(self, fen):
        pos = [[' ' for _ in range(8)] for _ in range(8)] 
        fen = fen.split('/')
        for i in range(8):
            cpos = 0
            for s in fen[i]:
                if not s.isnumeric():
                    pos[i][cpos] = s
                    cpos += 1
                else:
                    cpos += int(s)
        return pos
    def create_board(self, fen):
        pos = self.importfen(fen)
        for k in range(len(pos)):
            for s in range(len(pos)):
                if pos[k][s] != ' ':
                    pos[k][s] = Piece(s, 8-k, pos[k][s])
        self.board = pos
    def draw_board(self, colorlight=(255,228,196), colordark=(205,133,63), dfill=(255,248,220)):
        #colordark=(125, 135, 150); (232, 235, 235)
        pygame.display.set_caption("Impostor chess")
        self.display.fill(dfill)
        for i in range(8):
            for j in range(8):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    pygame.draw.rect(self.display, colorlight, (i*100, j*100, 100, 100))
                else:
                    pygame.draw.rect(self.display, colordark, (i*100, j*100, 100, 100))
        pygame.draw.line(self.display, (0, 0, 0), (802, 0), (802, 800), 6)

        drawimg = pygame.image.load(os.path.join(os.getcwd(), 'new', 'assets', f'!draw.png'))
        drawimg.convert()
        resignimg = pygame.image.load(os.path.join(os.getcwd(), 'new', 'assets', f'!resign.png'))
        resignimg.convert()
        drawimg = pygame.transform.scale(drawimg, (64, 64))
        resignimg = pygame.transform.scale(resignimg, (64, 64))
        self.display.blit(drawimg, (900-32, 400-32))
        self.display.blit(resignimg, (1100-32, 400-32))
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(900-32, 400-32, 64, 64).inflate(16, 16), 5, border_radius=10)
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(1100-32, 400-32, 64, 64).inflate(16, 16), 5, border_radius=10)
        if self.impostorselected == [True, True]:
            font = pygame.font.SysFont("Arial", 30)
            img = font.render(f'Move number: {self.movecount}', True, (0, 0, 0))
            rect = img.get_rect()
            rect.center = (1000, 300)
            self.display.blit(img, rect)
            if self.impostormove - self.movecount > 0:
                img = font.render(f'Moves till the switch: {self.impostormove - self.movecount}', True, (0, 0, 0))
            else:
                img = font.render(f'The switch has happened.', True, (0, 0, 0))
            rect = img.get_rect()
            rect.center = (1000, 200)
            self.display.blit(img, rect)
        else:
            wordthing = {False:' not ', True:' '}
            wordthing2 = {0:'Black', 1:'White'}
            font0 = pygame.font.SysFont("Arial", 30)
            font = pygame.font.SysFont("Arial", 20)
            img = font0.render(f'Please select an impostor', True, (0, 0, 0))
            rect = img.get_rect()
            rect.center = (1000, 100)
            self.display.blit(img, rect)
            img = font.render(f'White\'s impostor has{wordthing[self.impostorselected[0]]}been selected', True, (255, 0, 0))
            img2 = font.render(f'Black\'s impostor has{wordthing[self.impostorselected[1]]}been selected', True, (255, 0, 0))
            rect = img.get_rect()
            rect2 = img2.get_rect()
            rect.center = (1000, 200)
            rect2.center = (1000, 300)
            self.display.blit(img, rect)
            self.display.blit(img2, rect2)
    def draw_pieces(self):
        for s in range(len(self.board)):
            for k in range(len(self.board)):
                if self.board[s][k] != ' ':
                    self.board[s][k].draw(self.display)
    def movepiece(self, pcoord, place):
        if not self.gameended:
            validmove = False
            ptomove = self.board[pcoord[1]][pcoord[0]]
            if ptomove != ' ' and pcoord != place:
                if ((ptomove.ptype.isupper() and self.wmove) or (ptomove.ptype.islower() and not self.wmove)):
                    if self.board[place[1]][place[0]] == ' ' or (self.board[place[1]][place[0]] != ' ' and ((self.board[place[1]][place[0]].ptype.isupper() and ptomove.ptype.islower()) or (self.board[place[1]][place[0]].ptype.islower() and ptomove.ptype.isupper()))):
                        if ptomove.ptype.lower() == 'p':
                            if ptomove.ptype.isupper():
                                if place == [ptomove.x, 8-ptomove.y-1] and self.board[8-ptomove.y-1][ptomove.x] == ' ':
                                    validmove = True
                                if pcoord[1] == 6 and place == [ptomove.x, 8-ptomove.y-2] and self.board[8-ptomove.y-1][ptomove.x] == ' ' and self.board[8-ptomove.y-2][ptomove.x] == ' ':
                                    validmove = True
                                if place == [ptomove.x+1, 8-ptomove.y-1] and self.board[8-ptomove.y-1][ptomove.x+1] != ' ' or place == [ptomove.x-1, 8-ptomove.y-1] and self.board[8-ptomove.y-1][ptomove.x-1] != ' ':
                                    validmove = True
                                if pcoord[1] == 1 and validmove:
                                    ptomove.ptype = 'Q'
                                    ptomove.color = 'w'
                                    validmove = True
                                if abs(self.last_pawn_move[1][1] - self.last_pawn_move[0][1]) == 2:
                                    if self.last_pawn_move[1][1] == pcoord[1] and abs(self.last_pawn_move[0][0] - pcoord[0]) == 1:
                                        if place == [ptomove.x+1, 8-ptomove.y-1] and self.board[8-ptomove.y-1][ptomove.x+1] == ' ' or place == [ptomove.x-1, 8-ptomove.y-1] and self.board[8-ptomove.y-1][ptomove.x-1] == ' ':
                                            if place[0] == self.last_pawn_move[0][0]:
                                                self.board[self.last_pawn_move[1][1]][self.last_pawn_move[1][0]] = ' '
                                                validmove = True
                            elif ptomove.ptype.islower():
                                
                                if place == [ptomove.x, 8-ptomove.y+1] and self.board[8-ptomove.y+1][ptomove.x] == ' ':
                                    validmove = True
                                if pcoord[1] == 1 and place == [ptomove.x, 8-ptomove.y+2] and self.board[8-ptomove.y+1][ptomove.x] == ' ' and self.board[8-ptomove.y+2][ptomove.x] == ' ':
                                    validmove = True
                                if place == [ptomove.x+1, 8-ptomove.y+1] and self.board[8-ptomove.y+1][ptomove.x+1] != ' ' or place == [ptomove.x-1, 8-ptomove.y+1] and self.board[8-ptomove.y+1][ptomove.x-1] != ' ':
                                    validmove = True
                                if pcoord[1] == 6 and validmove:
                                    ptomove.ptype = 'q'
                                    ptomove.color = 'b'
                                    validmove = True
                                if abs(self.last_pawn_move[1][1] - self.last_pawn_move[0][1]) == 2:
                                    if self.last_pawn_move[1][1] == pcoord[1] and abs(self.last_pawn_move[0][0] - pcoord[0]) == 1:
                                        if place == [ptomove.x+1, 8-ptomove.y+1] and self.board[8-ptomove.y+1][ptomove.x+1] == ' ' or place == [ptomove.x-1, 8-ptomove.y+1] and self.board[8-ptomove.y+1][ptomove.x-1] == ' ':
                                            if place[0] == self.last_pawn_move[0][0]:
                                                self.board[self.last_pawn_move[1][1]][self.last_pawn_move[1][0]] = ' ' 
                                                validmove = True                      
                        
                        elif ptomove.ptype.lower() == 'q':
                            validmove = True
                        elif ptomove.ptype.lower() == 'k':
                            validmove = True
                        elif ptomove.ptype.lower() == 'b':
                            validmove = True
                        elif ptomove.ptype.lower() == 'n':
                            if abs(pcoord[0]-place[0]) == 1 and abs(pcoord[1]-place[1]) == 2:
                                validmove = True
                            if abs(pcoord[0]-place[0]) == 2 and abs(pcoord[1]-place[1]) == 1:
                                validmove = True
                        elif ptomove.ptype.lower() == 'r':
                            validmove = True

                        
                        if validmove:
                            ptomove.x = place[0]
                            ptomove.y = 8-place[1]
                            self.board[pcoord[1]][pcoord[0]] = ' '
                            self.board[place[1]][place[0]] = ptomove
                            self.wmove = not self.wmove
                            if self.wmove:
                                self.movecount += 1
                            if self.impostormove - self.movecount == 0:
                                for s in self.board:
                                    for k in s:
                                        if k != ' ':
                                            if k.impostor:
                                                if k.color == 'w':
                                                    k.color == 'b'
                                                    k.ptype = k.ptype.lower()
                                                elif k.color == 'b':
                                                    k.color == 'w'
                                                    k.ptype = k.ptype.upper()
                                #if time.now()/500 == 
                            self.last_pawn_move = [pcoord, place]

class CDTimer():
    def __init__(self, screen, originaltime, fps, x, y):
        self.originaltime = originaltime
        self.paused = False
        self.fps = fps
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont("Arial",60)
        self.screen = screen
        self.ended = False
    def convert_from_ms(self, milliseconds): 
        seconds, milliseconds = divmod(milliseconds,1000) 
        minutes, seconds = divmod(seconds, 60) 
        hours, minutes = divmod(minutes, 60) 
        if len(str(hours)) == 1:
            hours = f'0{str(hours)}'
        if len(str(minutes)) == 1:
            minutes = f'0{str(minutes)}'
        if len(str(seconds)) == 1:
            seconds = f'0{str(seconds)}'
        if len(str(milliseconds)) == 1:
            milliseconds = f'0{str(milliseconds)}'
        if len(str(milliseconds)) == 3:
            milliseconds = f'{str(milliseconds)[:-1]}'
        return [hours, minutes, seconds, milliseconds]
    def draw_text(self, text, font, text_col, x,y):
        img = font.render(text, True, text_col)
        rect = img.get_rect()
        rect.center = (self.x,self.y)
        pygame.draw.rect(self.screen, (0, 0, 0), rect.inflate(50, 50), 0, border_radius=10)
        self.screen.blit(img, rect)
    def draw_time(self):
        a,b,c,d = self.convert_from_ms(self.originaltime)
        strTime = f'{a}:{b}:{c}.{d}'
        self.draw_text(strTime, self.font, pygame.Color(255, 255, 255), 20,20)
        if not self.paused and not self.ended:
            self.originaltime -= int(1000/self.fps)
            if self.originaltime <= 0:
                self.ended = True

# c = ChessBoard(None)
# pp = pprint.PrettyPrinter(indent=1)
# pp.pprint(c.exportfen(c.importfen('2r5/5P2/3P1p1n/3p3p/3KBP1B/4p2p/P7/3k1n2')))
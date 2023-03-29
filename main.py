import pygame
import chesshelper as chh
import sys
pygame.init()

display = pygame.display.set_mode((1200, 800)) #w, h]
clock0 = pygame.time.Clock()
clock = pygame.time.Clock()

pboard = chh.ChessBoard(display)
pboard.create_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')


def game():
    global pboard, clock, display
    wtimer, btimer = chh.CDTimer(display, pboard.timew, chh.FPS, 1000, 700), chh.CDTimer(display, pboard.timeb, chh.FPS, 1000, 100)
    pygame.time.set_timer(pygame.USEREVENT, 10)
    while True:
        pboard.draw_board()
        pboard.draw_pieces()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3 and pboard.movecount == 1:
                    temp2 = pygame.mouse.get_pos()
                    selimppos = [temp2[0]//100, temp2[1]//100]
                    pboard.selectimpostors(selimppos)
        pygame.display.update()
        if pboard.impostorselected == [True, True]:
            break
        clock0.tick(chh.FPS)
        
    while True: 
        if pboard.timew <= 0 or pboard.timeb <= 0:
            pboard.gameended = True
        pboard.draw_board()
        pboard.draw_pieces()
        if pboard.wmove:
            btimer.paused = True
            wtimer.paused = False
        else:
            btimer.paused = False
            wtimer.paused = True

        wtimer.draw_time()
        btimer.draw_time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    temp1 = pygame.mouse.get_pos()
                    mpos1 = [temp1[0]//100, temp1[1]//100]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    temp2 = pygame.mouse.get_pos()
                    if temp1[0] < 800 and temp1[1] < 800 and temp2[0] < 800 and temp2[1] < 800:
                        mpos2 = [temp2[0]//100, temp2[1]//100]
                        pboard.movepiece(mpos1, mpos2)
                elif event.button == 3 and pboard.movecount == 1:
                    temp2 = pygame.mouse.get_pos()
                    selimppos = [temp2[0]//100, temp2[1]//100]

        pygame.display.update()
        clock.tick(chh.FPS)

if __name__ == '__main__':
    game()
    pygame.quit()
    sys.exit()
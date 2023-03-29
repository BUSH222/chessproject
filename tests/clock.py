import pygame
import datetime
pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)

screen = pygame.display.set_mode((1000,200))
pygame.display.set_caption("Clock")
loopclock = pygame.time.Clock()
FPS = 50

font = pygame.font.SysFont("Consolas",60)

class CDTimer():
    def __init__(self, screen, originaltime, fps, x, y):
        self.originaltime = originaltime
        self.paused = False
        self.fps = fps
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont("Consolas",60)
        self.screen = screen
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
        self.screen.blit(img, rect)

    def draw_time(self):
        a,b,c,d = self.convert_from_ms(self.originaltime)
        strTime = f'{a}:{b}:{c}.{d}'
        self.draw_text(strTime, font, WHITE, 20,20)
        if not self.paused:
            self.originaltime -= int(1000/self.fps)
            if self.originaltime <= 0:
                self.paused = True

wtimer = CDTimer(screen, 100000, FPS, 500, 100)
run_clock = True
while run_clock:
    screen.fill((0, 0, 0))
    wtimer.draw_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_clock = False
    
    pygame.display.update()
    loopclock.tick(FPS)

pygame.quit()
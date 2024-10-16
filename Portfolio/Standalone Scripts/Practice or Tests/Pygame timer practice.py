#Pygame timer test
import pygame

class Timer(pygame.sprite.Sprite):
    def __init__(self):
        Time = "0"
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Arial", 69)
        self.textSurf = self.font.render(Time, 1, "white")
        self.image = pygame.Surface((200, 100))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect(center=(500,300))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [200/2 - W/2, 100/2 - H/2])

    def update(self, time):
        Time = str(time)
        self.font = pygame.font.SysFont("Arial", 69)
        self.textSurf = self.font.render(Time, 1, "white")
        self.image = pygame.Surface((200, 100))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect(center=(500,300))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [200/2 - W/2, 100/2 - H/2])

pygame.init()

win = pygame.display.set_mode((800, 500), pygame.SCALED)
pygame.display.set_caption("Simple timer")

clock = pygame.time.Clock()
timer = Timer()

time = 0

run = True
while run:
    clock.tick(1000)

    win.blit(timer.image, timer.rect)
    pygame.display.update()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            pygame.time.set_timer(event, 1000)
            time += 1

    timer.update(time)
    pygame.display.update()
            
if not run:
    pygame.quit()

import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(Sprite, self).__init__()
        self.surf = pygame.Surface((1920,1080)) 
        self.surf.fill((255,255,255))
        self.image = pygame.image.load('sprite.png').convert()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.surf.get_rect(center=(960,540))

win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
winXY = pygame.display.get_window_size()
dimX = winXY[0] - 50
dimY = winXY[1] - 50
win = pygame.display.set_mode((dimX, dimY))

sprite = Sprite(dimX, dimY)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    
    
    win.fill((255, 255, 255))
    
    win.blit(sprite.image, sprite.rect)
    
    pygame.display.flip()

if run == False:
    pygame.quit()

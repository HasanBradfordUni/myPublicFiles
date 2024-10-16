#Pygame windows practice
import pygame, sys
from pygame.locals import *
from time import sleep

pygame.init()

#Create a displace surface object
DISPLAYSURF = pygame.display.set_mode((400, 300), pygame.FULLSCREEN)
sleep(1)
DISPLAYSURF = pygame.display.set_mode((400, 300), pygame.SCALED)

mainLoop = True

while mainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                pygame.display.toggle_fullscreen()
            if event.key == pygame.K_r:
                DISPLAYSURF = pygame.display.set_mode((400, 300), pygame.RESIZABLE)
    pygame.display.update()

pygame.quit()

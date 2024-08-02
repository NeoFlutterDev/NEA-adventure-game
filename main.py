import pygame
pygame.init()
import sys

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#window = pygame.display.set_mode((infoObject.current_w, inforObject.current_h))
#window = pygame.display.set_mode((800, 450))
inforObject = pygame.display.Info()
#initialises the window
running = True
#variable for checking if game is still running
pygame.display.set_caption('Ancient Discovery')
Icon = pygame.image.load('sprites/other/logo.png')
pygame.display.set_icon(Icon)
font = pygame.font.Font('spacefont.ttf', 30)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePOS = pygame.mouse.get_pos()
            if ((inforObject.current_w - 15) >= mousePOS[0] >= (inforObject.current_w - 35)) and (35 >= mousePOS[1] >= 15):
                pygame.quit()

    exitButton = pygame.image.load('sprites/other/exit button.png')
    exitButton = pygame.transform.scale(exitButton, (20, 20))
    window.blit(exitButton, (inforObject.current_w - 25, 20))

    pygame.display.update()

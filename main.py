import pygame
pygame.init()
import sys
import math

infoObject = pygame.display.Info()
screenScale = [infoObject.current_w / 1920, infoObject.current_h / 1080]
#this finds the size of the monitor, as well as making an array to scale the game sprites upon
window = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
pygame.display.set_caption('Ancient Discovery')
#initialises the window
running = True
#variable for checking if game is still running
font = pygame.font.Font('spacefont.ttf', 30)

def scale_sprite(image):
    return pygame.transform.scale(image, (int(image.get_width() * screenScale[0]), int(image.get_height() * screenScale[1])))

def coordinates_to_quadrant(coordinates):
    quadrantX = coordinates[0] / (20 * screenScale[0])
    quadrantY = coordinates[1] / (20 * screenScale[1])
    return (math.trunc(quadrantY) * 96) + math.trunc(quadrantX) + 1
    #this finds the quadrant in which the mouse is currently located, by finding which 20 pixels it is located in in both height and width
    #it then adds these values together, after multiplying the Y quadrant by 96, as there is 96 quadrants per row
    #the top left quadrant is 1, and the bottom right quadrant is 5184

def quadrant_to_coordinates(quadrant):
    quadrant -= 1
    coordinateX = (quadrant % 96) * 20 * screenScale[0]
    coordinateY = (quadrant // 96) * 20 * screenScale[1]
    return [coordinateX, coordinateY]

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseQuadrant = coordinates_to_quadrant(pygame.mouse.get_pos())
            if mouseQuadrant == 96:
                pygame.quit()

    exitButton = pygame.image.load('sprites/other/exit button.png')
    exitButton = scale_sprite(exitButton)
    print(quadrant_to_coordinates(96))
    window.blit(exitButton, (quadrant_to_coordinates(96)))

    pygame.display.update()

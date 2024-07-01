import pygame

window = pygame.display.set_mode((500, 500))
#initialises the window
running = True
#variable for checking if game is still running

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

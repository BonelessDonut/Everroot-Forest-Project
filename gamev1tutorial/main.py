import pygame, sys
from settings import *
from pygame.locals import(
    K_w,
    K_s,
    K_a,
    K_d,
    K_RETURN,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)



pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

player = pygame.Rect((255, 145, 50, 50))

protag = pygame.image.load("protagLattern(1).png").convert_alpha()


DEFAULT_SPRITE_SIZE = (90, 90)

protag = pygame.transform.scale(protag, DEFAULT_SPRITE_SIZE)
protag_rect = protag.get_rect()

running = True
while running == True:

    screen.fill((0, 0, 0))
    #pygame.draw.rect(screen, (20, 145, 54), player)
    pygame.draw.rect(screen, (0, 0, 0), protag_rect)

    screen.blit(protag, protag_rect)

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        protag_rect.move_ip(-1, 0)
    if key[pygame.K_d] == True:
        protag_rect.move_ip(1, 0)
    if key[pygame.K_w] == True:
        protag_rect.move_ip(0, -1)
    if key[pygame.K_s] == True:
        protag_rect.move_ip(0, 1)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    pygame.display.update()

#screen.fill((255, 155, 200))
#surf = pygame.Surface((50, 50))
#surf.fill((200, 200, 200))
#rect = surf.get_rect()
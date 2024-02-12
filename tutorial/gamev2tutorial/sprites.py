import pygame
from settings import *
import math
import random

class Player(pygame.sprite.Sprite):
    imagelist = []
    imgindex = 0
    clock = None
    timepassed = 0

    def __init__(self, game, x, y, clock):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.imagelist = ['../../protagLattern(1).png', '../../protagLatternAlt(2).png']
        self.clock = clock

        self.image = pygame.image.load(self.imagelist[self.imgindex])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


        #self.image = pygame.Surface([self.width, self.height])
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        #pass
        self.movement()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.timepassed += self.clock.get_time()/1000
        self.image = pygame.transform.scale(pygame.image.load(self.imagelist[self.imgindex]), (self.width, self.height))

        self.x_change = 0
        self.y_change = 0


    def movement(self):
        #The key press segments came from viewing this tutorial
        #https://www.youtube.com/watch?v=GakNgbiAxzs&list=PLkkm3wcQHjT7gn81Wn-e78cAyhwBW3FIc&index=2
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            # Two lines below change camera to move around player character, moving all other sprites
            # comment them out to create a static camera
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
            self.imgindex = not self.imgindex if ((self.timepassed)//(0.35)%2 == self.imgindex) else self.imgindex
            
        if keys[pygame.K_d]:
            # Two lines below change camera to move around player character, moving all other sprites
            # comment them out to create a static camera
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
            self.imgindex = not self.imgindex if ((self.timepassed)//(0.35)%2 == self.imgindex) else self.imgindex
            
        if keys[pygame.K_w]:
            # Two lines below change camera to move around player character, moving all other sprites
            # comment them out to create a static camera
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
            self.imgindex = not self.imgindex if ((self.timepassed)//(0.35)%2 == self.imgindex) else self.imgindex
            
        if keys[pygame.K_s]:
            #Two lines below change camera to move around player character, moving all other sprites
            # comment them out to create a static camera
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
            self.imgindex = not self.imgindex if ((self.timepassed)//(0.35)%2 == self.imgindex) else self.imgindex

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

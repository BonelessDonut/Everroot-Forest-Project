import pygame
from settings import *
import math
import random

class Player(pygame.sprite.Sprite):
    rightImgList = []
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
        self.rightImgList = ['../../Sprites/protagLattern(1).png', '../../Sprites/protagLatternAlt(2).png', '../../Sprites/protagLattern(1).png', '../../Sprites/protagLatternAlt(2).png']
        self.leftImgList = ['../../Sprites/protagBlobLeft.png', '../../Sprites/protagBlobLeftAlt.png', '../../Sprites/protagBlobLeft.png', '../../Sprites/protagBlobLeftAlt.png']
        self.upImgList = ['../../Sprites/protagBlobUpAlt.png', '../../Sprites/protagBlobUpLeftAlt.png', '../../Sprites/protagBlobUpAlt.png', '../../Sprites/protagBlobUpRight.png']
        self.downImgList = ['../../Sprites/protagBlobDown.png', '../../Sprites/protagBlobDownLeftAlt.png', '../../Sprites/protagBlobDown.png', '../../Sprites/protagBlobDownRightAlt.png',]
        self.clock = clock

        self.image = pygame.image.load(self.downImgList[self.imgindex])
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
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.timepassed += self.clock.get_time()/1000
        #Below line: Loads image using right image list (transforms it to scale with width and height) and sets it to the image
        if self.facing == 'right':
            self.image = pygame.transform.scale(pygame.image.load(self.rightImgList[self.imgindex]), (self.width, self.height)) 
        elif self.facing == 'left':
            self.image = pygame.transform.scale(pygame.image.load(self.leftImgList[self.imgindex]), (self.width, self.height))
        elif self.facing == 'up':
            self.image = pygame.transform.scale(pygame.image.load(self.upImgList[self.imgindex]), (self.width, self.height))
            print(self.upImgList[self.imgindex])
        else: # self.facing == 'down':
            self.image = pygame.transform.scale(pygame.image.load(self.downImgList[self.imgindex]), (self.width, self.height))
            print(self.downImgList[self.imgindex])
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
            self.imgindex = (self.imgindex + 1)%4 if ((self.timepassed)//(0.35)%4 == self.imgindex) else self.imgindex 
            #0.35//0.35%2


        if keys[pygame.K_d]:
            # Two lines below change camera to move around player character, moving all other sprites
            # comment them out to create a static camera
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
            self.imgindex = (self.imgindex + 1)%4 if ((self.timepassed)//(0.35)%4 == self.imgindex) else self.imgindex 
            
        if keys[pygame.K_w]:
            # Two lines below change camera to move around player character, moving all other sprites
            # comment them out to create a static camera
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
            self.imgindex = (self.imgindex + 1)%4 if ((self.timepassed)//(0.35)%4 == self.imgindex) else self.imgindex 
            

        if keys[pygame.K_s]:
            #Two lines below change camera to move around player character, moving all other sprites
            # comment them out to create a static camera
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
            self.imgindex = (self.imgindex + 1)%4 if ((self.timepassed)//(0.35)%4 == self.imgindex) else self.imgindex 

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            x_diff = 0
            if hits:
                if self.x_change > 0:
                    x_diff = (hits[0].rect.left-self.rect.width)-self.rect.x
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    x_diff = hits[0].rect.right - self.rect.x
                    self.rect.x = hits[0].rect.right
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= x_diff
        else:
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            y_diff = 0
            if hits:
                if self.y_change > 0:
                    y_diff = (hits[0].rect.top - self.rect.height) - self.rect.y
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    y_diff = hits[0].rect.bottom - self.rect.y
                    self.rect.y = hits[0].rect.bottom
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= y_diff

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

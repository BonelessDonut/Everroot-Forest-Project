import pygame
from settings import *
import math
import random
import re

class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y, clock):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.xChange = 0
        self.yChange = 0

        self.imgindex = 0
        self.facing = 'down'
        #Shows the file paths for each image, depending on which direction the player is facing
        self.rightImgList = ['Sprites/protag/protagLattern(1).png', 'Sprites/protag/protagLatternAlt(2).png', 'Sprites/protag/protagblobRight3.png', 'Sprites/protag/protagLatternAlt(2).png']
        self.leftImgList = ['Sprites/protag/protagBlobLeft.png', 'Sprites/protag/protagBlobLeftAlt.png', 'Sprites/protag/protagBlobLeft3.png', 'Sprites/protag/protagBlobLeftAlt.png']
        self.upImgList = ['Sprites/protag/protagBlobUpAlt.png', 'Sprites/protag/protagBlobUpLeftAlt.png', 'Sprites/protag/protagBlobUpAlt.png', 'Sprites/protag/protagBlobUpRight.png']
        #READ ME: FIX 'Sprites/protagBlobDown.png' being compressed too much by player size and looking weird as a result
        #Potential fixes: scale the image down in pygame before loading, or edit the sprite images to make them all the same resolution for more consistency (Using photoshop or smth)
        self.downImgList = ['Sprites/protag/protagBlobDownNew.png', 'Sprites/protag/protagBlobDownLeftAlt.png', 'Sprites/protag/protagBlobDownNew.png', 'Sprites/protag/protagBlobDownRightAltNew.png',]
        
        self.clock = clock
        self.timepassed = 0

        self.image = pygame.transform.scale(pygame.image.load(self.downImgList[self.imgindex]), (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        #pass
        self.movement()
        self.interact()

        self.rect.x += self.xChange
        self.collideBlocks('x')
        self.rect.y += self.yChange
        self.collideBlocks('y')

        self.timepassed += self.clock.get_time()/1000
        #Below line: Loads image using right image list (transforms it to scale with width and height) and sets it to the image
        if self.facing == 'right':
            self.image = pygame.transform.scale(pygame.image.load(self.rightImgList[self.imgindex]), (self.width * 1.02, self.height * 1.02))
        elif self.facing == 'left':
            self.image = pygame.transform.scale(pygame.image.load(self.leftImgList[self.imgindex]), (self.width * 1.02, self.height * 1.02))
        elif self.facing == 'up':
            self.image = pygame.transform.scale(pygame.image.load(self.upImgList[self.imgindex]), (self.width * 1.02, self.height * 1.02))
        else: # self.facing == 'down':
            self.image = pygame.transform.scale(pygame.image.load(self.downImgList[self.imgindex]), (self.width * 1.02, self.height * 1.02))
        self.xChange = 0
        self.yChange = 0

    def interact(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            interactRect = None
            if self.facing == 'right':
                interactRect = pygame.Rect(self.rect.left, self.rect.top, TILESIZE*2, TILESIZE)
            elif self.facing == 'left':
                interactRect = pygame.Rect(self.rect.left-self.width, self.rect.top, TILESIZE*2, TILESIZE)
            elif self.facing == 'up':
                interactRect = pygame.Rect(self.rect.left, self.rect.top-self.height, TILESIZE, TILESIZE*2)
            else:
                interactRect = pygame.Rect(self.rect.left, self.rect.top, TILESIZE, TILESIZE*2)
            flowerIndex = interactRect.collidelist(list(flower.rect for flower in self.game.flowers))
            if flowerIndex != -1:
                #READ ME, FINISH THE FLOWER CLASS KILL INTERACTION AND DO SOMETHING WITH THE NEW KILL ANIMATION CLASS
                self.game.state = 'flowerC'
                self.game.flowers.get_sprite(flowerIndex).state = 'cut'
                print('interacted')
                self.game.flowers.get_sprite(flowerIndex).anim()
            oreIndex = interactRect.collidelist(list(ore.rect for ore in self.game.ores))
            if oreIndex != -1:
                self.game.ores.get_sprite(oreIndex).kill()
            npcIndex = interactRect.collidelist(list(npc.rect for npc in self.game.npcs))
            if npcIndex != -1:
                self.game.npcs.get_sprite(npcIndex).interaction()
                pygame.time.wait(250)


    def movement(self):
        if self.game.state != 'explore':
            return
        #The key press segments came from viewing this tutorial
        #https://www.youtube.com/watch?v=GakNgbiAxzs&list=PLkkm3wcQHjT7gn81Wn-e78cAyhwBW3FIc&index=2
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            # Two lines below change camera to move around player character, moving all other sprites
            # comment them out to create a static camera
            #for sprite in self.game.all_sprites:
                #sprite.rect.x += PLAYER_SPEED
            self.xChange -= PLAYER_SPEED
            self.facing = 'left'
            self.imgindex = (self.imgindex + 1)%4 if ((self.timepassed)//(0.20)%4 == self.imgindex) else self.imgindex


        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            # Two lines below change camera to move around player character, moving all other sprites
            # comment them out to create a static camera
            #for sprite in self.game.all_sprites:
                #sprite.rect.x -= PLAYER_SPEED
            self.xChange += PLAYER_SPEED
            self.facing = 'right'
            self.imgindex = (self.imgindex + 1)%4 if ((self.timepassed)//(0.20)%4 == self.imgindex) else self.imgindex
            
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            # Two lines below change camera to move around player character, moving all other sprites
            # comment them out to create a static camera
            #for sprite in self.game.all_sprites:
                #sprite.rect.y += PLAYER_SPEED
            self.yChange -= PLAYER_SPEED
            self.facing = 'up'
            self.imgindex = (self.imgindex + 1)%4 if ((self.timepassed)//(0.18)%4 == self.imgindex) else self.imgindex
            

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            #Two lines below change camera to move around player character, moving all other sprites
            # comment them out to create a static camera
            #for sprite in self.game.all_sprites:
                #sprite.rect.y -= PLAYER_SPEED
            self.yChange += PLAYER_SPEED
            self.facing = 'down'
            self.imgindex = (self.imgindex + 1)%4 if ((self.timepassed)//(0.25)%4 == self.imgindex) else self.imgindex

    def collideBlocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) + pygame.sprite.spritecollide(self, self.game.npcs, False)
            xDiff = 0
            if hits:
                if self.xChange > 0:
                    x_diff = (hits[0].rect.left-self.rect.width)-self.rect.x
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.xChange < 0:
                    x_diff = hits[0].rect.right - self.rect.x
                    self.rect.x = hits[0].rect.right
                #for sprite in self.game.all_sprites:
                    #sprite.rect.x -= x_diff
        else:
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) + pygame.sprite.spritecollide(self, self.game.npcs, False)
            yDiff = 0
            if hits:
                if self.yChange > 0:
                    yDiff = (hits[0].rect.top - self.rect.height) - self.rect.y
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.yChange < 0:
                    yDiff = hits[0].rect.bottom - self.rect.y
                    self.rect.y = hits[0].rect.bottom
                #for sprite in self.game.all_sprites:
                    #sprite.rect.y -= yDiff

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

class Flower(pygame.sprite.Sprite):
    def __init__(self, game, x, y, clock):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.flowers
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.clock = clock
        self.timepassed = 0
        self.imgindex = 0

        #a self state helps ensure that only the interacted flower goes through anim()
        self.state = 'alive'

        hyacinImgL = ['Sprites/items/hyacinth.png', 'Sprites/items/hyacinth2.png', 'Sprites/items/hyacinth3.png', 'Sprites/items/hyacinth4.png', 'Sprites/items/hyacinth5.png']
        sunFloImgL = ['Sprites/items/sunflowernew.png', 'Sprites/items/sunflower2.png', 'Sprites/items/sunflower3.png', 'Sprites/items/sunflower4.png', 'Sprites/items/sunflower5.png']
        silentFImgL = ['Sprites/items/silentFlower.png', 'Sprites/items/silentFlower2.png', 'Sprites/items/silentFlower3.png', 'Sprites/items/silentFlower4.png', 'Sprites/items/silentFlower5.png']

        self.imageList = [['Sprites/items/hyacinth.png', hyacinImgL], ['Sprites/items/sunflowernew.png', sunFloImgL], ['Sprites/items/silentFlower.png', silentFImgL]]
        self.flowerSpriteNum = random.randint(0, len(self.imageList)-1)
        self.image = pygame.transform.scale(pygame.image.load(self.imageList[self.flowerSpriteNum][0]), (self.width, self.height))


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.timepassed += self.clock.get_time() / 1000
        if self.game.state == 'flowerC':
            if self.state == 'cut':
                print('updated')
                #READ ME, THIS UPDATES ALL THE FLOWERS AT ONCE AFTER INTERACTING WITH ONLY ONE FLOWER. - UNINTENDED OUTCOME, NEEDS FIXING
                self.anim()
                self.image = pygame.transform.scale(pygame.image.load(self.imageList[self.flowerSpriteNum][1][self.imgindex % 5]), (self.width, self.height))

    def anim(self): #READ ME, FINISH THIS FUNCTION
        #realized it was setting the state to flowerC every single loop from the Player.interact() method, so it never went to the else to kill
        #moved it in front to make sure it switched states when the imgindex got to 4
        if self.imgindex > 4:
            self.game.state = 'explore'
            print('state switched')
        if self.game.state == 'flowerC':
            print('should i switch to kill?')
            self.imgindex = (self.imgindex + 1) if ((self.timepassed) // (0.20) % 5 == self.imgindex) else self.imgindex
            print(self.imgindex)
            print(self.game.state)
            #print(self.timepassed)
            '''if self.imgindex > 4:
                self.game.state = 'explore'
                print('state switched')'''
            #put this into update cuz thought it fit better there
            #else:
                #self.image = pygame.transform.scale(pygame.image.load(self.imageList[self.flowerSpriteNum][1][self.imgindex % 5]), (self.width, self.height))
            #MAYBE TRY MAKING THE IMGINDEX INCREASE UNTIL IT GETS PASSED 5, THEN HAVE A CONDITIONAL CHECKING IF IT IS GREATER THAN 5
            #IF SO, CHANGE THE STATE BACK TO 'EXPLORE' AND KILL THE SPRITE

        else:
            print('should kill')
            #READ ME, SPRITE DOES NOT PROPERLY KILL, THE LAST IMAGE STILL REMAINS AFTER THE SPRITE HAS BEEN KILLED
            if self.state == 'cut':
                self.kill()

class Ore(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.ores
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        #self.imageList = []
        #self.image = pygame.transform.scale(pygame.image.load(self.imageList[random.randint(0, 1)]), (self.width, self.height))
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.npcs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.xChange = 0
        self.yChange = 0

        self.imagelist = ['Sprites/npcs/sampleNPC/hkprotagdown.jpg', 'Sprites/npcs/sampleNPC/hkprotagleft.jpg', 'Sprites/npcs/sampleNPC/hkprotagright.jpg', 'Sprites/npcs/sampleNPC/hkprotagdown.jpg']
        self.image = pygame.transform.scale(pygame.image.load(self.imagelist[0]), (self.width, self.height))

        self.TextBox = None

        #self.image = pygame.Surface([self.width, self.height])
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def interaction(self):
        if self.game.state == 'explore':
            self.TextBox = TextBox(self.game)
            self.TextBox.newText("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", 20)
            self.game.state = 'dialogue'
        else:
            self.TextBox.kill()
            self.game.state = 'explore'
            
        
        

class TextBox(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self._layer = TEXT_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.width = 920
        self.height = 170
        self.x = (WIDTH-self.width)//2
        self.y = (HEIGHT-self.height-50)

        self.area = pygame.Rect(0, 0, self.width*0.6, self.height*0.95)
        self.image = pygame.transform.scale(pygame.image.load('Sprites/SVTextboxTemplate.png'), (self.width, self.height))
        #To see where the area rectangle covers, uncomment below line
        #pygame.draw.rect(self.image, RED, self.area)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def newText(self, text, fontSize):
        maxLength = int((float(-2.2835*10**(-7))*self.width**2+0.000411706*self.width+0.767647)*self.width/fontSize)+1
        boxFont = pygame.font.SysFont('Courier', fontSize)
        countRows = 0
        while(len(text) > 0):
            cutoffIndex = len(text[:maxLength])-re.search('[^a-zA-Z0-9]', text[maxLength-1::-1]).end()+1
            self.image.blit(boxFont.render(text[0:cutoffIndex], False, (0, 0, 0)), (15, 10+countRows*fontSize), self.area)
            countRows += 1
            try:
                text = text[cutoffIndex:]
            except:
                break
        

        


        

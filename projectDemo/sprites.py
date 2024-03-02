import pygame
from settings import *
import math
import random
import re
import os

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

        self.mouseRect = pygame.Rect(0, 0, 40, 40)
        self.mouseRect.center = pygame.mouse.get_pos()

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

        #READ ME, ADD SPRITES FOR CUTTING WHILE FACING OTHER DIRECTIONS THAN RIGHT
        self.cutImgList = ['Sprites/protag/protagCut.png', 'Sprites/protag/protagCutRed.png', 'Sprites/protag/protagCutBlue.png', 'Sprites/protag/protagCutPlat.png']
        self.cutIndex = 0
        #READ ME, ADD SPRITES FOR MINING WHILE FACING OTHER DIRECTIONS THAN RIGHT
        self.mineImgList = ['Sprites/protag/protagMine.png', 'Sprites/protag/protagMineRed.png', 'Sprites/protag/protagMineBlue.png', 'Sprites/protag/protagMinePlat.png']
        self.mineIndex = 0

        self.clock = clock
        self.timepassed = 0

        self.image = pygame.transform.scale(pygame.image.load(self.downImgList[self.imgindex]).convert_alpha(), (self.width, self.height))
        

        #self.rect = self.image.get_rect().
        #self.rect.x = self.x
        #self.rect.y = self.y
        #Below line is to decrease the rectangle collision slightly
        #Was having trouble fitting in 1 tile gaps
        self.rect = pygame.Rect(self.x, self.y, 30, 30)

    def update(self):
        self.movement()
        self.interact()

        self.rect.x += self.xChange
        self.collideBlocks('x')
        self.rect.y += self.yChange
        self.collideBlocks('y')

        self.timepassed += self.clock.get_time()/1000
        #Below line: Loads image using right image list (transforms it to scale with width and height) and sets it to the image
        if self.game.state == 'explore':
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

        if self.game.state == 'dialogue':
            self.mouseRect.center = pygame.mouse.get_pos()
            interactRect = pygame.Rect(self.rect.left-TILESIZE*0.1, self.rect.top-TILESIZE*0.1, TILESIZE*1.2, TILESIZE*1.2)
            npcIndex = interactRect.collidelist(list(npc.rect for npc in self.game.npcs))
            npc = self.game.npcs.get_sprite(npcIndex)
            collisionList = []
            for rect in npc.TextBox.choiceRectList:
                collisionList.append(pygame.Rect(rect.left, rect.top, rect.width, rect.height))
            for rect in range(len(collisionList)):
                collisionList[rect].x = npc.TextBox.x + 13
                collisionList[rect].y = npc.TextBox.y + 25 + 30*rect
            if len(collisionList) > 0:
                highlighted = self.mouseRect.collidelist(collisionList) 
                if highlighted == -1:
                    return
                else:
                    npc.TextBox.selectedRect = highlighted


    #Method for different Player interactions
    def interact(self):
        keys = pygame.key.get_pressed()
        mouses = pygame.mouse.get_pressed()
        if keys[pygame.K_SPACE]:
            interactRect = None
            if self.facing == 'right':
                interactRect = pygame.Rect(self.rect.left, self.rect.top, TILESIZE*1.1, TILESIZE)
            elif self.facing == 'left':
                interactRect = pygame.Rect(self.rect.left-TILESIZE*0.1, self.rect.top, TILESIZE*1.1, TILESIZE)
            elif self.facing == 'up':
                interactRect = pygame.Rect(self.rect.left, self.rect.top-TILESIZE*0.1, TILESIZE, TILESIZE*1.1)
            else:
                interactRect = pygame.Rect(self.rect.left, self.rect.top, TILESIZE, TILESIZE*1.1)

            #Gets the index of the flower that the player interacted with
            flowerIndex = interactRect.collidelist(list(flower.rect for flower in self.game.flowers))
            if flowerIndex != -1:
                self.game.state = 'flowerC'
                self.game.flowers.get_sprite(flowerIndex).state = 'cutting'
                #READ ME, USE "self.facing" DIRECTIONS TO DETERMINE WHICH DIRECTION CUTTING SPRITE TO USE
                self.image = pygame.transform.scale(pygame.image.load(self.cutImgList[self.cutIndex]), (self.width * 1.04, self.height * 1.04))
                self.game.flowers.get_sprite(flowerIndex).anim()

            #Gets the index of the ore that the player interacted with
            oreIndex = interactRect.collidelist(list(ore.rect for ore in self.game.ores))
            if oreIndex != -1:
                self.game.state = 'oreMine'
                self.game.ores.get_sprite(oreIndex).state = 'mining'
                self.image = pygame.transform.scale(pygame.image.load(self.mineImgList[self.mineIndex]), (self.width * 1.04, self.height * 1.04))
                self.game.ores.get_sprite(oreIndex).killAnim()

            #Gets the index of the npc that the player interacted with
            npcIndex = interactRect.collidelist(list(npc.rect for npc in self.game.npcs))
            if npcIndex != -1:
                self.game.npcs.get_sprite(npcIndex).interaction()
                pygame.time.wait(250)
        elif self.game.state == 'dialogue' and (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            interactRect = None
            if self.facing == 'right':
                interactRect = pygame.Rect(self.rect.left, self.rect.top, TILESIZE*1.1, TILESIZE)
            elif self.facing == 'left':
                interactRect = pygame.Rect(self.rect.left-TILESIZE*0.1, self.rect.top, TILESIZE*1.1, TILESIZE)
            elif self.facing == 'up':
                interactRect = pygame.Rect(self.rect.left, self.rect.top-TILESIZE*0.1, TILESIZE, TILESIZE*1.1)
            else:
                interactRect = pygame.Rect(self.rect.left, self.rect.top, TILESIZE, TILESIZE*1.1)
            
            #Gets the index of the npc that the player interacted with
            npcIndex = interactRect.collidelist(list(npc.rect for npc in self.game.npcs))
            if npcIndex != -1:
                npc = self.game.npcs.get_sprite(npcIndex)
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    npc.TextBox.selectedRect = npc.TextBox.selectedRect - 1 if npc.TextBox.selectedRect > 0 else npc.TextBox.selectedRect
                    pygame.time.wait(150)
                else:
                    npc.TextBox.selectedRect = npc.TextBox.selectedRect + 1 if npc.TextBox.selectedRect < len(npc.TextBox.choiceRectList)-1 else npc.TextBox.selectedRect
                    pygame.time.wait(150)



        #Allows mouse click functionality for interactions
        elif mouses[0]:
            mouseRect = pygame.Rect(0, 0, 40, 40)
            mouseRect.center = pygame.mouse.get_pos()

            if self.game.state == 'dialogue':
                interactRect = pygame.Rect(self.rect.left-TILESIZE*0.1, self.rect.top-TILESIZE*0.1, TILESIZE*1.2, TILESIZE*1.2)
                npcIndex = interactRect.collidelist(list(npc.rect for npc in self.game.npcs))
                npc = self.game.npcs.get_sprite(npcIndex)
                rectCollisionList = npc.TextBox.choiceRectList[:]
                for rect in range(len(rectCollisionList)):
                    rectCollisionList[rect].x = npc.TextBox.x + 13
                    rectCollisionList[rect].y = npc.TextBox.y + 25 + 30*rect
                if len(rectCollisionList) > 0:
                    npc.selectedRect = mouseRect.collidelist(rectCollisionList)
                    npc.interaction()
                    pygame.time.wait(200)

            else:
                #Checks if the player is within a square's range of side length 60 pixels of the mouse
                if abs(mouseRect.x-self.rect.x) <= 60 and abs(mouseRect.y-self.rect.y) <= 60:
                    interactIndex = mouseRect.collidelist(list(ore.rect for ore in self.game.ores))
                    if interactIndex != -1:
                        self.game.ores.get_sprite(interactIndex).kill()
                    interactIndex = mouseRect.collidelist(list(flower.rect for flower in self.game.flowers))
                    if interactIndex != -1:
                        self.game.flowers.get_sprite(interactIndex).kill()
                    interactIndex = mouseRect.collidelist(list(npc.rect for npc in self.game.npcs))
                    if interactIndex != -1:
                        self.game.npcs.get_sprite(interactIndex).interaction()
                        pygame.time.wait(250)

        #Checks for teleport interactions
        interactRect = pygame.Rect(self.rect.left, self.rect.top, TILESIZE, TILESIZE)
        teleportIndex = interactRect.collidelist(list(teleport.rect for teleport in self.game.teleport))
        if teleportIndex != -1:
            tpSprite = self.game.teleport.get_sprite(teleportIndex)
            self.kill()
            self.game.createTilemap((tpSprite.x//TILESIZE, tpSprite.y//TILESIZE))
            pygame.time.wait(100)


    


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
            #for sprite in self.game.all_sprites:
                #sprite.rect.x -= PLAYER_SPEED
            self.xChange += PLAYER_SPEED
            self.facing = 'right'
            self.imgindex = (self.imgindex + 1)%4 if ((self.timepassed)//(0.20)%4 == self.imgindex) else self.imgindex
            
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            #for sprite in self.game.all_sprites:
                #sprite.rect.y += PLAYER_SPEED
            self.yChange -= PLAYER_SPEED
            self.facing = 'up'
            self.imgindex = (self.imgindex + 1)%4 if ((self.timepassed)//(0.18)%4 == self.imgindex) else self.imgindex
            

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
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
        self._layer = ITEM_LAYER
        self.groups = self.game.all_sprites, self.game.flowers
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.clock = clock
        self.timepassed = 0
        self.imgindex = 1

        self.state = 'alive'

        hyacinImgL = ['Sprites/items/hyacinth.png', 'Sprites/items/hyacinth2.png', 'Sprites/items/hyacinth3.png', 'Sprites/items/hyacinth4.png', 'Sprites/items/hyacinth5.png']
        sunFloImgL = ['Sprites/items/sunflowernew.png', 'Sprites/items/sunflower2.png', 'Sprites/items/sunflower3.png', 'Sprites/items/sunflower4.png', 'Sprites/items/sunflower5.png']
        silentFImgL = ['Sprites/items/silentFlower.png', 'Sprites/items/silentFlower2.png', 'Sprites/items/silentFlower3.png', 'Sprites/items/silentFlower4.png', 'Sprites/items/silentFlower5.png']

        self.imageList = [['Sprites/items/hyacinth.png', hyacinImgL], ['Sprites/items/sunflowernew.png', sunFloImgL], ['Sprites/items/silentFlower.png', silentFImgL]]
        #Randomly selects the flower to spawn as one of the flower options:
        #either a hyacinth, sunflower, or silent princess flower
        self.flowerSpriteNum = random.randint(0, len(self.imageList)-1)
        self.image = pygame.transform.scale(pygame.image.load(self.imageList[self.flowerSpriteNum][0]), (self.width, self.height))


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.timepassed += self.clock.get_time() / 1000
        if self.game.state == 'flowerC':
            if self.state == 'cutting':
                #READ ME, THIS UPDATES ALL THE FLOWERS AT ONCE AFTER INTERACTING WITH ONLY ONE FLOWER. - UNINTENDED OUTCOME, NEEDS FIXING
                self.anim()
                self.image = pygame.transform.scale(pygame.image.load(self.imageList[self.flowerSpriteNum][1][self.imgindex % 5]), (self.width, self.height))

    def anim(self): 
        #realized it was setting the state to flowerC every single loop from the Player.interact() method, so it never went to the else to kill
        #moved it in front to make sure it switched states when the imgindex got to 4
        if self.imgindex > 4:
            self.game.state = 'explore'
        if self.game.state == 'flowerC':
            self.imgindex = (self.imgindex + 1) if ((self.timepassed) // (0.3) % 5 == self.imgindex) else self.imgindex

        else:
            if self.state == 'cutting':
                self.kill()

class Ore(pygame.sprite.Sprite):
    def __init__(self, game, x, y, clock):
        self.game = game
        self._layer = ITEM_LAYER
        self.groups = self.game.all_sprites, self.game.ores
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.clock = clock
        self.timepassed = 0
        self.imgindex = 0

        self.state = 'alive'

        rubyImageL = ['Sprites/items/oreRuby.png', 'Sprites/items/oreRuby2.png', 'Sprites/items/oreRuby3.png', 'Sprites/items/oreRuby3.png']
        emeraldImageL = ['Sprites/items/oreEmerald.png', 'Sprites/items/oreEmerald2.png', 'Sprites/items/oreEmerald3.png', 'Sprites/items/oreEmerald3.png']
        copperImageL = ['Sprites/items/oreCopper.png', 'Sprites/items/oreCopper2.png', 'Sprites/items/oreCopper3.png', 'Sprites/items/oreCopper3.png']
        amethImageL = ['Sprites/items/oreAmethyst.png', 'Sprites/items/oreAmethyst2.png', 'Sprites/items/oreAmethyst3.png', 'Sprites/items/oreAmethyst3.png']
        ironImageL = ['Sprites/items/oreIron.png', 'Sprites/items/oreIron2.png', 'Sprites/items/oreIron3.png', 'Sprites/items/oreIron3.png']



        self.imageList = [['Sprites/items/oreRuby.png', rubyImageL], ['Sprites/items/oreEmerald.png', emeraldImageL], ['Sprites/items/oreCopper.png', copperImageL], ['Sprites/items/oreAmethyst.png', amethImageL], ['Sprites/items/oreIron.png', ironImageL]]
        self.oreSpriteNum = random.randint(0, len(self.imageList) - 1)

        self.image = pygame.transform.scale(pygame.image.load(self.imageList[self.oreSpriteNum][0]), (self.width, self.height))
        #self.image = pygame.Surface([self.width, self.height])
        #self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.timepassed += self.clock.get_time() / 1000
        if self.game.state == 'oreMine':
            if self.state == 'mining':
                #READ ME, THIS UPDATES ALL THE FLOWERS AT ONCE AFTER INTERACTING WITH ONLY ONE FLOWER. - UNINTENDED OUTCOME, NEEDS FIXING
                self.killAnim()
                self.image = pygame.transform.scale(pygame.image.load(self.imageList[self.oreSpriteNum][1][self.imgindex % 4]), (self.width, self.height))
                print(self.imgindex)


        pass

    def killAnim(self):
        if self.imgindex > 2:
            self.game.state = 'explore'
        if self.game.state == 'oreMine':
            self.imgindex = (self.imgindex + 1) if ((self.timepassed) // (0.31) % 4 == self.imgindex) else self.imgindex
        else:
            if self.state == 'mining':
                self.kill()
        pass



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

        self.meetings = 0
        self.name = 'Dubidubidu'

        self.xChange = 0
        self.yChange = 0

        self.imagelist = ['Sprites/npcs/sampleNPC/hkprotagdown.jpg', 'Sprites/npcs/sampleNPC/hkprotagleft.jpg', 'Sprites/npcs/sampleNPC/hkprotagright.jpg', 'Sprites/npcs/sampleNPC/hkprotagdown.jpg']
        self.image = pygame.transform.scale(pygame.image.load(self.imagelist[0]).convert_alpha(), (self.width, self.height))

        self.dialogueStage = '01:First Meet'
        self.dialogueStageIndex = 1
        #Always leave a space/punctuation at the end of the quote!
        self.dialogueList = {'01:First Meet':[{'Meetings': 1},
                                                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                                                "Chipichipi Chapachapa Dubidubi Dabadaba Magico Mi Dubi Dubi ",
                                                "Boom Boom Boom Boom ",
                                                "%Choices; Cats are cute?; Yes; Of Course; Meow",
                                                "%Choices; Do you want to submit 100 flowers?; Yes; No, not yet"],
                             '02:Second Meet': [{'Meetings':2},
                                                "Hi again... "]
                            }
        
        #What needs to be done:
        #For Choices strings, make it a list instead, depending on choice do selectedRect for next dialogue and then next dialogue after the choices string
        #Probably do in choiceResponse method.

        self.TextBox = None

        #self.image = pygame.Surface([self.width, self.height])
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def updateDialogue(self):
        conditions = self.dialogueList[self.dialogueStage][0]
        nextDialogue = True
        for check in conditions:
            if check == 'Meetings' and self.meetings < conditions[check]:
                nextDialogue = False
                break
        if nextDialogue:
            keys = list(self.dialogueList.keys())
            try:
                self.dialogueStage = keys[keys.index(self.dialogueStage)+1]
            except IndexError:
                pass
        self.dialogueStageIndex = 1


    def interaction(self):
        #Going into dialogue from explore
        if self.game.state == 'explore':
            self.meetings += 1
            self.TextBox = TextBox(self.game)
            self.TextBox.newText(self.dialogueList[self.dialogueStage][self.dialogueStageIndex], 20, 'Courier', self.name)
            self.dialogueStageIndex += 1
            self.game.state = 'dialogue'

        #While not finished with dialogue section
        elif self.dialogueStageIndex < len(self.dialogueList[self.dialogueStage]):
            nextDialogue = self.dialogueList[self.dialogueStage][self.dialogueStageIndex]
            #If there are choices displayed on the screen
            if len(self.TextBox.choiceRectList) > 0:
                self.choiceResponse(False)
                self.dialogueStageIndex += 1
                if self.dialogueStageIndex == len(self.dialogueList[self.dialogueStage]):
                    self.TextBox.kill()
                    self.updateDialogue()
                    self.game.state = 'explore'
                else:
                    self.interaction()
            #If the next dialogue to display is a choice list
            elif nextDialogue.find('%Choices') != -1:
                self.TextBox.kill()
                self.TextBox = TextBox(self.game)
                choicesList = nextDialogue.split(';')
                self.TextBox.newText(choicesList[1:], 20, 'Courier', self.name)
            #Displaying normal dialogue
            else:
                self.TextBox.kill()
                self.TextBox = TextBox(self.game)
                self.TextBox.newText(nextDialogue, 20, 'Courier', self.name)
                self.dialogueStageIndex += 1
        #When finished with dialogue
        else:
            self.TextBox.kill()
            self.updateDialogue()
            self.game.state = 'explore'

    #READ ME, FINISH WHEN CHOICES ARE DEFINED
    def choiceResponse(self, isFlavor):
        self.TextBox.choiceRectList = []
        pass
            
        
class Teleport(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.teleport
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.width = TILESIZE
        self.height = TILESIZE
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLUE)
        self.rect.x = self.x
        self.rect.y = self.y

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
        self.clock = game.clock
        self.timepassed = 0

        self.area = pygame.Rect(0, 0, self.width*0.6, self.height*0.95)
        self.avatarBox = pygame.Rect(self.width*0.693, self.height*0.1, self.width*0.219, self.height*0.65)
        self.image = pygame.transform.scale(pygame.image.load('Sprites/SVTextboxTemplate.png').convert_alpha(), (self.width, self.height))
        self.imagelist = os.listdir('Sprites/npcs/chipichipichapachapa')
        self.imgindex = 3

        self.selectedRect = 0
        self.choiceRectList = []

        image = pygame.transform.scale(pygame.image.load(f'Sprites/npcs/chipichipichapachapa/{self.imagelist[self.imgindex]}').convert_alpha(), (self.avatarBox.width, self.avatarBox.height))
        self.image.blit(image, self.avatarBox)
        #To see where the text and avatar area rectangles cover, uncomment below lines
        #pygame.draw.rect(self.image, RED, self.area)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def newText(self, text, fontSize, font, name):
        maxLength = int((float(-2.2835*10**(-7))*self.width**2+0.000411706*self.width+0.767647)*self.width/fontSize)+1
        boxFont = pygame.font.SysFont(font, fontSize)
        countRows = 0
        while(len(text) > 0):
            #If normal dialogue
            if type(text) == str:
                try:
                    cutoffIndex = len(text[:maxLength])-re.search('[^a-zA-Z0-9]', text[maxLength-1::-1]).end()+1
                except AttributeError:
                    cutoffIndex = maxLength
                self.image.blit(boxFont.render(text[0:cutoffIndex].strip(), False, (0, 0, 0)), (15, 10+countRows*fontSize), self.area)
                countRows += 1
                try:
                    text = text[cutoffIndex:]
                except:
                    break
            #If a choice dialogue
            else:
                if countRows == 0:
                    self.image.blit(pygame.font.SysFont(font, int(fontSize*1.2)).render(text[0].strip(), False, (0, 0, 0)), (15, 10+countRows*fontSize*1.2), self.area)
                    #self.choiceRectList.append(pygame.Rect(13, 10+countRows*fontSize*1.5, self.width*0.58, fontSize*1.5))
                else:
                    self.image.blit(boxFont.render(text[0].strip(), False, (0, 0, 0)), (15, 15+countRows*fontSize*1.5), self.area)
                    self.choiceRectList.append(pygame.Rect(13, 10+countRows*fontSize*1.5, self.width*0.58, fontSize*1.5))
                for rect in self.choiceRectList:
                    pygame.draw.rect(self.image, GRAY, rect, 2, 1)
                countRows += 1
                text = text[1:]
        self.image.blit(pygame.font.SysFont(font, 25).render(name, False, (0, 0, 0)), (self.avatarBox.x+self.avatarBox.width/2-len(name)*TILESIZE/5.5, self.height*0.79))

    
        
    def update(self):
        self.imgindex = (self.imgindex+1)%392 
        self.timepassed += self.clock.get_time()/1000
        image = pygame.transform.scale(pygame.image.load(f'Sprites/npcs/chipichipichapachapa/{self.imagelist[self.imgindex]}').convert_alpha(), (self.avatarBox.width, self.avatarBox.height))
        self.image.blit(image, self.avatarBox)
        if len(self.choiceRectList) > 0:
            for rect in range(len(self.choiceRectList)):
                if rect == self.selectedRect:
                    pygame.draw.rect(self.image, BLACK, self.choiceRectList[rect], 2, 1)
                else:
                    pygame.draw.rect(self.image, GRAY, self.choiceRectList[rect], 2, 1)


        

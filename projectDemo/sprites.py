import pygame
from settings import *
import items 
import math
import random
import re
import os


class Player(pygame.sprite.Sprite):
    itemUsed = False

    def __init__(self, game, x, y, clock):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        # The weapons available to the player are stored in a list

        self.weaponList = ['bubble', 'swordfish', 'trident']
        self.weaponNum = 0
        self.weapon = items.Weapon(self.game, self.weaponList[self.weaponNum], self)
        self.weaponAnimationCount = 0
        self.weaponAnimationSpeed = 18
        self.swordUsed = False
        self.spearUsed = False

        self.tutorial = Tutorial(self.game)

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
        self.downImgList = ['Sprites/protag/protagBlobDownNew.png', 'Sprites/protag/protagBlobDownLeftAlt.png', 'Sprites/protag/protagBlobDownNew.png', 'Sprites/protag/protagBlobDownRightAltNew.png',]

        #READ ME, ADD SPRITES FOR CUTTING WHILE FACING OTHER DIRECTIONS THAN RIGHT
        self.cutRightImgList = ['Sprites/protag/protagCut.png', 'Sprites/protag/protagCutRed.png', 'Sprites/protag/protagCutBlue.png', 'Sprites/protag/protagCutPlat.png']
        self.cutLeftImgList = ['Sprites/protag/protagCutLeft.png', 'Sprites/protag/protagCutRedLeft.png', 'Sprites/protag/protagCutBlueLeft.png', 'Sprites/protag/protagCutPlatLeft.png']
        self.cutUpImgList = ['Sprites/protag/protagCutUp.png', 'Sprites/protag/protagCutRedUp.png', 'Sprites/protag/protagCutBlueUp.png', 'Sprites/protag/protagCutPlatUp.png']
        self.cutDownImgList = ['Sprites/protag/protagCutDown.png', 'Sprites/protag/protagCutRedDown.png', 'Sprites/protag/protagCutBlueDown.png', 'Sprites/protag/protagCutPlatDown.png']
        self.cutUpgrade = 0


        #READ ME, ADD SPRITES FOR MINING WHILE FACING OTHER DIRECTIONS THAN RIGHT
        self.mineRightImgList = ['Sprites/protag/protagMine.png', 'Sprites/protag/protagMineRed.png', 'Sprites/protag/protagMineBlue.png', 'Sprites/protag/protagMinePlat.png']
        self.mineLeftImgList = ['Sprites/protag/protagMineLeft.png', 'Sprites/protag/protagMineRedLeft.png', 'Sprites/protag/protagMineBlueLeft.png', 'Sprites/protag/protagMinePlatLeft.png']
        self.mineUpImgList = ['Sprites/protag/protagMineUp.png', 'Sprites/protag/protagMineRedUp.png','Sprites/protag/protagMineBlueUp.png', 'Sprites/protag/protagMinePlatUp.png']
        self.mineDownImgList = ['Sprites/protag/protagMineDown.png', 'Sprites/protag/protagMineRedDown.png','Sprites/protag/protagMineBlueDown.png', 'Sprites/protag/protagMinePlatDown.png']
        self.mineUpgrade = 0

        self.rangedWeaponList = [pygame.image.load('Sprites/protag/protagRangedRight.png'), pygame.image.load('Sprites/protag/protagRangedDown.png'), pygame.image.load('Sprites/protag/protagRangedUp.png')]
        self.rangedWeaponList.append(pygame.transform.flip(self.rangedWeaponList[0], True, False))

        self.clock = clock
        self.timepassed = 0

        self.image = pygame.transform.scale(pygame.image.load(self.downImgList[self.imgindex]).convert_alpha(), (self.width, self.height))
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        #Below line is to decrease the rectangle collision slightly
        #Was having trouble fitting in 1 tile gaps
        #self.rect = pygame.Rect(self.x, self.y, 30, 30)

    def update(self):
        self.movement()
        self.interact()
        self.tutorial.draw()

        self.rect.x += self.xChange
        self.collideBlocks('x')
        self.rect.y += self.yChange
        self.collideBlocks('y')
        self.x = self.rect.x
        self.y = self.rect.y

        self.timepassed += self.clock.get_time()/1000
        #Below line: Loads image using right image list (transforms it to scale with width and height) and sets it to the image
        if self.game.state == 'explore' and not self.weapon.used:
            if self.facing == 'right':
                self.image = pygame.transform.scale(pygame.image.load(self.rightImgList[self.imgindex]), (self.width * 1, self.height * 1))
            elif self.facing == 'left':
                self.image = pygame.transform.scale(pygame.image.load(self.leftImgList[self.imgindex]), (self.width * 1, self.height * 1))
            elif self.facing == 'up':
                self.image = pygame.transform.scale(pygame.image.load(self.upImgList[self.imgindex]), (self.width * 1, self.height * 1))
            else: # self.facing == 'down':
                self.image = pygame.transform.scale(pygame.image.load(self.downImgList[self.imgindex]), (self.width * 1, self.height * 1))
        elif self.weapon.used and self.weapon.type == 'bubble'and self.weapon.ammo != 0:
            if self.facing == 'right':
                self.image = pygame.transform.scale(self.rangedWeaponList[0], (self.width * 1, self.height * 1))
            elif self.facing == 'left':
                self.image = pygame.transform.scale(self.rangedWeaponList[3], (self.width * 1, self.height * 1))
            elif self.facing == 'up':
                self.image = pygame.transform.scale(self.rangedWeaponList[2], (self.width * 1, self.height * 1))
            else: # self.facing == 'down':
                self.image = pygame.transform.scale(self.rangedWeaponList[1], (self.width * 1, self.height * 1))
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
        interacted = False

        if self.itemUsed:
            if self.facing == 'right':
                self.image = pygame.transform.scale(pygame.image.load(self.rightImgList[self.imgindex]), (self.width * 1, self.height * 1))
            elif self.facing == 'left':
                self.image = pygame.transform.scale(pygame.image.load(self.leftImgList[self.imgindex]),(self.width * 1, self.height * 1))
            elif self.facing == 'up':
                self.image = pygame.transform.scale(pygame.image.load(self.upImgList[self.imgindex]),(self.width * 1, self.height * 1))
            else:  # self.facing == 'down':
                self.image = pygame.transform.scale(pygame.image.load(self.downImgList[self.imgindex]),(self.width * 1, self.height * 1))



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
                interacted = True
                self.game.state = 'flowerC'
                self.game.flowers.get_sprite(flowerIndex).state = 'cutting'
                self.game.flowers.get_sprite(flowerIndex).anim()
                #READ ME, USE "self.facing" DIRECTIONS TO DETERMINE WHICH DIRECTION CUTTING SPRITE TO USE
                if self.facing == 'right':
                    self.image = pygame.transform.scale(pygame.image.load(self.cutRightImgList[self.cutUpgrade]), (self.width * 1.06, self.height * 1.06))
                elif self.facing == 'left':
                    self.image = pygame.transform.scale(pygame.image.load(self.cutLeftImgList[self.cutUpgrade]),   (self.width * 1.06, self.height * 1.06))
                elif self.facing == 'up':
                    self.image = pygame.transform.scale(pygame.image.load(self.cutUpImgList[self.cutUpgrade]), (self.width * 1.06, self.height * 1.06))
                else:
                    self.image = pygame.transform.scale(pygame.image.load(self.cutDownImgList[self.cutUpgrade]), (self.width * 1.06, self.height * 1.06))



            #Gets the index of the ore that the player interacted with
            oreIndex = interactRect.collidelist(list(ore.rect for ore in self.game.ores))
            if oreIndex != -1:
                interacted = True
                self.game.state = 'oreMine'
                self.game.ores.get_sprite(oreIndex).state = 'mining'
                self.game.ores.get_sprite(oreIndex).killAnim()
                if self.facing == 'right':
                    self.image = pygame.transform.scale(pygame.image.load(self.mineRightImgList[self.mineUpgrade]),(self.width * 1.06, self.height * 1.06))
                elif self.facing == 'left':
                    self.image = pygame.transform.scale(pygame.image.load(self.mineLeftImgList[self.mineUpgrade]),(self.width * 1.06, self.height * 1.06))
                elif self.facing == 'up':
                    self.image = pygame.transform.scale(pygame.image.load(self.mineUpImgList[self.mineUpgrade]),(self.width * 1.06, self.height * 1.06))
                else:
                    self.image = pygame.transform.scale(pygame.image.load(self.mineDownImgList[self.mineUpgrade]),(self.width * 1.06, self.height * 1.06))

            #Gets the index of the npc that the player interacted with
            npcIndex = interactRect.collidelist(list(npc.rect for npc in self.game.npcs))
            if npcIndex != -1:
                interacted = True
                self.game.npcs.get_sprite(npcIndex).interaction()
                pygame.time.wait(250)

            if not interacted:
                self.weapon.attack()

        #EDIT AFTER INVENTORY MADE
        elif keys[pygame.K_r]:
            self.weapon.reload()
            pygame.mixer.Channel(4).set_volume(0.025 * self.game.soundVol)
            pygame.mixer.Channel(4).play(pygame.mixer.Sound('Music/sound_effects/mag-slide-in-80901.mp3'))


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
                interacted = True
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
                if ((mouseRect.x-self.rect.x)**2+(mouseRect.y-self.rect.y)**2)**(1/2) <= 60:

                    interactIndex = mouseRect.collidelist(list(ore.rect for ore in self.game.ores))
                    if interactIndex != -1:
                        self.game.state = 'oreMine'
                        self.game.ores.get_sprite(interactIndex).state = 'mining'
                        self.game.ores.get_sprite(interactIndex).killAnim()
                        if self.facing == 'right':
                            self.image = pygame.transform.scale(pygame.image.load(self.mineRightImgList[self.mineUpgrade]),(self.width * 1.06, self.height * 1.06))
                        elif self.facing == 'left':
                            self.image = pygame.transform.scale(pygame.image.load(self.mineLeftImgList[self.mineUpgrade]),(self.width * 1.06, self.height * 1.06))
                        elif self.facing == 'up':
                            self.image = pygame.transform.scale(pygame.image.load(self.mineUpImgList[self.mineUpgrade]),(self.width * 1.06, self.height * 1.06))
                        else:
                            self.image = pygame.transform.scale(pygame.image.load(self.mineDownImgList[self.mineUpgrade]),(self.width * 1.06, self.height * 1.06))\

                    
                    interactIndex = mouseRect.collidelist(list(flower.rect for flower in self.game.flowers))
                    if interactIndex != -1:
                        self.game.state = 'flowerC'
                        self.game.flowers.get_sprite(interactIndex).state = 'cutting'
                        self.game.flowers.get_sprite(interactIndex).anim()
                        #READ ME, USE "self.facing" DIRECTIONS TO DETERMINE WHICH DIRECTION CUTTING SPRITE TO USE
                        if self.facing == 'right':
                            self.image = pygame.transform.scale(pygame.image.load(self.cutRightImgList[self.cutUpgrade]), (self.width * 1.06, self.height * 1.06))
                        elif self.facing == 'left':
                            self.image = pygame.transform.scale(pygame.image.load(self.cutLeftImgList[self.cutUpgrade]),   (self.width * 1.06, self.height * 1.06))
                        elif self.facing == 'up':
                            self.image = pygame.transform.scale(pygame.image.load(self.cutUpImgList[self.cutUpgrade]), (self.width * 1.06, self.height * 1.06))
                        else:
                            self.image = pygame.transform.scale(pygame.image.load(self.cutDownImgList[self.cutUpgrade]), (self.width * 1.06, self.height * 1.06))


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
            pygame.time.wait(50)
            self.game.createTilemap((tpSprite.x//TILESIZE, tpSprite.y//TILESIZE))
            pygame.time.wait(50)


    


    def movement(self):
        if self.game.state != 'explore':
            return
        #The key press segments came from viewing this tutorial
        #https://www.youtube.com/watch?v=GakNgbiAxzs&list=PLkkm3wcQHjT7gn81Wn-e78cAyhwBW3FIc&index=2
        keys = pygame.key.get_pressed()
        if not self.itemUsed:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                # Two lines below change camera to move around player character, moving all other sprites
                # comment them out to create a static camera
                #for sprite in self.game.all_sprites:
                    #sprite.rect.x += PLAYER_SPEED
                self.xChange -= PLAYER_SPEED
                self.facing = 'left'
                if ((self.timepassed) // (0.20) % 4 == self.imgindex):
                    self.imgindex = (self.imgindex + 1)%4
                    pygame.mixer.Channel(2).set_volume(0.04 * self.game.soundVol)
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/12_Player_Movement_SFX/08_Step_rock_02.wav'))
                else:
                    self.imgindex


            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                #for sprite in self.game.all_sprites:
                    #sprite.rect.x -= PLAYER_SPEED
                self.xChange += PLAYER_SPEED
                self.facing = 'right'
                if ((self.timepassed) // (0.20) % 4 == self.imgindex):
                    self.imgindex = (self.imgindex + 1)%4
                    pygame.mixer.Channel(2).set_volume(0.04 * self.game.soundVol)
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/12_Player_Movement_SFX/08_Step_rock_02.wav'))
                else:
                    self.imgindex

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                #for sprite in self.game.all_sprites:
                    #sprite.rect.y += PLAYER_SPEED
                self.yChange -= PLAYER_SPEED
                self.facing = 'up'
                if ((self.timepassed) // (0.18) % 4 == self.imgindex):
                    self.imgindex = (self.imgindex + 1)%4
                    pygame.mixer.Channel(2).set_volume(0.04 * self.game.soundVol)
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/12_Player_Movement_SFX/08_Step_rock_02.wav'))
                else:
                    self.imgindex


            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                #for sprite in self.game.all_sprites:
                    #sprite.rect.y -= PLAYER_SPEED
                self.yChange += PLAYER_SPEED
                self.facing = 'down'
                if ((self.timepassed) // (0.25) % 4 == self.imgindex):
                    self.imgindex = (self.imgindex + 1)%4
                    pygame.mixer.Channel(2).set_volume(0.04 * self.game.soundVol)
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/12_Player_Movement_SFX/08_Step_rock_02.wav'))
                else:
                    self.imgindex

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

    def attack(self, attackInstance):
        # This method will change the player's sprite when a melee attack is used, there will be separate images / animations
        # Depending on which melee weapon is in use
        # This method should only be getting called if the player's weapon type is one of the melee weapons
        if self.swordUsed:
            if self.facing == 'up':
                if attackInstance.animationPhase == 1:
                    self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingUp.png'), (self.width, self.height))
                elif attackInstance.animationPhase == 2:
                    self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingUp2.png'), (self.width, self.height))
                elif attackInstance.animationPhase == 3:
                    self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingUp3.png'), (self.width, self.height))

            elif self.facing == 'down':
                if attackInstance.animationPhase == 1:
                    self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingDown.png'), (self.width, self.height))
                elif attackInstance.animationPhase == 2:
                    self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingDown2.png'), (self.width, self.height))
                elif attackInstance.animationPhase == 3:
                    self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingDown3.png'), (self.width, self.height))

            elif self.facing == 'left':
                if attackInstance.animationPhase == 1:
                    self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingLeft.png'), (self.width, self.height))
                elif attackInstance.animationPhase == 2:
                    self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingLeft2.png'), (self.width, self.height))
                elif attackInstance.animationPhase == 3:
                    self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingLeft3.png'), (self.width, self.height))

            elif self.facing == 'right':
                if attackInstance.animationPhase == 1:
                    self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingRight.png'), (self.width, self.height))
                elif attackInstance.animationPhase == 2:
                    self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingRight2.png'), (self.width, self.height))
                elif attackInstance.animationPhase == 3:
                    self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingRight3.png'), (self.width, self.height))
        elif self.spearUsed:
            if self.facing == 'up':
                self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagThrowUp.png'), (self.width, self.height))
            elif self.facing == 'down':
                self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagThrowDown.png'),(self.width, self.height))
            elif self.facing == 'left':
                self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load('Sprites/protag/protagThrowRight.png'), True, False),(self.width, self.height))
            elif self.facing == 'right':
                self.image = pygame.transform.scale(pygame.image.load('Sprites/protag/protagThrowRight.png'),(self.width, self.height))

        pygame.display.update()

    def switchWeapons(self):
        # Method written by Eddie Suber
        if self.game.state == 'explore':
            # Player can use Q to switch weapons
            self.weaponNum += 1
            self.weaponNum %= len(self.weaponList)
            self.weapon.type = self.weaponList[self.weaponNum]
            self.weapon.updateDamage()
            pygame.mixer.Channel(1).set_volume(0.04 * self.game.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_UI_Menu_SFX/070_Equip_10.wav'))
        pass


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

        self.image = pygame.transform.scale(pygame.image.load('Sprites/tiles/brick1.png'), (self.width, self.height))
        #self.image.fill(RED)

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

        self.meetings = 0
        self.name = 'Dubidubidu'

        self.xChange = 0
        self.yChange = 0

        self.imagelist = ['Sprites/npcs/sampleNPC/hkprotagdown.jpg', 'Sprites/npcs/sampleNPC/hkprotagleft.jpg', 'Sprites/npcs/sampleNPC/hkprotagright.jpg', 'Sprites/npcs/sampleNPC/hkprotagdown.jpg']
        self.image = pygame.transform.scale(pygame.image.load(self.imagelist[0]).convert_alpha(), (self.width, self.height))

        self.dialogueStage = '01:First Meet'
        self.dialogueStageIndex = 1
        #Always leave a space/punctuation at the end of the quote!
        #Would you rather cum in the sink or sink in the cum? That is indeed the question for which we must all ponder and arrive at our own answers.
        self.dialogueList = {'01:First Meet':[{'Meetings': 1},
                                                "Testing dialogue ",
                                                "Chipichipi Chapachapa Dubidubi Dabadaba Magico Mi Dubi Dubi ",
                                                "Boom Boom Boom Boom ",
                                                "%Choices; Cats are cute?; Yes; Of Course; Meow"],
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
            self.game.play_music('dialogue')
            self.meetings += 1
            self.TextBox = TextBox(self.game)
            self.TextBox.newText(self.dialogueList[self.dialogueStage][self.dialogueStageIndex], 28, 'Garamond', self.name)
            self.dialogueStageIndex += 1
            self.game.state = 'dialogue'

        #While not finished with dialogue section
        elif self.dialogueStageIndex < len(self.dialogueList[self.dialogueStage]):
            nextDialogue = self.dialogueList[self.dialogueStage][self.dialogueStageIndex]
            #If there are choices displayed on the screen
            pygame.mixer.Channel(1).set_volume(0.06 * self.game.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/select-sound-121244.mp3'))
            if len(self.TextBox.choiceRectList) > 0:
                self.choiceResponse(False)
                self.dialogueStageIndex += 1
                if self.dialogueStageIndex == len(self.dialogueList[self.dialogueStage]):
                    self.TextBox.kill()
                    self.updateDialogue()
                    self.game.state = 'explore'
                    self.game.play_music('stop')
                    self.game.play_music('village')
                else:
                    self.interaction()
            #If the next dialogue to display is a choice list
            elif nextDialogue.find('%Choices') != -1:
                self.TextBox.kill()
                self.TextBox = TextBox(self.game)
                choicesList = nextDialogue.split(';')
                self.TextBox.newText(choicesList[1:], 28, 'Garamond', self.name)
            #Displaying normal dialogue
            else:
                self.TextBox.kill()
                self.TextBox = TextBox(self.game)
                self.TextBox.newText(nextDialogue, 28, 'Garamond', self.name)
                self.dialogueStageIndex += 1
        #When finished with dialogue
        else:
            self.TextBox.kill()
            self.updateDialogue()
            self.game.state = 'explore'
            self.game.play_music('stop')

    #READ ME, FINISH WHEN CHOICES ARE DEFINED
    def choiceResponse(self, isFlavor):
        self.TextBox.choiceRectList = []
        pass

#Authored by Max Chiu 4/16/2024
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.health = 100
        self.hitInvincible = False

        self.name = 'Udibudibudib'

        self.xChange = 0
        self.yChange = 0
        self.state = 'standing'

        self.imagelist = ['Sprites/npcs/sampleEnemy/sampleEnemyLeft.png', 'Sprites/npcs/sampleEnemy/sampleEnemyRight.png']
        #self.image = pygame.transform.scale(pygame.image.load(self.imagelist[0]).convert_alpha(), (2*self.width, 2*self.height))
        self.image = pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/joker.jpeg'), (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    #Authored: Max Chiu 4/18/2024
    def dealtDamage(self, damage, type):
        # print(self.hitInvincible)
        if type == 'bubble':
            self.health -= damage
            self.state = 'standing'
            pygame.mixer.Channel(4).set_volume(0.04 * self.game.soundVol)
            pygame.mixer.Channel(4).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_Battle_SFX/15_Impact_flesh_02.wav'))
        elif type == 'swordfish' or type == 'trident':
            self.health -= damage
            self.state = 'knockback'
            pygame.mixer.Channel(4).set_volume(0.04 * self.game.soundVol)
            pygame.mixer.Channel(4).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_Battle_SFX/03_Claw_03.wav'))
        if self.health <= 0:
            self.kill()
            pygame.mixer.Channel(4).set_volume(0.065 * self.game.soundVol)
            pygame.mixer.Channel(4).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_Battle_SFX/69_Enemy_death_01.wav'))
        print(f"enemy (self) health is {self.health}")


    #Authored: Max Chiu 4/18/2024
    def update(self):
        if self.state == 'standing':
            self.state = 'moving'
        elif self.state == 'knockback':
            pass
        else: #self.state == 'moving'

            self.x += self.xChange
            self.y += self.yChange

            self.rect.x = self.x
            self.rect.y = self.y
            
        
class Teleport(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
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

        self.area = pygame.Rect(0, 3, self.width*0.70, self.height*0.6)
        self.avatarBox = pygame.Rect(self.width*0.7134, self.height*0.13, self.width*0.24, self.height*0.73)
        self.image = pygame.transform.scale(pygame.image.load('Sprites/textbox2.png').convert_alpha(), (self.width, self.height*1.20))
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


    def textBreaker(self, text):
        # variable to keep track of text currently getting displayed
        # inspiration for this function: https://stackoverflow.com/questions/31381169/pygame-scrolling-dialogue-text
        # https://sentry.io/answers/python-yield-keyword/
        tprint = ''
        for letter in text:
            tprint += letter
            # this function yields and returns the updated text string for every character except if there is a space
            # in that case, the space is appended onto the string and the function yields after the following character
            if letter != ' ':
                # yield keyword pauses the current iteration of a sequence, in this case the for loop, and returns the
                # current value of the variable tprint. This iteration is picked up at the next letter when the function is called again.
                # it essentially returns the text given as a string that increases in length by one character each time.
                yield tprint


    #Function to actually display the text on the screen
    #Parameters: text is either a string displaying one textbox worth of dialogue or a list with the first element as the question and the rest as choices
    #fontSize is the font size, font is the font, and name is the NPC name
    def newText(self, text, fontSize, font, name):
        #Formula for the maximum number of characters that can fit on the screen assuming it's monospaced font
        maxLength = int((float(-2.2835*10**(-7))*self.width**2+0.001*self.width+0.767647)*self.width/fontSize)+1
        self.font = font
        self.fontSize = fontSize
        self.name = name
        boxFont = pygame.font.SysFont(font, fontSize)
        countRows = 0
        #currentText = textBreaker(text)
        while(len(text) > 0):
            #If normal dialogue
            if type(text) == str:
                try:
                    cutoffIndex = len(text[:maxLength])-re.search('[^a-zA-Z0-9]', text[maxLength-1::-1]).end()+1
                except AttributeError:
                    cutoffIndex = maxLength
                #print("cutoffIndex is ", cutoffIndex)
                #print("maxlength is ",  maxLength)
                #print("self.area is ", self.area)
                #print(15, 10+countRows*fontSize)
                self.image.blit(boxFont.render(text[0:cutoffIndex].strip(), False, (255, 255, 255)), (48, 40+countRows*fontSize), self.area)
                countRows += 1
                try:
                    text = text[cutoffIndex:]
                    #print(len(text))
                except:
                    break
            #If a choice dialogue
            else:
                if countRows == 0:
                    self.image.blit(pygame.font.SysFont(font, int(fontSize*1.2)).render(text[0].strip(), False, (255, 255, 255)), (48, 19+countRows*fontSize*1.2), self.area)
                    #self.choiceRectList.append(pygame.Rect(13, 10+countRows*fontSize*1.5, self.width*0.58, fontSize*1.5))
                else:
                    self.image.blit(boxFont.render(text[0].strip(), False, (255, 255, 255)), (48, 15+countRows*fontSize*1.5), self.area)
                    self.choiceRectList.append(pygame.Rect(44, 10+countRows*fontSize*1.5, self.width*0.58, fontSize*1.5))
                for rect in self.choiceRectList:
                    pygame.draw.rect(self.image, GRAY, rect, 2, 1)
                countRows += 1
                text = text[1:]


    
        
    def update(self):
        self.imgindex = (self.imgindex+1)%392 
        self.timepassed += self.clock.get_time()/1000
        image = pygame.transform.scale(pygame.image.load(f'Sprites/npcs/chipichipichapachapa/{self.imagelist[self.imgindex]}').convert_alpha(), (self.avatarBox.width, self.avatarBox.height))
        self.image.blit(image, self.avatarBox)
        self.image.blit(pygame.font.SysFont('Courier', 25).render(self.name, False, (255, 255, 255)),(self.avatarBox.x + self.avatarBox.width / 2 - len(self.name) * TILESIZE / 5.5, self.height * 0.89))
        if len(self.choiceRectList) > 0:
            for rect in range(len(self.choiceRectList)):
                if rect == self.selectedRect:
                    pygame.draw.rect(self.image, BLACK, self.choiceRectList[rect], 2, 1)
                else:
                    pygame.draw.rect(self.image, GRAY, self.choiceRectList[rect], 2, 1)


class Tutorial:
    def __init__(self, game):
        self.game = game
        self.appear = True


    def checkAppear(self):
        if (self.game.state != 'dialogue') and self.game.tutorialsActive:
            self.appear = True
        else:
            self.appear = False

    def draw(self):
        if self.appear:
            tutorialText = ["Use WASD to move, Q to switch weapons",
                            "E to attack using melee weapons",
                            "SPACE to fire ranged weapon or interact",
                            "R to reload ranged weapon",
                            "Press P to pause, change settings, disable tutorials, or quit."]
            #textSurf = pygame.font.SysFont('Garamond', 18).render(tutorialText[0].strip(), False, WHITE)
            #textSurf.set_alpha(127)
            #self.game.screen.blit(textSurf, (WIDTH * 0.72, HEIGHT * 0.78))
            self.game.screen.blit(pygame.font.SysFont('Garamond', 18).render(tutorialText[0].strip(), False, WHITE),(WIDTH * 0.72, HEIGHT * 0.78))
            #textSurf = pygame.font.SysFont('Garamond', 18).render(tutorialText[1].strip(), False, WHITE)
            #textSurf.set_alpha(127)
            #self.game.screen.blit(textSurf, (WIDTH * 0.78, HEIGHT * 0.81))
            self.game.screen.blit(pygame.font.SysFont('Garamond', 18).render(tutorialText[1].strip(), False, WHITE),(WIDTH * 0.78, HEIGHT * 0.81))
            #textSurf = pygame.font.SysFont('Garamond', 18).render(tutorialText[2].strip(), False, WHITE)
            #textSurf.set_alpha(127)
            #self.game.screen.blit(textSurf, (WIDTH * 0.73, HEIGHT * 0.84))
            #textSurf = pygame.font.SysFont('Garamond', 18).render(tutorialText[3].strip(), False, WHITE)
            #self.game.screen.blit(textSurf, (WIDTH * 0.81, HEIGHT * 0.87))
            self.game.screen.blit(pygame.font.SysFont('Garamond', 18).render(tutorialText[2].strip(), False, WHITE),(WIDTH * 0.73, HEIGHT * 0.84))
            #textSurf = pygame.font.SysFont('Garamond', 18).render(tutorialText[4].strip(), False, WHITE)
            #textSurf.set_alpha(127)
            #self.game.screen.blit(textSurf, (WIDTH * 0.64, HEIGHT * 0.9))
            self.game.screen.blit(pygame.font.SysFont('Garamond', 18).render(tutorialText[3].strip(), False, WHITE),(WIDTH * 0.81, HEIGHT * 0.87))
            self.game.screen.blit(pygame.font.SysFont('Garamond', 18).render(tutorialText[4].strip(), False, WHITE),(WIDTH * 0.64, HEIGHT * 0.9))
            #pygame.display.update()
        else:
            return
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
        self.weaponAnimationSpeed = 15
        self.swordUsed = False
        self.spearUsed = False

        self.tutorial = Tutorial(self.game)

        self.mouseRect = pygame.Rect(0, 0, 40, 40)
        self.mouseRect.center = pygame.mouse.get_pos()

        self.xChange = 0
        self.yChange = 0

        self.imgindex = 0
        self.facing = 'down'

        self.walkingList = [pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/12_Player_Movement_SFX/03_Step_grass_03.wav')]
        self.walkSoundNum = 0
        self.walkingSound = self.walkingList[self.walkSoundNum]
        # attribute to be used with the checkIdle function and used to regulate when the walking sound is played.
        # the walking sound should be played on a timer when the player's movement state is 'moving'
        self.movementState = 'idle'
        self.idleThreshold = 4
        self.idleTimer = self.idleThreshold
        self.walkSoundPlaying = False



        self.maxHealth = self.game.startPlayerMaxHealth
        self.targetHealth = self.game.priorPlayerHealth
        self.currentHealth = self.targetHealth
        #self.currentHealth = self.game.priorPlayerHealth
        self.maxHealthBarLength = 320
        self.healthBarHeight = 20
        self.healthRatio = self.maxHealth / self.maxHealthBarLength
        self.healthChangeSpeed = 12
        self.transitionWidth = 0
        self.transitionColor = (255, 0, 0)
        self.health_bar_rect = pygame.Rect(10, 10, self.currentHealth / self.healthRatio - 3, self.healthBarHeight)
        self.transition_bar_rect = pygame.Rect(self.health_bar_rect.right, 10, self.transitionWidth, self.healthBarHeight)
        self.hitInvulnerable = False
        self.hitInvulnerableTime = 0
        self.invulnerableTimer = 50

        #Shows the file paths for each image, depending on which direction the player is facing
        self.rightImgList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagLattern(1).png').convert_alpha(), (self.width, self.height)),
                             pygame.transform.scale(pygame.image.load('Sprites/protag/protagLatternAlt(2).png').convert_alpha(), (self.width, self.height)),
                             pygame.transform.scale(pygame.image.load('Sprites/protag/protagblobRight3.png').convert_alpha(), (self.width, self.height)),
                             pygame.transform.scale(pygame.image.load('Sprites/protag/protagLatternAlt(2).png').convert_alpha(), (self.width, self.height))]
        self.leftImgList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagBlobLeft.png').convert_alpha(), (self.width, self.height)),
                            pygame.transform.scale(pygame.image.load('Sprites/protag/protagBlobLeftAlt.png').convert_alpha(), (self.width, self.height)),
                            pygame.transform.scale(pygame.image.load('Sprites/protag/protagBlobLeft3.png').convert_alpha(), (self.width, self.height)),
                            pygame.transform.scale(pygame.image.load('Sprites/protag/protagBlobLeftAlt.png').convert_alpha(), (self.width, self.height))]
        self.upImgList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagBlobUpAlt.png').convert_alpha(), (self.width, self.height)),
                          pygame.transform.scale(pygame.image.load('Sprites/protag/protagBlobUpLeftAlt.png').convert_alpha(), (self.width, self.height)),
                          pygame.transform.scale(pygame.image.load('Sprites/protag/protagBlobUpAlt.png').convert_alpha(), (self.width, self.height)),
                          pygame.transform.scale(pygame.image.load('Sprites/protag/protagBlobUpRight.png').convert_alpha(), (self.width, self.height))]
        self.downImgList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagBlobDownNew.png').convert_alpha(), (self.width, self.height)),
                            pygame.transform.scale(pygame.image.load('Sprites/protag/protagBlobDownLeftAlt.png').convert_alpha(), (self.width, self.height)),
                            pygame.transform.scale(pygame.image.load('Sprites/protag/protagBlobDownNew.png').convert_alpha(), (self.width, self.height)),
                            pygame.transform.scale(pygame.image.load('Sprites/protag/protagBlobDownRightAltNew.png').convert_alpha(), (self.width, self.height))]

        #READ ME, ADD SPRITES FOR CUTTING WHILE FACING OTHER DIRECTIONS THAN RIGHT
        self.cutRightImgList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagCut.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                                pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutRed.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                                pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutBlue.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                                pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutPlat.png').convert_alpha(), (self.width * 1.06, self.height * 1.06))]
        self.cutLeftImgList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutLeft.png').convert_alpha()   , (self.width * 1.06, self.height * 1.06)),
                               pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutRedLeft.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                               pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutBlueLeft.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                               pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutPlatLeft.png').convert_alpha(), (self.width * 1.06, self.height * 1.06))]
        self.cutUpImgList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutUp.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                             pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutRedUp.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                             pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutBlueUp.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                             pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutPlatUp.png').convert_alpha(), (self.width * 1.06, self.height * 1.06))]
        self.cutDownImgList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutDown.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                               pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutRedDown.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                               pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutBlueDown.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                               pygame.transform.scale(pygame.image.load('Sprites/protag/protagCutPlatDown.png').convert_alpha(), (self.width * 1.06, self.height * 1.06))]
        self.cutUpgrade = 0


        #READ ME, ADD SPRITES FOR MINING WHILE FACING OTHER DIRECTIONS THAN RIGHT
        self.mineRightImgList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagMine.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                                 pygame.transform.scale(pygame.image.load('Sprites/protag/protagMineRed.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                                 pygame.transform.scale(pygame.image.load('Sprites/protag/protagMineBlue.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                                 pygame.transform.scale(pygame.image.load('Sprites/protag/protagMinePlat.png').convert_alpha(), (self.width * 1.06, self.height * 1.06))]
        self.mineLeftImgList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagMineLeft.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                                pygame.transform.scale(pygame.image.load('Sprites/protag/protagMineRedLeft.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                                pygame.transform.scale(pygame.image.load('Sprites/protag/protagMineBlueLeft.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                                pygame.transform.scale(pygame.image.load('Sprites/protag/protagMinePlatLeft.png').convert_alpha(), (self.width * 1.06, self.height * 1.06))]
        self.mineUpImgList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagMineUp.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                              pygame.transform.scale(pygame.image.load('Sprites/protag/protagMineRedUp.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                              pygame.transform.scale(pygame.image.load('Sprites/protag/protagMineBlueUp.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                              pygame.transform.scale(pygame.image.load('Sprites/protag/protagMinePlatUp.png').convert_alpha(), (self.width * 1.06, self.height * 1.06))]
        self.mineDownImgList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagMineDown.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                                pygame.transform.scale(pygame.image.load('Sprites/protag/protagMineRedDown.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                                pygame.transform.scale(pygame.image.load('Sprites/protag/protagMineBlueDown.png').convert_alpha(), (self.width * 1.06, self.height * 1.06)),
                                pygame.transform.scale(pygame.image.load('Sprites/protag/protagMinePlatDown.png').convert_alpha(), (self.width * 1.06, self.height * 1.06))]
        self.mineUpgrade = 0

        self.rangedWeaponList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagRangedRight.png').convert_alpha(), (self.width, self.height)),
                                 pygame.transform.scale(pygame.image.load('Sprites/protag/protagRangedDown.png').convert_alpha(), (self.width, self.height)),
                                 pygame.transform.scale(pygame.image.load('Sprites/protag/protagRangedUp.png').convert_alpha(), (self.width, self.height))]
        self.rangedWeaponList.append(pygame.transform.flip(self.rangedWeaponList[0], True, False))

        self.swingUpList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingUp.png').convert_alpha(), (self.width, self.height)),
                            pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingUp2.png').convert_alpha(), (self.width, self.height)),
                            pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingUp3.png').convert_alpha(), (self.width, self.height))]
        self.swingDownList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingDown.png').convert_alpha(), (self.width, self.height)),
                              pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingDown2.png').convert_alpha(), (self.width, self.height)),
                              pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingDown3.png').convert_alpha(), (self.width, self.height))]

        self.swingLeftList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingLeft.png').convert_alpha(), (self.width, self.height)),
                              pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingLeft2.png').convert_alpha(), (self.width, self.height)),
                              pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingLeft3.png').convert_alpha(), (self.width, self.height))]
        self.swingRightList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingRight.png').convert_alpha(), (self.width, self.height)),
                               pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingRight2.png').convert_alpha(), (self.width, self.height)),
                               pygame.transform.scale(pygame.image.load('Sprites/protag/protagSwingRight3.png').convert_alpha(), (self.width, self.height))]
        self.pokeList = [pygame.transform.scale(pygame.image.load('Sprites/protag/protagThrowUp.png').convert_alpha(), (self.width, self.height)),
                         pygame.transform.scale(pygame.image.load('Sprites/protag/protagThrowDown.png').convert_alpha(),(self.width, self.height)),
                         pygame.transform.scale(pygame.transform.flip(pygame.image.load('Sprites/protag/protagThrowRight.png').convert_alpha(), True, False),(self.width, self.height)),
                         pygame.transform.scale(pygame.image.load('Sprites/protag/protagThrowRight.png').convert_alpha(),(self.width, self.height))]

        self.clock = clock
        self.timepassed = 0

        self.image = self.downImgList[self.imgindex]
        

        #self.rect = self.image.get_rect()
        #Below line is to decrease the rectangle collision slightly
        #Was having trouble fitting in 1 tile gaps
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.checkIdle()
        self.interact()
        self.tutorial.draw()
        if self.currentHealth <= 0:
            self.game.state = 'game over'

        self.rect.x += self.xChange
        self.collideBlocks('x')
        self.rect.y += self.yChange
        self.collideBlocks('y')
        self.x = self.rect.x
        self.y = self.rect.y


        if self.hitInvulnerable:
            self.hitInvulnerableTime += 1
            if self.hitInvulnerableTime > self.invulnerableTimer:
                self.hitInvulnerable = False
                self.hitInvulnerableTime = 0


        self.timepassed += self.clock.get_time()/1000
        #Below line: Loads image using right image list (transforms it to scale with width and height) and sets it to the image
        if self.game.state == 'explore' and not self.weapon.used:
            if self.facing == 'right':
                self.image = self.rightImgList[self.imgindex]
            elif self.facing == 'left':
                self.image = self.leftImgList[self.imgindex]
            elif self.facing == 'up':
                self.image = self.upImgList[self.imgindex]
            else: # self.facing == 'down':
                self.image = self.downImgList[self.imgindex]
        elif self.weapon.used and self.weapon.type == 'bubble'and self.weapon.ammo != 0:
            if self.facing == 'right':
                self.image = self.rangedWeaponList[0]
            elif self.facing == 'left':
                self.image = self.rangedWeaponList[3]
            elif self.facing == 'up':
                self.image = self.rangedWeaponList[2]
            else: # self.facing == 'down':
                self.image = self.rangedWeaponList[1]

        self.flicker()

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

    def setLocation(self, x, y):
        pass

    # inspiration for this function and the damage flickering effect was gotten from:
    # https://www.youtube.com/watch?v=QU1pPzEGrqw
    def flicker(self):
        alpha = 0
        value = math.sin(pygame.time.get_ticks())
        if value >= 0:
            alpha = 255
        else:
            alpha = 0
        if self.hitInvulnerable:
            self.image.set_alpha(alpha)
            #print(self.image.get_alpha())
        else:
            self.image.set_alpha(255)
        pass

    def getDamage(self, amount):
        # self.currentHealth = self.targetHealth
        if self.hitInvulnerable:
            return
        else:
            self.hitInvulnerable = True
            if self.targetHealth > 0:
                self.targetHealth = self.targetHealth - amount
            if self.targetHealth <=0:
                self.targetHealth = 0
            pygame.mixer.Channel(1).set_volume(0.035 * self.game.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_Battle_SFX/77_flesh_02.wav'))

    def getHealth(self, amount):
        if self.targetHealth < self.maxHealth:
            self.targetHealth = self.targetHealth + amount
        if self.targetHealth > self.maxHealth:
            self.targetHealth = self.maxHealth
        pygame.mixer.Channel(1).set_volume(0.015 * self.game.soundVol)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/8_Buffs_Heals_SFX/02_Heal_02.wav'))

    def healthBar(self): # Static health bar function
        pygame.draw.rect(self.game.screen, (255, 0, 0), (10, 10, self.targetHealth/self.healthRatio, self.healthBarHeight))
        pygame.draw.rect(self.game.screen, (255, 255, 255), (10, 10, self.maxHealthBarLength,self.healthBarHeight), 4)

    def animateHealth(self): # Animated health bar function
        if self.currentHealth < self.targetHealth:
            self.currentHealth += self.healthChangeSpeed
            self.transitionWidth = int((self.targetHealth - self.currentHealth)/self.healthRatio)
            self.transitionColor = (0, 255, 0)
            self.health_bar_rect = pygame.Rect(10, 10, self.currentHealth / self.healthRatio - 3, self.healthBarHeight)
            self.transition_bar_rect = pygame.Rect(self.health_bar_rect.right, 10, self.transitionWidth, self.healthBarHeight)
        elif self.currentHealth > self.targetHealth:
            self.currentHealth -= self.healthChangeSpeed
            self.transitionWidth = int((self.currentHealth - self.targetHealth)/self.healthRatio)
            self.transitionColor = (255, 255, 0)
            self.health_bar_rect = pygame.Rect(10, 10, self.targetHealth / self.healthRatio - 3, self.healthBarHeight)
            self.transition_bar_rect = pygame.Rect(self.health_bar_rect.right, 10, self.transitionWidth, self.healthBarHeight)


        pygame.draw.rect(self.game.screen, (255, 0, 0 ), self.health_bar_rect)
        pygame.draw.rect(self.game.screen, self.transitionColor, self.transition_bar_rect)
        pygame.draw.rect(self.game.screen, (255, 255, 255), (10, 10, self.maxHealthBarLength, self.healthBarHeight), 4)


    #Method for different Player interactions
    def interact(self):
        keys = pygame.key.get_pressed()
        mouses = pygame.mouse.get_pressed()
        interacted = False

        if self.itemUsed:
            if self.facing == 'right':
                self.image = self.rightImgList[self.imgindex]
            elif self.facing == 'left':
                self.image = self.leftImgList[self.imgindex]
            elif self.facing == 'up':
                self.image = self.upImgList[self.imgindex]
            else:  # self.facing == 'down':
                self.image = self.downImgList[self.imgindex]



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
                    self.image = self.cutRightImgList[self.cutUpgrade]
                elif self.facing == 'left':
                    self.image = self.cutLeftImgList[self.cutUpgrade]
                elif self.facing == 'up':
                    self.image = self.cutUpImgList[self.cutUpgrade]
                else:
                    self.image = self.cutDownImgList[self.cutUpgrade]



            #Gets the index of the ore that the player interacted with
            oreIndex = interactRect.collidelist(list(ore.rect for ore in self.game.ores))
            if oreIndex != -1:
                interacted = True
                self.game.state = 'oreMine'
                self.game.ores.get_sprite(oreIndex).state = 'mining'
                self.game.ores.get_sprite(oreIndex).killAnim()
                if self.facing == 'right':
                    self.image = self.mineRightImgList[self.mineUpgrade]
                elif self.facing == 'left':
                    self.image = self.mineLeftImgList[self.mineUpgrade]
                elif self.facing == 'up':
                    self.image = self.mineUpImgList[self.mineUpgrade]
                else:
                    self.image = self.mineDownImgList[self.mineUpgrade]

            #Gets the index of the npc that the player interacted with
            npcIndex = interactRect.collidelist(list(npc.rect for npc in self.game.npcs))
            if npcIndex != -1:
                interacted = True
                self.game.npcs.get_sprite(npcIndex).interaction()
                pygame.time.wait(250)

            if not interacted:
                self.weapon.attack()

            

        #EDIT AFTER INVENTORY MADE
        elif keys[pygame.K_r] and self.weapon.type == 'bubble':
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
                            self.image = self.mineRightImgList[self.mineUpgrade]
                        elif self.facing == 'left':
                            self.image = self.mineLeftImgList[self.mineUpgrade]
                        elif self.facing == 'up':
                            self.image = self.mineUpImgList[self.mineUpgrade]
                        else:
                            self.image = self.mineDownImgList[self.mineUpgrade]

                    
                    interactIndex = mouseRect.collidelist(list(flower.rect for flower in self.game.flowers))
                    if interactIndex != -1:
                        self.game.state = 'flowerC'
                        self.game.flowers.get_sprite(interactIndex).state = 'cutting'
                        self.game.flowers.get_sprite(interactIndex).anim()

                        #READ ME, USE "self.facing" DIRECTIONS TO DETERMINE WHICH DIRECTION CUTTING SPRITE TO USE
                        if self.facing == 'right':
                            self.image = self.cutRightImgList[self.cutUpgrade]
                        elif self.facing == 'left':
                            self.image = self.cutLeftImgList[self.cutUpgrade]
                        elif self.facing == 'up':
                            self.image = self.cutUpImgList[self.cutUpgrade]
                        else:
                            self.image = self.cutDownImgList[self.cutUpgrade]


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
            #pygame.time.wait(50)
            self.game.createTilemap((tpSprite.x//TILESIZE, tpSprite.y//TILESIZE))
            #pygame.time.wait(50)


    


    def movement(self):
        if self.game.state != 'explore':
            return

        if self.imgindex == 1:
            self.playWalkSound()
            #if self.walkSoundNum == 3:
            #    self.walkSoundNum = 4
            #elif self.walkSoundNum == 4:
            #    self.walkSoundNum = 3
            #self.walkSoundNum = random.randint(0, len(self.walkingList) - 1)
            self.walkingSound = self.walkingList[self.walkSoundNum]
        elif (self.imgindex != 1):
            self.walkSoundPlaying = False


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
                self.idleTimer = 0
                if ((self.timepassed) // (0.20) % 4 == self.imgindex):
                    self.imgindex = (self.imgindex + 1)%4
                    #if self.imgindex == 1 or self.imgindex == 3:
                    #    pygame.mixer.Channel(2).set_volume(0.08 * self.game.soundVol)
                    #    pygame.mixer.Channel(2).play(self.walkingSound)
                else:
                    self.imgindex


            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                #for sprite in self.game.all_sprites:
                    #sprite.rect.x -= PLAYER_SPEED
                self.xChange += PLAYER_SPEED
                self.facing = 'right'
                self.idleTimer = 0
                if ((self.timepassed) // (0.20) % 4 == self.imgindex):
                    self.imgindex = (self.imgindex + 1)%4
                    #if self.imgindex == 1 or self.imgindex == 3:
                    #    pygame.mixer.Channel(2).set_volume(0.08 * self.game.soundVol)
                    #    pygame.mixer.Channel(2).play(self.walkingSound)
                else:
                    self.imgindex

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                #for sprite in self.game.all_sprites:
                    #sprite.rect.y += PLAYER_SPEED
                self.yChange -= PLAYER_SPEED
                self.facing = 'up'
                self.idleTimer = 0
                if ((self.timepassed) // (0.18) % 4 == self.imgindex):
                    self.imgindex = (self.imgindex + 1)%4
                    #if self.imgindex == 1 or self.imgindex == 3:
                    #    pygame.mixer.Channel(2).set_volume(0.08* self.game.soundVol)
                    #    pygame.mixer.Channel(2).play(self.walkingSound)
                else:
                    self.imgindex


            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                #for sprite in self.game.all_sprites:
                    #sprite.rect.y -= PLAYER_SPEED
                self.yChange += PLAYER_SPEED
                self.facing = 'down'
                self.idleTimer = 0
                if ((self.timepassed) // (0.25) % 4 == self.imgindex):
                    self.imgindex = (self.imgindex + 1)%4
                    #if self.imgindex == 1 or self.imgindex == 3:
                    #    pygame.mixer.Channel(2).set_volume(0.08 * self.game.soundVol)
                    #    pygame.mixer.Channel(2).play(self.walkingSound)
                else:
                    self.imgindex

    # function that will check if the player is idle from moving. This will be done by using a timer that is decremented unless the player moves, or the movement state will be changed to idle from moving.
    def checkIdle(self):
        self.idleTimer += 1
        if self.game.state != 'explore':
            self.movementState = 'idle'
        elif self.idleTimer >= self.idleThreshold:
            self.movementState = 'idle'
        else:
            self.movementState = 'moving'
        if self.movementState == 'idle' and self.game.state == 'explore':
            self.imgindex = 0
            if self.facing == 'right':
                self.image = self.rightImgList[self.imgindex]
            elif self.facing == 'left':
                self.image = self.leftImgList[self.imgindex]
            elif self.facing == 'up':
                self.image = self.upImgList[self.imgindex]
            else:  # self.facing == 'down':
                self.image = self.downImgList[self.imgindex]


    def playWalkSound(self):
        if self.movementState != 'idle' and (not self.walkSoundPlaying):
            pygame.mixer.Channel(2).set_volume(0.08 * self.game.soundVol)
            pygame.mixer.Channel(2).play(self.walkingSound)
            self.walkSoundPlaying = True

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
                    self.image = self.swingUpList[0]
                elif attackInstance.animationPhase == 2:
                    self.image = self.swingUpList[1]
                elif attackInstance.animationPhase == 3:
                    self.image = self.swingUpList[2]

            elif self.facing == 'down':
                if attackInstance.animationPhase == 1:
                    self.image = self.swingDownList[0]
                elif attackInstance.animationPhase == 2:
                    self.image = self.swingDownList[1]
                elif attackInstance.animationPhase == 3:
                    self.image = self.swingDownList[2]

            elif self.facing == 'left':
                if attackInstance.animationPhase == 1:
                    self.image = self.swingLeftList[0]
                elif attackInstance.animationPhase == 2:
                    self.image = self.swingLeftList[1]
                elif attackInstance.animationPhase == 3:
                    self.image = self.swingLeftList[2]

            elif self.facing == 'right':
                if attackInstance.animationPhase == 1:
                    self.image = self.swingRightList[0]
                elif attackInstance.animationPhase == 2:
                    self.image = self.swingRightList[1]
                elif attackInstance.animationPhase == 3:
                    self.image = self.swingRightList[2]
        elif self.spearUsed:
            if self.facing == 'up':
                self.image = self.pokeList[0]
            elif self.facing == 'down':
                self.image = self.pokeList[1]
            elif self.facing == 'left':
                self.image = self.pokeList[2]
            elif self.facing == 'right':
                self.image = self.pokeList[3]

        pygame.display.update()

    def switchWeapons(self):
        # Method written by Eddie Suber
        if self.game.state == 'explore':
            # Player can use Q to switch weapons
            self.weaponNum += 1
            self.weaponNum %= len(self.weaponList)
            self.weapon.type = self.weaponList[self.weaponNum]
            self.weapon.updateDamage()
            if self.weapon.type == 'swordfish':
                self.weaponAnimationSpeed = 15
            elif self.weapon.type == 'trident':
                self.weaponAnimationSpeed = 18
            pygame.mixer.Channel(1).set_volume(0.04 * self.game.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_UI_Menu_SFX/070_Equip_10.wav'))
        pass


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, index):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        #self.width = TILESIZE
        #self.height = TILESIZE

        #self.imagelist = ['Sprites/tiles/brick1.png',
        #                  'Sprites/tiles/water1.png',
        #                  'Sprites/tiles/sapling2.png',
        #                  'Sprites/tiles/rock1.png']
        self.image = self.game.tileList[1][index]
        #self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class WalkableBlock(pygame.sprite.Sprite):
    def __init__(self, game, x, y, index):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.walk_blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        #self.imagelist = [pygame.transform.scale(pygame.image.load('Sprites/tiles/crossBridge1.png').convert_alpha(), (self.width, self.height)),
        #                pygame.transform.scale(pygame.image.load('Sprites/tiles/growth1.png').convert_alpha(), (self.width, self.height))]
        self.image = self.game.tileList[0][index]
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

        self.imagelist = ['Sprites/npcs/sampleNPC/hkprotagdown.jpg',
                          'Sprites/npcs/sampleNPC/hkprotagleft.jpg',
                          'Sprites/npcs/sampleNPC/hkprotagright.jpg',
                          'Sprites/npcs/sampleNPC/hkprotagdown.jpg']
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
            pygame.mixer.Channel(1).set_volume(0.03 * self.game.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/select-sound-121244.mp3'))
            self.meetings += 1
            self.TextBox = TextBox(self.game)
            self.TextBox.newText(self.dialogueList[self.dialogueStage][self.dialogueStageIndex], 28, 'Garamond', self.name)
            self.dialogueStageIndex += 1
            self.game.state = 'dialogue'

        #While not finished with dialogue section
        elif self.dialogueStageIndex < len(self.dialogueList[self.dialogueStage]):
            nextDialogue = self.dialogueList[self.dialogueStage][self.dialogueStageIndex]
            #If there are choices displayed on the screen
            pygame.mixer.Channel(1).set_volume(0.03 * self.game.soundVol)
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
        self.map = currentTileMap[mapList[self.game.map[0]][self.game.map[1]]]
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.type = 'pumpkinRobot'

        self.health = 100
        self.damage = 120
        self.speed = PLAYER_SPEED * 0.6

        self.hitInvincible = False
        self.hitInvulnerable = False
        self.hitInvulnerableTime = 0
        self.invulnerableTimer = 24
        self.stunned = False
        self.stunCount = 0
        self.stunTimer = 8

        self.name = 'Udibudibudib'

        self.xChange = 0
        self.yChange = 0
        self.state = 'standing'
        self.moving = False
        self.facingDirection = 'down'

        self.pumpkinImgDown = [
            pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeIdle.png').convert_alpha(),(TILESIZE * 0.99, TILESIZE * 0.99)),
            pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeDownRight (1).png').convert_alpha(),(TILESIZE * 0.99, TILESIZE * 0.99)),
            pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeIdle.png').convert_alpha(),(TILESIZE * 0.99, TILESIZE * 0.99)),
            pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeDownLeft.png').convert_alpha(),(TILESIZE * 0.99, TILESIZE * 0.99))]
        # pumpkinImgDown = [pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeDownRight (1).png').convert_alpha(), (TILESIZE * 0.99, TILESIZE * 0.99)),
        #                  pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeDownLeft.png').convert_alpha(), (TILESIZE * 0.99, TILESIZE * 0.99))]

        self.pumpkinRobot = {'down': self.pumpkinImgDown, 'damage': 120, 'health': 100, 'speed': PLAYER_SPEED * 0.5}

        self.imagelist = self.pumpkinRobot['down']
        #self.deathImgList = [pygame.transform.scale(pygame.image.load('').convert_alpha(), (self.width, self.height))]
        #self.image = pygame.transform.scale(pygame.image.load(self.imagelist[0]).convert_alpha(), (2*self.width, 2*self.height))
        self.imageIndex = 0
        self.image = self.imagelist[self.imageIndex]
        self.animationCount = 0
        self.animationSpeed = 36

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.setup()

    def setup(self):
        if self.type == 'pumpkinRobot':
            self.health = self.pumpkinRobot['health']
            self.speed = self.pumpkinRobot['speed']
            self.damage = self.pumpkinRobot['damage']
            self.imagelist = self.pumpkinRobot['down']

    def deathAnimation(self):
        pass

    def flicker(self):
        alpha = 0
        value = math.sin(pygame.time.get_ticks())
        if value >= 0:
            alpha = 255
        else:
            alpha = 0
        if self.hitInvulnerable:
            self.image.set_alpha(alpha)
            print(self.image.get_alpha())
        else:
            self.image.set_alpha(255)
        pass

    #Authored: Max Chiu 4/18/2024
    def dealtDamage(self, damage, type):
        # print(self.hitInvincible)
        if not self.hitInvulnerable:
            if type == 'bubble':
                self.health -= damage
                self.stunned = True
                self.state = 'standing'
                pygame.mixer.Channel(4).set_volume(0.06 * self.game.soundVol)
                pygame.mixer.Channel(4).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_Battle_SFX/15_Impact_flesh_02.wav'))
            elif type == 'swordfish' or type == 'trident':
                self.speed *= 0.7
                self.hitInvulnerable = True
                self.health -= damage
                self.state = 'knockback'
                pygame.mixer.Channel(4).set_volume(0.06 * self.game.soundVol)
                pygame.mixer.Channel(4).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_Battle_SFX/03_Claw_03.wav'))
            if self.health <= 0:
                self.kill()
                pygame.mixer.Channel(4).set_volume(0.065 * self.game.soundVol)
                pygame.mixer.Channel(4).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_Battle_SFX/69_Enemy_death_01.wav'))
            print(f"enemy (self) health is {self.health}")
        else:
            return

    def animate(self):

        if self.moving:
            self.animationCount+= 1
            if self.animationCount >= self.animationSpeed:
                self.animationCount = 0
           # for i in range(len(self.imagelist)):
                #if self.animationCount < (self.animationSpeed // len(self.imagelist) * (i + 1)):
                    #self.imageIndex = i
                    #break
            if self.animationCount < (self.animationSpeed // len(self.imagelist)):
                self.imageIndex = 0
            elif self.animationCount < (self.animationSpeed // len(self.imagelist) * 2):
                self.imageIndex = 1
            elif self.animationCount < (self.animationSpeed // len(self.imagelist) * 3):
                self.imageIndex = 2
            elif self.animationCount < (self.animationSpeed // len(self.imagelist) * 4):
                self.imageIndex = 3
            self.image = self.imagelist[self.imageIndex]
        self.flicker()

    #Authored: Max Chiu 4/18/2024
    def update(self):
        if self.game.state != 'dialogue' and self.game.state != 'scene' and self.game.state != 'pause' and self.game.state != 'game over':
            self.searchPlayer()
            self.animate()
            self.attack()



            if self.state == 'standing':
                self.yChange = 0
                self.xChange = 0
                if self.stunned:
                    self.stunCount += 1
                    if self.stunCount > self.stunTimer:
                        self.stunned = False
                        self.stunCount = 0

            elif self.state == 'knockback':
                self.rect.x += self.xChange * -1
                self.collideBlocks('x')
                self.rect.y += self.yChange * -1
                self.collideBlocks('y')

                self.x = self.rect.x
                self.y = self.rect.y
                pass
            else: #self.state == 'chasing'
                self.rect.x += self.xChange
                self.collideBlocks('x')
                self.rect.y += self.yChange
                self.collideBlocks('y')

                self.x = self.rect.x
                self.y = self.rect.y

            if self.hitInvulnerable:
                self.hitInvulnerableTime += 1
                if self.hitInvulnerableTime > self.invulnerableTimer:
                    self.hitInvulnerable = False
                    self.hitInvulnerableTime = 0
                    self.speed *= (1/0.7)

    #Authored: Max Chiu 4/28/2024
    def searchPlayer(self):
        playerPos = [self.game.player.x, self.game.player.y]

        lines=[]
        px = playerPos[0]+self.game.player.width/2
        py = playerPos[1]+self.game.player.height/2
        ex = self.x+self.width/2
        ey = self.y+self.height/2
        n = 4
        dx = (px - ex)/n
        dy = (py - ey)/n

        distance = math.sqrt((dx*n)**2+(dy*n)**2)

        surface = pygame.Surface(self.game.screen.get_size(), pygame.SRCALPHA)
        for i in range(n):
            lines.append(pygame.draw.line(surface, (0, 255, 0, 0), (ex+dx*i, ey+dy*i), (ex+dx*(i+1), ey+dy*(i+1)), 1))
        #line = pygame.draw.line(self.screen, RED, (self.enemy.x+self.enemy.width/2, self.enemy.y+self.enemy.height/2), (self.player.x+self.player.width/2, self.player.y+self.player.height/2), 2)
        index = [line.collidelist(list(block.rect for block in self.game.blocks)) for line in lines]
        move = True
        for i in index:
            if i != -1:
                #print(i)
                rect = self.game.blocks.get_sprite(i)
                #rect.image.fill(BLUE)
                move = False

        if move:
            self.moving = True
            if not self.hitInvulnerable and not self.stunned:
                self.state = 'chasing'
            try:
                dx *= n/distance
                dy *= n/distance
            except ZeroDivisionError:
                dy = dy
                dx = dx
            self.xChange = dx * self.speed
            self.yChange = dy * self.speed
            # print(self.xChange, self.yChange)
        elif not move:
            self.xChange = 0
            self.yChange = 0
            self.state = 'standing'
            self.moving = False
            return

    #Authored: Max Chiu 4/28/2024
    def collideBlocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) + pygame.sprite.spritecollide(self, self.game.npcs, False) + pygame.sprite.spritecollide(self, self.game.enemies, False)
            if hits and hits[0] != self:
                if self.xChange > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.xChange < 0:
                    self.rect.x = hits[0].rect.right
        else:
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) + pygame.sprite.spritecollide(self, self.game.npcs, False) + pygame.sprite.spritecollide(self, self.game.enemies, False)
            if hits and hits[0] != self:
                if self.yChange > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.yChange < 0:
                    self.rect.y = hits[0].rect.bottom

    def attack(self):
        if pygame.sprite.collide_rect(self, self.game.player):
            self.game.player.getDamage(self.damage)

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


class Inventory(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self._layer = TEXT_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.hotbar_img = [pygame.transform.scale(pygame.image.load('Sprites/items/sunflowernew.png').convert_alpha(), (TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/oreAmethyst.png').convert_alpha(), (TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/potion.png').convert_alpha(), (TILESIZE, TILESIZE))]


        self.x = 1*TILESIZE
        self.y = 15.5*TILESIZE
        self.width = 5.5*TILESIZE
        self.height = 2.5*TILESIZE

        self.image = pygame.transform.scale(pygame.image.load('Sprites/hudImages/pixil-frame-0_cropped.png'), (self.width, self.height))
        #self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.font = pygame.font.SysFont("Calibri", 20)
        self.slots = {"flower":0, "ore":0, "potion": 0}

        for i in range(len(self.hotbar_img)):
            self.image.blit(self.hotbar_img[i], pygame.Rect(25+65*(i),30,0,0))

        self.numList = []
        self.numList.append(self.image.blit(self.font.render(str(self.slots.get('flower')),False,(WHITE)),(60,53)))
        self.numList.append(self.image.blit(self.font.render(str(self.slots.get('ore')),False,(WHITE)),(125,53)))
        self.numList.append(self.image.blit(self.font.render(str(self.slots.get('potion')),False,(WHITE)),(190,53)))

    def add_item(self, item):
        self.slots[item] =  self.slots.get(item) + 1
        for image in self.numList:
            pygame.draw.rect(self.image, BLACK, image)
        self.numList.append(self.image.blit(self.font.render(str(self.slots.get('flower')),False,(WHITE)),(60,53)))
        self.numList.append(self.image.blit(self.font.render(str(self.slots.get('ore')),False,(WHITE)),(125,53)))
        self.numList.append(self.image.blit(self.font.render(str(self.slots.get('potion')),False,(WHITE)),(190,53)))
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

import pygame
#from pygame.sprite import _Group
from settings import *
import items 
import math
import random
import re
import os
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


class Player(pygame.sprite.Sprite):
    itemUsed = False



    def __init__(self, game, x, y, clock):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.non_background
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * 0.98
        self.height = TILESIZE * 0.98
        self.speed = PLAYER_SPEED


        # The weapons available to the player are stored in a list

        self.weaponList = ['swordfish', 'bubble', 'trident']
        # This list below holds the weapons that the player can switch to and use
        # It should start with only the swordfish weapon available
        # the rest would be appended to this list when unlocked
        # self.activeWeaponList = ['swordfish', 'bubble', 'trident']
        self.activeWeaponList = ['swordfish']
        self.weaponNum = 0
        self.weapon = items.Weapon(self.game, self.weaponList[self.weaponNum], self)
        self.weaponAnimationCount = 0
        self.weaponAnimationSpeed = 15
        self.swordUsed = False
        self.spearUsed = False
        #bubble, swordfish, trident
        self.bonusDamage = [0, 0, 0]


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


        # Variables for the player's health, healthbar, and taking damage / invulnerability

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
        self.statusList = [pygame.transform.scale(pygame.image.load('Sprites/items/SpeedSymbol.png').convert_alpha(), (30, 30)),
                           pygame.transform.scale(pygame.image.load('Sprites/items/TridentSymbol.png').convert_alpha(), (30,30)),
                           pygame.transform.scale(pygame.image.load('Sprites/items/SwordfishSymbol.png').convert_alpha(), (30,30)),
                           pygame.transform.scale(pygame.image.load('Sprites/items/BubbleSymbol.png').convert_alpha(), (30,30))]


        #list of active status effects
        self.showList = []
        self.descFont = pygame.font.Font('Fonts/minecraft-font/MinecraftRegular-Bmg3.otf', 16)


        self.clock = clock
        self.timepassed = 0


        self.image = self.downImgList[self.imgindex]
        

        #self.rect = self.image.get_rect()
        #Below line is to decrease the rectangle collision slightly
        #Was having trouble fitting in 1 tile gaps
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.rect.x = self.x
        self.rect.y = self.y


    #Authored: Max Chiu 5/20/2024
    #Sets the player's position using a tile position (where xTile goes up to 32 and yTile goes up to 18)
    def setPosition(self, xTile, yTile):
        self.x = xTile*TILESIZE
        self.y = yTile*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y



    # function is supposed to update the player's sprite when they use the ranged attack. doesn't currently work
    def rangedAttackVisual(self, direction):
        if direction == 'right':
            self.image = self.rangedWeaponList[0]
        elif direction == 'left':
            self.image = self.rangedWeaponList[3]
        elif direction == 'up':
            self.image = self.rangedWeaponList[2]
        else:  # self.facing == 'down':
            self.image = self.rangedWeaponList[1]



    def update(self):
        # checks for any movement from the player
        self.movement()
        # checks to see if the player has gone idle
        self.checkIdle()
        # calls the function to check for any interactions
        self.interact()
        # calls the function to draw the tutorials on screen
        self.tutorial.draw()
        # if the player's health is reduced to zero, they get a game over and lose the game
        if self.currentHealth <= 0 or self.targetHealth <= 0:
            self.game.state = 'game over'

        # updates the player's position based on any movement and checks for collisions with any blocks or friendly npcs
        self.rect.x += self.xChange
        self.collideBlocks('x')
        self.rect.y += self.yChange
        self.collideBlocks('y')
        self.x = self.rect.x
        self.y = self.rect.y

        # if the player has been hit an is invulnerable, this code executes
        if self.hitInvulnerable:
            # counts down the time they can continue being invulnerable for
            self.hitInvulnerableTime += 1
            # when it reaches the limit
            if self.hitInvulnerableTime > self.invulnerableTimer:
                # the player is no longer invulnerable
                self.hitInvulnerable = False
                self.hitInvulnerableTime = 0


        # updates the variable that counts how much time is passing
        self.timepassed += self.clock.get_time()/1000
        #Below line: Loads image using right image list (transforms it to scale with width and height) and sets it to the image

        # updates the player's image sprite based on the direction they are facing and if they have used the ranged weapon
        if self.game.state == 'explore':
            if self.facing == 'right':
                self.image = self.rightImgList[self.imgindex]
            elif self.facing == 'left':
                self.image = self.leftImgList[self.imgindex]
            elif self.facing == 'up':
                self.image = self.upImgList[self.imgindex]
            else: # self.facing == 'down':
                self.image = self.downImgList[self.imgindex]
        # if they have used the ranged attack, sets their sprites accordingly
        #elif self.weapon.used and self.weapon.type == 'bubble'and self.weapon.ammo != 0:
        #    if self.facing == 'right':
        #        self.image = self.rangedWeaponList[0]
        #    elif self.facing == 'left':
        #        self.image = self.rangedWeaponList[3]
        #    elif self.facing == 'up':
        #        self.image = self.rangedWeaponList[2]
        #    else: # self.facing == 'down':
        #        self.image = self.rangedWeaponList[1]


        # makes the player's current sprite flicker if they are invulnerable after taking damage
        self.flicker()

        # resets x and y direction change to 0 for the next game loop
        self.xChange = 0
        self.yChange = 0


        # allows the mouse to used for selection during dialogue
        if self.game.state == 'dialogue':
            self.mouseRect.center = pygame.mouse.get_pos()
            interactRect = pygame.Rect(self.rect.left-TILESIZE*0.1, self.rect.top-TILESIZE*0.1, TILESIZE*1.2, TILESIZE*1.2)
            npcIndex = interactRect.collidelist(list(npc.rect for npc in self.game.npcs))
            npc = self.game.npcs.get_sprite(npcIndex)
            self.game.activeNPC = npc
            self.game.activeNPC.pastItem = self.game.activeNPC.selectedItem

            collisionList = []
            for rect in npc.TextBox.choiceRectList:
                collisionList.append(pygame.Rect(rect.left, rect.top, rect.width-30, rect.height))

            for rect in range(len(collisionList)):
                collisionList[rect].x = npc.TextBox.x + 60
                collisionList[rect].y = npc.TextBox.y + 30 + 45*rect

            if len(collisionList) > 0:
                highlighted = self.mouseRect.collidelist(collisionList) 
                if highlighted == -1:
                    return
                else:
                    npc.TextBox.selectedRect = highlighted
                    self.game.activeNPC.selectedItem = highlighted

        elif self.game.state == 'shopping':
            self.mouseRect.center = pygame.mouse.get_pos()
            collisionList = self.game.activeNPC.itemRects
            if len(collisionList) > 0:
                highlighted = self.mouseRect.collidelist(collisionList) 
                if highlighted == -1:
                    return
                else:
                    self.game.activeNPC.selectedItem = highlighted

    # inspiration for this function and the damage flickering effect was gotten from:
    # https://www.youtube.com/watch?v=QU1pPzEGrqw
    # Makes the player's sprite flicker by changing the alpha values rapidly
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

    # lwoers the player's health
    def getDamage(self, amount):
        # self.currentHealth = self.targetHealth
        if self.hitInvulnerable:
            return
        else:
            self.hitInvulnerable = True
            if self.targetHealth > 0:
                self.targetHealth = self.targetHealth - amount # decreases the target health for the animated healthbar
                self.game.screenshake = amount // 5
            if self.targetHealth <=0:
                self.targetHealth = 0 # target health cannot go below zero
            pygame.mixer.Channel(1).set_volume(0.050 * self.game.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_Battle_SFX/77_flesh_02.wav'))

    def getHealth(self, amount):
        if self.targetHealth < self.maxHealth:
            self.targetHealth = self.targetHealth + amount # increases the target health for the animated healthbar
        if self.targetHealth > self.maxHealth:
            self.targetHealth = self.maxHealth # target health cannot increase past the max health
        pygame.mixer.Channel(1).set_volume(0.015 * self.game.soundVol)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/8_Buffs_Heals_SFX/02_Heal_02.wav'))

    def healthBar(self): # Static health bar function, not currently in use
        pygame.draw.rect(self.game.screen, (255, 0, 0), (10, 10, self.targetHealth/self.healthRatio, self.healthBarHeight))
        pygame.draw.rect(self.game.screen, (255, 255, 255), (10, 10, self.maxHealthBarLength,self.healthBarHeight), 4)

    def animateHealth(self): # Animated health bar function
        if self.currentHealth < self.targetHealth: # if health should increase
            self.currentHealth += self.healthChangeSpeed # increases the current health (red bar) by the health bar's speed
            # updates the width of the transition health bar to be the distance between the current health and target health points
            self.transitionWidth = int((self.targetHealth - self.currentHealth)/self.healthRatio)
            self.transitionColor = (0, 255, 0) # transition bar color is set to Green if increasing
            # creates the rectangle for the current health bar (red bar)
            self.health_bar_rect = pygame.Rect(10, 10, self.currentHealth / self.healthRatio - 3, self.healthBarHeight)
            # creates the rectangle for the transition bar
            self.transition_bar_rect = pygame.Rect(self.health_bar_rect.right, 10, self.transitionWidth, self.healthBarHeight)


        elif self.currentHealth > self.targetHealth: # if health should decrease
            self.currentHealth -= self.healthChangeSpeed # decreases the current health (red bar) by the health bar's speed
            # updates the width of the transition health bar to be the distance between the current health and target health points
            self.transitionWidth = int((self.currentHealth - self.targetHealth)/self.healthRatio)
            self.transitionColor = (255, 255, 0) # transition bar color is set to Yellow if decreasing
            # creates the rectangle for the current health bar (red bar)
            self.health_bar_rect = pygame.Rect(10, 10, self.targetHealth / self.healthRatio - 3, self.healthBarHeight)
            # creates the rectangle for the transition bar
            self.transition_bar_rect = pygame.Rect(self.health_bar_rect.right, 10, self.transitionWidth, self.healthBarHeight)

        # draws the health bar onto the screen (red bar)
        pygame.draw.rect(self.game.screen, (255, 0, 0 ), self.health_bar_rect)
        # draws the transition bar onto the screen (yellow / green bar)
        pygame.draw.rect(self.game.screen, self.transitionColor, self.transition_bar_rect)
        # draws the outline border for the health bar
        pygame.draw.rect(self.game.screen, (255, 255, 255), (10, 10, self.maxHealthBarLength, self.healthBarHeight), 4)

    #Authored Max Chiu 5/30/2024
    def showStatus(self):
        self.showList = []
        if self.speed != PLAYER_SPEED and 'speed' not in self.showList:
            self.showList.append('speed')
        if self.bonusDamage[0] != 0 and 'bulletPen' not in self.showList:
            self.showList.append('bulletPen')
        if self.bonusDamage[1] != 0 and 'swordDamage' not in self.showList:
            self.showList.append('swordDamage')
        if self.bonusDamage[2] != 0 and 'sharpTrident' not in self.showList:
            self.showList.append('sharpTrident')


        for i in range(len(self.showList)):
            statCoord = (10+self.maxHealthBarLength+10+20+5+50*i, 10+self.healthBarHeight/2+5)
            pygame.draw.circle(self.game.screen, WHITE, statCoord, 20)
            pygame.draw.circle(self.game.screen, GREEN, statCoord, 20, 1)
            if self.showList[i] == 'speed':
                self.game.screen.blit(self.statusList[0], (statCoord[0]-15, statCoord[1]-15))
            elif self.showList[i] == 'sharpTrident':
                self.game.screen.blit(self.statusList[1], (statCoord[0]-15, statCoord[1]-15))
            elif self.showList[i] == 'swordDamage':
                self.game.screen.blit(self.statusList[2], (statCoord[0]-15, statCoord[1]-15))
            elif self.showList[i] == 'bulletPen':
                self.game.screen.blit(self.statusList[3], (statCoord[0]-15, statCoord[1]-15))


        self.mouseRect.center = pygame.mouse.get_pos()
        interactRect = pygame.Rect(self.mouseRect.center[0]-TILESIZE*0.05, self.mouseRect.center[1]-TILESIZE*0.05, TILESIZE*0.1, TILESIZE*0.1)
        for i in range(len(self.showList)):
            statRect = pygame.Rect(10+self.maxHealthBarLength+10+5+50*i, 5, 40, 40)
            if pygame.Rect.colliderect(interactRect, statRect):
                statusText = ''
                if self.showList[i] == 'speed':
                    statusText = f'Speed Multiplier: {self.speed/PLAYER_SPEED:.2f}'
                elif self.showList[i] == 'sharpTrident':
                    statusText = f'Added Trident Damage: {self.bonusDamage[2]}'
                elif self.showList[i] == 'swordDamage':
                    statusText = f'Added Sword Damage: {self.bonusDamage[1]}'
                elif self.showList[i] == 'bulletPen':
                    statusText = f'Added Bullet Damage: {self.bonusDamage[0]}'
                pygame.draw.rect(self.game.screen, BROWN, pygame.Rect(self.mouseRect.left, self.mouseRect.top, 9.3*len(statusText)-4.7*(statusText.count('i')+statusText.count('l')), 25))
                self.game.screen.blit(self.descFont.render(statusText, False, OFFWHITE), (self.mouseRect.left+4, self.mouseRect.top+4))

        


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
                # interacted = True
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
                # interacted = True
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
            if self.game.state == 'shopping':
                #gets the item that was purchased
                item = self.game.activeNPC.interaction()
                if item == 'trident':
                    self.activeWeaponList.append('trident')
                    self.game.activeNPC.resetInventory('trident')
                elif item == 'bubble':
                    self.activeWeaponList.append('bubble')
                    self.game.activeNPC.resetInventory('bubble')
                elif item == 'speedPotion': #minecraft potion drinking sound effect https://quicksounds.com/sound/107/minecraft-potion-drinking
                    pygame.mixer.Channel(4).set_volume(0.05 * self.game.soundVol)
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound('Music/sound_effects/Minecraft Potion Drinking - QuickSounds (mp3cut.net).mp3'))
                    self.speed *= 1.1
                elif item == 'sharpTrident':
                    self.bonusDamage[2] += 10
                elif item == 'bulletPen':
                    self.bonusDamage[0] += 10
                elif item == 'swordDamage':
                    self.bonusDamage[1] += 10
                elif item == 'healthPotion':
                    self.game.inventory.add_item('potion', 1)
                #pygame.time.wait(250)
            elif npcIndex != -1:
                # interacted = True
                self.game.npcs.get_sprite(npcIndex).interaction()
                pygame.time.wait(250)

            #if not interacted:
            #    self.weapon.attack()

            


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
                self.game.activeNPC = npc
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    npc.TextBox.selectedRect = npc.TextBox.selectedRect - 1 if npc.TextBox.selectedRect > 0 else npc.TextBox.selectedRect
                    pygame.time.wait(150)
                elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    npc.TextBox.selectedRect = npc.TextBox.selectedRect + 1 if npc.TextBox.selectedRect < len(npc.TextBox.choiceRectList)-1 else npc.TextBox.selectedRect
                    pygame.time.wait(150)


        #Modified: Max Chiu 5/18/2024
        elif self.game.state == 'shopping' and (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            npc = self.game.activeNPC
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                npc.pastItem = npc.selectedItem
                npc.selectedItem = npc.selectedItem - 1 if (npc.selectedItem > 0 and npc.selectedItem != len(npc.itemList)-1) else npc.selectedItem
                pygame.time.wait(150)

            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                npc.pastItem = npc.selectedItem
                npc.selectedItem = npc.selectedItem + 1 if npc.selectedItem < len(npc.itemList)-2 else npc.selectedItem
                pygame.time.wait(150)

            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                npc.pastItem = npc.selectedItem
                npc.selectedItem = len(npc.itemList)-1
                pygame.time.wait(150)

            elif keys[pygame.K_w] or keys[pygame.K_UP]:
                if npc.pastItem == 3:
                    npc.pastItem = 1
                npc.selectedItem = npc.pastItem
                pygame.time.wait(150)


        #Allows mouse click functionality for interactions
        elif mouses[0]:
            mouseRect = pygame.Rect(0, 0, 40, 40)
            mouseRect.center = pygame.mouse.get_pos()

            if self.game.state == 'dialogue':
                interactRect = pygame.Rect(self.rect.left-TILESIZE*0.1, self.rect.top-TILESIZE*0.1, TILESIZE*1.2, TILESIZE*1.2)
                npcIndex = interactRect.collidelist(list(npc.rect for npc in self.game.npcs))
                npc = self.game.npcs.get_sprite(npcIndex)
                self.game.activeNPC = npc
                rectCollisionList = npc.TextBox.choiceRectList[:]

                for rect in range(len(rectCollisionList)):
                    rectCollisionList[rect].x = npc.TextBox.x + 13
                    rectCollisionList[rect].y = npc.TextBox.y + 25 + 30*rect


                if len(rectCollisionList) > 0:
                    npc.selectedRect = mouseRect.collidelist(rectCollisionList)
                    npc.interaction()
                    pygame.time.wait(200)

            elif self.game.state == 'shopping':
                interactIndex = mouseRect.collidelist(self.game.activeNPC.itemRects)
                if interactIndex != -1:
                    item = self.game.activeNPC.interaction()
                    if item == 'trident':
                        self.activeWeaponList.append('trident')
                        self.game.activeNPC.resetInventory('trident')
                    elif item == 'bubble':
                        self.activeWeaponList.append('bubble')
                        self.game.activeNPC.resetInventory('bubble')
                    elif item == 'speedPotion': #potion sounds https://quicksounds.com/sound/107/minecraft-potion-drinking
                        pygame.mixer.Channel(4).set_volume(0.05 * self.game.soundVol)
                        pygame.mixer.Channel(4).play(pygame.mixer.Sound('Music/sound_effects/Minecraft Potion Drinking - QuickSounds (mp3cut.net).mp3'))
                        self.speed *= 1.1
                    elif item == 'sharpTrident':
                        self.bonusDamage[2] += 10
                    elif item == 'bulletPen':
                        self.bonusDamage[0] += 10
                    elif item == 'swordDamage':
                        self.bonusDamage[1] += 10
                    elif item == 'healthPotion':
                        self.game.inventory.add_item('potion', 1)
                    self.game.activeNPC.interaction()
                    #pygame.time.wait(250)


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

        #Checks for endgates - hitboxes that signify the game should end and credits should play
        endgateIndex = interactRect.collidelist(list(endgate.rect for endgate in self.game.endgates))
        if endgateIndex != -1:
            self.game.game_won()


    


    def movement(self):
        # movement is only allowed if the game state is 'explore'
        if self.game.state != 'explore':
            return
        # plays the walk sound effect if it's on the right frame of the walk animation
        if self.imgindex == 1:
            self.playWalkSound()
            #if self.walkSoundNum == 3:
            #    self.walkSoundNum = 4
            #elif self.walkSoundNum == 4:
            #    self.walkSoundNum = 3
            #self.walkSoundNum = random.randint(0, len(self.walkingList) - 1)
            self.walkingSound = self.walkingList[self.walkSoundNum] # walking sound is selected from a list of sound effects (might be changed)
        elif (self.imgindex != 1):
            self.walkSoundPlaying = False # allows the walk sound effect to be played again


        #The key press segments came from viewing this tutorial
        #https://www.youtube.com/watch?v=GakNgbiAxzs&list=PLkkm3wcQHjT7gn81Wn-e78cAyhwBW3FIc&index=2
        keys = pygame.key.get_pressed()
        if not self.itemUsed: # if there is not an item being used
            if keys[pygame.K_a]:
                # Two lines below change camera to move around player character, moving all other sprites
                # comment them out to create a static camera
                #for sprite in self.game.all_sprites:
                    #sprite.rect.x += PLAYER_SPEED
                self.xChange -= self.speed
                self.facing = 'left'
                self.idleTimer = 0
                # updates the player's walking sprite if enough time has passed
                if ((self.timepassed) // (0.20) % 4 == self.imgindex):
                    self.imgindex = (self.imgindex + 1)%4
                    #if self.imgindex == 1 or self.imgindex == 3:
                    #    pygame.mixer.Channel(2).set_volume(0.08 * self.game.soundVol)
                    #    pygame.mixer.Channel(2).play(self.walkingSound)
                else:
                    self.imgindex


            if keys[pygame.K_d]:
                #for sprite in self.game.all_sprites:
                    #sprite.rect.x -= PLAYER_SPEED
                self.xChange += self.speed
                self.facing = 'right'
                self.idleTimer = 0
                # updates the player's walking sprite if enough time has passed
                if ((self.timepassed) // (0.20) % 4 == self.imgindex):
                    self.imgindex = (self.imgindex + 1)%4
                    #if self.imgindex == 1 or self.imgindex == 3:
                    #    pygame.mixer.Channel(2).set_volume(0.08 * self.game.soundVol)
                    #    pygame.mixer.Channel(2).play(self.walkingSound)
                else:
                    self.imgindex

            if keys[pygame.K_w]:
                #for sprite in self.game.all_sprites:
                    #sprite.rect.y += PLAYER_SPEED
                self.yChange -= self.speed
                self.facing = 'up'
                self.idleTimer = 0
                # updates the player's walking sprite if enough time has passed
                if ((self.timepassed) // (0.18) % 4 == self.imgindex):
                    self.imgindex = (self.imgindex + 1)%4
                    #if self.imgindex == 1 or self.imgindex == 3:
                    #    pygame.mixer.Channel(2).set_volume(0.08* self.game.soundVol)
                    #    pygame.mixer.Channel(2).play(self.walkingSound)
                else:
                    self.imgindex


            if keys[pygame.K_s]:
                #for sprite in self.game.all_sprites:
                    #sprite.rect.y -= PLAYER_SPEED
                self.yChange += self.speed
                self.facing = 'down'
                self.idleTimer = 0
                # updates the player's walking sprite if enough time has passed
                if ((self.timepassed) // (0.25) % 4 == self.imgindex):
                    self.imgindex = (self.imgindex + 1)%4
                    #if self.imgindex == 1 or self.imgindex == 3:
                    #    pygame.mixer.Channel(2).set_volume(0.08 * self.game.soundVol)
                    #    pygame.mixer.Channel(2).play(self.walkingSound)
                else:
                    self.imgindex

    # function that will check if the player is idle from moving. This will be done by using a timer that is decremented unless the player moves, or the movement state will be changed to idle from moving.
    def checkIdle(self):
        self.idleTimer += 1 # increments the idle timer
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
            self.walkSoundPlaying = True # makes it so the walking sound cannot play multiple times for the same frame

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
            # updates the player's sprite to match the current frame of the attack animation and the weapon's location, taking facing direction into account
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
            # updates the player's image based on the direction they are facing
            if self.facing == 'up':
                self.image = self.pokeList[0]
            elif self.facing == 'down':
                self.image = self.pokeList[1]
            elif self.facing == 'left':
                self.image = self.pokeList[2]
            elif self.facing == 'right':
                self.image = self.pokeList[3]
        # updates the game's display (might be unnecessary)
        pygame.display.update()

    def switchWeapons(self):
        # Method written by Eddie Suber
        if self.game.state == 'explore':
            # Player can use Q to switch weapons
            self.weaponNum += 1
            self.weaponNum %= len(self.weaponList)
            while self.weaponList[self.weaponNum] not in self.activeWeaponList:
                self.weaponNum += 1
                self.weaponNum %= len(self.weaponList)
            self.weapon.type = self.weaponList[self.weaponNum]
            self.weapon.updateDamage(self.bonusDamage)
            if self.weapon.type == 'swordfish':
                self.weaponAnimationSpeed = 15
            elif self.weapon.type == 'trident':
                self.weaponAnimationSpeed = 18
            pygame.mixer.Channel(1).set_volume(0.04 * self.game.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_UI_Menu_SFX/070_Equip_10.wav'))
            self.game.weaponsHud.checkActiveWep()


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
    def __init__(self, game, x, y, mapPos):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.npcs, self.game.non_background
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        #attribute checking which room it's in
        self.mapPos = (mapPos[0], mapPos[1])

        self.meetings = 0


        self.xChange = 0
        self.yChange = 0


        if mapPos == (2, 1):
            self.npcImgNum = 3
            self.width = 2.5*TILESIZE
            self.height = 2*TILESIZE
            self.name = 'le chat'
            self.avatarImg = self.game.avatarImgList[-1]
            self.image = pygame.transform.scale(pygame.image.load('Sprites/npcs/NPCs-Char/catNPCno4.png').convert_alpha(), (self.width, self.height))


        else:
            self.npcImgNum = random.randint(0, len(self.game.npcImageList) -1)
            self.image = pygame.transform.scale(pygame.image.load(self.game.npcImageList[self.npcImgNum]).convert_alpha(), (self.width, self.height))
            self.avatarImg = self.game.avatarImgList[self.npcImgNum]
            self.name = self.game.nameList[self.npcImgNum]

            self.game.npcImageList.pop(self.npcImgNum)
            self.game.avatarImgList.pop(self.npcImgNum)
            self.game.nameList.pop(self.npcImgNum)

        self.dialogueStage = '01:First Meet'
        self.dialogueStageIndex = 1
        self.totalItemCost = [{'flower': 2}, {'ore': 5}, {'flower': 4}, {'ore': 5}, {'flower': 5}]
        self.totalItemList = ['healthPotion', 'sharpTrident', 'speedPotion', 'swordDamage', 'bulletPen']
        self.totalItemDesc = ['Restores health (Consumable) ', 'Increases trident damage ', 'Increases movement speed ', 'Increases sword damage ', 'Increases bullet damage ']

        self.totalItemImgs = [pygame.transform.scale(pygame.image.load('Sprites/items/HealthPotion2.png'), (200, 200)),
                                pygame.transform.scale(pygame.image.load('Sprites/items/trident2.png'), (200, 200)),
                                pygame.transform.scale(pygame.image.load('Sprites/items/SpeedPotion.png'), (200, 200)),
                                pygame.transform.scale(pygame.image.load('Sprites/items/swordfish3.png'), (200, 200)),
                                pygame.transform.scale(pygame.image.load('Sprites/items/bubble.png'), (200, 200))]

        
        #these are empty arrays for which item will be shown by this NPC.
        self.itemCost = []
        self.itemList = []
        self.itemDesc = []
        self.itemImgs = []

        #If the weapons haven't been bought yet, give it priority in what items show
        if 'trident' not in self.game.player.activeWeaponList:
            self.itemCost.append({'ore': 4})
            self.itemList.append('trident')
            self.itemDesc.append('Throwing Trident ')
            self.itemImgs.append(pygame.transform.scale(pygame.image.load('Sprites/items/trident2.png'), (200, 200)))

        if 'bubble' not in self.game.player.activeWeaponList:
            self.itemCost.append({'flower': 4})
            self.itemList.append('bubble')
            self.itemDesc.append('Burst gun ')
            self.itemImgs.append(pygame.transform.scale(pygame.image.load('Sprites/items/bubblegun.png'), (200, 200)))

        #Randomly chooses items to add to the list until 3 are chosen in total
        while len(self.itemList) < 3:
            randomInd = random.randint(0, len(self.totalItemList)-1)
            if self.totalItemList[randomInd] not in self.itemList:
                self.itemCost.append(self.totalItemCost[randomInd])
                self.itemList.append(self.totalItemList[randomInd])
                self.itemDesc.append(self.totalItemDesc[randomInd])
                self.itemImgs.append(self.totalItemImgs[randomInd])
        
        #add a leave button
        self.itemList.append('leave')
        self.itemRects = []
        self.selectedItem = 0
        self.pastItem = 0
        #self.descFont = pygame.font.SysFont('Garamond', 20)
        self.descFont = pygame.font.Font('Fonts/minecraft-font/MinecraftRegular-Bmg3.otf', 16)
        #self.descFont = pygame.font.Font('Fonts/pixel-font/Pixel-y14Y.ttf', 20)
        #self.descFont = pygame.font.Font('Fonts/roboto-remix-font/Minecraftchmc-dBlX.ttf', 20)
        #self.descFont = pygame.font.Font('Fonts/scarlet-devil-pixel-script-font/ScarletDevilPixelScript-0Vjr.ttf', 20)


        #Always leave a space/punctuation at the end of the quote!
        #Would you rather cum in the sink or sink in the cum? That is indeed the question for which we must all ponder and arrive at our own answers.
        #change this later

        if self.name == 'le chat':
            self.dialogueList = {'01:First Meet':[{'Meetings': 1},
                                                    "Meow! My name is le chat, the guardian of the forest!! ",
                                                    "You're the Slime Kingdom's reinforcements right? ",
                                                    "%Choices; Want to save the forest?; Yes; No...; I speak for the trees ",
                                                    "The Evil CEO of pollution is taking all of our flowers and ores. Without it, the forest's ecosystem is thrown all out of wack! ",
                                                    "So, since you're the best fighter of all of us (you do have a sword after all), I'm entrusting you to defeat him! ",
                                                    "Just in case you forgot how to fight though, use WASD to move, J to attack using the sword and trident, and arrow keys to attack using the bubble gun.",
                                                    "In order to get other weapons, you need to collect flowers and ores using Space then trade it in the shop (via me and my friends) ",
                                                    "But be careful, if you take too long to collect the flowers and ores, they'll start decomposing from the Evil CEO's pollution (heard he doesn't shower) ",
                                                    "In the shop, only the health potion can be saved for later, and is drunk using H. The other potions/upgrades give you a permanent upgrade ",
                                                    "And uh... I think that's it! Thanks for helping save me and my friends' home!! "
                                                    "%Choices; What do you want to do?; Shop; Leave; Meow "],
                                '02:Second Meet': [{'Meetings':2},
                                                    "Hi again... ",
                                                    "%Choices; What do you want to do?; Shop; Leave; Meow "]
                                }
            
            self.choiceList = {'01:Yes':["Meow! That's amazing! Because we really need your help! "],
                            '01:No...':["Oh... that's awkward ", "Um... I'll just keep talking and pretend you didn't say that "],
                            '01:I speak for the trees':["I LOVE the Lorax! Then, you should also know the trees are asking for our help!"],
                            '01:Shop': ["Hope your purchase helps you not die! "],
                            '01:Leave': ["Byeeeeee "],
                            '01:Meow': ["Meow! "],
                            '02:Shop': ["You better not die! >:( "],
                            '02:Leave': ["Good luck!! "],
                            '02:Meow': ["Woof Woof Woof RGHHHHH", "I mean... Meow! "]
                            }
        
        elif self.name == 'leaf':
            self.dialogueList = {'01:First Meet':[{'Meetings': 1},
                                                    "Ouch! You can’t cut me!! I am the great Leaf, not a flower >:| ",
                                                    "%Choices; What do you say?; Sorry... I needed to gather resources.; Oh. My bad.; I thought you were a flower! ",
                                                    "But I guess I have to do my job... ",
                                                    "What would you like to do? Shop ore leaf ",
                                                    "%Choices; What do you want to do?; Shop; Leaf "],
                                '02:Second Meet': [{'Meetings':2},
                                                    "You’re back? You guys just won’t leaf me alone!! ",
                                                    "What do you want? Don’t even shop, just leaf",
                                                    "%Choices; What do you want to do?; Shop; Leaf "],
                                '03:Third Meet': [{'Meetings':3},
                                                  "...No "]
                                }
            
            self.choiceList = {'01:Sorry... I needed to gather resources. What can I trade with what I have?': ["So rude… slimes these days, I’m just trying to leaf in peace."],
                            '01:Oh. My bad.':["So rude… slimes these days, I’m just trying to leaf in peace."],
                            '01:I thought you were a flower!':["So rude… slimes these days, I’m just trying to leaf in peace."],
                            '01:Shop': ["Don't come back!! "],
                            '01:Leaf': ["Good "],
                            '02:Shop': ["Leaf me alone!! "],
                            '02:Leaf': ["Good riddance "]
                            }
            
        elif self.name == 'bucket':
            self.dialogueList = {'01:First Meet':[{'Meetings': 1},
                                                    "Hello there! I am the guardian of the grounds, Bucket. I see you’re on a mission to save our forest from the CEO of pollution! ",
                                                    "Some ground rules (not actually, I just like saying ground) ",
                                                    "Be careful of Heart, underneath that smile is an evil nature ",
                                                    "You should probably leave Leaf alone, they are quite the grumpy one, constantly mumbling about leafing them alone. ",
                                                    "Come to me to trade! I am definitely the nicest of the bunch :) ",
                                                    "Please shop until your bucket list is all checked off! ",
                                                    "%Choices; What do you want to do?; Shop; Leave "],
                                '02:Second Meet': [{'Meetings':2},
                                                    "Welcome back!! Are you here to fill your bucket? ",
                                                    "%Choices; What do you want to do?; Shop; Leave "]
                                }
            
            self.choiceList = {
                            '01:Shop': ["Good Luck! "],
                            '01:Leave': ["Come back soon! "],
                            '02:Shop': ["Come back as many times as you want "],
                            '02:Leave': ["You're welcome back anytime! "]
                            }
            
        elif self.name == 'heart':
            self.dialogueList = {'01:First Meet':[{'Meetings': 1},
                                                    "Oh... ew ",
                                                    "I mean Hi! How are you? How can I help you? ",
                                                    "Actually don’t answer that, doesn’t matter ",
                                                    "Did you come to fight the evil CEO? ",
                                                    "Oh, YOU are going to need all the help you can get ",
                                                    "Try not to die too fast ",
                                                    "%Choices; What do you want to do?; Shop; Leave "],
                                '02:Second Meet': [{'Meetings':2},
                                                    "Heart's closed off. Goodbye! "]
                                }
            
            self.choiceList = {
                            '01:Shop': ["Stay alive! ... or not "],
                            '01:Leave': ["Come back soon! (I hope you won't tho!) "]
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
            self.TextBox = TextBox(self.game, self)
            self.TextBox.newText(self.dialogueList[self.dialogueStage][self.dialogueStageIndex], 28, 'Garamond', self.name)
            self.dialogueStageIndex += 1
            self.game.state = 'dialogue'


        elif self.game.state == 'shopping':
            pygame.mixer.Channel(1).set_volume(0.03 * self.game.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/select-sound-121244.mp3'))
            purchase = True
            if self.selectedItem == 3:
                self.itemRects = []
                self.game.state = 'dialogue'
                return -1
            
            for req in self.itemCost[self.selectedItem]:
                if self.game.inventory.get(req) < self.itemCost[self.selectedItem].get(req):
                    purchase = False

            if purchase:
                for req in self.itemCost[self.selectedItem]:
                    self.game.inventory.add_item(req, -1*self.itemCost[self.selectedItem].get(req))
                self.game.state = 'dialogue'
                self.itemRects = []
                return self.itemList[self.selectedItem]
            return -1
        #While not finished with dialogue section
        elif self.game.state == 'dialogue' and self.dialogueStageIndex < len(self.dialogueList[self.dialogueStage]):
            nextDialogue = self.dialogueList[self.dialogueStage][self.dialogueStageIndex]
            pygame.mixer.Channel(1).set_volume(0.03 * self.game.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/select-sound-121244.mp3'))
            #If there are choices displayed on the screen

            if len(self.TextBox.choiceRectList) > 0:
                self.choiceResponse()
                selection = self.dialogueList[self.dialogueStage][self.dialogueStageIndex].split(';')
                selection = selection[self.TextBox.selectedRect+2]
                selection = f'{self.dialogueStage[0:2]}:{selection.strip()}'
                for i in range(len(self.choiceList[selection])-1, -1, -1):
                    line = self.choiceList[selection][i]
                    self.dialogueList[self.dialogueStage].insert(self.dialogueStageIndex+1,line)


                self.dialogueStageIndex += 1
                if self.dialogueStageIndex == len(self.dialogueList[self.dialogueStage]) and self.game.state != 'shopping':
                    self.TextBox.kill()
                    self.updateDialogue()
                    self.game.state = 'explore'
                    self.game.play_music('stop')
                    self.game.play_music('village')

                elif self.TextBox.selectedRect != 0:
                    self.interaction()
                    return -1
                

            #If the next dialogue to display is a choice list
            elif nextDialogue.find('%Choices') != -1:
                self.TextBox.kill()
                self.TextBox = TextBox(self.game, self)
                choicesList = nextDialogue.split(';')
                self.TextBox.newText(choicesList[1:], 28, 'Garamond', self.name)

            #Displaying normal dialogue
            else:
                self.TextBox.kill()
                self.TextBox = TextBox(self.game, self)
                self.TextBox.newText(nextDialogue, 28, 'Garamond', self.name)
                self.dialogueStageIndex += 1

                
        #When finished with dialogue
        elif self.game.state == 'dialogue':
            index = -1
            for i in range(len(self.dialogueList[self.dialogueStage])):
                text = self.dialogueList[self.dialogueStage][i]
                if isinstance(text, str) and text.find('%Choices') != -1:
                    index = i+1
            if index != -1:
                self.dialogueList[self.dialogueStage] = self.dialogueList[self.dialogueStage][0:index]



            self.selectedItem = -1
            self.TextBox.kill()
            self.updateDialogue()
            self.game.state = 'explore'
            self.game.play_music('stop')
            self.game.play_music('village')
        self.itemRects = []
        return -1

    #READ ME, FINISH WHEN CHOICES ARE DEFINED
    #Modified Max Chiu 5/17-5/20/2024
    def choiceResponse(self):
        self.TextBox.choiceRectList = []
        #variable for each letter width of the font
        textWidth = 9
        if self.TextBox.selectedRect == 0 and self.dialogueStageIndex == len(self.dialogueList[self.dialogueStage])-1:
            self.game.state = 'shopping'

            # displays the count of flowers when in the shop
            pygame.draw.rect(self.game.screen, BLACK, (WIDTH * 0.4, HEIGHT * 0.08, TILESIZE, TILESIZE))
            pygame.draw.rect(self.game.screen, OFFWHITE, (WIDTH * 0.4, HEIGHT * 0.08, TILESIZE, TILESIZE), 1)
            self.game.screen.blit(self.game.sunFloImgL[0], pygame.Rect(WIDTH * 0.4, HEIGHT * 0.08, 0, 0))
            self.game.screen.blit(self.descFont.render(f"Flowers held: {self.game.inventory.get('flower')}", False, OFFWHITE), (WIDTH * 0.37, HEIGHT * 0.15))

            # displays the count of ores when in the shop
            pygame.draw.rect(self.game.screen, BLACK, (WIDTH * 0.57, HEIGHT * 0.08, TILESIZE, TILESIZE))
            pygame.draw.rect(self.game.screen, OFFWHITE, (WIDTH * 0.57, HEIGHT * 0.08, TILESIZE, TILESIZE), 1)
            self.game.screen.blit(self.game.amethImageL[0], pygame.Rect(WIDTH * 0.57, HEIGHT * 0.08, 0, 0))
            self.game.screen.blit(self.descFont.render(f"Ores held: {self.game.inventory.get('ore')}", False, OFFWHITE),(WIDTH * 0.54, HEIGHT * 0.15))

            #Displaying each of the potions
            for item in range(len(self.itemList)-1):

                #Draws the potion on the screen with background BROWN
                itemRect = pygame.Rect(190+item*350, 140, 200, 300)
                pygame.draw.rect(self.game.screen, BROWN, itemRect)
                self.game.screen.blit(self.itemImgs[item], itemRect)
                
                #Displays the text for each item: name, cost, and description
                if self.itemList[item] == 'healthPotion':
                    nameText = 'Health Potion'
                elif self.itemList[item] == 'sharpTrident':
                    nameText = 'Increased Trident Sharpness'
                elif self.itemList[item] == 'speedPotion':
                    nameText = 'Increased Speed'
                elif self.itemList[item] == 'swordDamage':
                    nameText = 'Increased Sword Damage'
                elif self.itemList[item] == 'bulletPen':
                    nameText = 'Increased Bullet Penetration'
                elif self.itemList[item] == 'trident':
                    nameText = 'Trident'
                elif self.itemList[item] == 'bubble':
                    nameText = 'Bubble Gun'
                self.game.screen.blit(self.descFont.render(nameText, False, OFFWHITE), (itemRect.x+100-textWidth*(len(nameText)/2), itemRect.y+200))

                #Item cost
                #ShiftedDown checks if there was an extra line of text added right after name for if the user has enough resources
                shiftedDown = False
                for req in self.itemCost[item].keys():
                    if self.game.inventory.get(req) < self.itemCost[item][req]:
                        shiftedDown = True
                        self.game.screen.blit(self.descFont.render('Need More Resources', False, RED), (itemRect.x+100-textWidth*(19/2), itemRect.y+220))
                        break

                numRows = 0
                #Checks through every requirement for 1 item
                for req in self.itemCost[item].keys():
                    if req == 'flower':
                        costText = f'Cost: {self.itemCost[item][req]} Flowers'
                    elif req == 'ore':
                        costText = f'Cost: {self.itemCost[item][req]} Ores'
                    if not shiftedDown:
                        self.game.screen.blit(self.descFont.render(costText, False, OFFWHITE), (itemRect.x+100-textWidth*(len(costText)/2), itemRect.y+220+numRows*20))
                    else:
                        self.game.screen.blit(self.descFont.render(costText, False, OFFWHITE), (itemRect.x+100-textWidth*(len(costText)/2), itemRect.y+240+numRows*20))
                    numRows += 1

                text = self.itemDesc[item]
                maxLength = 20
                while len(text) > 0:
                    try:
                        cutoffIndex = len(text[:maxLength])-re.search('[^a-zA-Z0-9()]', text[maxLength-1::-1]).end()+1
                    except AttributeError:
                        cutoffIndex = maxLength
                    if shiftedDown:
                        self.game.screen.blit(self.descFont.render(text[:cutoffIndex], False, OFFWHITE), (itemRect.x+100-textWidth*(len(text[:cutoffIndex])/2), itemRect.y+240+numRows*20))
                    else:
                        self.game.screen.blit(self.descFont.render(text[:cutoffIndex], False, OFFWHITE), (itemRect.x+100-textWidth*(len(text[:cutoffIndex])/2), itemRect.y+220+numRows*20))
                    text = text[cutoffIndex:]
                    numRows += 1


                #Displays all the borders
                if item == self.selectedItem:
                    pygame.draw.rect(self.game.screen, BLUE, itemRect, 2, 2)
                else:
                    pygame.draw.rect(self.game.screen, WHITE, itemRect, 2, 2)
                itemRect.x += 2
                itemRect.y += 2
                itemRect.width -= 4
                itemRect.height -=104
                pygame.draw.rect(self.game.screen, BLACK, itemRect, 1, 1)
                if len(self.itemRects) < 3:
                    self.itemRects.append(itemRect)

            #For the leave button
            itemRect = pygame.Rect(600, 460, 80, 25)
            if len(self.itemRects) < 4:
                self.itemRects.append(itemRect)
            pygame.draw.rect(self.game.screen, BROWN, itemRect)
            self.game.screen.blit(self.descFont.render('Leave', False, OFFWHITE), (itemRect.x+itemRect.width/2-textWidth*(len('Leave')/2), itemRect.y+5))
            if self.selectedItem == 3:
                pygame.draw.rect(self.game.screen, BLUE, itemRect, 2, 2)
            else:
                pygame.draw.rect(self.game.screen, WHITE, itemRect, 2, 2)

    #Authored: Max Chiu 5/27/24
    def resetInventory(self, item):
        index = self.itemList.index(item)
        self.itemCost.pop(index)
        self.itemList.pop(index)
        self.itemDesc.pop(index)
        self.itemImgs.pop(index)
        while len(self.itemList) < 4:
            randomInd = random.randint(0, len(self.totalItemList)-1)
            if self.totalItemList[randomInd] not in self.itemList:
                self.itemCost.insert(index, self.totalItemCost[randomInd])
                self.itemList.insert(index, self.totalItemList[randomInd])
                self.itemDesc.insert(index, self.totalItemDesc[randomInd])
                self.itemImgs.insert(index, self.totalItemImgs[randomInd])
        



#Authored by Max Chiu 4/16/2024
class Enemy(pygame.sprite.Sprite):

    def __init__(self, game, x, y, attackType):
        self.game = game
        self.clock = self.game.clock
        self.map = currentTileMap[mapList[self.game.map[0]][self.game.map[1]]]
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies, self.game.non_background
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.defaultPos = (x, y)
        self.width = TILESIZE
        self.height = TILESIZE
        # determines the type of the enemy (if multiple enemy types are added)
        self.type = 'pumpkinRobot'
        # checks for melee or ranged attack
        self.attackType = attackType
        self.timepassed = 0

        self.health = 100
        self.damage = 60
        self.speed = PLAYER_SPEED * 0.6

        # Variables to handle enemy - player attack interaction

        self.hitInvincible = False
        self.hitInvulnerable = False
        self.hitInvulnerableTime = 0
        self.invulnerableTimer = 24
        self.stunned = False
        self.stunCount = 0
        self.stunTimer = 8
        self.attackTimer = 4

        self.name = 'Udibudibudib'

        self.xChange = 0
        self.yChange = 0
        self.state = 'standing'
        self.moving = False
        self.facingDirection = 'down'

        # sets up the enemy's images based on the attack type (if statement may be unnecessary since it seems it is doing the same thing either way)

        if self.attackType == 'melee':
            self.pumpkinImgDown = [
                pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeIdle.png').convert_alpha(),(TILESIZE * 0.99, TILESIZE * 0.99)),
                pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeDownRight (1).png').convert_alpha(),(TILESIZE * 0.99, TILESIZE * 0.99)),
                pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeIdle.png').convert_alpha(),(TILESIZE * 0.99, TILESIZE * 0.99)),
                pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeDownLeft.png').convert_alpha(),(TILESIZE * 0.99, TILESIZE * 0.99))]
        else:
            self.pumpkinImgDown = [
                pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeIdle.png').convert_alpha(),(TILESIZE * 0.99, TILESIZE * 0.99)),
                pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeDownRight (1).png').convert_alpha(),(TILESIZE * 0.99, TILESIZE * 0.99)),
                pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeIdle.png').convert_alpha(),(TILESIZE * 0.99, TILESIZE * 0.99)),
                pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeDownLeft.png').convert_alpha(),(TILESIZE * 0.99, TILESIZE * 0.99))]
        # pumpkinImgDown = [pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeDownRight (1).png').convert_alpha(), (TILESIZE * 0.99, TILESIZE * 0.99)),
        #                  pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinMeleeDownLeft.png').convert_alpha(), (TILESIZE * 0.99, TILESIZE * 0.99))]

        # list containing the images for the ranged enemy variant

        self.rangedImgL = [pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinRangedIdle.png').convert_alpha(), (TILESIZE * 0.99, TILESIZE * 0.99)),
                           pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinRangedLeft.png').convert_alpha(), (TILESIZE *0.99, TILESIZE * 0.99)),
                           pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinRangedRight.png').convert_alpha(), (TILESIZE * 0.99, TILESIZE * 0.99)),
                           pygame.transform.scale(pygame.image.load('Sprites/npcs/sampleEnemy/pumpkinRangedUp.png').convert_alpha(), (TILESIZE * 0.99, TILESIZE * 0.99))]

        # holds the data for the enemy types

        self.pumpkinRobot = {'down': self.pumpkinImgDown, 'damage': 80, 'health': 80, 'speed': PLAYER_SPEED * 0.5}
        self.rangedPumpkin = {'image': self.rangedImgL,  'damage': 100, 'health': 60}

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

        self.map = currentTileMap[mapList[self.game.map[0]][self.game.map[1]]]
        self.path = Pathfinder(self.map, self)
        playerPos = self.game.player.rect.center
        enemyPos = self.rect.center
        self.xChange, self.yChange = (coord*self.speed for coord in self.path.createPath((enemyPos[0]//TILESIZE, enemyPos[1]//TILESIZE), (playerPos[0]//TILESIZE, playerPos[1]//TILESIZE)))

    # sets up the enemy instance depending on enemy type
    def setup(self):
        if self.type == 'pumpkinRobot':
            self.health = self.pumpkinRobot['health']
            self.speed = self.pumpkinRobot['speed']
            self.damage = self.pumpkinRobot['damage']
            self.imagelist = self.pumpkinRobot['down']
        if self.attackType == 'ranged':
            self.imagelist = self.rangedPumpkin['image']
            self.image = self.imagelist[self.imageIndex]
            self.health = self.rangedPumpkin['health']
            self.damage = self.rangedPumpkin['damage']

    def deathAnimation(self):
        pass

    ### EDDIE
    # Makes the player's sprite flicker by changing the alpha values rapidly
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

    #Authored: Max Chiu 4/18/2024
    # Does damage to the enemy based on type of the attack it is hit with
    def dealtDamage(self, damage, type):
        if not self.hitInvulnerable:
            if type == 'bubble':
                self.health -= damage
                self.stunned = True
                self.state = 'stunned'
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
                self.game.updateAliveLists('enemy', self.defaultPos)
                pygame.mixer.Channel(4).set_volume(0.065 * self.game.soundVol)
                pygame.mixer.Channel(4).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_Battle_SFX/69_Enemy_death_01.wav'))
            # print(f"enemy (self) health is {self.health}")
        else:
            return

    def animate(self):
        if self.attackType != 'ranged':
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
        else:
            if self.facingDirection == 'right':
                self.imageIndex = 2
            elif self.facingDirection == 'down':
                self.imageIndex = 0
            elif self.facingDirection == 'left':
                self.imageIndex = 1
            elif self.facingDirection == 'up':
                self.imageIndex = 3
        self.image = self.imagelist[self.imageIndex]
        self.flicker()

    #Authored: Max Chiu 4/18/2024
    def update(self):
        enemyPos = self.rect.center
        self.path.start = (enemyPos[0], enemyPos[1])

        if self.game.state not in ['dialogue', 'scene', 'pause', 'game over', 'shopping']:
            if self.attackType == 'melee':
                self.searchPlayer()
            self.animate()
            self.attack()


            if self.state == 'standing' or self.state == 'stunned':
                self.yChange = 0
                self.xChange = 0
                if self.stunned:
                    self.stunCount += 1
                    if self.stunCount > self.stunTimer:
                        self.stunned = False
                        self.stunCount = 0

            elif self.state == 'knockback':
                if self.rect.x + self.rect.width + self.xChange *-1 > 1240:
                    self.rect.x = 1240-self.rect.width
                else:
                    self.rect.x += self.xChange * -1
                self.collideBlocks('x')
                if self.rect.y + self.rect.height + self.yChange *-1 > 680:
                    self.rect.y = 680-self.rect.height
                else:
                    self.rect.y += self.yChange * -1
                self.collideBlocks('y')

                self.x = self.rect.x
                self.y = self.rect.y

            else: #self.state == 'chasing'
                self.searchPlayer()
                self.rect.x += self.xChange
                collideX = self.collideBlocks('x')
                self.rect.y += self.yChange
                collideY = self.collideBlocks('y')
                #print('before', self.path.collision_rects)
                #print('before state check:', self.state)
                if (self.state == 'searching' or self.state == 'returning') and (collideX or collideY):
                    if collideX:
                        #print('collided x')
                        if self.yChange < 0: #need to move up
                            #print('x up')
                            self.path.collision_rects.insert(0, pygame.Rect(enemyPos[0]-1, enemyPos[1]-TILESIZE-1, 2, 2))
                        elif self.yChange > 0: #need to move down
                            #print('x down')
                            self.path.collision_rects.insert(0, pygame.Rect(enemyPos[0]-1, enemyPos[1]+TILESIZE-1, 2, 2))
                        # elif self.xChange > 0 and self.yChange == 0: #need to move left
                        #     print('x left')
                        #     self.path.collision_rects.insert(0, pygame.Rect(enemyPos[0]-TILESIZE-1, enemyPos[1]-1, 2, 2))
                        # elif self.xChange < 0 and self.yChange == 0: #need to move right
                        #     print('x right')
                        #     self.path.collision_rects.insert(0, pygame.Rect(enemyPos[0]+TILESIZE-1, enemyPos[1]-1, 2, 2))
                    elif collideY:
                        #print('collided y')
                        if self.xChange < 0: #need to move left
                            #print('y left')
                            self.path.collision_rects.insert(0, pygame.Rect(enemyPos[0]-TILESIZE-1, enemyPos[1]-1, 2, 2))
                        elif self.xChange > 0: #need to move right
                            #print('y right')
                            self.path.collision_rects.insert(0, pygame.Rect(enemyPos[0]+TILESIZE+1, enemyPos[1]-1, 2, 2))
                        # elif self.yChange < 0 and self.xChange == 0: #need to move down
                        #     print('y down')
                        #     self.path.collision_rects.insert(0, pygame.Rect(enemyPos[0]-1, enemyPos[1]-TILESIZE-1, 2, 2))
                        # elif self.yChange > 0 and self.xChange == 0: #need to move up
                        #     print('y up')
                        #     self.path.collision_rects.insert(0, pygame.Rect(enemyPos[0]-1, enemyPos[1]-TILESIZE-1, 2, 2))
                #print('after ', self.path.collision_rects)
                #print('dx', self.xChange, 'dy', self.yChange)
                self.x = self.rect.x
                self.y = self.rect.y


            if self.hitInvulnerable:
                self.hitInvulnerableTime += 1
                if self.hitInvulnerableTime > self.invulnerableTimer:
                    self.hitInvulnerable = False
                    self.hitInvulnerableTime = 0
                    self.speed *= (1/0.7)

            
            
    #Authored: Max Chiu 4/28/2024
    #Modified: Max Chiu 4/28/2024 - 5/10/2024
    def searchPlayer(self):
        #print(self.state)
        if not self.hitInvulnerable and not self.stunned and self.attackType == 'melee':
            self.state = 'chasing' if self.state not in ['chasing', 'searching', 'standing', 'returning'] else self.state
            #print(self.xChange, self.yChange)

        if self.state == 'stunned' or self.state == 'knockback':
            return
        
        if self.state == 'returning':
            #print(len(self.path.collision_rects))
            if self.path.collision_rects == []:
                self.path = Pathfinder(self.map, self)
                enemyPos = self.rect.center
                self.path.createPath((enemyPos[0]//TILESIZE, enemyPos[1]//TILESIZE), (self.defaultPos[0], self.defaultPos[1]))
            change = self.path.checkCollisions()
            #print(change)
            if change and change != (0, 0):
                self.xChange, self.yChange = change[0]*self.speed*0.7, change[1]*self.speed*0.7
            else:  
                self.state = 'standing'
                self.moving = False
                self.path.emptyPath()
        elif self.state == 'searching':
            change = self.path.checkCollisions()
            # print('change dx dy', change)
            # print(len(self.path.collision_rects))
            # print(change != (0, 0))
            if change != (0, 0):
                self.xChange, self.yChange = change[0]*self.speed, change[1]*self.speed
                if self.xChange == 0 and self.yChange == 0:
                    self.state = 'chasing'
            else:
                self.state = 'returning'
                self.path.emptyPath()
            return
        playerPos = [self.game.player.x, self.game.player.y]

        ### MAX FINAL PRESENTATION
        #px and py are the coordinates for the center of the player
        lines=[]
        px = playerPos[0]+self.game.player.width/2
        py = playerPos[1]+self.game.player.height/2
        #ex and ey are the coordinates for the center of the enemy
        ex = self.x+self.width/2
        ey = self.y+self.height/2
        #split up the line of sight into n line segments and calculate the dx and dy for 1 line segment
        n = 5
        dx = (px - ex)/n
        dy = (py - ey)/n
        #print(dx, dy)

        #find the distance between player and enemy, check if this distance is outside the range of the enemy
        distance = math.sqrt((dx*n)**2+(dy*n)**2)
        #print(distance)
        if distance > 300: #implement pathfinding for the last 4-5 tiles of the player
            # self.xChange = 0
            # self.yChange = 0
            if self.state != 'standing' and self.state != 'returning':
                self.state = 'searching'
                playerPos = self.game.player.rect.center
                enemyPos = self.rect.center
                self.path = Pathfinder(self.map, self)
                # self.xChange, self.yChange = (coord*self.speed for coord in self.path.createPath((enemyPos[0]//TILESIZE, enemyPos[1]//TILESIZE), (playerPos[0]//TILESIZE, playerPos[1]//TILESIZE)))
                self.path.createPath((enemyPos[0]//TILESIZE, enemyPos[1]//TILESIZE), (playerPos[0]//TILESIZE, playerPos[1]//TILESIZE))
                change = self.path.checkCollisions()

                if change != (0, 0):
                    self.xChange, self.yChange = change[0]*self.speed, change[1]*self.speed

                else:
                    # self.state = 'chasing'
                    # self.path.emptyPath()
                    # print('searching to chasing')
                    self.state = 'returning'
                    self.path.emptyPath()
            return

        surface = pygame.Surface(self.game.screen.get_size(), pygame.SRCALPHA)
        for i in range(n):
            lines.append(pygame.draw.line(surface, (0, 0, 0, 0), (ex+dx*i, ey+dy*i), (ex+dx*(i+1), ey+dy*(i+1)), 1))
        index = [line.collidelist(list(block.rect for block in self.game.blocks)) for line in lines]
        isChasing = True

        #if any of these indices are not -1, there is no line of sight between the player and the enemy
        for i in index:
            if i != -1:
                # print(i)
                # rect = self.game.blocks.get_sprite(i)
                # rect.image.fill(BLUE)
                isChasing = False

        #if move and not self.path.collision_rects:
        if isChasing:
            #print('line collisions', index)
            self.state = 'chasing'
            self.path.emptyPath()
            self.moving = True
            dx, dy = Multiclass.normalize(dx*n, dy*n)
            self.xChange = dx * self.speed
            self.yChange = dy * self.speed
            #print(self.xChange, self.yChange)
            
        elif not isChasing and self.state not in ['returning', 'standing']:
            
            # self.xChange = 0
            # self.yChange = 0
            playerPos = self.game.player.rect.center
            enemyPos = self.rect.center
            self.path = Pathfinder(self.map, self)
            self.xChange, self.yChange = (coord*self.speed for coord in self.path.createPath((enemyPos[0]//TILESIZE, enemyPos[1]//TILESIZE), (playerPos[0]//TILESIZE, playerPos[1]//TILESIZE)))
            change = self.path.checkCollisions()
            if change:
                self.xChange, self.yChange = change[0]*self.speed, change[1]*self.speed
                self.state = 'searching'
            else:
                self.state = 'standing'
                self.moving = False
                self.path.emptyPath()
            return

    #Authored: Max Chiu 4/28/2024
    def collideBlocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) + pygame.sprite.spritecollide(self, self.game.npcs, False)
            #    if self.xChange > 0:
            #        self.rect.x = self.game.player.rect.left - self.rect.width
            #    if self.xChange < 0:
            #        self.rect.x = self.game.player.rect.right
            #elif hits and hits[0] != self:
            if hits:
                if self.xChange > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.xChange < 0:
                    self.rect.x = hits[0].rect.right
                #print('collided method x')
                return True
        else:
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) + pygame.sprite.spritecollide(self, self.game.npcs, False)
            #if pygame.sprite.collide_rect(self, self.game.player):
            #    if self.yChange > 0:
            #        self.rect.y = self.game.player.rect.top - self.rect.height
            #    if self.yChange < 0:
            #        self.rect.y = self.game.player.rect.bottom
            #elif hits and hits[0] != self:
            if hits: 
                if self.yChange > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.yChange < 0:
                    self.rect.y = hits[0].rect.bottom
                #print('collided method y')
                return True
        return False

    
    def attack(self):
        if pygame.sprite.collide_rect(self, self.game.player):
            self.game.player.getDamage(self.damage)
        elif self.attackType == 'ranged': ### MAX !!!
            self.timepassed += self.clock.get_time()/1000
            if self.timepassed > self.attackTimer:
                playerPos = self.game.player.rect.center
                enemyPos = self.rect.center
                dy = (playerPos[1] - enemyPos[1])
                dx = (playerPos[0] - enemyPos[0])
                #print(dx)
                #print(dy)
                if dx > 0:
                    angle = math.atan(-1*dy/dx)
                elif dx < 0 and dy < 0:
                    angle = math.pi - math.atan(dy/dx)
                elif dx < 0 and dy > 0:
                    angle = math.pi + math.atan(-1*dy/dx)
                if dx > 0 and (abs(dx) > abs(dy)):
                    self.facingDirection = 'right'
                elif dy < 0 and (abs(dy) > abs(dx)):
                    self.facingDirection = 'up'
                elif dx < 0 and (abs(dx) > abs(dy)):
                    self.facingDirection = 'left'
                elif dy < 0 and (abs(dy) > abs(dx)):
                    self.facingDirection = 'down'
                try:
                    #print(angle)
                    items.Bullet(self.game, self.x, self.y, angle, 1000, self.damage, 'enemy')
                except UnboundLocalError:
                    pass
                self.timepassed = 0
            

class Pathfinder:
    
    #Authored: Max Chiu 5/2/2024
    #Followed documentation guide: https://github.com/brean/python-pathfinding/blob/main/docs/01_basic_usage.md
    def __init__(self, map, enemy):
        matrix = []
        for i in range(len(map[1])):
            if i >= len(map):
                matrix.append([0]*32)
            else:
                matrix.append([])
                for j in range(len(map[1])):
                    if map[i][j:j+1] == 'B' or map[i][j:j+1] == 'N':
                        matrix[i].append(0)
                    else:
                        matrix[i].append(1)
        # for i in matrix:
        #     print(i)
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.enemy = enemy
        self.start = enemy.rect.center

    #Authored: Max Chiu 5/2/2024
    #Followed documentation guide: https://github.com/brean/python-pathfinding/blob/main/docs/01_basic_usage.md
    def createPath(self, startPos, endPos):
        start = self.grid.node(startPos[0], startPos[1])
        end = self.grid.node(endPos[0], endPos[1])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
        self.path, runs = finder.find_path(start, end, self.grid)
        #self.grid.cleanup()
        #print('operations:', runs, 'path length:', len(self.path))
        #print(self.grid.grid_str(path=self.path, start=start, end=end))
        self.getRectPath()
        return self.getDirection()

    #Authored: Max Chiu 5/3/2024
    #Followed sample code: https://github.com/clear-code-projects/Python-Pathfinder/blob/main/roomba%20project/pathfinding_roomba.py 
    def getRectPath(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = (point.x*TILESIZE)+self.enemy.width/2
                y = (point.y*TILESIZE)+self.enemy.width/2
                rect = pygame.Rect((x-1), (y-1), 2, 2)
                self.collision_rects.append(rect)
    
    #Authored: Max Chiu 5/3/2024
    #Followed sample code: https://github.com/clear-code-projects/Python-Pathfinder/blob/main/roomba%20project/pathfinding_roomba.py
    def getDirection(self):
        try:
            if self.collision_rects:
                end = self.collision_rects[0].center
                #print('start', self.start[0], self.start[1])
                #print('end', end[0], end[1])
                dx = (end[0] - self.start[0])
                dy = (end[1] - self.start[1])
                #print('dx', dx, 'dy', dy)

                #find the distance between player and enemy, check if this distance is outside the range of the enemy
                # distance = math.sqrt((dx)**2+(dy)**2)
                # dx /= distance
                # dy /= distance
                dx, dy = Multiclass.normalize(dx, dy)
                return dx, dy
            else:
                self.emptyPath()
                return 0, 0
        except AttributeError:
            self.emptyPath()
            return 0,0


    #Authored: Max Chiu 5/3/2024
    #Followed sample code: https://github.com/clear-code-projects/Python-Pathfinder/blob/main/roomba%20project/pathfinding_roomba.py
    def checkCollisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if pygame.Rect.colliderect(rect, self.enemy.rect):
                    del self.collision_rects[0]        
            return self.getDirection()
                
    #Authored: Max Chiu 5/3/2024
    #Followed sample code: https://github.com/clear-code-projects/Python-Pathfinder/blob/main/roomba%20project/pathfinding_roomba.py
    def emptyPath(self):
        self.collision_rects = []
        self.path = []


class Boss(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.all_sprites, self.game.enemies, self.game.non_background
        pygame.sprite.Sprite.__init__(self, self.groups)
        self._layer = ENEMY_LAYER
        self.x = x
        self.y = y
        self.width = TILESIZE * 3
        self.height = self.width * 5/4

        self.speed = PLAYER_SPEED * 0.35

        #self.maxHealth = 500
        # Lowered max health for testing and demonstration purposes
        self.maxHealth = 100
        self.currentHealth = self.maxHealth
        self.healthBarLength = WIDTH * 0.6
        self.healthBarHeight = HEIGHT * 0.05
        self.healthBarPos = (WIDTH * 0.25, HEIGHT * 0.8)
        self.healthRatio = self.maxHealth / self.healthBarLength
        self.collideDamage = 135
        # Line below to be used to pull boss images from the main.py file, where the images should be pre-loaded at the start of the game within the setupimages function.
        # May not look exactly like this, but this is the way that boss images should be referenced. There will be seperate lists of images within the overall bossImageList.
        # These lists will hold base boss sprites, as well as attacking sprites.
        # self.imageListNum = 0
        self.imageList = self.game.bossImageList[0]
        self.imageIndex = 1
        self.image = pygame.transform.scale(self.imageList[self.imageIndex], (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.directionX = 0
        self.directionY = 0

        self.particles = self.game.particleList[0]
        self.currentParticleIn = 0

        self.attackTimer = 0
        self.attackLimiter = 100
        self.attacking = False
        self.doneAttacking = True
        self.attackList = ['wave', 'barrage', 'quickbarrage', 'cluster']
        self.chosenAttack = ''

        self.attackPause = 16
        self.attackPauseCount = 0
        self.attackDurationCounter = 0
        self.attackDuration = 150
        self.reachedDestination = False
        self.currentDestination = (0, 0)

        self.upLeftClusterLoc = (WIDTH * 0.22, HEIGHT * 0.22)
        self.upRightClusterLoc = (WIDTH * 0.68, HEIGHT * 0.22)
        self.downLeftClusterLoc = (WIDTH * 0.22, HEIGHT * 0.68)
        self.downRightClusterLoc = (WIDTH * 0.68, HEIGHT * 0.68)


        self.moving = False
        self.dying = False
        self.hitInvincible = False
        self.hitInvulnerable = False
        self.hitInvulnerableTime = 0
        self.invulnerableTimer = 24
        self.animateTime = 0
        self.animateTimer = 40
        self.particles = Particle(self.game, self.x, self.y + self.height * 0.7, self.width, self.height * 0.3, 'boss')

    # Every frame of the game loop this will be called.
    # The boss should move if needed, the healthbar will be displayer, the boss's title should be displayed above the healthbar, and the boss should attack if needed.
    def update(self):
        if self.hitInvulnerable:
            self.hitInvulnerableTime += 1
            if self.hitInvulnerableTime > self.invulnerableTimer:
                self.hitInvulnerable = False
                self.hitInvulnerableTime = 0

        if (not self.game.player.swordUsed and not self.game.player.spearUsed and not self.game.player.weapon.used):
            self.hitInvincible = False
        #print(f'self.hitInvulnerable is {self.hitInvulnerable}, self.hitInvincible is {self.hitInvincible}')
        # This line is a placeholder, there will be a conditional that will check if the boss should be moving currently.
        # Haven't thought of what condition that will be checking yet, maybe just if the boss is not currently attacking.
        if not self.attacking:
            self.moving = True
        self.attack()
        self.move()
        self.animate()
        self.flicker()
        self.ui()
        self.particles.setPosition(self.x, self.y + self.height * 0.7)
        if (not isinstance(self.directionX, float) or not isinstance(self.directionY, float) or (self.x == self.currentDestination[0] and self.y == self.currentDestination[1])) and self.attacking:
            self.reachedDestination = True

        pass

    def ui(self):
        if self.game.bossActive:
            self.healthbar()
            bossTitle = "CEO of Pollution"
            self.game.screen.blit(pygame.font.SysFont('Garamond', 18).render(bossTitle.strip(), False, WHITE),(self.healthBarPos[0], self.healthBarPos[1] - HEIGHT * 0.04))
            #pygame.display.update()#

    # Function should create the boss's healthbar on the screen, including the max length and the current percentage of health remaining. The boss's name would also be displayed right above the healthbar.
    def healthbar(self):
        pygame.draw.rect(self.game.screen, (255, 0, 0),(self.healthBarPos[0], self.healthBarPos[1], self.currentHealth / self.healthRatio, self.healthBarHeight))
        pygame.draw.rect(self.game.screen, (255, 255, 255), (self.healthBarPos[0], self.healthBarPos[1], self.healthBarLength, self.healthBarHeight), 4)
        pass

    def dealtDamage(self, damage, type):
        if not self.hitInvulnerable:
            if type == 'trident':
                self.currentHealth -= damage * 1.5
            else:
                self.currentHealth -= damage
            self.hitInvulnerable = True
        if self.currentHealth <= 0:
            self.death()
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
            #print(self.image.get_alpha())
        else:
            self.image.set_alpha(255)
        pass

    # General attack function for boss
    # Will function to decide which attacks the boss is going to use if there needs to be a choice made
    # An attack choice will happen when the boss is not attacking and it is not on attack cooldown (there will be multiple attacks to choose from, assuming these are implemented properly)
    def attack(self):
        if pygame.sprite.collide_rect(self, self.game.player):
            self.game.player.getDamage(self.collideDamage)
        if not self.attacking:
            self.attackTimer += 1
            if self.attackTimer >= self.attackLimiter:
                self.attackTimer = 0
                randomNum = random.randint(0, 100)
                if randomNum >= 20 and randomNum <= 40:
                    self.chosenAttack = self.attackList[0]
                elif randomNum > 77:
                    self.chosenAttack = self.attackList[1]
                elif randomNum > 35 and randomNum <= 55:
                    self.chosenAttack = self.attackList[2]
                elif randomNum > 55 and randomNum <= 77:
                    self.chosenAttack = self.attackList[3]
        if self.chosenAttack == self.attackList[0]:
            self.attackWave()
        elif self.chosenAttack == self.attackList[1]:
            self.attackBarrage()
        elif self.chosenAttack == self.attackList[2]:
            self.attackBarrageQuick()
        elif self.chosenAttack == self.attackList[3]:
            self.attackCluster()
        #print(self.chosenAttack)
        pass

    # This function will cause the boss to perform an attack in which they launch a cascading wave type attack out.
    # This might go in the player's direction, or it could just be an attack that hits a predetermined location.
    def attackWave(self):
        self.attackDuration = 300
        self.attackPause = 16
        self.moving = False
        self.attacking = True
        if self.reachedDestination:
            self.attackDurationCounter += 1
        if self.doneAttacking and self.reachedDestination:
            self.doneAttacking = False
            for attack in range(20):
                BossAttack(self.game, self.x + attack * (self.width // 20), self.y + self.height * 1.05, 110, (math.cos(math.pi / (57.7 / ((attack + 1) * 18)) + self.attackDurationCounter % 15), math.sin(math.pi / (57.7 / ((attack+1) * 18)) + self.attackDurationCounter % 15)))
        self.attackPauseCount += 1
        if self.attackPauseCount >= self.attackPause:
            self.attackPauseCount = 0
            self.doneAttacking = True
        if self.attackDurationCounter >= self.attackDuration:
            self.attackDurationCounter = 0
            self.resetStatus()
        pass

    def attackBarrage(self):
        self.attackDuration = 150
        self.attackPause = 16
        self.moving = False
        self.attacking = True
        self.attackDurationCounter += 1
        if self.doneAttacking == True:
            self.doneAttacking = False
            BossAttack(self.game, self.x + self.width * 0.5, self.y + self.height * 1.1, 160, self.getDirection(self.game.player.rect.center))
        self.attackPauseCount += 1
        if self.attackPauseCount >= self.attackPause:
            self.attackPauseCount = 0
            self.doneAttacking = True
        if self.attackDurationCounter >= self.attackDuration:
            self.attackDurationCounter = 0
            self.resetStatus()

    def attackBarrageQuick(self):
        self.attackDuration = 200
        self.attackPause = 4
        self.moving = False
        self.attacking = True
        self.attackDurationCounter += 1
        if self.doneAttacking == True:
            self.doneAttacking = False
            BossAttack(self.game, self.x + self.width * 0.5, self.y + self.height * 1.1, 130, self.getDirection(self.game.player.rect.center), 6)
        self.attackPauseCount += 1
        if self.attackPauseCount >= self.attackPause:
            self.attackPauseCount = 0
            self.doneAttacking = True
        if self.attackDurationCounter >= self.attackDuration:
            self.attackDurationCounter = 0
            self.resetStatus()

    def attackCluster(self):
        self.attackDuration = 350
        self.moving = False
        self.attacking = True
        self.doneAttacking = False
        self.directionX = 0
        self.directionY = 0
        self.attackDurationCounter += 1
        print("doing attack cluster")
        self.attackClustersBurst()
        if self.attackDurationCounter >= self.attackDuration:
            self.attackDurationCounter = 0
            self.resetStatus()

    def attackClustersBurst(self):
        self.attackPause = self.attackDuration / 3
        print(self.attackPauseCount)
        self.attackPauseCount += 1
        if self.attackPauseCount >= self.attackPause - 10:
            for attack in range(12):
                if attack < 3:
                    BossAttack(self.game, self.upLeftClusterLoc[0], self.upLeftClusterLoc[1], 90, (math.cos(math.pi / (57.7 / ((attack + 1) * 36)) + self.attackDurationCounter % self.attackDuration // 3), math.sin(math.pi / (57.7 / ((attack+1) * 36)) + self.attackDurationCounter % self.attackDuration // 3)), 4)
                elif attack >= 3 and attack < 6:
                    BossAttack(self.game, self.downLeftClusterLoc[0], self.downLeftClusterLoc[1], 90, (math.cos(math.pi / (57.7 / ((attack + 1) * 36)) + self.attackDurationCounter % self.attackDuration // 3), math.sin(math.pi / (57.7 / ((attack + 1) * 36)) + self.attackDurationCounter % self.attackDuration // 3)), 4)
                elif attack >= 6 and attack < 9:
                    BossAttack(self.game, self.upRightClusterLoc[0], self.upRightClusterLoc[1], 90, (math.cos(math.pi / (57.7 / ((attack + 1) * 36)) + self.attackDurationCounter % self.attackDuration // 3), math.sin(math.pi / (57.7 / ((attack + 1) * 36)) + self.attackDurationCounter % self.attackDuration // 3)), 4)
                else:
                    BossAttack(self.game, self.downRightClusterLoc[0], self.downRightClusterLoc[1], 90, (math.cos(math.pi / (57.7 / ((attack + 1) * 36)) + self.attackDurationCounter % self.attackDuration // 3), math.sin(math.pi / (57.7 / ((attack + 1) * 36)) + self.attackDurationCounter % self.attackDuration // 3)), 4)
        if self.attackPauseCount >= self.attackPause:
            self.attackPauseCount = 0
        elif self.attackPauseCount == 0 or self.attackPauseCount == 1:
            BossAttackIndicator(self.game, self.upLeftClusterLoc[0], self.upLeftClusterLoc[1], TILESIZE, TILESIZE, 'circle', self.attackPause - 10)
            BossAttackIndicator(self.game, self.upRightClusterLoc[0], self.upRightClusterLoc[1], TILESIZE, TILESIZE,'circle', self.attackPause - 10)
            BossAttackIndicator(self.game, self.downLeftClusterLoc[0], self.downLeftClusterLoc[1], TILESIZE, TILESIZE,'circle', self.attackPause - 10)
            BossAttackIndicator(self.game, self.downRightClusterLoc[0], self.downRightClusterLoc[1], TILESIZE, TILESIZE,'circle', self.attackPause - 10)



    def animate(self):
        if self.reachedDestination and self.attacking and self.chosenAttack == 'wave':
            self.imageList = self.game.bossImageList[1]
            self.animateTime += 1
            if self.animateTime >= self.animateTimer:
                self.animateTime = 0
            if self.animateTime < (self.animateTimer // 3):
                self.imageIndex = 0
            elif self.animateTime < (self.animateTimer // 3 * 2):
                self.imageIndex = 1
            elif self.animateTime < (self.animateTimer):
                self.imageIndex = 2
        elif not self.reachedDestination and not self.attacking:
            self.animateTime = 0
        self.image = pygame.transform.scale(self.imageList[self.imageIndex], (self.width, self.height))

        pass

    # Inspired by https://www.youtube.com/watch?v=QU1pPzEGrqw
    def getDirection(self, location):
        enemyVector = pygame.math.Vector2(self.rect.center)
        objVector = pygame.math.Vector2(location)
        distance = (objVector - enemyVector).magnitude()

        if distance > 0:
            direction = (objVector - enemyVector).normalize()
        else:
            direction = pygame.math.Vector2()

        return direction

    def getDistance(self, location):
        enemyVector = pygame.math.Vector2(self.rect.center)
        objVector = pygame.math.Vector2(location)
        distance = (objVector - enemyVector).magnitude()

        return distance

    # The boss should move around the room in a certain pattern. The specific pattern they follow could depend on the player's position, but they should not just strictly follow the player around.
    def move(self):
        if self.moving:
            self.directionX = self.getDirection(self.game.player.rect.center)[0]
            self.directionY = self.getDirection(self.game.player.rect.center)[1]
        #print(self.directionX, self.directionY)
        elif self.attacking and self.chosenAttack == 'wave':
            self.directionX, self.directionY = self.getDirection((WIDTH * 0.5, HEIGHT * 0.5))
            self.currentDestination = (WIDTH * 0.5, HEIGHT * 0.5)
            if self.getDistance(self.currentDestination) < 10:
                self.reachedDestination = True
        try:
            self.x += self.directionX * self.speed
            self.y += self.directionY * self.speed
            self.rect.x = self.x
            self.rect.y = self.y
        except TypeError:
            self.x = self.x
            self.y = self.y
            self.rect.x = self.x
            self.rect.y = self.y
            print("error avoided")

        pass

    # Resets the boss's status back to default, which should be moving around the boss room.
    def resetStatus(self):
        self.attacking = False
        self.doneAttacking = True
        self.moving = True
        self.chosenAttack = ''
        self.reachedDestination = False
        self.imageList = self.game.bossImageList[0]
        self.imageIndex = 1
        self.attackDuration = 150
        pass

    def death(self):
        self.game.bossDefeated = True
        self.particles.kill()
        self.kill()
        # self.game.game_won()
        GameEndTeleport(self.game, 15, 3)
        GameEndTeleport(self.game, 16, 3)
        pass

class Particle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, version='general'):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.groups = self.game.all_sprites, self.game.particles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self._layer = ITEM_LAYER
        # version should be boss or general, this will determine which list of images the particle effect will reference
        self.version = version
        self.imageList = self.game.particleList[1]
        self.image = pygame.transform.scale(self.imageList[0], (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.animationTimer = 40
        self.animationCount = 0
        self.animationPhase = 1

        self.setup()

    def setup(self):
        if self.version == 'boss':
            self.imageList = self.game.particleList[1]
        else:
            self.imageList = self.game.particleList[0]

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.animate()
        pass

    def reset(self):
        self.animationCount = 0
        self.animationPhase = 1

    def animate(self):
        self.animationCount += 1
        if self.animationCount >= self.animationTimer:
            self.reset()
        if self.animationCount < (self.animationTimer // 3):
            self.animationPhase = 1
        elif self.animationCount < (self.animationTimer // 3 * 2):
            self.animationPhase = 2
        elif self.animationCount < (self.animationTimer):
            self.animationPhase = 3
        self.image = pygame.transform.scale(self.imageList[self.animationPhase - 1], (self.width, self.height))

        pass

    def setPosition(self, newX, newY):
        self.x = newX
        self.y = newY


class BossAttack(pygame.sprite.Sprite):
    def __init__(self, game, x, y, damage, direction, speed=4, moving = True):
        self.game = game
        self.x = x
        self.y = y
        self.damage = damage
        self.direction = direction
        self.speed = speed
        self.moving = moving
        self._layer = ENEMY_LAYER
        self.image = self.game.bossAttacks[2]
        self.groups = self.game.all_sprites, self.game.non_background
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.decayTimer = 180
        if not self.moving:
            self.decayTimer = 40

    def setPosition(self, newX, newY):
        self.x = newX
        self.y = newX

        pass

    def move(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.move()
        self.collision()
        self.decay()
        pass

    def collision(self):
        if pygame.sprite.collide_rect(self, self.game.player):
            self.game.player.getDamage(self.damage)
        for block in self.game.blocks:
            if pygame.sprite.collide_rect(self, block):
                self.kill()
        pass

    def decay(self):
        self.decayTimer -= 1
        if self.decayTimer <= 0:
            self.kill()

class BossAttackIndicator(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, shape, decay):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.groups = self.game.all_sprites, self.game.non_background
        pygame.sprite.Sprite.__init__(self, self.groups)
        if shape == 'circle':
            self.image = pygame.transform.scale(pygame.image.load('Sprites/items/bubble.png').convert_alpha(), (TILESIZE, TILESIZE))
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.decayLength = decay

    def update(self):
        self.decayLength -= 1
        if self.decayLength <= 0:
            self.kill()


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
        self.image = self.game.tileList[0][1]
        #self.image = pygame.Surface([self.width, self.height])
        #self.image.fill(BLUE)
        self.rect.x = self.x
        self.rect.y = self.y

class GameEndTeleport(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.endgates
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.width = TILESIZE
        self.height = TILESIZE
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = self.game.tileList[0][2]
        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill(BLUE)
        self.rect.x = self.x
        self.rect.y = self.y

class TextBox(pygame.sprite.Sprite):
    def __init__(self, game, npc):
        self.game = game
        self.npc = npc
        self._layer = TEXT_LAYER
        self.groups = self.game.all_sprites, self.game.user_interface
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
        #self.imagelist = os.listdir('Sprites/npcs/chipichipichapachapa')
        #self.imgindex = 3

        self.selectedRect = 0
        self.choiceRectList = []

        #image = pygame.transform.scale(pygame.image.load(f'Sprites/npcs/chipichipichapachapa/{self.imagelist[self.imgindex]}').convert_alpha(), (self.avatarBox.width, self.avatarBox.height))
        image = self.npc.avatarImg
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
                    cutoffIndex = len(text[:maxLength])-re.search("[^a-zA-Z0-9()']", text[maxLength-1::-1]).end()+1
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
        #self.imgindex = (self.imgindex+1)%392
        self.timepassed += self.clock.get_time()/1000
        image = self.npc.avatarImg
        self.image.blit(image, self.avatarBox)
        self.image.blit(pygame.font.SysFont('Courier', 25).render(self.name, False, (255, 255, 255)),(self.avatarBox.x + self.avatarBox.width / 2 - len(self.name) * TILESIZE / 5.5, self.height * 0.89))
        if len(self.choiceRectList) > 0:
            for rect in range(len(self.choiceRectList)):
                if rect == self.selectedRect:
                    pygame.draw.rect(self.image, BLACK, self.choiceRectList[rect], 2, 1)
                else:
                    pygame.draw.rect(self.image, GRAY, self.choiceRectList[rect], 2, 1)

class Multiclass:
    def normalize(dx, dy):
        if dx == 0 and dy == 0:
            return 0, 0
        distance = math.sqrt(dx**2+dy**2)
        return dx/distance, dy/distance
        

class Inventory(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self._layer = TEXT_LAYER
        self.groups = self.game.all_sprites, self.game.user_interface
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.hotbar_img = [pygame.transform.scale(pygame.image.load('Sprites/items/sunflowernew.png').convert_alpha(), (TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/oreAmethyst.png').convert_alpha(), (TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/potion.png').convert_alpha(), (TILESIZE, TILESIZE))]


        self.x = 1*TILESIZE
        self.y = 15.5*TILESIZE
        self.width = 5.5*TILESIZE
        self.height = 2.5*TILESIZE

        self.image = pygame.transform.scale(pygame.image.load('Sprites/hudImages/pixil-frame-0_cropped.png').convert_alpha(), (self.width, self.height))
        #self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.font = pygame.font.SysFont("Calibri", 20)
        self.slots = {"flower":20, "ore":20, "potion": 0}

        for i in range(len(self.hotbar_img)):
            self.image.blit(self.hotbar_img[i], pygame.Rect(25+65*(i),30,0,0))

        self.numList = []
        self.numList.append(self.image.blit(self.font.render(str(self.slots.get('flower')),False,(WHITE)),(60,53)))
        self.numList.append(self.image.blit(self.font.render(str(self.slots.get('ore')),False,(WHITE)),(125,53)))
        self.numList.append(self.image.blit(self.font.render(str(self.slots.get('potion')),False,(WHITE)),(190,53)))

    ### RACHEL
    def add_item(self, item, number):
        self.slots[item] =  self.slots.get(item) + number
        for image in self.numList:
            pygame.draw.rect(self.image, BLACK, image)
        flowerX = 60
        oreX = 125
        potionX = 190
        if self.slots.get('flower') > 9:
            flowerX = 55
            self.numList.append(self.image.blit(self.font.render(str(self.slots.get('flower')),False,(WHITE)),(flowerX,53)))
        else:
            self.numList.append(self.image.blit(self.font.render(str(self.slots.get('flower')),False,(WHITE)),(flowerX,53)))
        if self.slots.get('ore') > 9:
            oreX = 120
            self.numList.append(self.image.blit(self.font.render(str(self.slots.get('ore')),False,(WHITE)),(oreX,53)))
        else:
            self.numList.append(self.image.blit(self.font.render(str(self.slots.get('ore')),False,(WHITE)),(oreX,53)))
        if self.slots.get('potion') > 9:
            potionX = 185
            self.numList.append(self.image.blit(self.font.render(str(self.slots.get('potion')),False,(WHITE)),(potionX,53)))
        else:
            self.numList.append(self.image.blit(self.font.render(str(self.slots.get('potion')),False,(WHITE)),(potionX,53)))

    def get(self, item):
        return self.slots.get(item)

    def draw(self):
        if self.game.state == 'explore' or self.game.state == 'oreMine' or self.game.state == 'flowerC':
            if self not in self.game.all_sprites:
                self.groups = self.game.all_sprites, self.game.user_interface
                self.add(self.game.all_sprites, self.game.user_interface)
        else:
        # removes the inventory from the list of sprites to be drawn if it should not be shown
            self.remove(self.game.all_sprites, self.game.user_interface)


class WeaponDisplay(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self._layer = TEXT_LAYER
        self.groups = self.game.all_sprites, self.game.user_interface
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.swordfishWep = {'name' : 'swordfish', 'image': pygame.image.load('Sprites/items/swordfish3.png').convert_alpha(), 'inactiveImg' : pygame.image.load('Sprites/items/swordfishGray.png').convert_alpha(), 'active' : True}
        self.tridentWep = {'name' : 'trident', 'image' : pygame.image.load('Sprites/items/trident3.png').convert_alpha(), 'inactiveImg' : pygame.image.load('Sprites/items/tridentGray.png').convert_alpha(), 'active' : False}
        self.bubblegunWep = {'name' : 'bubble', 'image' : self.game.player.weapon.imagelist[0], 'inactiveImg' : pygame.image.load('Sprites/items/bubblegunGray.png').convert_alpha(), 'active' : False}
        self.weaponList = [self.swordfishWep,
                           self.bubblegunWep,
                           self.tridentWep]
        self.x = WIDTH * 0.83
        self.y = HEIGHT * 0.018
        self.width = 4.5 * TILESIZE
        self.height = 2 * TILESIZE
        self.image = pygame.transform.scale(pygame.image.load('Sprites/hudImages/pixil-frame-0_cropped.png').convert_alpha(), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.changeTimer = 20
        self.changeCount = 0
        self.hasSwitched = False
        self.highlightColorList = [(176, 176, 46), (156, 90, 60)]
        self.highlightNumber = 0

    def update(self):
        if self.hasSwitched:
            self.changeCount += 1
            value = math.sin(self.changeCount)
            if value > 0:
                self.highlightNumber = 1
            else:
                self.highlightNumber = 0
            if self.changeCount >= self.changeTimer:
                self.changeCount = 0
                self.highlightNumber = 0
                self.hasSwitched = False

    # draws the weapons display onto the screen if needed
    def draw(self):
        if self.game.state == 'explore' or self.game.state == 'oreMine' or self.game.state == 'flowerC':
            if self not in self.game.all_sprites:
                self.groups = self.game.all_sprites, self.game.user_interface
                self.add(self.game.all_sprites, self.game.user_interface)
            if self.game.player.weapon.type == 'bubble':
                self.displayRangedAmmo()
            for i in range(len(self.weaponList)):
                if self.weaponList[i]['name'] in self.game.player.activeWeaponList:
                    currentImage = pygame.transform.scale(self.weaponList[i]['image'].convert_alpha(), (TILESIZE * 0.8, TILESIZE * 0.8))
                    self.image.blit(currentImage, pygame.Rect((self.width*0.1) + self.width * 0.3*(i),self.height * 0.25,0,0))
                    if self.weaponList[i]['active']:
                        pygame.draw.rect(self.game.screen, self.highlightColorList[self.highlightNumber],(self.x + 10 + self.width * 0.3 * i, self.y + 18, TILESIZE * 1.3, TILESIZE * 1.1), 3)
                else:
                    # if the weapons are not in the active list, they will be grayed out on the display
                    currentImage = pygame.transform.scale(self.weaponList[i]['inactiveImg'].convert_alpha(), (TILESIZE * 0.8, TILESIZE * 0.8))
                    self.image.blit(currentImage, pygame.Rect((self.width * 0.1) + self.width * 0.3 * (i), self.height * 0.25, 0, 0))

        else:
            # removes the weapon hud from the list of sprites to be drawn if it should not be shown
            self.remove(self.game.all_sprites, self.game.user_interface)

    def displayRangedAmmo(self):
        #print("in displayRangedAmmo func")
        ammoCount = self.game.player.weapon.ammo // 3
        for ammo in range(ammoCount):
            pygame.draw.circle(self.game.screen, PINK, (20 + ammo * 13, 45), 8)

    # checks the weapon that is actively equipped and updates the info within the hud to reflect that
    def checkActiveWep(self):
        currWeapon = self.game.player.weapon.type
        self.changeCount = 0
        self.hasSwitched = True
        if currWeapon == 'swordfish':
            self.swordfishWep.update({'active': True})
            self.tridentWep.update({'active': False})
            self.bubblegunWep.update({'active': False})
        elif currWeapon == 'trident':
            self.swordfishWep.update({'active': False})
            self.tridentWep.update({'active': True})
            self.bubblegunWep.update({'active': False})
        elif currWeapon == 'bubble':
            self.swordfishWep.update({'active': False})
            self.tridentWep.update({'active': False})
            self.bubblegunWep.update({'active': True})


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
                            "E to attack using melee & ranged weapons",
                            "SPACE to interact",
                            "R to reload ranged weapon",
                            "Press P to pause, change settings, disable tutorials, or quit."]
            #textSurf = pygame.font.SysFont('Garamond', 18).render(tutorialText[0].strip(), False, WHITE)
            #textSurf.set_alpha(127)
            #self.game.screen.blit(textSurf, (WIDTH * 0.72, HEIGHT * 0.78))
            self.game.screen.blit(pygame.font.SysFont('Garamond', 18).render(tutorialText[0].strip(), False, WHITE),(WIDTH * 0.7225, HEIGHT * 0.78))
            #textSurf = pygame.font.SysFont('Garamond', 18).render(tutorialText[1].strip(), False, WHITE)
            #textSurf.set_alpha(127)
            #self.game.screen.blit(textSurf, (WIDTH * 0.78, HEIGHT * 0.81))
            self.game.screen.blit(pygame.font.SysFont('Garamond', 18).render(tutorialText[1].strip(), False, WHITE),(WIDTH * 0.725, HEIGHT * 0.81))
            #textSurf = pygame.font.SysFont('Garamond', 18).render(tutorialText[2].strip(), False, WHITE)
            #textSurf.set_alpha(127)
            #self.game.screen.blit(textSurf, (WIDTH * 0.73, HEIGHT * 0.84))
            #textSurf = pygame.font.SysFont('Garamond', 18).render(tutorialText[3].strip(), False, WHITE)
            #self.game.screen.blit(textSurf, (WIDTH * 0.81, HEIGHT * 0.87))
            self.game.screen.blit(pygame.font.SysFont('Garamond', 18).render(tutorialText[2].strip(), False, WHITE),(WIDTH * 0.859, HEIGHT * 0.84))
            #textSurf = pygame.font.SysFont('Garamond', 18).render(tutorialText[4].strip(), False, WHITE)
            #textSurf.set_alpha(127)
            #self.game.screen.blit(textSurf, (WIDTH * 0.64, HEIGHT * 0.9))
            self.game.screen.blit(pygame.font.SysFont('Garamond', 18).render(tutorialText[3].strip(), False, WHITE),(WIDTH * 0.81, HEIGHT * 0.87))
            self.game.screen.blit(pygame.font.SysFont('Garamond', 18).render(tutorialText[4].strip(), False, WHITE),(WIDTH * 0.64, HEIGHT * 0.9))
            #pygame.display.update()
        else:
            return

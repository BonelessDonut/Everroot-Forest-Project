import random, math
from sprites import *
from settings import *
import pygame


# Assuming one melee and multiple ranged weapons
# type - weapon name: currently presumably some variation of sword and bubble gun (shotgun)
swordfish_imgs = [pygame.image.load('Sprites/items/swordfish.png'),
                  pygame.image.load('Sprites/items/swordfish2.png'), pygame.image.load('Sprites/items/swordfish3.png')]
swordfish_imgs = [pygame.transform.rotate(swordfish_imgs[0], 45),
                  pygame.transform.rotate(swordfish_imgs[1], 90),
                  swordfish_imgs[2],
                  pygame.transform.rotate(swordfish_imgs[0], 135),
                  pygame.transform.rotate(swordfish_imgs[1], 270),
                  pygame.transform.rotate(swordfish_imgs[2], 270),
                  pygame.transform.rotate(swordfish_imgs[0], 45),
                  pygame.transform.rotate(swordfish_imgs[1], 180),
                  pygame.transform.rotate(swordfish_imgs[2], 180),
                  pygame.transform.flip(pygame.transform.rotate(swordfish_imgs[0], 45), True, True),
                  pygame.transform.flip(pygame.transform.rotate(swordfish_imgs[1], 180), True, True),
                  pygame.transform.flip(pygame.transform.rotate(swordfish_imgs[2], 180), True, True)]
trident_imgs = [pygame.image.load('Sprites/items/trident2.png')]
trident_imgs = [trident_imgs[0], pygame.transform.flip(trident_imgs[0], False, True), pygame.transform.rotate(trident_imgs[0], 90), pygame.transform.rotate(trident_imgs[0], 270)]

#Author: Max Chiu 4/10/24
class Weapon(pygame.sprite.Sprite):
    def __init__(self, game, type, player):
        self.game = game
        self.clock = game.clock
        self.player = player
        self.groups = self.game.all_sprites, self.game.weapons
        self._layer = ITEM_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.type = type
        #timer used to count the time between attacks
        self.timer = 0
        self.timepassed = 0
        self.spread = None
        self.damage = None
        self.pause = None
        self.range = None
        self.reloadTime = None
        self.ammo = None
        self.x = self.player.x
        self.y = self.player.y
        self.width = TILESIZE//2
        self.height = TILESIZE//2
        self.used = False

        self.imagelist = [pygame.image.load('Sprites/items/bubblegun.png'), pygame.image.load('Sprites/items/bubblegunDown.png'), pygame.image.load('Sprites/items/bubblegunUp.png')]
        self.imagelist.append(pygame.transform.flip(pygame.image.load('Sprites/items/bubblegun.png'), True, False))
        self.image = pygame.transform.scale(self.imagelist[1], (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100


        #bubble is a burst of 3 bullets with 15 bullet ammo
        if type == 'bubble':
            #7 degrees spread of bubble bullets
            self.spread = 5
            self.damage = 10
            self.ammo = 60
            #how long to pause between each bullet
            self.pause = 0.3
            self.range = 5*TILESIZE
            #how long to reload ammo
            self.reloadTime = 2
            #how long each between each bullet during a burst (3 bullets should be separated by self.burstTime)
            self.burstTime = self.pause/10
        #melee
        else:
            #75 degrees spread of melee swing
            self.spread = 75
            self.damage = 20
            self.pause = 0.4

    def reload(self):
        if self.type == 'bubble':
            self.ammo = 60
    
    #Author: Max Chiu 4/10/2024
    def attack(self):
        if self.timer == 0:
            #self.player.itemUsed = True
            self.used = True
            #Can only shoot if having enough ammo
            #Since it's a burst weapon, you're only allowed to shoot after each burst is done shooting
            #After the first shot of each burst here, the other 2 bubbles are shot in the update method
            self.updateLocation()
            if self.type == 'bubble' and self.ammo > 0 and self.ammo % 3 == 0:
                Bullet(self.game, self.x, self.y, self.calculateAngle(), self.range, self.damage, 'player')
                self.ammo -= 1
                self.timer = self.pause

    def updateDamage(self):
        if self.type == 'bubble':
            self.damage = 10
        elif self.type == 'swordfish':
            self.damage = 20
        elif self.type == 'trident':
            self.damage = 35

        
    #Author: Max Chiu 4/12/2024
    def update(self):
        self.timepassed = self.clock.get_time() / 1000
        
        #To space out the bubble shots by burstTime
        if self.ammo % 3 == 2 and -1*self.burstTime < self.timer - self.pause < 0 or self.ammo % 3 == 1 and -2*self.burstTime < self.timer - self.pause < -1*self.burstTime:
            Bullet(self.game, self.x, self.y, self.calculateAngle(), self.range, self.damage, 'player')
            self.ammo -= 1
            pygame.mixer.Channel(1).set_volume(0.09 * self.game.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/shooting-sound-fx-159024.mp3'))

        #editing the timer between shots
        self.timer -= self.timepassed
        if self.timer <= 0:
            self.timer = 0
            #self.player.itemUsed = False
            self.used = False

        #moves the Weapon sprite with the player and updates weapon image
        if self.player.itemUsed and self.used:
            self.updateLocation()
            self.rect.x = self.x
            self.rect.y = self.y
        else:
            self.rect.x = -100
            self.rect.y = -100

    def updateLocation(self):
        if self.player.facing == 'up':
            self.x = self.player.x+TILESIZE//2
            self.y = self.player.y-TILESIZE//2
            self.image = pygame.transform.scale(self.imagelist[2], (self.width, self.height))

        elif self.player.facing == 'down':
            self.x = self.player.x
            self.y = self.player.y+TILESIZE//2
            self.image = pygame.transform.scale(self.imagelist[1], (self.width, self.height))

        elif self.player.facing == 'left':
            self.x = self.player.x-TILESIZE//3
            self.y = self.player.y+TILESIZE//2
            self.image = pygame.transform.scale(self.imagelist[3], (self.width, self.height))

        else:
            self.x = self.player.x+TILESIZE//1.5
            self.y = self.player.y+TILESIZE//2
            self.image = pygame.transform.scale(self.imagelist[0], (self.width, self.height))

    #MAX!!!
    #Author: Max Chiu 4/12/2024
    def calculateAngle(self):
        angle = random.uniform(-1*self.spread, self.spread)
        if self.player.facing == 'up':
            angle += 90
        elif self.player.facing == 'left':
            angle += 180
        elif self.player.facing == 'down':
            angle += 270
        angle = angle - 360 if angle >= 360 else angle
        return angle*math.pi/180
    
#Author: Max Chiu 4/10/24
class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, angle, range, damage, side):
        self.game = game
        self.clock = game.clock
        self.timepassed = 0
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE/1.5
        self.height = TILESIZE/1.5
        self.side = side
        if self.side == 'player':
            self.image = pygame.transform.scale(pygame.image.load('Sprites/items/bubble.png'), (self.width, self.height))
        else: #if it's an enemy bullet
            self.image = pygame.transform.scale(pygame.image.load('Sprites/items/bubbleStream7.png'), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = 6
        self.range = range
        self.damage = damage

        self.xIncrement = self.speed*math.cos(angle)
        self.yIncrement = -1*self.speed*math.sin(angle)


    #Author: Max Chiu 4/15/2024, 4/16/2024
    def update(self):
        self.range -= math.sqrt(self.xIncrement**2 + self.yIncrement**2)
        if self.range <= 0:
            self.kill()
        self.x += self.xIncrement
        self.y += self.yIncrement
        self.rect.x = self.x
        self.rect.y = self.y

        if self.side == 'player':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) + pygame.sprite.spritecollide(self, self.game.npcs, False)
            if hits:
                self.timepassed += self.clock.get_time()
            if self.timepassed > 50:
                self.kill()
                self.timepassed = 0

        if self.side == 'player':
            enemyIndex = self.rect.collidelist(list(enemy.rect for enemy in self.game.enemies))
            if enemyIndex != -1:
                self.timepassed += self.clock.get_time()

                if self.timepassed > 50:
                    self.game.enemies.get_sprite(enemyIndex).dealtDamage(self.damage, 'bubble')
                    self.kill()
                    self.timepassed = 0
        else:
            playerHit = pygame.Rect.colliderect(self.rect, self.game.player.rect)
            if playerHit:
                self.timepassed += self.clock.get_time()

                if self.timepassed > 50:
                    self.game.player.getDamage(self.damage)
                    self.kill()
                    self.timepassed = 0


            

class MeleeAttack(pygame.sprite.Sprite):
    # This code was written by Eddie Suber (the MeleeAttack class), written with the help and inspiration of:
    # https://www.youtube.com/watch?v=mFPfNHbsWYw
    # https://www.dropbox.com/s/tdjzeuhsc6twuyu/AdventureGame(with_exe)(Ver.1).zip?dl=0&e=1&file_subpath=%2FAdventure+Game%2Fitems.py

    # This class is intended to handle the sprite for a melee weapon when attacking using those
    # As well as the hitbox associated with that attack

    # For a swinging weapon, the weapon sprite should move across the arc and the hitbox should follow accordingly

    # For a stabbing / poking weapon, the weapon sprite and hitbox could just come out and be static for the duration of the attack
    # With the hitbox fading away a bit sooner than the visual sprite

    # As a resource, I'm currently using https://www.dropbox.com/s/tdjzeuhsc6twuyu/AdventureGame(with_exe)(Ver.1).zip?dl=0&e=1&file_subpath=%2FAdventure+Game%2Fitems.py
    # And https://www.youtube.com/watch?v=mFPfNHbsWYw (The dropbox is the files for the game in the video)
    # weapon is the specific weapon being used, while facing is the direction the character is facing
    def __init__(self, game, weapon, player):
        self.weapon = weapon
        self.game = game
        self.clock = game.clock
        self._layer = PLAYER_LAYER
        self.player = player
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        #self.image = pygame.transform.scale(pygame.image.load(swordfish_imgs[0]), (TILESIZE//1.5, TILESIZE//1.5))

        self.x = self.player.x
        self.y = self.player.y

        if self.player.weapon.type == 'trident':
            self.width = TILESIZE // 1.2
            self.height = TILESIZE // 1.2
        else:
            self.width = TILESIZE // 1.2
            self.height = TILESIZE // 1.2

        self.image = pygame.surface.Surface([self.width, self.height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        # Starting the weapon rectangles offscreen, just for fun, but also because they did it in the tutorial
        self.rect.x = -2000
        self.rect.y = -2000
        # The variable for the actual hitbox of the attack
        self.hitbox = pygame.surface.Surface((self.width, self.width))
        self.animationCount = 0
        self.animationPhase = 0



        pass

    # For when attacking while facing upward
    def facingUp(self):
        if self.player.weapon.type == 'swordfish':
            self.x = self.player.x + TILESIZE // 1.4
            self.y = self.player.y - TILESIZE + 8
            self.rect.x = self.player.rect.x
            self.rect.y = self.player.rect.y - TILESIZE + 8
            #print(self.animationCount // (self.player.weaponAnimationSpeed // 3) % 3)

            if self.animationPhase == 1:
                self.x = self.player.x + (TILESIZE // 1.4)
                self.rect.x = self.player.rect.x + (TILESIZE // 1.4)
                # self.hitbox = (self.rect.x + TILESIZE//1.5, self.rect.y + TILESIZE // 2, TILESIZE//2, TILESIZE//2)
            elif self.animationPhase == 2:
                self.x = self.player.x + (TILESIZE // 1.4) - self.height
                self.rect.x = self.player.rect.x + (TILESIZE // 1.4) - self.height
                # self.hitbox = (self.rect.x - TILESIZE//4, self.rect.y, TILESIZE * 1.5, TILESIZE * 2)
            elif self.animationPhase == 3:
                self.x = self.player.x + (TILESIZE // 1.4) - self.height * 2
                self.rect.x = self.player.rect.x + (TILESIZE // 1.4) - self.height * 2
                # self.hitbox = (self.rect.x, self.rect.y + TILESIZE//2, TILESIZE//2, TILESIZE//2)
        elif self.player.weapon.type == 'trident':
            self.height = TILESIZE // 0.6
            self.x = self.player.x + self.width // 7
            self.rect.x = self.player.rect.x + self.width // 7
            if self.animationPhase == 1:
                self.y = self.player.y - (self.height * 1.5)
                self.rect.y = self.player.rect.y - (self.height * 1.5)
                # self.hitbox = (self.rect.x, self.rect.y + TILESIZE // 2,(self.width, self.height))
            elif self.animationPhase == 2:
                self.y = self.player.y - (self.height * 2)
                self.rect.y = self.player.rect.y - (self.height * 2)
                # self.hitbox = (self.rect.x - TILESIZE//4, self.rect.y, TILESIZE * 1.5, TILESIZE * 2)
            elif self.animationPhase == 3:
                self.y = self.player.y - (self.height * 2.5)
                self.rect.y = self.player.rect.y - (self.height * 2.5)
                # self.hitbox = (self.rect.x, self.rect.y + TILESIZE//2, TILESIZE//2, TILESIZE//2)
            if self.checkWalls():
                print("wall blocking")
                self.endAttack()



    # For when attacking while facing downward
    def facingDown(self):
        if self.player.weapon.type == 'swordfish':
            self.x = self.player.x + (TILESIZE // 1.4) - self.width * 2
            self.y = self.player.y + TILESIZE - 8
            self.rect.x = self.player.rect.x
            self.rect.y = self.player.rect.y + TILESIZE - 8
            # print(self.animationCount // (self.player.weaponAnimationSpeed // 3) % 3)

            if self.animationPhase == 1:
                self.x = self.player.x + (TILESIZE // 1.4) - self.width * 2
                self.rect.x = self.player.rect.x + (TILESIZE // 1.4) - self.width * 2
                # self.hitbox = (self.rect.x + TILESIZE//1.5, self.rect.y + TILESIZE // 2, TILESIZE//2, TILESIZE//2)
            elif self.animationPhase == 2:
                self.x = self.player.x + (TILESIZE // 1.4) - self.width
                self.rect.x = self.player.rect.x + (TILESIZE // 1.4) - self.width
                # self.hitbox = (self.rect.x - TILESIZE//4, self.rect.y, TILESIZE * 1.5, TILESIZE * 2)
            elif self.animationPhase == 3:
                self.x = self.player.x + (TILESIZE // 1.4)
                self.rect.x = self.player.rect.x + (TILESIZE // 1.4)
                # self.hitbox = (self.rect.x, self.rect.y + TILESIZE//2, TILESIZE//2, TILESIZE//2)
        elif self.player.weapon.type == 'trident':
            self.height = TILESIZE // 0.6
            self.x = self.player.x + self.width // 7
            self.rect.x = self.player.rect.x + self.width // 7
            if self.animationPhase == 1:
                self.y = self.player.y + (self.height * 1.5)
                self.rect.y = self.player.rect.y + (self.height * 1.5)
                # self.hitbox = (self.rect.x, self.rect.y + self.height, self.width, self.height)
            elif self.animationPhase == 2:
                self.y = self.player.y + (self.height * 2)
                self.rect.y = self.player.rect.y + (self.height * 2)
                # self.hitbox = (self.rect.x, self.rect.y + self.height, self.width, self.height)
            elif self.animationPhase == 3:
                self.y = self.player.y + (self.height * 2.5)
                self.rect.y = self.player.rect.y + (self.height * 2.5)
                # self.hitbox = (self.rect.x, self.rect.y + self.height, self.width, self.height)
            if self.checkWalls():
                print("wall blocking")
                self.endAttack()

    # For when attacking while facing left
    def facingLeft(self):
        if self.player.weapon.type == 'swordfish':
            self.x = self.player.x - (TILESIZE // 1.2)
            self.y = self.player.y + TILESIZE - 8
            self.rect.x = self.player.rect.x - (TILESIZE // 1.2)
            self.rect.y = self.player.rect.y + TILESIZE - 8
            # print(self.animationCount // (self.player.weaponAnimationSpeed // 3) % 3)

            if self.animationPhase == 1:
                self.y = self.player.y + (TILESIZE // 1.4) - self.height * 2
                self.rect.y = self.player.rect.y + (TILESIZE // 1.4) - self.height * 2
                self.hitbox = (self.rect.x + TILESIZE//1.5, self.rect.y + TILESIZE // 2, TILESIZE//2, TILESIZE//2)
            elif self.animationPhase == 2:
                self.y = self.player.y + (TILESIZE // 1.4) - self.height
                self.rect.y = self.player.rect.y + (TILESIZE // 1.4) - self.height
                self.hitbox = (self.rect.x - TILESIZE//4, self.rect.y, TILESIZE * 1.5, TILESIZE * 2)
            elif self.animationPhase == 3:
                self.y = self.player.y + (TILESIZE // 1.4)
                self.rect.y = self.player.rect.y + (TILESIZE // 1.4)
                self.hitbox = (self.rect.x, self.rect.y + TILESIZE//2, TILESIZE//2, TILESIZE//2)
        elif self.player.weapon.type == 'trident':
            self.width = TILESIZE // 0.6
            self.y = self.player.y + self.height // 7
            self.rect.y = self.player.rect.y + self.height // 7
            if self.animationPhase == 1:
                self.x = self.player.x - (self.width * 1.5)
                self.rect.x = self.player.rect.x - (self.width * 1.5)
                self.hitbox = (self.rect.x, self.rect.y, self.width, self.height)
            elif self.animationPhase == 2:
                self.x = self.player.x - (self.width * 2)
                self.rect.x = self.player.rect.x - (self.width * 2)
                self.hitbox = (self.rect.x, self.rect.y, self.width, self.height)
            elif self.animationPhase == 3:
                self.x = self.player.x - (self.width * 2.5)
                self.rect.x = self.player.rect.x - (self.width * 2.5)
                self.hitbox = (self.rect.x, self.rect.y, self.width, self.height)
            if self.checkWalls():
                print("wall blocking")
                self.endAttack()

    # For when attacking while facing right
    def facingRight(self):
        if self.player.weapon.type == 'swordfish':
            self.x = self.player.x + (TILESIZE * 1.2)
            self.y = self.player.y + TILESIZE - 8
            self.rect.x = self.player.rect.x + (TILESIZE * 1.2)
            self.rect.y = self.player.rect.y + TILESIZE - 8
            # print(self.animationCount // (self.player.weaponAnimationSpeed // 3) % 3)

            if self.animationPhase == 1:
                self.y = self.player.y + (TILESIZE // 1.4)
                self.rect.y = self.player.rect.y + (TILESIZE // 1.4)
                self.hitbox = (self.rect.x + TILESIZE//1.5, self.rect.y + TILESIZE // 2, TILESIZE//2, TILESIZE//2)
            elif self.animationPhase == 2:
                self.y = self.player.y + (TILESIZE // 1.4) - self.height
                self.rect.y = self.player.rect.y + (TILESIZE // 1.4) - self.height
                self.hitbox = (self.rect.x - TILESIZE//4, self.rect.y, TILESIZE * 1.5, TILESIZE * 2)
            elif self.animationPhase == 3:
                self.y = self.player.y + (TILESIZE // 1.4) - self.height * 2
                self.rect.y = self.player.rect.y + (TILESIZE // 1.4) - self.height * 2
                self.hitbox = (self.rect.x, self.rect.y + TILESIZE//2, TILESIZE//2, TILESIZE//2)
        elif self.player.weapon.type == 'trident':
            self.width = TILESIZE // 0.6
            self.y = self.player.y + self.height // 7
            self.rect.y = self.player.rect.y + self.height // 7
            if self.animationPhase == 1:
                self.x = self.player.x + (self.width)
                self.rect.x = self.player.rect.x + (self.width)
                self.hitbox = (self.rect.x + self.width, self.rect.y, self.width, self.height)
            elif self.animationPhase == 2:
                self.x = self.player.x + (self.width * 1.5)
                self.rect.x = self.player.rect.x + (self.width * 1.5)
                self.hitbox = (self.rect.x + self.width, self.rect.y, self.width, self.height)
            elif self.animationPhase == 3:
                self.x = self.player.x + (self.width * 2)
                self.rect.x = self.player.rect.x + (self.width * 2)
                self.hitbox = (self.rect.x + self.width, self.rect.y, self.width, self.height)
            pass
            if self.checkWalls():
                print("wall blocking")
                self.endAttack()

    def animate(self):
        # This function is intended to handle switching the weapon's sprite based on which direction the player is facing
        # , which weapon the player has currently equipped, and what part of the attack animation is happening
        # This could be done using self.player.facing, self.weaponAnimationSpeed, and self.animationCount

        if self.player.weapon.type == 'swordfish':
            if self.player.facing == 'up':
                if self.animationPhase == 1:
                    self.image = pygame.transform.scale(swordfish_imgs[2], (self.width, self.height))
                elif self.animationPhase == 2:
                    self.image = pygame.transform.scale(swordfish_imgs[1], (self.width, self.height))
                elif self.animationPhase == 3:
                    self.image = pygame.transform.scale(swordfish_imgs[0], (self.width, self.height))
            if self.player.facing == 'down':
                if self.animationPhase == 1:
                    self.image = pygame.transform.scale(swordfish_imgs[3], (self.width, self.height))
                elif self.animationPhase == 2:
                    self.image = pygame.transform.scale(swordfish_imgs[4], (self.width, self.height))
                elif self.animationPhase == 3:
                    self.image = pygame.transform.scale(swordfish_imgs[5], (self.width, self.height))
            if self.player.facing == 'left':
                if self.animationPhase == 1:
                    self.image = pygame.transform.scale(swordfish_imgs[6], (self.width,  self.height))
                elif self.animationPhase == 2:
                    self.image = pygame.transform.scale(swordfish_imgs[7], (self.width, self.height))
                elif self.animationPhase == 3:
                    self.image = pygame.transform.scale(swordfish_imgs[8], (self.width, self.height))
            if self.player.facing == 'right':
                if self.animationPhase == 1:
                    self.image = pygame.transform.scale(swordfish_imgs[9], (self.width, self.height))
                elif self.animationPhase == 2:
                    self.image = pygame.transform.scale(swordfish_imgs[10], (self.width, self.height))
                elif self.animationPhase == 3:
                    self.image = pygame.transform.scale(swordfish_imgs[11], (self.width, self.height))

        elif self.player.weapon.type == 'trident':
            # To be edited, replace the swordfish images with the trident images
            if self.player.facing == 'up':
                self.image = pygame.transform.scale(trident_imgs[0], (self.width, self.height))

            if self.player.facing == 'down':

                self.image = pygame.transform.scale(trident_imgs[1], (self.width, self.height))

            if self.player.facing == 'left':
                self.image = pygame.transform.scale(trident_imgs[2], (self.width,  self.height))

            if self.player.facing == 'right':

                self.image = pygame.transform.scale(trident_imgs[3], (self.width, self.height))
            pass

    def checkWalls(self):
        # creates lines
        lines = []
        # attack instance x and y positional values
        ax = self.x + self.width / 2
        ay = self.y + self.height / 2
        px = self.game.player.x + self.game.player.width / 2
        py = self.game.player.y + self.game.player.height / 2
        n = 4
        dx = (ax - px) / n
        dy = (ay - py) / n
        surface = pygame.Surface(self.game.screen.get_size(), pygame.SRCALPHA)
        for i in range(n):
            lines.append(pygame.draw.line(surface, (0, 255, 0, 1), (px + dx * i, py + dy * i),
                                          (px + dx * (i + 1), py + dy * (i + 1)), 1))
        index = [line.collidelist(list(block.rect for block in self.game.blocks)) for line in lines]
        wallBlocking = False
        for i in index:
            if i != -1:
                print(i)
                rect = self.game.blocks.get_sprite(i)
                # rect.image.fill(BLUE)
                wallBlocking = True
        return wallBlocking

    def collide(self):
        # This function is intended to check for collisions between the attack instance and any enemies on the screen
        # This could be done in a variety of ways, like making a list of every enemy object (the Enemy class) and using
        # pygame.sprite.collide_rect() to check to see if any enemies have been hit, then decreasing their health appropriately if hit
        betweenBlocks = False


        for enemy in self.game.enemies:
            if pygame.sprite.collide_rect(self, enemy):
                if not enemy.hitInvincible and not betweenBlocks:
                    if not self.checkWalls():
                        #print("colliding")
                        #print(f"Self damage is {self.weapon.damage}")
                        enemy.dealtDamage(self.weapon.damage, self.player.weapon.type)
                        #self.player.getHealth(self.weapon.damage * 0.8)
                        enemy.hitInvincible = True
                        #print(enemy.hitInvincible)
                        #print(f"enemy health is {enemy.health}")
            else:
                #print("not colliding")
                enemy.hitInvincible = False

        pass

    def endAttack(self):
        self.animationCount = 0
        self.player.itemUsed = False
        self.player.swordUsed = False
        self.kill()

    #EDDIE!!!
    def update(self):

        if self.player.itemUsed:
            self.animationCount += 1
            if self.animationCount >= self.player.weaponAnimationSpeed:
                self.endAttack()
            if self.player.weapon.type == 'swordfish':
                if self.animationCount < (self.player.weaponAnimationSpeed // 3):
                    self.animationPhase = 1
                elif self.animationCount < (self.player.weaponAnimationSpeed // 3 * 2):
                    self.animationPhase = 2
                elif self.animationCount < (self.player.weaponAnimationSpeed):
                    self.animationPhase = 3
            else:
                if self.animationCount < (self.player.weaponAnimationSpeed * 1.3 // 3):
                    self.animationPhase = 1
                elif self.animationCount < (self.player.weaponAnimationSpeed * 1.3 // 3 * 2):
                    self.animationPhase = 2
                elif self.animationCount < (self.player.weaponAnimationSpeed * 1.3):
                    self.animationPhase = 3

            if self.player.facing == 'up':
                self.facingUp()
            elif self.player.facing == 'left':
                self.facingLeft()
            elif self.player.facing == 'right':
                self.facingRight()
            else:
                self.facingDown()

            self.player.attack(self)
        else:
            self.rect.x = -2000
            self.rect.y = -2000
            self.hitbox = (self.rect.x, self.rect.y, self.width, self.height)
            self.kill()

        if self.animationCount == 0:

            if self.player.weapon.type == 'trident':
                pygame.mixer.Channel(1).set_volume(0.03 * self.game.soundVol)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/movement-swipe-whoosh-3-186577.mp3'))
            else:
                pygame.mixer.Channel(1).set_volume(0.055 * self.game.soundVol)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/sword_swipe.wav'))
        self.animate()
        self.collide()

        # Uncomment the lines below to see the attack's hitbox as a transparent blue rectangle
        # hitbox = pygame.surface.Surface([self.width, self.height])
        # hitbox.set_alpha(128)
        # hitbox.fill(GREEN)
        # self.game.screen.blit(hitbox, (self.rect.x, self.rect.y))
        # pygame.display.update()

        # Could add sounds effects for using a melee attack in this method, or within the Player class attack() method
        # So that the proper sound would play whenever the attack is used

    pass


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
        self.name = 'flower'

        #READ ME, EDIT ALL OF THE FLOWER SPRITES TO NOT INCLUDE THE CUTTING SHEARS
        #THIS WILL LIKELY IMPROVE ANIMATION FLUIDITY WHEN FLOWERS ARE INTERACTED WITH
        #WILL ALSO REMOVE DUPLICATE SHEARS WITH THE PLAYER CUTTING ANIMATION



        self.imageList = [[self.game.hyacinImgL[0], self.game.hyacinImgL], [self.game.sunFloImgL[0], self.game.sunFloImgL], [self.game.silentFImgL[0], self.game.silentFImgL]]
        #Randomly selects the flower to spawn as one of the flower options:
        #either a hyacinth, sunflower, or silent princess flower
        self.flowerSpriteNum = random.randint(0, len(self.imageList)-1)
        self.image = self.imageList[self.flowerSpriteNum][0]


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.timepassed += self.clock.get_time() / 1000
        if self.game.state == 'flowerC':
            if self.state == 'cutting':
                #READ ME, THIS UPDATES ALL THE FLOWERS AT ONCE AFTER INTERACTING WITH ONLY ONE FLOWER. - UNINTENDED OUTCOME, NEEDS FIXING
                self.anim()
                self.image = self.imageList[self.flowerSpriteNum][1][self.imgindex % 3]

    def anim(self):
        #realized it was setting the state to flowerC every single loop from the Player.interact() method, so it never went to the else to kill
        #moved it in front to make sure it switched states when the imgindex got to 4
        if self.imgindex > 2:
            self.game.state = 'explore'
        if self.game.state == 'flowerC':
            if ((self.timepassed) // (0.31) % 3 == self.imgindex):
                self.imgindex = (self.imgindex + 1)
                pygame.mixer.Channel(3).set_volume(0.05 * self.game.soundVol)
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_Battle_SFX/22_Slash_04.wav'))

        else:
            if self.state == 'cutting':
                self.kill()
                self.game.inventory.add_item('flower')
                print(self.game.inventory.slots)
                pygame.mixer.Channel(3).set_volume(0.01 * self.game.soundVol)
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('Music/sound_effects/mixkit_game_treasure_coin.wav'))

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
        self.name = 'ore'




        self.imageList = [[self.game.rubyImageL[0], self.game.rubyImageL], [self.game.emeraldImageL[0], self.game.emeraldImageL], [self.game.copperImageL[0], self.game.copperImageL], [self.game.amethImageL[0], self.game.amethImageL], [self.game.ironImageL[0], self.game.ironImageL]]
        self.oreSpriteNum = random.randint(0, len(self.imageList) - 1)

        self.image = self.imageList[self.oreSpriteNum][0]
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
                self.image = self.imageList[self.oreSpriteNum][1][self.imgindex % 4]


        pass

    def killAnim(self):
        if self.imgindex > 2:
            self.game.state = 'explore'
        if self.game.state == 'oreMine':
            if ((self.timepassed) // (0.31) % 4 == self.imgindex):
                self.imgindex = (self.imgindex + 1)
                pygame.mixer.Channel(3).set_volume(0.05 * self.game.soundVol)
                pygame.mixer.Channel(3).play(
                pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_Battle_SFX/08_Bite_04.wav'))

        else:
            if self.state == 'mining':
                self.kill()
                self.game.inventory.add_item('ore')
                print(self.game.inventory.slots)
                pygame.mixer.Channel(3).set_volume(0.01 * self.game.soundVol)
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('Music/sound_effects/mixkit_game_treasure_coin.wav'))
        pass

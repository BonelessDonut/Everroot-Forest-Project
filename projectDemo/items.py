import random, math
from sprites import *
import pygame


# Assuming one melee and multiple ranged weapons
# type - weapon name: currently presumably some variation of sword and bubble gun (shotgun)
class Weapon():
    def __init__(self, game, type, player):
        self.game = game
        self.player = player
        self.type = type
        # timer used to count the time between attacks
        self.timer = 0
        self.spread = None
        self.damage = None
        self.pause = None
        self.range = None
        self.reloadTime = None
        self.ammo = None

        if type == 'bubble':
            # 45 degrees spread of bubble bullets
            self.spread = 45
            self.damage = 10
            self.ammo = 12
            # how long to pause between each bullet
            self.pause = 1
            self.range = 2 * TILESIZE
            # how long to reload ammo
            self.reloadTime = 2
        # melee
        else:
            # 75 degrees spread of melee swing
            #self.spread = 75
            self.damage = 25
            self.pause = 0.4

    def attack(self):
        print("Attacking")
        if self.timer == 0:
            print("Through the first if")
            if self.type == 'bubble':
                print("Through the second if")
                angle = random.uniform(-1 * self.spread, self.spread)
                if self.player.facing == 'up':
                    angle += 90
                elif self.player.facing == 'left':
                    angle += 180
                elif self.player.facing == 'down':
                    angle += 270
                angle = angle - 360 if angle >= 360 else angle
                Bullet(self.game, self.player.x, self.player.y, angle)
            else:
                # This section is for handling attacking with melee weapons
                pass

        else:
            return False

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, angle):
        self.game = game
        self.clock = game.clock
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.timepassed = 0
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE//4
        self.height = TILESIZE//4
        self.image = pygame.transform.scale(pygame.image.load('Sprites/items/bubble.png'), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = 6

        self.xIncrement = self.speed*math.cos(angle)
        self.yIncrement = self.speed*math.sin(angle)


    def update(self):
        self.timepassed += self.clock.get_time() / 1000
        self.x += self.xIncrement
        self.y += self.yIncrement

class MeleeSprite(pygame.sprite.Sprite):
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
        self._layer = BLOCK_LAYER
        self.timepassed = 0
        self.player = player
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.transform.scale(pygame.image.load(swordfish_imgs[0]), TILESIZE//2, TILESIZE//2)
        self.rect = self.image.get_rect()
        self.x = self.player.x
        self.y = self.player.y
        # Starting the weapon rectangles offscreen, just for fun, but also because they did it in the tutorial
        self.rect.x = -2000
        self.rect.y = -2000
        # The variable for the actual hitbox of the attack
        self.hitbox = (self.rect.x, self.rect.y, TILESIZE, TILESIZE)
        self.imgindex = 0

        pass

    # For when attacking while facing upward
    def facingUp(self):
        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y + 8

        if self.imgindex % 3 == 0:
            self.rect.x = self.player.rect.x - TILESIZE // 2
            self.hitbox = (self.rect.x + TILESIZE//2, self.rect.y + TILESIZE // 2, TILESIZE//2, TILESIZE//2)
        elif self.imgindex % 3 == 1:
            self.rect.x = self.player.rect.x
            self.hitbox = (self.rect.x - TILESIZE//4, self.rect.y, TILESIZE * 1.5, TILESIZE * 2)
        elif self.imgindex % 3 == 2:
            self.rect.x = self.player.rect.x + TILESIZE // 2
            self.hitbox = (self.rect.x, self.rect.y + TILESIZE//2, TILESIZE//2, TILESIZE//2)


    # For when attacking while facing downward
    def facingDown(self):
        pass

    # For when attacking while facing left
    def facingLeft(self):
        pass

    # For when attacking while facing right
    def facingRight(self):
        pass

    def update(self):
        if self.player.itemUsed:
            self.timepassed += self.clock.get_time() / 1000
            self.imgindex = (self.imgindex + 1) if ((self.timepassed) // (0.31) % 3 == self.imgindex) else self.imgindex

            if self.player.facing == 'up':
                self.facingUp()
            elif self.player.facing == 'left':
                self.facingLeft()
            elif self.player.facing == 'right':
                self.facingRight()
            else:
                self.facingDown()

        else:
            self.rect.x = -2000
            self.rect.y = -2000
            self.hitbox = (self.rect.x, self.rect.y, TILESIZE, TILESIZE)

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

        #READ ME, EDIT ALL OF THE FLOWER SPRITES TO NOT INCLUDE THE CUTTING SHEARS
        #THIS WILL LIKELY IMPROVE ANIMATION FLUIDITY WHEN FLOWERS ARE INTERACTED WITH
        #WILL ALSO REMOVE DUPLICATE SHEARS WITH THE PLAYER CUTTING ANIMATION

        hyacinImgL = ['Sprites/items/hyacinth.png', 'Sprites/items/hyacinth3New.png', 'Sprites/items/hyacinth5.png']
        sunFloImgL = ['Sprites/items/sunflowernew.png', 'Sprites/items/sunflower3New.png', 'Sprites/items/sunflower5.png']
        silentFImgL = ['Sprites/items/silentFlower.png', 'Sprites/items/silentFlower3New.png', 'Sprites/items/silentFlower5.png']

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
                self.image = pygame.transform.scale(pygame.image.load(self.imageList[self.flowerSpriteNum][1][self.imgindex % 3]), (self.width, self.height))

    def anim(self):
        #realized it was setting the state to flowerC every single loop from the Player.interact() method, so it never went to the else to kill
        #moved it in front to make sure it switched states when the imgindex got to 4
        if self.imgindex > 2:
            self.game.state = 'explore'
        if self.game.state == 'flowerC':
            self.imgindex = (self.imgindex + 1) if ((self.timepassed) // (0.31) % 3 == self.imgindex) else self.imgindex

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

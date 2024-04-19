import pygame, sys
import settings
from items import *
from sprites import *
from pygame import mixer
from pygame.locals import(
    K_w,
    K_s,
    K_a,
    K_d,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_RETURN,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

class Game():
    def __init__(self):
        mixer.init()
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock() 

        self.player = None
        self.state = 'explore'
        #Game states:
        #explore - Player can move around
        #dialogue - Player is currently in dialogue, player can't move
        #flowerC - flower animation is playing, player can't move

        self.map = [-1, -1]
        
        self.running = True
    
    #written by Rachel Tang 4/19/24
    def play_music(self, songType):
        if songType == 'dialogue':
            mixer.music.load('Music/CI103_-_normal_dialogue_background.mp3')
            mixer.music.set_volume(0.3)
            mixer.music.play()
        if songType == 'stop':
            mixer.music.stop()


    def createTilemap(self, prevPosition):
        #Only for initial map creation
        # -1, -1 is the convention to make known that the map doesnt currently exist
        if self.map == [-1, -1]:
            for row in range(len(settings.currentTilemap[0])):
                #print(f"{row} ", end="")   
                for col in range(len(settings.currentTilemap[0][row])):
                    if (settings.currentTilemap[0][row])[col] == "B":
                        Block(self, col, row)
                    elif (settings.currentTilemap[0][row])[col] == "P":
                        self.player = Player(self, col, row, self.clock)
                    elif (settings.currentTilemap[0][row])[col] == "F":
                        Flower(self, col, row, self.clock)
                    elif (settings.currentTilemap[0][row])[col] == 'O':
                        Ore(self, col, row, self.clock)
                    elif (settings.currentTilemap[0][row])[col] == 'N':
                        NPC(self, col, row)
                    elif (settings.currentTilemap[0][row])[col] == 'E':
                        Enemy(self, col, row)
                    elif (settings.currentTilemap[0][row])[col] == 'T':
                        Teleport(self, col, row)
                    #print(f"{col}", end="")
                #print()
            # 1, 1 : the map now exists from the list in settings.py
            self.map = [1, 1]
        #For moving between rooms
        else:
            # kill all the current sprites in the current room
            self.all_sprites.empty()
            self.blocks.empty()
            self.ground.empty()
            self.flowers.empty()
            self.ores.empty()
            self.npcs.empty()
            self.teleport.empty()
            self.enemies.empty()


            # This is a variable to allow the weapon that was equipped in the current room to stay equipped
            # Otherwise it would reset to the default weapon everytime the player changes rooms
            priorWeapon = self.player.weapon.type

            # figures out which preloaded map to move the player to. 
            # looks at the direction the player moves in and moves to the appropriate map tile
            if prevPosition[0] == 31:
                mapNumber = mapList[self.map[0]][self.map[1]+1] 
                self.map[1] += 1
            elif prevPosition[0] == 0:
                mapNumber = mapList[self.map[0]][self.map[1]-1] 
                self.map[1] -= 1
            elif prevPosition[1] == 17:
                mapNumber = mapList[self.map[0]+1][self.map[1]] 
                self.map[0] += 1
            elif prevPosition[1] == 0:
                mapNumber = mapList[self.map[0]-1][self.map[1]] 
                self.map[0] -= 1
            
            for row in range(len(settings.currentTilemap[mapNumber])):
                #print(f"{row} ", end="")
                for col in range(len(settings.currentTilemap[mapNumber][row])):
                    # looks at the premade room in settings.py, if a tile is on the map, print the corresponding sprite on the new map
                    if (settings.currentTilemap[mapNumber][row])[col] == "B":
                        Block(self, col, row)
                    elif (settings.currentTilemap[mapNumber][row])[col] == "F":
                        Flower(self, col, row, self.clock)
                    elif (settings.currentTilemap[mapNumber][row])[col] == 'O':
                        Ore(self, col, row, self.clock)
                    elif (settings.currentTilemap[mapNumber][row])[col] == 'N':
                        NPC(self, col, row)
                    elif (settings.currentTilemap[mapNumber][row])[col] == 'E':
                        Enemy(self, col, row)
                    elif (settings.currentTilemap[mapNumber][row])[col] == 'T':
                        # teleports the player's position on the screen when they move rooms
                        Teleport(self, col, row)
                        if prevPosition[0] == 0 and col == 31 and prevPosition[1] == row:
                            self.player = Player(self, col-1, row, self.clock)
                        elif prevPosition[0] == 31 and col == 0 and prevPosition[1] == row:
                            self.player = Player(self, col+1, row, self.clock)
                        elif prevPosition[1] == 0 and row == 17 and prevPosition[0] == col:
                            self.player = Player(self, col, row-1, self.clock)
                        elif prevPosition[1] == 17 and row == 0 and prevPosition[0] == col:
                            self.player = Player(self, col, row+1, self.clock)
                        self.player.weapon.type = priorWeapon

    def new(self):

        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.ground = pygame.sprite.LayeredUpdates()
        self.flowers = pygame.sprite.LayeredUpdates()
        self.ores = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.teleport = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.weapons = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.bullets = pygame.sprite.LayeredUpdates()
        self.createTilemap(None)
        #self.player = Player(self, 1, 2)
    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing == False
                self.running == False
                pygame.font.quit()
                pygame.quit()
                sys.exit()
            # Use E to attack using a melee weapon
            if event.type == pygame.KEYUP and (event.key == pygame.K_e and not self.player.itemUsed) and ((self.player.weapon.type == 'swordfish' or self.player.weapon.type == 'hammershark') and self.state == 'explore'):
                self.player.itemUsed = True
                if False: # This line is a placeholder for a conditional that will check if the melee weapon type is the spear weapon or swordfish
                    pass
                elif self.player.weapon.type == 'swordfish':
                    self.player.swordUsed = True
                elif self.player.weapon.type == 'hammershark':
                    self.player.spearUsed = True
                MeleeAttack(self, self.player.weapon, self.player)
            # Q is used to switch weapons for the player
            if event.type == pygame.KEYUP and event.key == pygame.K_q:
                self.player.switchWeapons()

    def update(self):
        #game loop updates
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        #Play the game over screen
        #To be created later
        pass

    def intro_screen(self):
        #Play the intro screen
        #To be created later
        pass




g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()

import pygame, sys, random
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
    #used this website: https://www.educative.io/answers/how-to-play-an-audio-file-in-pygame
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
            for row in range(len(settings.currentTileMap[0])):
                #print(f"{row} ", end="")   
                for col in range(len(settings.currentTileMap[0][row])):
                    if (settings.currentTileMap[0][row])[col] == "B":
                        Block(self, col, row)
                    elif (settings.currentTileMap[0][row])[col] == "P":
                        self.player = Player(self, col, row, self.clock)
                    elif (settings.currentTileMap[0][row])[col] == "F":
                        Flower(self, col, row, self.clock)
                    elif (settings.currentTileMap[0][row])[col] == 'O':
                        Ore(self, col, row, self.clock)
                    elif (settings.currentTileMap[0][row])[col] == 'N':
                        NPC(self, col, row)
                    elif (settings.currentTileMap[0][row])[col] == 'E':
                        Enemy(self, col, row)
                    elif (settings.currentTileMap[0][row])[col] == 'T':
                        Teleport(self, col, row)
                    #print(f"{col}", end="")
                #print()
            # 1, 1 : the map now exists from the list in settings.py
            self.map = [2, 1]
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

            # if the room is unloaded and listed as -2, a randomly assigned purple enemy room will be loaded and added to the map list
            if mapNumber == -2:
                purpleRandomRoomIndex = random.randint(0, len(purpleRandomRooms)-1)
                randomPurpleMap = purpleRandomRooms[purpleRandomRoomIndex]
                currentTileMap.append(randomPurpleMap)
                mapNumber = len(currentTileMap)-1
                mapList[self.map[0]][self.map[1]] = mapNumber
            # if the room is unloaded and listed as -3, a randomly assigned green npc room will be loaded and added to the map list
            elif mapNumber == -3:
                #greenRandomRoomIndex = random.randint(0, len(greenRandomRooms)-1)
                #randomGreenMap = greenRandomRooms[greenRandomRoomIndex]
                randomGreenMap = template
                currentTileMap.append(randomGreenMap)
                mapNumber = len(currentTileMap)-1
                mapList[self.map[0]][self.map[1]] = mapNumber
            # if the room is unloaded and listed as -4, the red boss room will be loaded and added to the map list
            elif mapNumber == -4:
                redMap = redRoom
                currentTileMap.append(redMap)
                mapNumber = len(currentTileMap)-1
                mapList[self.map[0]][self.map[1]] = mapNumber
            
            # print(self.map[1]-1)
            # print(mapList[self.map[0]][self.map[1]-1])

            # create doors in a new room if it is meant to exist
            # going up
            if self.map[0]-1 >= 0 and mapList[self.map[0]-1][self.map[1]] != -1:
                # the top row of a map
                row = currentTileMap[mapNumber][0]
                row = row[0:15] + 'TT' + row[17:]
                currentTileMap[mapNumber][0] = row
            #down
            if self.map[0]+1 <= 5 and mapList[self.map[0]+1][self.map[1]] != -1:
                row = currentTileMap[mapNumber][17]
                row = row[0:15] + 'TT' + row[17:]
                currentTileMap[mapNumber][17] = row
            # left
            if self.map[1]-1 >= 0 and mapList[self.map[0]][self.map[1]-1] != -1:
                # each row needs to be edited individually => row1 and row2
                row1 = currentTileMap[mapNumber][8]
                row1 = 'T' + row1[1:]
                row2 = currentTileMap[mapNumber][9]
                row2 = 'T' + row2[1:]
                currentTileMap[mapNumber][8] = row1
                currentTileMap[mapNumber][9] = row2
                # print('row 1:', row1)
                # print('row 2:', row2)
            # right
            if self.map[1]+1 <= 12 and mapList[self.map[0]][self.map[1]+1] != -1:
                row1 = currentTileMap[mapNumber][8]
                row1 = row1[:-1] + 'T'
                row2 = currentTileMap[mapNumber][9]
                row2 = row2[:-1] + 'T'
                currentTileMap[mapNumber][8] = row1
                currentTileMap[mapNumber][9] = row2
                
            # print(self.map, mapNumber)
            # for i in mapList:
            #     print(i) 
            # print('Current Map:')
            # for i in currentTileMap[mapNumber]:
            #     print(i)

                     
            for row in range(len(settings.currentTileMap[mapNumber])):
                #print(f"{row} ", end="")
                for col in range(len(settings.currentTileMap[mapNumber][row])):
                    # looks at the premade room in settings.py, if a tile is on the map, print the corresponding sprite on the new map
                    if (settings.currentTileMap[mapNumber][row])[col] == "B":
                        Block(self, col, row)
                    elif (settings.currentTileMap[mapNumber][row])[col] == "F":
                        Flower(self, col, row, self.clock)
                    elif (settings.currentTileMap[mapNumber][row])[col] == 'O':
                        Ore(self, col, row, self.clock)
                    elif (settings.currentTileMap[mapNumber][row])[col] == 'N':
                        NPC(self, col, row)
                    elif (settings.currentTileMap[mapNumber][row])[col] == 'E':
                        Enemy(self, col, row)
                    elif (settings.currentTileMap[mapNumber][row])[col] == 'T':
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

        # print("mapList:", mapList)
        # print("currentTileMap:", currentTileMap)
    
    def addRoom(self, prevPosition):
        emptyRoom = []
        for row in range(18):
            emptyRow = ''
            for col in range(32):
                if prevPosition[0] == 0 and col == 31 and prevPosition[1] == row:
                    emptyRow += 'T'
                elif prevPosition[0] == 31 and col == 0 and prevPosition[1] == row:
                    emptyRow += 'T'
                elif prevPosition[1] == 0 and row == 17 and prevPosition[0] == col:
                    emptyRow += 'T'
                elif prevPosition[1] == 17 and row == 0 and prevPosition[0] == col:
                    emptyRow += 'T'
                elif row == 0 or row == 17 or col == 0 or col == 31:
                    emptyRow += 'B'
                else:
                    emptyRow += '.'
            emptyRoom.append(emptyRow)
        currentTileMap.append(emptyRoom)

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
                self.playing == Falsed
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

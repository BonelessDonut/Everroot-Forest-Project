import pygame, sys, random
import settings
import cutscenes
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
        pygame.mixer.pre_init(44100, -16, -1, 64)
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.renderSurface = pygame.Surface((WIDTH, HEIGHT))
        self.renderOffset = [0, 0]
        self.screenshake = 0

        # The title for the game window is randomly selected at the start, because why not? - Eddie Suber
        windowTitle = ['Everroot Forrest - A CS Story',
                       'Everroot Forest - Spelled Correctly This Time',
                       'Everroot Forest - Unending Torment',
                       'Everroot Forest - Tranquil Quest',
                       'Everrot Forest - The Rot Consumes',
                       'Everroot Forest - PLEASE COMMIT SOMETHING',
                       'Everroot Forest - Why Hello There',
                       'Everroot Forest - Pure Bliss',
                       'Everroot Forest - This Is The One', 
                       'Everroot Forest - SAVE BEFORE PULLING']
        titleNum = random.randint(0, len(windowTitle) - 1)
        pygame.display.set_caption(windowTitle[titleNum])
        self.clock = pygame.time.Clock() 

        self.player = None
        self.inventory = None
        self.weaponsHud = None
        self.state = 'menu'
        self.boss = None
        self.bossActive = False
        self.bossDefeated = False
        self.previousMapType = None
        self.currentMapType = None
        #Game states:
        #explore - Player can move around
        #dialogue - Player is currently in dialogue, player can't move
        #flowerC - flower animation is playing, player can't move

        self.cutsceneManage = cutscenes.CutsceneManager(self)
        self.map = [-1, -1]
        # This list contains all the special tiles for the game, preloaded here when the game starts to save loading time
        # When going from room to room.
        # The first nested list is for walkable blocks, while the second list is for not walkable ones
        self.tileList = None
        self.hyacinImgL = None
        self.sunFloImgL = None
        self.silentFImgL = None
        self.rubyImageL = None
        self.emeraldImageL = None
        self.ironImageL = None
        self.amethImageL = None
        self.copperImageL = None

        self.setupImages()

        self.tutorialsActive = False
        
        self.running = True
        self.finishedScene = False
        self.cutsceneSkip = False
        self.musicVol = 10
        self.soundVol = 10
        self.startPlayerMaxHealth = 1000
        self.priorPlayerHealth = self.startPlayerMaxHealth

        self.npcImageList = [
                          'Sprites/npcs/NPCs-Char/bucket.png',
                          'Sprites/npcs/NPCs-Char/heart.png',
                          'Sprites/npcs/NPCs-Char/leaf.png']
        self.avatarImgList = [pygame.transform.scale(pygame.image.load(self.npcImageList[0]).convert_alpha(), (920*0.24, 170*0.73)),
                              pygame.transform.scale(pygame.image.load(self.npcImageList[1]).convert_alpha(), (920*0.24, 170*0.73)),
                              pygame.transform.scale(pygame.image.load(self.npcImageList[2]).convert_alpha(), (920*0.24, 170*0.73)),
                              pygame.transform.scale(pygame.image.load('Sprites/npcs/NPCs-Char/catNPCno4.png').convert_alpha(), (920*0.3, 170*0.73))]
        self.nameList = ['bucket', 'heart', 'leaf']

        #list of rooms that's visited by the player, starts off with all demo rooms.
        #self.visited = [(2,0), (2,1), (1,1), (3, 1), (2,2), (2, 7)]
        self.visited = [(2, 1), (2, 7)]
        self.notVisited = [(2, 0), (1,1), (3, 1), (2,2), (2, 3), (3, 3), (4, 3), (2, 4), (4, 4), (5, 4), (1, 5), (2, 5), (3, 5), (5, 5), (2, 6), (3, 6), (4, 6), (5, 6), (1, 8), (0, 9), (1, 9), (2, 9), (3, 9), (0, 10), (3, 10), (4, 10), (0, 11), (2, 11), (3, 11), (2, 12)]

        #list of flowers
        self.aliveFlowers = {}
        #list of ores
        self.aliveOres = {}
        #list of enemies
        self.aliveEnemies = {}
        #list of npcs
        self.visitedNPCs = []
    
    #written by Rachel Tang 4/19/24
    #used this website: https://www.educative.io/answers/how-to-play-an-audio-file-in-pygame
    def play_music(self, songType):
        if songType == 'dialogue':
            mixer.music.load('Music/CI103_-_normal_dialogue_background.mp3')
            mixer.music.set_volume(0.07 * self.musicVol)
            mixer.music.play()
        elif songType == 'openingCutscene':
            mixer.music.load('Music/Chopin-nocturne-op-9-no-2.mp3')
            mixer.music.set_volume(0.1 * self.musicVol)
            mixer.music.play()
        elif songType == 'village':
            mixer.music.load('Music/everrootforestVillagetheme.mp3')
            mixer.music.set_volume(0.065 * self.musicVol)
            mixer.music.play(100)
        elif songType == 'enemy':
            mixer.music.load('Music/enemy-music.mp3')
            mixer.music.set_volume(0.045 * self.musicVol)
            mixer.music.play(100)
        elif songType == 'boss':
            mixer.music.load('Music/boss_music_final.mp3')
            mixer.music.set_volume(0.050 * self.musicVol)
            mixer.music.play(100)
        elif songType == 'death':
            mixer.music.load('Music/Bleach_-_Never_meant_to_belong.mp3')
            mixer.music.set_volume(0.070 * self.musicVol)
            mixer.music.play(10)
        elif songType == 'win':
            mixer.music.load('Music/Aspertia.ogg')
            mixer.music.set_volume(0.06 * self.musicVol)
            mixer.music.play(10)
        if songType.lower() == 'stop':
            mixer.music.stop()



    def createTilemap(self, prevPosition):
        #Only for initial map creation
        # -1, -1 is the convention to make known that the map doesnt currently exist
        if self.map == [-1, -1]:
            # 1, 1 : the map now exists from the list in settings.py
            self.map = [2, 1]
            self.inventory = Inventory(self)
            for row in range(len(settings.currentTileMap[0])):
                #print(f"{row} ", end="")   
                for col in range(len(settings.currentTileMap[0][row])):
                    WalkableBlock(self, col, row, 1)
                    if (settings.currentTileMap[0][row])[col] == "B": # brick
                        Block(self, col, row, 5)
                    elif (settings.currentTileMap[0][row])[col] == "W": # water
                        Block(self, col, row, 1)
                    elif (settings.currentTileMap[0][row])[col] == "S": # sapling
                        Block(self, col, row, 2)
                    elif (settings.currentTileMap[0][row])[col] == "R": # rock
                        Block(self, col, row, 3)
                    elif (settings.currentTileMap[0][row])[col] == "C": # crossBridge
                        WalkableBlock(self, col, row, 0)
                    elif (settings.currentTileMap[0][row])[col] == "G": # growth
                        WalkableBlock(self, col, row, 1)                                                                      
                    elif (settings.currentTileMap[0][row])[col] == "P": # player
                        self.player = Player(self, col, row, self.clock)
                    elif (settings.currentTileMap[0][row])[col] == "F": # flower
                        self.aliveFlowers[(2, 1)] = self.aliveFlowers.get((2, 1), []) + [Flower(self, col, row, self.clock)]
                    elif (settings.currentTileMap[0][row])[col] == 'O': # ore
                        self.aliveOres[(2, 1)] = self.aliveOres.get((2, 1), []) + [Ore(self, col, row, self.clock)]
                    elif (settings.currentTileMap[0][row])[col] == 'N': # NPC
                        self.visitedNPCs.append(NPC(self, col, row, (2,1)))
                    elif (settings.currentTileMap[0][row])[col] == 'E': # melee enemy
                        self.aliveEnemies[(2, 1)] = self.aliveEnemies.get((2, 1), []) + [Enemy(self, col, row, 'melee')]
                    elif (settings.currentTileMap[0][row])[col] == 'D': # ranged enemy
                        Enemy(self, col, row, 'ranged')
                    elif (settings.currentTileMap[0][row])[col] == 'T': # teleport/door
                        Teleport(self, col, row)
                    #print(f"{col}", end="")
                #print()
            # initializes the visual element that displays the player's weapons
            self.weaponsHud = WeaponDisplay(self)
            # THIS LINE BELOW IS HERE FOR TESTING THE BOSS ONLY
            # self.boss = Boss(self, WIDTH * 0.4, HEIGHT * 0.4)
        #For moving between rooms
        else:
            # kill all the current sprites in the current room
            # empties all the sprites lists
            self.all_sprites.empty()
            self.blocks.empty()
            self.walk_blocks.empty()
            self.ground.empty()
            self.flowers.empty()
            self.ores.empty()
            self.npcs.empty()
            self.teleport.empty()
            self.enemies.empty()
            self.teleport.empty()
            self.particles.empty()
            self.non_background.empty()
            self.user_interface.empty()


            # This is a variable to allow the weapon that was equipped in the current room to stay equipped
            # Otherwise it would reset to the default weapon everytime the player changes rooms
            priorWeaponNum = self.player.weaponNum
            self.priorPlayerHealth = self.player.targetHealth

            mapNumber = mapList[self.map[0]][self.map[1]] 
            self.previousMapType = currentTileMap[mapNumber][0][-1]
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
            

            purpleRoomsIndexes = []
            greenRoomsIndexes = [0, 1, 2, 3, 4]

            # if the room is unloaded and listed as -2, a randomly assigned purple enemy room will be loaded and added to the map list
            if mapNumber == -2:
                purpleRandomRoomIndex = random.randint(0, len(purpleRandomRooms)-1)
                randomPurpleMap = purpleRandomRooms[purpleRandomRoomIndex]
                # RANDOMLY SPAWNING THE FLOWERS AND ORES
                # double flower: FF
                i = 5
                while i > 0:
                    row = random.randint(1,17)
                    column = random.randint(1,31)
                    if randomPurpleMap[row][column] == '.':
                        if randomPurpleMap[row][column+1] == '.':
                            string1 = self.replaceString(randomPurpleMap[row], column, 'F')
                            string1 = self.replaceString(string1, column+1, 'F')
                            randomPurpleMap[row] = string1
                            i -= 1
                        else:
                            i -= 1
                            pass
                    else:
                        i -= 1
                        pass
                # triple flower: F    1
                #                FF   23
                i = 3
                while i > 0:
                    row = random.randint(1,17)
                    column = random.randint(1,31)
                    if randomPurpleMap[row][column] == '.': # checks for period at 2
                        if randomPurpleMap[row][column+1] == '.': #checks for period at 3
                            if randomPurpleMap[row-1][column] == '.': # checks for period at 1
                                string1 = self.replaceString(randomPurpleMap[row], column, 'F') 
                                string1 = self.replaceString(string1, column+1, 'F')
                                string2 = self.replaceString(randomPurpleMap[row-1], column, 'F')
                                randomPurpleMap[row] = string1
                                randomPurpleMap[row-1] = string2
                                i -= 1
                            else:
                                i -= 1
                                pass
                        else:
                            i -= 1
                            pass
                    else:
                        i -= 1
                        pass
                # single ore: O
                i = 5
                while i > 0:
                    row = random.randint(1,17)
                    column = random.randint(1,31)
                    if randomPurpleMap[row][column] == '.':
                        string1 = self.replaceString(randomPurpleMap[row], column, 'O')
                        randomPurpleMap[row] = string1
                        i -= 1
                    else:
                        i -= 1
                        pass
                # ore box: OO  12
                #          OO  34
                i = 2
                while i > 0:
                    row = random.randint(1,17)
                    column = random.randint(1,31)
                    if randomPurpleMap[row][column] == '.': # ore 3
                        if randomPurpleMap[row][column+1] == '.': # ore 4
                            if randomPurpleMap[row-1][column] == '.': # ore 1
                                if randomPurpleMap[row-1][column+1] == '.': # ore 2
                                    string1 = self.replaceString(randomPurpleMap[row], column, 'O')
                                    string1 = self.replaceString(string1, column+1, 'O')
                                    string2 = self.replaceString(randomPurpleMap[row-1], column, 'O')
                                    string2 = self.replaceString(string2, column+1, 'O')
                                    randomPurpleMap[row] = string1
                                    randomPurpleMap[row-1] = string2
                                    i -= 1
                                else:
                                    i -= 1
                                    pass
                            else:
                                i -= 1
                                pass
                        else:
                            i -= 1
                            pass
                    else:
                        i -= 1
                        pass

                currentTileMap.append(randomPurpleMap)
                mapNumber = len(currentTileMap)-1
                purpleRoomsIndexes.append(mapNumber) # keeps track of purple room numbers to play music in
                mapList[self.map[0]][self.map[1]] = mapNumber
                # doesnt work here -char | self.play_music('enemy') play enemy bgm fighting music in this room
            # if the room is unloaded and listed as -3, a randomly assigned green npc room will be loaded and added to the map list
            elif mapNumber == -3:
                usedGreenRooms = [] # empty list that holds all green room indexes so that green rooms don't repeat throughout exploration
                while True: ### CHARLENNE
                    greenRandomRoomIndex = random.randint(0, len(greenRandomRooms)-1) # pick random green room
                    if greenRandomRoomIndex not in usedGreenRooms:
                        usedGreenRooms.append(greenRandomRoomIndex)
                        randomGreenMap = greenRandomRooms[greenRandomRoomIndex]
                        currentTileMap.append(randomGreenMap) # add the green map 
                        mapNumber = len(currentTileMap)-1
                        greenRoomsIndexes.append(mapNumber) # keeps track of green room numbers to play music in
                        mapList[self.map[0]][self.map[1]] = mapNumber
                        break
                # doesnt work here - char | self.play_music('village') The village bgm would play whenever you enter a peaceful npc room
            # if the room is unloaded and listed as -4, the red boss room will be loaded and added to the map list
            elif mapNumber == -4:
                # redMap / boss room
                currentTileMap.append(redMap)
                mapNumber = len(currentTileMap)-1
                mapList[self.map[0]][self.map[1]] = mapNumber

            self.currentMapType = currentTileMap[mapNumber][0][-1]
            if self.currentMapType == 'g' and self.previousMapType != 'g':
                self.play_music('village')
            elif self.currentMapType == 'p' and self.previousMapType != 'p':
                self.play_music('enemy')

            # if mapNumber in greenRoomsIndexes:
            #     print('greenRoomsIndexes', greenRoomsIndexes)
            #     print('mapTypesA', self.previousMapType, self.currentMapType)
            #     # if mapNumber-1 in greenRoomsIndexes:
            #     #     pass
            #     if self.previousMapType != self.currentMapType:
            #         self.play_music('village')
            # elif mapNumber in purpleRoomsIndexes:
            #     print('purpleRoomsIndexes', purpleRoomsIndexes)
            #     print('mapTypesB', self.previousMapType, self.currentMapType)
            #     # if mapNumber-1 in purpleRoomsIndexes:
            #     #     pass
            #     if self.previousMapType != self.currentMapType:
            #         self.play_music('enemy')

            print('self.map:', self.map, 'mapNumber', mapNumber)
            print('up:', self.map[0]-1 >= 0, end = ' ')
            if self.map[0]-1 >= 0:
                print(mapList[self.map[0]-1][self.map[1]] != -1, end = ' ')
            print('down:', self.map[0]+1 <= 5, end = ' ')
            if self.map[0]+1 <= 5:
                print(mapList[self.map[0]+1][self.map[1]] != -1, end = ' ')
            print('left:', self.map[1]-1 >= 0, end = ' ')
            if self.map[1]-1 >= 0:
                print(mapList[self.map[0]][self.map[1]-1] != -1, end = ' ')
            print('right:', self.map[1]+1 <= 12, end = ' ')
            if self.map[1]+1 <= 12:
                print(mapList[self.map[0]][self.map[1]+1] != -1)
            
            # print(self.map[1]-1)
            # print(mapList[self.map[0]][self.map[1]-1])

            # CREATES DOORS in a new room if it is meant to exist
            # going up
            if self.map[0]-1 >= 0 and mapList[self.map[0]-1][self.map[1]] != -1:
                # the top row of a map
                row = currentTileMap[mapNumber][0]
                row = row[0:15] + 'TT' + row[17:]
                currentTileMap[mapNumber][0] = row
            try:
                if mapList[self.map[0]-1][self.map[1]] == -1:
                    row = currentTileMap[mapNumber][0]
                    row = row[0:15] + 'BB' + row[17:]
                    currentTileMap[mapNumber][0] = row
            except IndexError:
                pass
            #down
            if self.map[0]+1 <= 5 and mapList[self.map[0]+1][self.map[1]] != -1:
                row = currentTileMap[mapNumber][17]
                row = row[0:15] + 'TT' + row[17:]
                currentTileMap[mapNumber][17] = row
            try:
                if mapList[self.map[0]+1][self.map[1]] == -1:
                    row = currentTileMap[mapNumber][17]
                    row = row[0:15] + 'BB' + row[17:]
                    currentTileMap[mapNumber][17] = row
            except IndexError:
                pass
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
            try:
                if mapList[self.map[0]][self.map[1]-1] == -1:
                    row1 = currentTileMap[mapNumber][8]
                    row1 = 'B' + row1[1:]
                    row2 = currentTileMap[mapNumber][9]
                    row2 = 'B' + row2[1:]
                    currentTileMap[mapNumber][8] = row1
                    currentTileMap[mapNumber][9] = row2
            except IndexError:
                pass
            # right
            if self.map[1]+1 <= 12 and mapList[self.map[0]][self.map[1]+1] != -1:
                row1 = currentTileMap[mapNumber][8]
                row1 = row1[:-1] + 'T'
                row2 = currentTileMap[mapNumber][9]
                row2 = row2[:-1] + 'T'
                currentTileMap[mapNumber][8] = row1
                currentTileMap[mapNumber][9] = row2
            try:
                if mapList[self.map[0]][self.map[1] + 1] == -1:
                    row1 = currentTileMap[mapNumber][8]
                    row1 = row1[:-1] + 'B'
                    row2 = currentTileMap[mapNumber][9]
                    row2 = row2[:-1] + 'B'
                    currentTileMap[mapNumber][8] = row1
                    currentTileMap[mapNumber][9] = row2
            except IndexError:
                pass
            try:
                print(f"up: {mapList[self.map[0] - 1][self.map[1]]}, {(self.map[0]-1, self.map[1])}")
            except IndexError:
                print("up: out of map range")
                row = currentTileMap[mapNumber][0]
                row = row[0:15] + 'BB' + row[17:]
                currentTileMap[mapNumber][0] = row
            try:
                print(f"down: {mapList[self.map[0] + 1][self.map[1]]}, {(self.map[0] + 1, self.map[1])}")
            except IndexError:
                print("down: out of map range")
                row = currentTileMap[mapNumber][17]
                row = row[0:15] + 'BB' + row[17:]
                currentTileMap[mapNumber][17] = row
            try:
                print(f"left: {mapList[self.map[0]][self.map[1] - 1]}, {(self.map[0], self.map[1] - 1)}")
            except IndexError:
                print("left: out of map range")
                row1 = currentTileMap[mapNumber][8]
                row1 = 'B' + row1[1:]
                row2 = currentTileMap[mapNumber][9]
                row2 = 'B' + row2[1:]
                currentTileMap[mapNumber][8] = row1
                currentTileMap[mapNumber][9] = row2
            try:
                print(f"right: {mapList[self.map[0]][self.map[1] + 1]}, {(self.map[0], self.map[1] + 1)}")
            except IndexError:
                print("right: out of map range")
                row1 = currentTileMap[mapNumber][8]
                row1 = row1[:-1] + 'B'
                row2 = currentTileMap[mapNumber][9]
                row2 = row2[:-1] + 'B'
                currentTileMap[mapNumber][8] = row1
                currentTileMap[mapNumber][9] = row2
            # print(self.map, mapNumber)

            # if mapNumber == -1:
            #     for i in mapList:
            #         print(i) 
            # print('Current Map:')
            # for i in currentTileMap[mapNumber]:
            #     print(i)


            self.all_sprites.add(self.inventory)
            self.all_sprites.add(self.weaponsHud)
            self.all_sprites.add(self.player)
            self.all_sprites.add(self.player.weapon)
            self.non_background.add(self.player)

            position = (self.map[0], self.map[1])
            for row in range(len(settings.currentTileMap[mapNumber])):
                #print(f"{row} ", end="")
                for col in range(len(settings.currentTileMap[mapNumber][row])):
                    if (settings.currentTileMap[mapNumber][0][-1] == 'r'):
                        WalkableBlock(self, col, row, 3)
                    else:
                        WalkableBlock(self, col, row, 1)
                    # looks at the premade room in settings.py, if a tile is on the map, print the corresponding sprite on the new map
                    if (settings.currentTileMap[mapNumber][row])[col] == "B": # brick
                        if (settings.currentTileMap[mapNumber][0][-1] == 'r'):
                            Block(self, col, row, 4)
                        else:
                            Block(self, col, row, 5)
                    elif (settings.currentTileMap[mapNumber][row])[col] == "W": # water
                        Block(self, col, row, 1)
                    elif (settings.currentTileMap[mapNumber][row])[col] == "S": # sapling
                        Block(self, col, row, 2)
                    elif (settings.currentTileMap[mapNumber][row])[col] == "R": # rock
                        Block(self, col, row, 3)
                    elif (settings.currentTileMap[mapNumber][row])[col] == "C": # crossBridge
                        WalkableBlock(self, col, row, 0)
                    elif (settings.currentTileMap[mapNumber][row])[col] == "G": # growth
                        WalkableBlock(self, col, row, 1)
                    elif (settings.currentTileMap[mapNumber][row])[col] == "F": # flower
                        if position in self.notVisited:
                            self.aliveFlowers[position] = self.aliveFlowers.get(position, []) + [Flower(self, col, row, self.clock)]
                        else:
                            for i in range(len(self.aliveFlowers[position])):
                                self.all_sprites.add(self.aliveFlowers[position][i])
                                self.flowers.add(self.aliveFlowers[position][i])
                    elif (settings.currentTileMap[mapNumber][row])[col] == 'O': # ore
                        if position in self.notVisited:
                            self.aliveOres[position] = self.aliveOres.get(position, []) + [Ore(self, col, row, self.clock)]
                        else:
                            for i in range(len(self.aliveOres[position])):
                                self.all_sprites.add(self.aliveOres[position][i])
                                self.ores.add(self.aliveOres[position][i])
                    elif (settings.currentTileMap[mapNumber][row])[col] == 'N': # NPC
                        position = (self.map[0], self.map[1])
                        if position in self.notVisited:
                            self.visitedNPCs.append(NPC(self, col, row, self.map))
                        else:
                            for i in range(len(self.visitedNPCs)):
                                if self.visitedNPCs[i].mapPos == position:
                                    self.all_sprites.add(self.visitedNPCs[i])
                                    self.npcs.add(self.visitedNPCs[i])
                    elif (settings.currentTileMap[mapNumber][row])[col] == 'E': # melee enemy
                        if position in self.notVisited:
                            self.aliveEnemies[position] = self.aliveEnemies.get(position, []) + [Enemy(self, col, row, 'melee')]
                        else:
                            for i in range(len(self.aliveEnemies[position])):
                                self.all_sprites.add(self.aliveEnemies[position][i])
                                self.enemies.add(self.aliveEnemies[position][i])
                    elif (settings.currentTileMap[mapNumber][row])[col] == 'D': # ranged enemy
                        if position in self.notVisited:
                            self.aliveEnemies[position] = self.aliveEnemies.get(position, []) + [Enemy(self, col, row, 'ranged')]
                        else:
                            for i in range(len(self.aliveEnemies[position])):
                                self.all_sprites.add(self.aliveEnemies[position][i])
                                self.enemies.add(self.aliveEnemies[position][i])
                    elif (settings.currentTileMap[mapNumber][row])[col] == 'T': # teleport door
                        # teleports the player's position on the screen when they move rooms
                        if self.currentMapType != 'r':
                            Teleport(self, col, row)
                        else:
                            Block(self, col, row, 4)
                        if prevPosition[0] == 0 and col == 31 and prevPosition[1] == row:
                            self.player.setPosition(col-1, row)
                        elif prevPosition[0] == 31 and col == 0 and prevPosition[1] == row:
                            self.player.setPosition(col+1, row)
                        elif prevPosition[1] == 0 and row == 17 and prevPosition[0] == col:
                            self.player.setPosition(col, row-1)
                        elif prevPosition[1] == 17 and row == 0 and prevPosition[0] == col:
                            self.player.setPosition(col, row+1)
                        # maintains the previously equipped weapon from the previous screen
                        self.player.weaponNum = priorWeaponNum
                        self.player.weapon.type = self.player.weaponList[self.player.weaponNum]
                        self.player.weapon.updateDamage(self.player.bonusDamage)
            
            #tracks rooms that have been visited
            position = (self.map[0], self.map[1])
            if position not in self.visited:
                self.visited.append(position)
                self.notVisited.remove(position)
            # [2, 7] and [2, 12] are currently the two locations in the maplist where the boss room is located
            #if (self.map == [2, 12] or self.map == [2, 7]):
            #    self.boss = Boss(self, WIDTH * 0.4, HEIGHT * 0.4)
            #    self.bossActive = True
            #    self.play_music('boss')
            #else:
            #    self.bossActive = False
            if (settings.currentTileMap[mapNumber][0][-1] == 'r'):
                self.boss = Boss(self, WIDTH * 0.4, HEIGHT * 0.4)
                self.bossActive = True
                self.play_music('boss')
            else:
                self.bossActive = False



        # print("mapList:", mapList)
        # print("currentTileMap:", currentTileMap)

    # def addRoom(self, prevPosition):
    #     emptyRoom = []
    #     for row in range(18):
    #         emptyRow = ''
    #         for col in range(32):
    #             if prevPosition[0] == 0 and col == 31 and prevPosition[1] == row:
    #                 emptyRow += 'T'
    #             elif prevPosition[0] == 31 and col == 0 and prevPosition[1] == row:
    #                 emptyRow += 'T'
    #             elif prevPosition[1] == 0 and row == 17 and prevPosition[0] == col:
    #                 emptyRow += 'T'
    #             elif prevPosition[1] == 17 and row == 0 and prevPosition[0] == col:
    #                 emptyRow += 'T'
    #             elif row == 0 or row == 17 or col == 0 or col == 31:
    #                 emptyRow += 'B'
    #             else:
    #                 emptyRow += '.'
    #         emptyRoom.append(emptyRow)
    #     currentTileMap.append(emptyRoom)

    def new(self):

        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.non_background = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.walk_blocks = pygame.sprite.LayeredUpdates()
        self.ground = pygame.sprite.LayeredUpdates()
        self.flowers = pygame.sprite.LayeredUpdates()
        self.ores = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.teleport = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.weapons = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.bullets = pygame.sprite.LayeredUpdates()
        self.particles = pygame.sprite.LayeredUpdates()
        self.user_interface = pygame.sprite.LayeredUpdates()
        self.endgates = pygame.sprite.LayeredUpdates()
        self.createTilemap(None)
        #self.player = Player(self, 1, 2)
    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if the exit button in the top corner of the window is pressed, then the game closes
                pygame.font.quit()
                pygame.quit()
                sys.exit()
            # Use E to attack using a melee weapon
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_j and not self.player.itemUsed) and ((self.player.weapon.type == 'swordfish' or self.player.weapon.type == 'trident') and self.state == 'explore'):
                self.player.itemUsed = True
                if False: # This line is a placeholder for a conditional that will check if the melee weapon type is the spear weapon or swordfish
                    pass
                elif self.player.weapon.type == 'swordfish': # if the weapon equipped is the swordfish
                    self.player.swordUsed = True
                elif self.player.weapon.type == 'trident': # if the weapon equipped is the trident
                    self.player.spearUsed = True
                MeleeAttack(self, self.player.weapon, self.player)
            # Uses the bubblegun to attack with E if that is the weapon currently equipped is the bubblegun
            if event.type == pygame.KEYDOWN and ((event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]) and not self.player.itemUsed) and (self.player.weapon.type == 'bubble' and self.state == 'explore'):
                if (event.key == pygame.K_LEFT):
                    self.player.weapon.attack('left')
                    self.player.rangedAttackVisual('left')
                elif (event.key == pygame.K_UP):
                    self.player.weapon.attack('up')
                    self.player.rangedAttackVisual('up')
                elif (event.key == pygame.K_RIGHT):
                    self.player.weapon.attack('right')
                    self.player.rangedAttackVisual('right')
                else:
                    self.player.weapon.attack('down')
                    self.player.rangedAttackVisual('down')
            # switches weapon equipped using q
            if event.type == pygame.KEYUP and event.key == pygame.K_q and not self.player.itemUsed and self.state == 'explore':
                self.player.switchWeapons()
            if event.type == pygame.KEYUP and event.key == pygame.K_p and (self.state != 'shopping' and self.state != 'dialogue'): # pauses the game with P
                self.pause()
            if event.type == pygame.KEYUP and event.key == pygame.K_m and (self.state != 'shopping' and self.state != 'dialogue'):
                self.showMap()
            if event.type == pygame.KEYUP and event.key == pygame.K_h and not self.player.itemUsed and self.state == 'explore' and self.inventory.get('potion') > 0: # keybind to heal, will have added functionality with potions in the inventory later
                self.player.getHealth(300)
                self.inventory.add_item('potion', -1)
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE: # closes the game if escape is pressed
                pygame.font.quit()
                pygame.quit()
                sys.exit()
            # if event.type == pygame.KEYUP and event.key == pygame.K_n and not self.player.itemUsed and self.state == 'explore': # keybind to speed, will have added functionality with potions in the inventory later
            #     self.game.potions.potionSpeed()

    def update(self):
        # game loop updates
        self.all_sprites.update()  # calls update() function for all sprites within the all_sprites group
        # checks if the tutorial should appear based on the settings and state of the game
        self.player.tutorial.checkAppear() # checks if the tutorial should be drawn on the screen, if it is enabled

    def draw(self):
        if self.state != 'game over' and self.state != 'victory':
            self.screen.fill(BLACK)
            self.renderSurface.fill(BLACK)
            self.doScreenShake()
            self.all_sprites.draw(self.renderSurface)
            # credit for the sorting camera comes from this video - https://www.youtube.com/watch?v=u7LPRqrzry8
            # the line below sorts the sprites in the non_background group based on their y positions, putting those at a lower position on a layer in front.
            for sprite in sorted(self.non_background, key = lambda sprite: sprite.rect.centery):
                self.renderSurface.blit(sprite.image, sprite.rect)
            for element in self.user_interface:
                self.renderSurface.blit(element.image, element.rect)
            self.screen.blit(self.renderSurface, self.renderOffset)
            #self.all_sprites.draw(self.screen)


            # draws the tutorial text on screen if needed
            if self.tutorialsActive:
                self.player.tutorial.draw()
            # draws the player's health bar on the screen if needed
            if (self.state == 'explore' or self.state == 'oreMine' or self.state == 'flowerC'):
                self.player.animateHealth()
                self.player.showStatus()
            if self.state == 'shopping':
                self.activeNPC.choiceResponse()
            if self.bossActive:
                self.boss.ui()
            self.weaponsHud.draw() # calls the function to draw the weapon display hud on the screen
            self.inventory.draw()
            self.clock.tick(FPS)
            pygame.display.update() # updates the screen with any changes

    def main(self):
        # main game loop
        while self.playing: # while the game is being played
            self.events()
            if self.state == 'opening': # if the opening should be happening
                self.intro_screen()
            if self.state == 'game over': # if the player has died or triggered a game over
                self.game_over()
            self.update()
            self.draw()
        self.running = False # after the game is done being played, the game should not be running

    #
    def game_over(self):
        # Play the game over screen
        # To be created later
        self.screen.fill(BLACK)
        cutscenes.playGameOver(self.cutsceneManage)
        pass

    def game_won(self):
        self.state = 'victory'
        self.screen.fill(SWAMPGREEN)
        cutscenes.playGameWon(self.cutsceneManage)


    # Charlenne 5/15/24: to replace the string of a map row where an item needs to be added
    def replaceString(self, string, column, replacement):
        beginning = string[:column]
        end = string[column+1:]
        newString = beginning + replacement + end
        return newString
        

    # handles events happening while the game is in the pause state
    def pauseEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # allows the game to be closed with the x in the top right corner of the window
                pygame.font.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_p and (self.state != 'shopping' and self.state != 'dialogue'): # if p is pressed, the pause() function is called to unpause the game
                self.pause()
            if event.type == pygame.KEYUP and event.key == pygame.K_m and (self.state != 'shopping' and self.state != 'dialogue' and self.state != 'pause'): # if p is pressed, the pause() function is called to unpause the game
                self.showMap()
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE: # escape closes the game
                pygame.font.quit()
                pygame.quit()
                sys.exit()
            # This lowers the game music volume by using the down arrow key in the pause menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.musicVol -= 1
                if self.musicVol < 0:
                    self.musicVol = 0
                #print(self.musicVol)
                pygame.mixer.Channel(1).set_volume(0.015 * self.soundVol)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_UI_Menu_SFX/029_Decline_09.wav'))
            # This raises the game music volume by using the up arrow key in the pause menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.musicVol += 1
                if self.musicVol > 20:
                    self.musicVol = 20
                #print(self.musicVol)
                pygame.mixer.Channel(1).set_volume(0.025 * self.soundVol)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_UI_Menu_SFX/013_Confirm_03.wav'))
            # This raises the game sound effect volume by using the right arrow key in the pause menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.soundVol += 1
                if self.soundVol > 20:
                    self.soundVol = 20
                #print(self.soundVol)
                pygame.mixer.Channel(1).set_volume(0.025 * self.soundVol)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_UI_Menu_SFX/013_Confirm_03.wav'))
            # This lowers the game sound effect volume by using the left arrow key in the pause menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.soundVol -= 1
                if self.soundVol < 0:
                    self.soundVol = 0
                #print(self.soundVol)
                pygame.mixer.Channel(1).set_volume(0.015 * self.soundVol)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_UI_Menu_SFX/029_Decline_09.wav'))
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:  # Use spacebar to access settings menu when paused
                # this currently toggles if the tutorials should actively appear on the screen
                pygame.mixer.Channel(1).set_volume(0.015 * self.soundVol)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_UI_Menu_SFX/001_Hover_01.wav'))
                if self.tutorialsActive:
                    self.tutorialsActive = False
                else:
                    self.tutorialsActive = True

    # function to display the settings and options within the pause menu
    def pauseMenuDisplay(self):
        self.screen.blit(pygame.font.SysFont('Garamond', 38).render(f"Adjust Music with Up/Down Arrows | Music Volume: {(self.musicVol / 20 * 100):.1f}%", False, WHITE), (WIDTH * 0.135 ,HEIGHT * 0.45))
        self.screen.blit(pygame.font.SysFont('Garamond', 38).render(f"Adjust SoundFX with Left/Right Arrows | Sound FX Volume: {(self.soundVol / 20 * 100):.1f}%", False,WHITE), (WIDTH * 0.105, HEIGHT * 0.55))
        self.screen.blit(pygame.font.SysFont('Garamond', 38).render(f"Use Spacebar to toggle tutorials", False,WHITE), (WIDTH * 0.32, HEIGHT * 0.65))
        # In the future, possible replace the text and percentages on screen with buttons to adjust settings
        # Also maybe work on a way to fix how the numbers look when being adjusted in the pause screen
        # The old numbers linger partially transparent after a change
        tutorialStatus = ''
        if self.tutorialsActive:
            tutorialStatus = "On"
        else:
            tutorialStatus = "Off"
        self.screen.blit(pygame.font.SysFont('Garamond', 38).render(f"Tutorials: {tutorialStatus}", False, WHITE),(WIDTH * 0.42, HEIGHT * 0.75))
        pass

    # function to handle the process of pausing the game when P is pressed
    def pause(self):
        if self.state == 'explore': # pauses the game if it is not paused already
            self.state = 'pause'
            # lowers the volume of music when the game is paused
            pygame.mixer.Channel(1).set_volume(0.025 * self.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_UI_Menu_SFX/092_Pause_04.wav'))
            while self.state == 'pause':
                mixer.music.set_volume(0.035 * self.musicVol)
                # Text to be displayed in the pause screen as a string below
                pauseText = (["Game Paused", "Press P again to unpause", "Press ESC to quit at anytime"])
                # alpha value for the gray screen filter rectangle that is applied when the game is paused
                # the lines of code below implement and create that rectangle
                alpha = 4
                pauseRect = pygame.Surface((WIDTH, HEIGHT))
                #pauseRect = pauseRect.convert_alpha()
                pauseRect.set_alpha(alpha)
                #print(f"Alpha is {pauseRect.get_alpha()}")
                pauseRect.fill(pygame.Color(100, 100, 100, alpha))
                self.screen.blit(pauseRect, (0,0))
                #pygame.draw.rect(self.screen, (128, 128, 128, 128), [0, 0, WIDTH, HEIGHT])
                # putting the pause text on the screen while the game is paused
                self.screen.blit(pygame.font.SysFont('Garamond', 55).render(pauseText[0].strip(), False, WHITE),(WIDTH * 0.4225, HEIGHT * 0.1))
                self.screen.blit(pygame.font.SysFont('Garamond', 55).render(pauseText[1].strip(), False, WHITE),(WIDTH * 0.3271875, HEIGHT * 0.2277))
                self.screen.blit(pygame.font.SysFont('Garamond', 45).render(pauseText[2].strip(), False, ORANGE),(WIDTH * 0.3446875, HEIGHT * 0.34166))
                # handling events while the game is paused
                self.pauseEvents()
                self.pauseMenuDisplay()
                pygame.display.update()

                # SOMEWHERE DURING THE PAUSE MENU, ADD TEXT TO EXPLAIN USING THE SPACEBAR TO TOGGLE TUTORIALS
                # ALSO ADD TEXT TO EXPLAIN USING THE ARROW KEYS TO ADJUST SOUND EFFECT AND MUSIC VOLUME
                # EITHER REPRESENT THE VOLUME STATUS USING SLIDERS OR JUST DISPLAY THE NUMBER AS A FRACTION OF THE MAX VOLUME
                
        else:
            self.state = 'explore' # unpauses the game
            # returns the music to the former volume
            pygame.mixer.Channel(1).set_volume(0.025 * self.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_UI_Menu_SFX/098_Unpause_04.wav'))
            mixer.music.set_volume(0.065 * self.musicVol)
        pass

    def intro_screen(self):
        #Play the intro screen
        #To be created later
        self.play_music('win')
        while self.state == 'menu':
            self.screen.blit(pygame.transform.scale(pygame.image.load('Sprites/hudImages/title3.png').convert_alpha(), (WIDTH, HEIGHT)), self.renderOffset)
            text = "Press Space to Play"
            render_text = pygame.font.Font('Fonts/minecraft-font/MinecraftRegular-Bmg3.otf', 70).render(text, True, RED)
            text_rect = render_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.4))
            pygame.draw.rect(self.screen, BROWN, text_rect)
            self.screen.blit(render_text, text_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.font.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.font.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.state = 'opening'
        cutscenes.playIntroScene(self.cutsceneManage) # starts the intro scene using the cutscene manager
        if self.finishedScene: # after the introduction finishes
            self.state = 'explore'
            self.play_music('village')
        pass

    # credit comes from https://www.youtube.com/watch?v=3nhQLJq0Lwk and https://www.youtube.com/watch?v=2JXR7IASSog
    def doScreenShake(self):
        if self.screenshake > 0:
            self.screenshake -= 1
        if self.screenshake:
            self.renderOffset[0] = random.randint(0, self.screenshake // 5) - self.screenshake // 10
            self.renderOffset[1] = random.randint(0, self.screenshake // 4) - self.screenshake // 8



    # This function sets up many of the images to be used in the game, then stores them in lists
    def setupImages(self):
        # sets up all the tile images to be placed in the game, then stores them in a list
        # the walkable tiles and unwalkable blocks are stored in two different sub lists that are within the larger list
        self.tileList = [[pygame.transform.scale(pygame.image.load('Sprites/tiles/crossBridge1.png').convert_alpha(),(TILESIZE, TILESIZE)),
                          pygame.transform.scale(pygame.image.load('Sprites/tiles/growth1.png').convert_alpha(),(TILESIZE, TILESIZE)),
                          pygame.transform.scale(pygame.image.load('Sprites/tiles/metalglass.jpg').convert_alpha(), (TILESIZE, TILESIZE)),
                          pygame.transform.scale(pygame.image.load('Sprites/tiles/brushwalker437.png').convert_alpha(), (TILESIZE, TILESIZE))],
                         [pygame.transform.scale(pygame.image.load('Sprites/tiles/brick1.png').convert_alpha(),(TILESIZE, TILESIZE)),
                          #pygame.transform.scale(pygame.image.load('Sprites/tiles/water1.png').convert_alpha(),(TILESIZE, TILESIZE)),
                          pygame.transform.scale(pygame.image.load('Sprites/tiles/brushwalker137.png').convert_alpha(),(TILESIZE, TILESIZE)),
                          pygame.transform.scale(pygame.image.load('Sprites/tiles/sapling2.png').convert_alpha(),(TILESIZE, TILESIZE)),
                          pygame.transform.scale(pygame.image.load('Sprites/tiles/rock1.png').convert_alpha(),(TILESIZE, TILESIZE)),
                          pygame.transform.scale(pygame.image.load('Sprites/tiles/metalwall.png').convert_alpha(), (TILESIZE, TILESIZE)),
                          pygame.transform.scale(pygame.image.load('Sprites/tiles/tree-dark-green-isaiah658.png').convert_alpha(), (TILESIZE, TILESIZE)),
                          ]]
        # sets up all the images for the hyacinth type flower
        self.hyacinImgL = [pygame.transform.scale(pygame.image.load('Sprites/items/hyacinth.png').convert_alpha(),(TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/hyacinth3New.png').convert_alpha(),(TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/hyacinth5.png').convert_alpha(),(TILESIZE, TILESIZE))]
        # sets up all the images for the sunflower type flower
        self.sunFloImgL = [pygame.transform.scale(pygame.image.load('Sprites/items/sunflowernew.png').convert_alpha(),(TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/sunflower3New.png').convert_alpha(),(TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/sunflower5.png').convert_alpha(),(TILESIZE, TILESIZE))]
        # sets up all the images for the silent flower type flower
        self.silentFImgL = [pygame.transform.scale(pygame.image.load('Sprites/items/silentFlower.png').convert_alpha(),(TILESIZE, TILESIZE)),
                       pygame.transform.scale(pygame.image.load('Sprites/items/silentFlower3New.png').convert_alpha(),(TILESIZE, TILESIZE)),
                       pygame.transform.scale(pygame.image.load('Sprites/items/silentFlower5.png').convert_alpha(),(TILESIZE, TILESIZE))]
        # sets up all the images for the ruby type ore
        self.rubyImageL = [pygame.transform.scale(pygame.image.load('Sprites/items/oreRuby.png').convert_alpha(),(TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/oreRuby2.png').convert_alpha(),(TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/oreRuby3.png').convert_alpha(),(TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/oreRuby3.png').convert_alpha(),(TILESIZE, TILESIZE))]
        # sets up all the images for the emerald type ore
        self.emeraldImageL = [pygame.transform.scale(pygame.image.load('Sprites/items/oreEmerald.png').convert_alpha(),(TILESIZE, TILESIZE)),
                         pygame.transform.scale(pygame.image.load('Sprites/items/oreEmerald2.png').convert_alpha(),(TILESIZE, TILESIZE)),
                         pygame.transform.scale(pygame.image.load('Sprites/items/oreEmerald3.png').convert_alpha(),(TILESIZE, TILESIZE)),
                         pygame.transform.scale(pygame.image.load('Sprites/items/oreEmerald3.png').convert_alpha(),(TILESIZE, TILESIZE))]
        # sets up all the images for the copper type ore
        self.copperImageL = [pygame.transform.scale(pygame.image.load('Sprites/items/oreCopper.png').convert_alpha(),(TILESIZE, TILESIZE)),
                        pygame.transform.scale(pygame.image.load('Sprites/items/oreCopper2.png').convert_alpha(),(TILESIZE, TILESIZE)),
                        pygame.transform.scale(pygame.image.load('Sprites/items/oreCopper3.png').convert_alpha(),(TILESIZE, TILESIZE)),
                        pygame.transform.scale(pygame.image.load('Sprites/items/oreCopper3.png').convert_alpha(),(TILESIZE, TILESIZE))]
        # sets up all the images for the amethyst type ore
        self.amethImageL = [pygame.transform.scale(pygame.image.load('Sprites/items/oreAmethyst.png').convert_alpha(),(TILESIZE, TILESIZE)),
                       pygame.transform.scale(pygame.image.load('Sprites/items/oreAmethyst2.png').convert_alpha(),(TILESIZE, TILESIZE)),
                       pygame.transform.scale(pygame.image.load('Sprites/items/oreAmethyst3.png').convert_alpha(),(TILESIZE, TILESIZE)),
                       pygame.transform.scale(pygame.image.load('Sprites/items/oreAmethyst3.png').convert_alpha(),(TILESIZE, TILESIZE))]
        # sets up all the images for the iron type ore
        self.ironImageL = [pygame.transform.scale(pygame.image.load('Sprites/items/oreIron.png').convert_alpha(),(TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/oreIron2.png').convert_alpha(),(TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/oreIron3.png').convert_alpha(),(TILESIZE, TILESIZE)),
                      pygame.transform.scale(pygame.image.load('Sprites/items/oreIron3.png').convert_alpha(),(TILESIZE, TILESIZE))]
        self.bossImageList = [[pygame.image.load('Sprites/npcs/boss/bossHead.png'), pygame.image.load('Sprites/npcs/boss/bossidea4_5.png')], [pygame.image.load('Sprites/npcs/boss/bossattack.png'), pygame.image.load('Sprites/npcs/boss/bossattack_2.png'), pygame.image.load('Sprites/npcs/boss/bossattack_3.png')]]
        self.particleList = [[pygame.image.load('Sprites/particles_vfx/bossparticles1.png'), pygame.image.load('Sprites/particles_vfx/bossparticles2.png'), pygame.image.load('Sprites/particles_vfx/bossparticles3.png')], [pygame.image.load('Sprites/particles_vfx/genparticles1.png'), pygame.image.load('Sprites/particles_vfx/genparticles2.png'), pygame.image.load('Sprites/particles_vfx/genparticles3.png')]]
        self.bossAttacks = [pygame.transform.scale(pygame.image.load('Sprites/items/bubbleCluster.png').convert_alpha(), (TILESIZE, TILESIZE)), pygame.transform.scale(pygame.image.load('Sprites/items/bubble.png').convert_alpha(), (TILESIZE * 3, TILESIZE * 3)), pygame.transform.scale(pygame.image.load('Sprites/items/bossProjectile.png').convert_alpha(), (TILESIZE, TILESIZE))]
        self.mapImg = pygame.transform.scale(pygame.image.load('Sprites/hudImages/Map.png').convert_alpha(), (1080, 405))

    def showMap(self):
        if self.state == 'explore': # pauses the game if it is not paused already
            self.state = 'map'
            # lowers the volume of music when the game is paused
            pygame.mixer.Channel(1).set_volume(0.025 * self.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_UI_Menu_SFX/092_Pause_04.wav'))
            while self.state == 'map':
                mixer.music.set_volume(0.035 * self.musicVol)
                # Text to be displayed in the pause screen as a string below
                #pauseText = (["Game Paused", "Press P again to unpause", "Press ESC to quit at anytime"])
                # alpha value for the gray screen filter rectangle that is applied when the game is paused
                # the lines of code below implement and create that rectangle
                alpha = 4
                pauseRect = pygame.Surface((WIDTH, HEIGHT))
                #pauseRect = pauseRect.convert_alpha()
                pauseRect.set_alpha(alpha)
                #print(f"Alpha is {pauseRect.get_alpha()}")
                pauseRect.fill(pygame.Color(100, 100, 100, alpha))
                self.screen.blit(pauseRect, (0,0))
                self.screen.blit(self.mapImg, (100,157.5))

                for i in range(len(self.notVisited)):
                    position = self.notVisited[i]
                    pygame.draw.rect(self.screen, BLACK, pygame.Rect(100+(6+position[1]*15)*1080/208, 157.5+(6+position[0]*11)*1080/208, 15*1100/208, 11*1100/208))
                
                playerPos = self.map
                playerCoord = (self.player.x*11/1280, self.player.y*7/720)
                pygame.draw.rect(self.screen, PURPLE, pygame.Rect(100+(6+playerPos[1]*15+playerCoord[0]+1)*1080/208, 157.5+(6+playerPos[0]*11+playerCoord[1]+1)*1080/208, 2*1100/208, 2*1100/208))
                #pygame.draw.rect(self.screen, BLACK,pygame.Rect(100 + (6 + playerPos[1] * 15 + playerCoord[0] + 1) * 1080 / 208,157.5 + (6 + playerPos[0] * 11 + playerCoord[1] + 1) * 1080 / 208,2 * 1100 / 208, 2 * 1100 / 208), 1)
                


                #pygame.draw.rect(self.screen, (128, 128, 128, 128), [0, 0, WIDTH, HEIGHT])
                # putting the pause text on the screen while the game is paused
                # self.screen.blit(pygame.font.SysFont('Garamond', 55).render(pauseText[0].strip(), False, WHITE),(WIDTH * 0.4225, HEIGHT * 0.1))
                # self.screen.blit(pygame.font.SysFont('Garamond', 55).render(pauseText[1].strip(), False, WHITE),(WIDTH * 0.3271875, HEIGHT * 0.2277))
                # self.screen.blit(pygame.font.SysFont('Garamond', 45).render(pauseText[2].strip(), False, ORANGE),(WIDTH * 0.3446875, HEIGHT * 0.34166))
                # handling events while the game is paused
                self.pauseEvents()
                #self.pauseMenuDisplay()
                pygame.display.update()

                # SOMEWHERE DURING THE PAUSE MENU, ADD TEXT TO EXPLAIN USING THE SPACEBAR TO TOGGLE TUTORIALS
                # ALSO ADD TEXT TO EXPLAIN USING THE ARROW KEYS TO ADJUST SOUND EFFECT AND MUSIC VOLUME
                # EITHER REPRESENT THE VOLUME STATUS USING SLIDERS OR JUST DISPLAY THE NUMBER AS A FRACTION OF THE MAX VOLUME
                
        else:
            self.state = 'explore' # unpauses the game
            # returns the music to the former volume
            pygame.mixer.Channel(1).set_volume(0.025 * self.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_UI_Menu_SFX/098_Unpause_04.wav'))
            mixer.music.set_volume(0.065 * self.musicVol)
        pass

    def updateAliveLists(self, spriteType, originalPos):
        position = (self.map[0], self.map[1])
        try:
            if spriteType == 'flower':
                for i in range(len(self.aliveFlowers[position])):
                    if self.aliveFlowers[position][i].originalPos == originalPos:
                        self.aliveFlowers[position].pop(i)
            elif spriteType == 'ore':
                for i in range(len(self.aliveOres[position])):
                    if self.aliveOres[position][i].originalPos == originalPos:
                        self.aliveOres[position].pop(i)
            elif spriteType == 'enemy':
                for i in range(len(self.aliveEnemies[position])):
                    if self.aliveEnemies[position][i].defaultPos == originalPos:
                        self.aliveEnemies[position].pop(i)
        except IndexError:
            pass


g = Game()
g.intro_screen()
# g.new()

while g.running:
    g.main()
    g.game_over()
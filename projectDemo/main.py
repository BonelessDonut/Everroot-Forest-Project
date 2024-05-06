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

        # The title for the game window is randomly selected at the start, because why not? - Eddie Suber
        windowTitle = ['Everroot Forrest - A CS Story',
                       'Everroot Forest - Spelled Correctly This Time',
                       'Everroot Forest - Unending Torment',
                       'Everroot Forest - Tranquil Quest',
                       'Everrot Forest - The Rot Consumes',
                       'Everroot Forest - PLEASE COMMIT SOMETHING',
                       'Everroot Forest - Why Hello There',
                       'Everroot Forest - Pure Bliss',
                       'Everroot Forest - This Is The One']
        titleNum = random.randint(0, len(windowTitle) - 1)
        pygame.display.set_caption(windowTitle[titleNum])
        self.clock = pygame.time.Clock() 

        self.player = None
        self.state = 'opening'
        #Game states:
        #explore - Player can move around
        #dialogue - Player is currently in dialogue, player can't move
        #flowerC - flower animation is playing, player can't move

        self.cutsceneManage = cutscenes.CutsceneManager(self)
        self.map = [-1, -1]

        self.tutorialsActive = True
        
        self.running = True
        self.finishedScene = False
        self.cutsceneSkip = False
        self.musicVol = 10
        self.soundVol = 10
        self.startPlayerMaxHealth = 1000
        self.priorPlayerHealth = self.startPlayerMaxHealth
    
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
        elif songType == 'boss': # Add boss music to be played when facing a boss, perhaps use music Jose recommended? - Eddie
            pass
        if songType.lower() == 'stop':
            mixer.music.stop()



    def createTilemap(self, prevPosition):
        #Only for initial map creation
        # -1, -1 is the convention to make known that the map doesnt currently exist
        if self.map == [-1, -1]:
            for row in range(len(settings.currentTileMap[0])):
                #print(f"{row} ", end="")   
                for col in range(len(settings.currentTileMap[0][row])):
                    if (settings.currentTileMap[0][row])[col] == "B": # brick
                        Block(self, col, row, 0)
                    elif (settings.currentTileMap[0][row])[col] == "W": # water
                        Block(self, col, row, 1)
                    elif (settings.currentTileMap[0][row])[col] == "S": # sapling
                        Block(self, col, row, 2)
                    elif (settings.currentTileMap[0][row])[col] == "R": # rock
                        Block(self, col, row, 3)                                                                        
                    elif (settings.currentTileMap[0][row])[col] == "P": # player
                        self.player = Player(self, col, row, self.clock)
                    elif (settings.currentTileMap[0][row])[col] == "F": # flower
                        Flower(self, col, row, self.clock)
                    elif (settings.currentTileMap[0][row])[col] == 'O': # ore
                        Ore(self, col, row, self.clock)
                    elif (settings.currentTileMap[0][row])[col] == 'N': # NPC
                        NPC(self, col, row)
                    elif (settings.currentTileMap[0][row])[col] == 'E': # enemy
                        Enemy(self, col, row)
                    elif (settings.currentTileMap[0][row])[col] == 'T': # teleport/door
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
            self.teleport.empty()


            # This is a variable to allow the weapon that was equipped in the current room to stay equipped
            # Otherwise it would reset to the default weapon everytime the player changes rooms
            priorWeaponNum = self.player.weaponNum
            self.priorPlayerHealth = self.player.targetHealth

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
                usedGreenRooms = [] # empty list that holds all green room indexes so that green rooms don't repeat throughout exploration
                while True:
                    greenRandomRoomIndex = random.randint(0, len(greenRandomRooms)-1) # pick random green room
                    if greenRandomRoomIndex not in usedGreenRooms:
                        usedGreenRooms.append(greenRandomRoomIndex)
                        randomGreenMap = greenRandomRooms[greenRandomRoomIndex]
                        currentTileMap.append(randomGreenMap) # add the green map 
                        mapNumber = len(currentTileMap)-1
                        mapList[self.map[0]][self.map[1]] = mapNumber
                        break
                # self.play_music('village') The village bgm would play whenever you enter a peaceful npc room
            # if the room is unloaded and listed as -4, the red boss room will be loaded and added to the map list
            elif mapNumber == -4:
                # redMap / boss room
                currentTileMap.append(redMap)
                mapNumber = len(currentTileMap)-1
                mapList[self.map[0]][self.map[1]] = mapNumber

            print(self.map, mapNumber)
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

            if mapNumber == -1:
                for i in mapList:
                    print(i) 
            print('Current Map:')
            for i in currentTileMap[mapNumber]:
                print(i)
                     
            for row in range(len(settings.currentTileMap[mapNumber])):
                #print(f"{row} ", end="")
                for col in range(len(settings.currentTileMap[mapNumber][row])):
                    # looks at the premade room in settings.py, if a tile is on the map, print the corresponding sprite on the new map
                    if (settings.currentTileMap[mapNumber][row])[col] == "B": # brick
                        Block(self, col, row, 0)
                    elif (settings.currentTileMap[mapNumber][row])[col] == "W": # water
                        Block(self, col, row, 1)
                    elif (settings.currentTileMap[mapNumber][row])[col] == "S": # sapling
                        Block(self, col, row, 2)
                    elif (settings.currentTileMap[mapNumber][row])[col] == "R": # rock
                        Block(self, col, row, 3)
                    elif (settings.currentTileMap[mapNumber][row])[col] == "F": # flower
                        Flower(self, col, row, self.clock)
                    elif (settings.currentTileMap[mapNumber][row])[col] == 'O': # ore
                        Ore(self, col, row, self.clock)
                    elif (settings.currentTileMap[mapNumber][row])[col] == 'N': # NPC
                        NPC(self, col, row)
                    elif (settings.currentTileMap[mapNumber][row])[col] == 'E': # enemy
                        Enemy(self, col, row)
                    elif (settings.currentTileMap[mapNumber][row])[col] == 'T': # teleport door
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
                        self.player.weaponNum = priorWeaponNum
                        self.player.weapon.type = self.player.weaponList[self.player.weaponNum]
                        self.player.weapon.updateDamage()

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
                pygame.font.quit()
                pygame.quit()
                sys.exit()
            # Use E to attack using a melee weapon
            if event.type == pygame.KEYUP and (event.key == pygame.K_e and not self.player.itemUsed) and ((self.player.weapon.type == 'swordfish' or self.player.weapon.type == 'trident') and self.state == 'explore'):
                self.player.itemUsed = True
                if False: # This line is a placeholder for a conditional that will check if the melee weapon type is the spear weapon or swordfish
                    pass
                elif self.player.weapon.type == 'swordfish':
                    self.player.swordUsed = True
                elif self.player.weapon.type == 'trident':
                    self.player.spearUsed = True
                MeleeAttack(self, self.player.weapon, self.player)
            # Q is used to switch weapons for the player
            if event.type == pygame.KEYUP and event.key == pygame.K_q and not self.player.itemUsed:
                self.player.switchWeapons()
            if event.type == pygame.KEYUP and event.key == pygame.K_p:
                self.pause()
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                pygame.font.quit()
                pygame.quit()
                sys.exit()

    def update(self):
        #game loop updates
        self.all_sprites.update()
        # checks if the tutorial should appear based on the settings and state of the game
        self.player.tutorial.checkAppear()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # draws the tutorial text on screen if needed
        if self.tutorialsActive:
            self.player.tutorial.draw()
        if (self.state == 'explore' or self.state == 'oreMine' or self.state == 'flowerC'):
            self.player.animateHealth()
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        while self.playing:
            self.events()
            if self.state == 'opening':
                self.intro_screen()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        #Play the game over screen
        #To be created later
        pass

    def pauseEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.font.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_p:
                self.pause()
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
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

    def pause(self):
        if self.state == 'explore':
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
                self.screen.blit(pygame.font.SysFont('Garamond', 55).render(pauseText[0].strip(), False, WHITE),  (WIDTH * 0.4225, HEIGHT * 0.1))
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
            self.state = 'explore'
            # returns the music to the former volume
            pygame.mixer.Channel(1).set_volume(0.025 * self.soundVol)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/sound_effects/RPG_Essentials_Free/10_UI_Menu_SFX/098_Unpause_04.wav'))
            mixer.music.set_volume(0.065 * self.musicVol)
        pass

    def intro_screen(self):
        #Play the intro screen
        #To be created later
        cutscenes.playIntroScene(self.cutsceneManage)
        if self.finishedScene:
            self.state = 'explore'
            self.play_music('village')
        pass




g = Game()
g.intro_screen()
# g.new()

while g.running:
    g.main()
    g.game_over()
import pygame, sys
import settings
from sprites import *
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
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock() 

        self.state = 'explore'
        #Game states:
        #explore - Player can move around
        #dialogue - Player is currently in dialogue, player can't move
        #flowerC - flower animation is playing, player can't move

        self.map = [-1, -1]
        
        #self.font = pygame.font.Font('Arial', 32)
        self.running = True

    def createTilemap(self, prevPosition):
        #Only for initial map creation
        if self.map == [-1, -1]:
            for row in range(len(settings.currentTilemap[0])):
                #print(f"{row} ", end="")
                for col in range(len(settings.currentTilemap[0][row])):
                    if (settings.currentTilemap[0][row])[col] == "B":
                        Block(self, col, row)
                    elif (settings.currentTilemap[0][row])[col] == "P":
                        Player(self, col, row, self.clock)
                    elif (settings.currentTilemap[0][row])[col] == "F":
                        Flower(self, col, row, self.clock)
                    elif (settings.currentTilemap[0][row])[col] == 'O':
                        Ore(self, col, row, self.clock)
                    elif (settings.currentTilemap[0][row])[col] == 'N':
                        NPC(self, col, row)
                    elif (settings.currentTilemap[0][row])[col] == 'T':
                        Teleport(self, col, row)
                    #print(f"{col}", end="")
                #print()
            self.map = [1, 1]
        #For moving between rooms
        else:
            self.all_sprites.empty()
            self.blocks.empty()
            self.ground.empty()
            self.flowers.empty()
            self.ores.empty()
            self.npcs.empty()
            self.teleport.empty()

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
                    if (settings.currentTilemap[mapNumber][row])[col] == "B":
                        Block(self, col, row)
                    elif (settings.currentTilemap[mapNumber][row])[col] == "F":
                        Flower(self, col, row, self.clock)
                    elif (settings.currentTilemap[mapNumber][row])[col] == 'O':
                        Ore(self, col, row, self.clock)
                    elif (settings.currentTilemap[mapNumber][row])[col] == 'N':
                        NPC(self, col, row)
                    elif (settings.currentTilemap[mapNumber][row])[col] == 'T':
                        Teleport(self, col, row)
                        if prevPosition[0] == 0 and col == 31 and prevPosition[1] == row:
                            Player(self, col-1, row, self.clock)
                        elif prevPosition[0] == 31 and col == 0 and prevPosition[1] == row:
                            Player(self, col+1, row, self.clock)
                        elif prevPosition[1] == 0 and row == 17 and prevPosition[0] == col:
                            Player(self, col, row-1, self.clock)
                        elif prevPosition[1] == 17 and row == 0 and prevPosition[0] == col:
                            Player(self, col, row+1, self.clock)

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

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
        self.map = 0
        
        #self.font = pygame.font.Font('Arial', 32)
        self.running = True

    def createTilemap(self, prevPosition):
        if self.map == 0:
            for row in range(len(settings.currentTilemap)):
                #print(f"{row} ", end="")d
                for col in range(len(settings.currentTilemap[row])):
                    if (settings.currentTilemap[row])[col] == "B":
                        Block(self, col, row)
                    elif (settings.currentTilemap[row])[col] == "P":
                        Player(self, col, row, self.clock)
                    elif (settings.currentTilemap[row])[col] == "F":
                        Flower(self, col, row, self.clock)
                    elif (settings.currentTilemap[row])[col] == 'O':
                        Ore(self, col, row)
                    elif (settings.currentTilemap[row])[col] == 'N':
                        NPC(self, col, row)
                    elif (settings.currentTilemap[row])[col] == 'T':
                        Teleport(self, col, row)
                    #print(f"{col}", end="")
                #print()
            self.map = 1
        else:
            self.all_sprites.empty()
            self.blocks.empty()
            self.flowers.empty()
            self.ores.empty()
            self.npcs.empty()
            self.teleport.empty()
            mapNumber = settings.nextTilemap[0][-1]
            for row in range(len(settings.nextTilemap)):
                #print(f"{row} ", end="")d
                for col in range(len(settings.nextTilemap[row])):
                    if (settings.nextTilemap[row])[col] == "B":
                        Block(self, col, row)
                    elif (settings.nextTilemap[row])[col] == "F":
                        Flower(self, col, row, self.clock)
                    elif (settings.nextTilemap[row])[col] == 'O':
                        Ore(self, col, row)
                    elif (settings.nextTilemap[row])[col] == 'N':
                        NPC(self, col, row)
                    elif (settings.nextTilemap[row])[col] == 'T':
                        Teleport(self, col, row)
                        if int(mapNumber) == 1 and row == prevPosition[1]:
                            Player(self, col-1, row, self.clock)
                        elif int(mapNumber) == 2 and row == prevPosition[1]:
                            Player(self, col+1, row, self.clock)
            temp = settings.currentTilemap
            settings.currentTilemap = settings.nextTilemap
            settings.nextTilemap = temp

    def new(self):

        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.flowers = pygame.sprite.LayeredUpdates()
        self.ores = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.teleport = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
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

import pygame
import sys
from settings import *


# Code for the CutsceneManager and DialogueScene class, and many other things were obtained from
# https://www.codewithc.com/advanced-cutscene-creation-in-pygame/?amp=1

# Frame rate
clock = pygame.time.Clock()


# Cutscene manager class
class CutsceneManager:
    def __init__(self, game):
        self.scenes = []
        self.active_scene = None
        self.scene_index = 0
        self.game = game
        self.done = False

    def add_scene(self, scene):
        self.scenes.append(scene)

    def clear_scenes(self):
        self.scenes = []

    def start(self):
        if self.scenes:
            # print("Started")
            self.active_scene = self.scenes[0]
            self.scene_index = 0
            # print(self.active_scene)
            self.active_scene.start()

    def getCurrentScene(self):
        return self.active_scene

    def update(self):
        if self.active_scene is not None:
            if self.active_scene.is_finished():
                self.scene_index += 1
                if self.scene_index < len(self.scenes):
                    self.active_scene = self.scenes[self.scene_index]
                    self.active_scene.start()
                else:
                    self.active_scene = None
                    self.game.finishedScene = True
            else:
                self.active_scene.update()
        else:
            if self.scene_index >= len(self.scenes):
                self.game.finishedScene = True


    def draw(self, screen):
        if self.active_scene is not None:
            self.active_scene.draw(screen)
        else:
            self.done = True

    def finished(self):
        return self.done


# Base class for scenes
class Scene:
    def start(self):
        pass

    def update(self):
        pass

    def printSkip(self, screen):
        text = "Press Space to skip a cutscene"
        render_text = pygame.font.SysFont('Arial', 24).render(text, True, GRAY)
        text_rect = render_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.1))
        screen.blit(render_text, text_rect)


    def draw(self, screen):
        pass

    def is_finished(self):
        return True

class ImageScene(Scene):
    def __init__(self, text, duration, images, imageNum, fontColor=WHITE, skip=True):
        self.text = text
        self.duration = duration
        self.images = images
        self.imageNum = imageNum
        self.font = pygame.font.SysFont('Arial', 32)
        self.fontColor = fontColor
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.skipAppear = skip
        pass

    def __str__(self):
        return self.text

    def start(self):
        self.start_ticks = pygame.time.get_ticks()

    def update(self):
        current_ticks = pygame.time.get_ticks()
        self.elapsed_time = (current_ticks - self.start_ticks) / 1000

    def draw(self, screen):
        screen.fill(BLACK)
        currentImg = pygame.transform.scale(self.images[self.imageNum], (WIDTH//1.3, HEIGHT//1.68))
        imgRect = (WIDTH - WIDTH//1.125, HEIGHT - HEIGHT // 1.25)
        screen.blit(currentImg, imgRect)
        pygame.draw.rect(screen, (255, 255, 255),(WIDTH - WIDTH // 1.125, HEIGHT - HEIGHT // 1.25, WIDTH // 1.3, HEIGHT // 1.68), 2)
        render_text = self.font.render(self.text, True, self.fontColor)
        text_rect = render_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.2))
        screen.blit(render_text, text_rect)
        if self.skipAppear:
            self.printSkip(screen)
        pygame.display.update()
        pass

    def setSkip(self, skip):
        self.skipAppear = skip # skip should be a boolean value

    def is_finished(self):
        return self.elapsed_time >= self.duration

    def finishScene(self):
        self.elapsed_time = self.duration + 1


# Example of a specific scene
class DialogueScene(Scene):
    def __init__(self, text, duration):
        Scene.__init__(self)
        self.text = text
        self.duration = duration
        self.font = pygame.font.SysFont('Arial', 32)
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed_time = 0

    def __str__(self):
        return self.text

    def start(self):
        self.start_ticks = pygame.time.get_ticks()

    def update(self):
        current_ticks = pygame.time.get_ticks()
        self.elapsed_time = (current_ticks - self.start_ticks) / 1000

    def draw(self, screen):
        screen.fill(BLACK)
        render_text = self.font.render(self.text, True, WHITE)
        text_rect = render_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
        screen.blit(render_text, text_rect)
        self.printSkip(screen)


    def is_finished(self):
        return self.elapsed_time >= self.duration



sampleDialogueScene = [['Text 1',
                        'Text 2',
                        'Text 3',
                        'Text 4',
                        'Text 5'],
                       [6, 7, 7, 8, 9]]

def playIntroScene(cutscene_manager):
    # Create a cutscene manager and add scenes
    cutscene_manager.game.play_music('openingCutscene')
    cutscene_manager.game.state = 'scene'
    images = [pygame.image.load('Sprites/protag/protagBlobDown.png'),
              pygame.image.load('Sprites/protag/protagSwingDown.png'),
              pygame.image.load('Sprites/protag/protagThrowUp.png'),
              pygame.image.load('Sprites/protag/protagThrowDown.png'),
              pygame.image.load('Sprites/protag/protagRangedDown.png')]
    '''
    cutscene_manager.add_scene(DialogueScene(sampleDialogueScene[0][0], sampleDialogueScene[1][0]))
    cutscene_manager.add_scene(DialogueScene(sampleDialogueScene[0][1], sampleDialogueScene[1][1]))
    cutscene_manager.add_scene(DialogueScene(sampleDialogueScene[0][2], sampleDialogueScene[1][2]))
    cutscene_manager.add_scene(DialogueScene(sampleDialogueScene[0][3], sampleDialogueScene[1][3]))
    '''
    cutscene_manager.add_scene(ImageScene(sampleDialogueScene[0][0], sampleDialogueScene[1][0], images, 0))
    cutscene_manager.add_scene(ImageScene(sampleDialogueScene[0][1], sampleDialogueScene[1][1], images, 1))
    cutscene_manager.add_scene(ImageScene(sampleDialogueScene[0][2], sampleDialogueScene[1][2], images, 2))
    cutscene_manager.add_scene(ImageScene(sampleDialogueScene[0][3], sampleDialogueScene[1][3], images, 3))
    cutscene_manager.add_scene(ImageScene(sampleDialogueScene[0][4], sampleDialogueScene[1][4], images, 4))

    sceneTimeDuration = 0
    for i in sampleDialogueScene[1]:
        sceneTimeDuration += i
    cutscene_manager.start()
    start_ticks = 0
    elapsedTime = 0
    while not cutscene_manager.game.finishedScene:
        cutscene_manager.update()
        cutscene_manager.draw(cutscene_manager.game.screen)
        current_ticks = pygame.time.get_ticks()
        elapsedTime = (current_ticks - start_ticks) / 1000
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                cutscene_manager.game.cutsceneSkip = True
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                pygame.font.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.QUIT:
                pygame.font.quit()
                pygame.quit()
                sys.exit()
        if cutscene_manager.game.cutsceneSkip:
            if cutscene_manager.getCurrentScene() != None:
                cutscene_manager.getCurrentScene().finishScene()
                cutscene_manager.game.cutsceneSkip = False
        if elapsedTime > sceneTimeDuration or cutscene_manager.finished():
            cutscene_manager.game.finishedScene = True
            cutscene_manager.game.state = 'playing'
            cutscene_manager.game.new()
            #cutscene_manager.game.createTilemap(None)
            cutscene_manager.game.cutsceneSkip = False
            cutscene_manager.game.play_music('stop')

def playGameOver(cutscene_manager):
    cutscene_manager.game.play_music('death')
    cutscene_manager.clear_scenes()
    cutscene_manager.add_scene(ImageScene('You Died. Press R to restart or exit with Space / Escape', 300, [pygame.image.load('Sprites/deth.jpg').convert_alpha()], 0, WHITE, False))
    cutscene_manager.start()
    sceneTimeDuration = 300
    start_ticks = 0
    elapsedTime = 0
    cutscene_manager.game.finishedScene = False
    while not cutscene_manager.game.finishedScene:
        cutscene_manager.update()
        cutscene_manager.draw(cutscene_manager.game.screen)
        current_ticks = pygame.time.get_ticks()
        elapsedTime = (current_ticks - start_ticks) / 1000
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                cutscene_manager.game.cutsceneSkip = True
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                cutscene_manager.game.__init__()
                #cutscene_manager.game.new()
                cutscene_manager.game.intro_screen()
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                pygame.font.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.QUIT:
                pygame.font.quit()
                pygame.quit()
                sys.exit()
        if cutscene_manager.game.cutsceneSkip:
            elapsedTime = sceneTimeDuration + 1
        if elapsedTime > sceneTimeDuration:
            cutscene_manager.game.finishedScene = True
            cutscene_manager.game.cutsceneSkip = False
            cutscene_manager.game.play_music('stop')
            pygame.quit()
            sys.exit()
    pass

def playGameWon(cutscene_manager):
    cutscene_manager.game.play_music('win')
    cutscene_manager.clear_scenes()
    cutscene_manager.add_scene(ImageScene('You defeated the ceo of pollution and saved Everroot Forest. Nice job!', 15,
                                          [pygame.image.load('Sprites/hudImages/title3.png').convert_alpha()], 0, WHITE, False))
    cutscene_manager.add_scene(ImageScene('Now just to find that place...', 10,
                                          [pygame.image.load('Sprites/hudImages/title3.png').convert_alpha()], 0, WHITE,
                                          False))
    cutscene_manager.add_scene(ImageScene('Thanks for playing!', 200,
                                          [pygame.image.load('Sprites/hudImages/title3.png').convert_alpha()], 0, WHITE,
                                          False))
    cutscene_manager.start()
    sceneTimeDuration = 225
    start_ticks = 0
    elapsedTime = 0
    cutscene_manager.game.finishedScene = False
    while not cutscene_manager.game.finishedScene:
        cutscene_manager.update()
        cutscene_manager.draw(cutscene_manager.game.screen)
        current_ticks = pygame.time.get_ticks()
        elapsedTime = (current_ticks - start_ticks) / 1000
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                cutscene_manager.game.cutsceneSkip = True
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                cutscene_manager.game.__init__()
                # cutscene_manager.game.new()
                cutscene_manager.game.intro_screen()
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                pygame.font.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.QUIT:
                pygame.font.quit()
                pygame.quit()
                sys.exit()
        if cutscene_manager.game.cutsceneSkip:
            if cutscene_manager.getCurrentScene() != None:
                cutscene_manager.getCurrentScene().finishScene()
                cutscene_manager.game.cutsceneSkip = False
        if elapsedTime > sceneTimeDuration or cutscene_manager.finished():
            cutscene_manager.game.finishedScene = True
            # cutscene_manager.game.createTilemap(None)
            cutscene_manager.game.cutsceneSkip = False
            cutscene_manager.game.play_music('stop')
            pygame.quit()
            sys.exit()

def transition_Out(game):

    pass

def transition_In(game):
    pass

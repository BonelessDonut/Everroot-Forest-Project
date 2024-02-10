# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0.06
timepassed = 0

#Sprite cycles between the images in imagelist using imgindex
imagelist = [pygame.image.load('ci102lab/protagLattern(1).png'), pygame.image.load('ci102lab/protagLatternAlt(2).png')]
imgindex = 1
#player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
border = pygame.Rect(1000, 100, 4, 400)
sprite = pygame.Rect(0, 0, 120, 80)
sprite.centerx = screen.get_width() /2
sprite.centery = screen.get_height() /2

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    keys = pygame.key.get_pressed()
    #Below keys edit movement and swaps sprites 
    if keys[pygame.K_w]:
        sprite.y -= 300 * dt
        imgindex = not imgindex if (timepassed//(0.30)%2 == imgindex) else imgindex
    if keys[pygame.K_s]:
        sprite.y += 300 * dt
        imgindex = not imgindex if (timepassed//(0.30)%2 == imgindex) else imgindex
    if keys[pygame.K_a]:
        sprite.x -= 300 * dt
        imgindex = not imgindex if (timepassed//(0.30)%2 == imgindex) else imgindex
    if keys[pygame.K_d]:
        sprite.x += 300 * dt
        imgindex = not imgindex if (timepassed//(0.30)%2 == imgindex) else imgindex

    collide = border.colliderect(sprite)
    color1 = 'purple' if collide else 'green'
    color2 = 'blue' if collide else 'red'
    pygame.draw.rect(screen, color1, border)
    #imgindex = not imgindex if (timepassed//(0.35)%2 == imgindex) else imgindex
    pygame.Surface.blit(screen, pygame.transform.scale(imagelist[imgindex], (120, 80)), sprite)
    #pygame.draw.circle(screen, color2, (sprite.x, sprite.y) or do player_pos, 40)

    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    timepassed += dt

pygame.quit()
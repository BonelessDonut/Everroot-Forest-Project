WIDTH = 1280
HEIGHT = 720
TILESIZE = 40

GREEN = (20, 145, 54)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60

PLAYER_LAYER = 1
PLAYER_SPEED = 4
BLOCK_LAYER = 2
GROUND_LAYER = 3

#tiles to represent the world, each 'B' represents a block, the 'P' is the player's position
#There are 32 horizontal tiles (width of 1280 / 40) and 18 vertical tiles (height of 720 / 40))
tilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..............................B',
    'B..........BBBB................B',
    'B.........BB..BB...............B',
    'B.........BB..BB...............B',
    'B..............................B',
    'B..................B.B.........B',
    'B..............................B',
    'B.....BBBBBBB..................B',
    'B...............P..............B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]
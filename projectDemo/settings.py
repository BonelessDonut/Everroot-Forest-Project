WIDTH = 1280
HEIGHT = 720
TILESIZE = 40

GREEN = (20, 145, 54)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FPS = 60

TEXT_LAYER = 4
PLAYER_LAYER = 2
PLAYER_SPEED = 5
BLOCK_LAYER = 1
GROUND_LAYER = 3

#tiles to represent the world, each 'B' represents a block, the 'P' is the player's position
#There are 32 horizontal tiles (width of 1280 / 40) and 18 vertical tiles (height of 720 / 40))
currentTilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB1',
    'B..............................B',
    'B..........BBBB................B',
    'B.........BBF.BB......O........B',
    'B.........BB..BB...............B',
    'B..............................B',
    'B...F..............B.B.........B',
    'B..............................T',
    'B.....BBBBBBB..................B',
    'B...............P......N.......B',
    'B..............................B',
    'B.......O.................O....B',
    'B....................F.........B',
    'B.......F......................B',
    'B..............O...............B',
    'B..............................B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]

nextTilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB2',
    'B..............................B',
    'B..............................B',
    'B.........BBF.BB......O........B',
    'B.........BB..BB...............B',
    'B..........BBBB................B',
    'B...F..............B.B.........B',
    'T.......B....N.................B',
    'B.......B......................B',
    'B.......B......................B',
    'B.......B......................B',
    'B.......O.................O....B',
    'B....................F.........B',
    'B.......F......................B',
    'B..............O...............B',
    'B..............................B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]
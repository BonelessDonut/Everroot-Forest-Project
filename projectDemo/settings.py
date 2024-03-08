WIDTH = 1280
HEIGHT = 720
TILESIZE = 40

GREEN = (20, 145, 54)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

FPS = 60

TEXT_LAYER = 5
ITEM_LAYER = 2
PLAYER_LAYER = 3
PLAYER_SPEED = 5
BLOCK_LAYER = 4
GROUND_LAYER = 1

mapList = [[-1, 2, -1],
           [4, 0, 1],
           [-1, 3, -1]]

#tiles to represent the world, each 'B' represents a block, the 'P' is the player's position
#There are 32 horizontal tiles (width of 1280 / 40) and 18 vertical tiles (height of 720 / 40))
currentTilemap = [[
    'BBBBBBBBBBBBBBBTTBBBBBBBBBBBBBBB',
    'B..............................B',
    'B..........BBBB................B',
    'B.........BBF.BB......O........B',
    'B.........BB..BB...............B',
    'B..............................B',
    'B...F..............B.B.........B',
    'B..............................T',
    'B.....BBBBBBB..................T',
    'B...............P......N.......B',
    'B..............................B',
    'B.......O.....F...........O....B',
    'T....................F.........B',
    'T.......F......................B',
    'B..............O...............B',
    'B.......................F......B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBTTBBBBBBBBB'
], [#right
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..............................B',
    'B..............................B',
    'B.........BBF.BB......O........B',
    'B.........BB..BB...............B',
    'B..........BBBB................B',
    'B...F..............B.B.........B',
    'T.......B....N.................B',
    'T.......B......................B',
    'B.......B......................B',
    'B.......B......................B',
    'B.......O.................O....B',
    'B....................F.........B',
    'B.......F......................B',
    'B..............O...............B',
    'B..............................B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [#up
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..............................B',
    'B..............................B',
    'B.........BBF.BB......O........B',
    'B.........BB..BB......N........B',
    'B..............................B',
    'B..............................B',
    'B.......B........B.............B',
    'B.......B........B.............B',
    'B.......B........B.............B',
    'B..............................B',
    'B....O..............O.....F....B',
    'B.....O............O...........B',
    'B......OOOOOOOOOOOO............B',
    'B..............................B',
    'B..............F........F......B',
    'B..............................B',
    'BBBBBBBBBBBBBBBTTBBBBBBBBBBBBBBB'
], [#down
    'BBBBBBBBBBBBBBBBBBBBBTTBBBBBBBBB',
    'B..............................B',
    'B..............................B',
    'B.....................O........B',
    'B..........F...................B',
    'B..............................B',
    'B...F..........................B',
    'B............O.................B',
    'B............O.................B',
    'B......................N.......B',
    'B..............................B',
    'B.........................O....B',
    'B..............O...............B',
    'B......O........O..............B',
    'B...............O..............B',
    'B...............O.......F......B',
    'B.............O................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [#left
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..............................B',
    'B..............................B',
    'B.........BBF.BB......O........B',
    'B.........BB..BB...............B',
    'B..............................B',
    'B...F..............B.B.........B',
    'B..............................B',
    'B.....BBBBBBB..................B',
    'B...............P......N.......B',
    'B..............................B',
    'B.......O.....F...........O....B',
    'B.........F....FF....F.....F...T',
    'B.......F.............F........T',
    'B..............O...............B',
    'B.......F...............F......B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]]
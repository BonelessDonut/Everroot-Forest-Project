WIDTH = 1280
HEIGHT = 720
TILESIZE = 40


GREEN = (20, 145, 54)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
ORANGE = (255, 200, 120)
SWAMPGREEN = (114, 134, 57)
BROWN = (109, 85, 49)
LIGHTBROWN = (178, 160, 129)
LIGHTGRAY = (189, 184, 177)
DARKGRAY = (169, 162, 152)
OFFWHITE = (232, 231, 228)

FPS = 60

TEXT_LAYER = 6
ITEM_LAYER = 4
PLAYER_LAYER = 3
ENEMY_LAYER = 2
PLAYER_SPEED = 4
BLOCK_LAYER = 5
GROUND_LAYER = 1
UNMADE_ROOM = -1

# -1 = rooms that will never be loaded | -2 = unloaded purple rooms | -3 = unloaded green rooms | -4 = unloaded boss room
mapList = [[-1, -1, -1, -1, -1, -1, -1, -1, -3, -2, -3, -1, -1,],
           [-1,  2, -1, -1, -2, -3, -1, -2, -2, -1, -1, -1, -1,],
           [ 4,  0,  1, -2, -2, -2, -2, -2, -2, -1, -2, -4, -1,],
           [-1,  3, -1, -3, -1, -2, -2, -1, -2, -2, -2, -1, -1,],
           [-1, -1, -1, -2, -2, -1, -3, -1, -1, -3, -1, -1, -1,],
           [-1, -1, -1, -1, -2, -2, -2, -1, -1, -1, -1, -1, -1]]

#tiles to represent the world, each 'B' represents a block, the 'P' is the player's position
#There are 32 horizontal tiles (width of 1280 / 40) and 18 vertical tiles (height of 720 / 40))
currentTileMap = [[ #index 0
    'BBBBBBBBBBBBBBBTTBBBBBBBBBBBBBBB1',
    'B..R...........................B',
    'B.R.R..........................B',
    'B.R.R..........................B',
    'B..R...........................B',
    'B..............................B',
    'B...F..............BBB.........B',
    'B..............................B',
    'T..............................T',
    'T.........................P....T',
    'B..............................B',
    'B.......O......................B',
    'B...................N..........B',
    'B.......F......................B',
    'B..............O...............B',
    'B.......E...............F......B',
    'B..............................B',
    'BBBBBBBBBBBBBBBTTBBBBBBBBBBBBBBB'
], [ #index 1
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB2',
    'B..............................B',
    'B.R............................B',
    'B.R.......BBF.BB......O........B',
    'B.R.......BB..BB...............B',
    'B.R........BBBB................B',
    'B...F..............B.B.........B',
    'B............N..WRS............B',
    'T................FF............T',
    'T................OO............T',
    'B..............................B',
    'B..............................B',
    'B....................F.........B',
    'B.......F......................B',
    'B..............O...............B',
    'B..............................B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [#index 2
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB3',
    'B..RR..........................B',
    'B.R..R.........................B',
    'B...R.....BBF.BB......O........B',
    'B..R......BB..BB......N........B',
    'B.RRRR.........................B',
    'B.......B........B.............B',
    'B.......B........B.............B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B....O..............O.....F....B',
    'B.....O............O...........B',
    'B......OOOOOOOOOOOO............B',
    'B..............................B',
    'B..............F........F......B',
    'B..............................B',
    'BBBBBBBBBBBBBBBTTBBBBBBBBBBBBBBB'
], [#index 3
    'BBBBBBBBBBBBBBBTTBBBBBBBBBBBBBBB4',
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
    'B..............O...............B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [#index 4
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB5',
    'BBBBB..........................B',
    'B..............................B',
    'B.........BBF.BB......O........B',
    'B.........BB..BB...............B',
    'B..............................B',
    'B...F....D.........B.B.........B',
    'B..............................B',
    'B.....BBBBBBB..................T',
    'B...............P..............T',
    'B..............................B',
    'B.......O.....F...........O....B',
    'B.........F....FF....F..E..F...B',
    'B.......F.............F........B',
    'B..........D...O...............B',
    'B.......F...............F......B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]]

purpleRandomRooms = [[
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..............................B',
    'B..............................B',
    'B.........B..E.......B.........B',
    'B........BB.....E....BB........B',
    'B....BBBBBB..........BBBBBB....B',
    'B..............................B',
    'B..........E...BB...E..........B',
    'B.............B..B.............B',
    'B.............B..B.............B',
    'B..........E...BB...E..........B',
    'B..............................B',
    'B....BBBBBB..........BBBBBB....B',
    'B........BB....E.....BB........B',
    'B.........B.......E..B.........B',
    'B..............................B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBB....................BBBBBB',
    'BBB..................E.......BBB',
    'BB........E...................BB',
    'BB.......BBBBBBBBBBBBBB.......BB',
    'B..............................B',
    'B..............................B',
    'B..............BB..............B',
    'B....BB....EBBBBBBBBE....BB....B',
    'B....BB....EBBBBBBBBE....BB....B',
    'B..............BB..............B',
    'B..............................B',
    'B..............................B',
    'BB.......BBBBBBBBBBBBBB.......BB',
    'BB........E...................BB',
    'BBB..................E.......BBB',
    'BBBBBB....................BBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..............................B',
    'B..............................B',
    'B..........E...................B',
    'B.....BBBBBB........B..BB......B',
    'B...BBBB..BBBB..E..B....BB.....B',
    'B..................B.....B.....B',
    'B..................BB...BB.....B',
    'B.......E......E....BBBBB......B',
    'B.....BBBBB...........E........B',
    'B....BB...BB...................B',
    'B....B.....B...................B',
    'B....BB....B...E..BBBB..BBBB...B',
    'B.....BB..B.........BBBBBB.....B',
    'B...................E..........B',
    'B..............................B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..............................B',
    'B..............................B',
    'B....B.........B..........B....B',
    'B............BB.BB.............B',
    'B.......B..............B.......B',
    'B.......BB..E.....E..BB........B',
    'B.......BB...........BB........B',
    'B........B....B.B....B.........B',
    'B........E....BBB....E.........B',
    'B..............B...............B',
    'B.....B.................B......B',
    'B.....BB....E.....E....BB......B',
    'B......B...............B.......B',
    'B..............B...............B',
    'B..............................B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBB........................BBBB',
    'BB......E.....................BB',
    'B..................E...........B',
    'B.........E....................B',
    'B..............................B',
    'B......BBBBBBBBBBBBBBBBBB......B',
    'B......BBBBBBBBBBBBBBBBBB......B',
    'B......BBBBBBBBBBBBBBBBBB......B',
    'B......BBBBBBBBBBBBBBBBBB......B',
    'B......BBBBBBBBBBBBBBBBBB......B',
    'B......BBBBBBBBBBBBBBBBBB......B',
    'B..............................B',
    'B....................E.........B',
    'B............E.................B',
    'BB......................E.....BB',
    'BBBB........................BBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBB........................BBBB',
    'BBBB.....E............E.....BBBB',
    'BBB........B........B........BBB',
    'BBB........BBBBBBBBBB........BBB',
    'BB....BB....BBBBBBBB....BB....BB',
    'B.....BB................BB.....B',
    'B.....BB................BB.....B',
    'B....BB.....E.......E....BB....B',
    'B....BB.....E.......E....BB....B',
    'B.....BB................BB.....B',
    'B.....BB................BB.....B',
    'BB....BB....BBBBBBBB....BB....BB',
    'BBB........BBBBBBBBBB........BBB',
    'BBB........B........B........BBB',
    'BBBB.....E............E.....BBBB',
    'BBBB........................BBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]]

#Authored by Charlenne Tan 4/27/2024
# B = block/wall | W = water | F = flower | P = path/bridge | S = stone/rock
greenRandomRooms = [[ # 0: water swirl room
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BWWWWWWWWWWWWW.......FFWWWWWWWWB',
    'BWWWWWWWWF............FFWWWWWWWB',
    'BWWWWWWFF..............FFFFWWWWB',
    'BWW............FWWFFF...FFFWWWWB',
    'BFF........CCCCWWWWWWF...FFFWWWB',
    'B..........CCCCCCWWWWW.....FWWWB',
    'B........FFWWCCCCCWWWWWF....WWWB',
    'B.......FFWWWWWCCCCWWWWW....CCCB',
    'B......FWWWWWWWCCCCCWWWF...CCCCB',
    'B.....FWWWWWFFFCCCCCCWWF...CFWWB',
    'B.....FWWWWFNFF.WWCCCCFFF..FFWWB',
    'BW...FFFWWWWWFFFFWWWCCCC....FWWB',
    'BW..FFFFWWWWWFFFWFWWWCCC....FFWB',
    'BWWFFFFFFWWWWWWWWWWWFFCC.....FFB',
    'BWWWWWWWWWWWWWWWWFFFFFF......FFB',
    'BWWWWWWWWWWWWWWFFFFF.......FFFFB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    ],[ # 1: balance room
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBFF....................BBBBB',
    'BBBFFF...BBBB.............FFFBBB',
    'BBFF...BB.....B.....BBBBBFFF..BB',
    'BF...BB.....BB.....B.....BB....B',
    'B...B......BFF....B........B...B',
    'B...B.....BFF....B...N......B..B',
    'B..B......BFF....B..........B..B',
    'B..B.......BBF....B.........B..B',
    'B..B.........B.....BB.......B..B',
    'B..B..........B......B......B..B',
    'B...B.....N...B......B.....B...B',
    'B...B........B......B......B...B',
    'B....BB.....B.....BB.....BB...FB',
    'BB..FFFBBBBB.....B.....BB...FFBB',
    'BBBFFF.............BBBB...FFFBBB',
    'BBBBB....................FFBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    ],[ # 2: stone walls room
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BRRRB.FFFRRRB....RR..BBRRRRRRF.B',
    'BRRBB..FFRRB......R....BRRRFFF.B',
    'BRRB..NFRRBF......BR....BR..NFRB',
    'BRRB....RRBFFFFF...BR....B..FRRB',
    'B.RB....RRBRRRFFF...RR.......RBB',
    'B.RRB..RRRRRRRRRR...........RB.B',
    'B.RRB..RFRRRRBRRRR..........RB.B',
    'B..R....FFFRRBBB......RR...RB..B',
    'B..R.....FRRB.......RRRR...B...B',
    'B..R......RRB....RRRRRFF..RB...B',
    'B....R....RB...RRRRRFFF...RB...B',
    'BFF..RB..RB.....RBBRRFF..RB....B',
    'BFFRRRB..R.........BRRF.......FB',
    'BFRRRB......RR......BR.......FFB',
    'B.RRRB....BRR.......FFR...RRRFFB',
    'B.RRB....BRR.......FFFFR...RRRRB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    ],[ # 3: rocky caves room
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBR...RWWWWR..........RRRWWWWWB',
    'BBR.....RWWR..............RRWWWB',
    'BBR.....RWR...........RR....RRWB',
    'BR.......R...........RRRR....RRB',
    'B...................RWWWR.....RB',
    'B.........RRRRR....RRWWWR......B',
    'B.......RR....RRR.FRRWWR.......B',
    'B.....RR...N.....FFFFRRR.......B',
    'B....FFRR.......F...F.R........B',
    'B.....FFFRR...RR......R........B',
    'B.......FFFRRR........R........B',
    'B.........FF...................B',
    'BR...........................FRB',
    'BRRW....R..RRRR...........FFRRBB',
    'BRRWWWWWRRRRR..........FFFFRRRBB',
    'BBRRWWWWWRRR.........FFFFRRRRBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    ],[ # 4: forest room
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BGF......FGGG......GGGGRRGG....B',
    'BFGF..S.FGGSGGF......FGGRGFF...B',
    'B.GG....FFFFFF........FGGFF....B',
    'B.....GG......G.........F..S...B',
    'B.....GG......G..............FGB',
    'B....GGG...FGGGG............FFFB',
    'B...FGRRF.FFGRGGG.....GG.......B',
    'B...GGGF...FFFGGG...SGGG.......B',
    'B..............NR..GGGRGG......B',
    'B...........GG......FFRRG......B',
    'BG.S.......GGGG......FFFGN.....B',
    'BGG......GGGRRGF...G...FFF...SGB',
    'BGGFF...FFGGFFFF..GGG.......FGGB',
    'BGGGF.....S.......GRGG.....FFGRB',
    'BRGGGFF.........FGGRGGF....FGGGB',
    'BRGGGGF.S........FGRRGGF..FFFFFB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    ],[ # 5: deforestation room
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B.............B.........SSSSSGGB',
    'B..........GG.B........GGGGSSGGB',
    'B..G..G...G..GB....S.....GGGGG.B',
    'B..G..G...GGGGB.GSSGG..........B',
    'B..G.G....GG..B.GSSGG.S........B',
    'B..G.....G....B.GSGG.SSS.......B',
    'BBBBBBBBBBBBBBB.GGG..GSSSGG....B',
    'B...........GGS.GG...GGGSSG....B',
    'BG..........GGSS.......GGGG....B',
    'BGG........S.GGSG..............B',
    'BSSG....GGSSG.GGG.GSSGG.......GB',
    'BSSG....GSSGG.....GSSSG......G.B',
    'BSG.....GGGG.......GSSG......GGB',
    'BGGGSSGG...........GGGG...N.GGSB',
    'BG.GGSSG...................GGSSB',
    'B.G.GGGG...GG..............GSSSB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    ]]

redMap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BWWWWWWWW..............WWWWWWWWB',
    'BWWWWWW..................WWWWWWB',
    'BWWWWW....................WWWWWB',
    'BWWWW......................WWWWB',
    'BWWWW.......................WWWB',
    'BWWW........................WWWB',
    'BWW.........................WWWB',
    'B............................WWB',
    'B............................WWB',
    'BWW.........................WWWB',
    'BWWW........................WWWB',
    'BWWWW.......................WWWB',
    'BWWWW......................WWWWB',
    'BWWWWW....................WWWWWB',
    'BWWWWWW..................WWWWWWB',
    'BWWWWWWWW..............WWWWWWWWB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB']

#Room template
template = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB']

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
PURPLE = (82,71,150)
PINK = (255, 192, 203)

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
mapList = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -3, -2, -3, -1, -1,],
           [-1,  2, -1, -1, -1, -3, -1, -1, -2, -2, -1, -1, -1, -1,],
           [ 4,  0,  1, -2, -2, -2, -2, -4, -1, -2, -1, -2, -4, -1,],
           [-1,  3, -1, -3, -1, -2, -2, -1, -1, -2, -2, -2, -1, -1,],
           [-1, -1, -1, -2, -2, -1, -3, -1, -1, -1, -3, -1, -1, -1,],
           [-1, -1, -1, -1, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1]]

#tiles to represent the world, each 'B' represents a block, the 'P' is the player's position
#There are 32 horizontal tiles (width of 1280 / 40) and 18 vertical tiles (height of 720 / 40))
currentTileMap = [[ #index 0
    'BBBBBBBBBBBBBBBTTBBBBBBBBBBBBBBBg',
    'BSSBBBBBBBBB.GGGGG...SSSSSSS...B',
    'BSSBB.....BB..GGG...SSSS.SS..SSB',
    'BSSBB.....BB...GGG.........SS..B',
    'BSBBB.....BB...GGG.............B',
    'BS........SSS..SGGG............B',
    'B.............SS.GGGBB.........B',
    'B..........SS....GGGG..........B',
    'TGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGT',
    'TGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGT',
    'BGGG.......GGGGGG.......P......B',
    'B..SSS..O...GGGG...........SS..B',
    'B...SS.......GGG....N.....SSS..B',
    'BSS.....F.....GGG.............SB',
    'BSSS..........GGG......S.SS....B',
    'BSSSSS.........GG....SSSF.S...SB',
    'B....SSSS......GGG..SSSSS...SSSB',
    'BBBBBBBBBBBBBBBTTBBBBBBBBBBBBBBB'
], [ #index 1
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBg',
    'BSSSSSSSSSSSSS.........SSSS....B',
    'BSSSSSSS................SSSWWWWB',
    'BS........BBF.BB......O...SSWWWB',
    'B.........BB..BB............SWWB',
    'B...........BBBB.............CCB',
    'B...F..............B.B.........B',
    'BGGGGGGGGGGG....WRS...G...G..G.B',
    'TGGGGGGGGGGGGGGGG.GGGG.GGG.GG.GT',
    'TGGGGGGGGGGGGGG.GGG.GGG.G.G..G.T',
    'BGGGGGGGGG.....G..G...G....G...B', 
    'B..............................B',
    'B....................F.........B',
    'B.......F....................S.B',
    'BSS............O...........SS..B',
    'BSSSSS...............SSS..SSSSSB',
    'B.....SSSSSSS.......SSSSSSSSSSSB',

    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [#index 2
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBg',
    'B..RR..........................B',
    'B.R..R..O......................B',
    'B...R.....BBF.BB......O........B',
    'B..R......BB..BB...............B',
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
    'BBBBBBBBBBBBBBBTTBBBBBBBBBBBBBBBg',
    'B..............................B',
    'B....F.........................B',
    'B.....................O........B',
    'B..........F...................B',
    'B..............................B',
    'B...F..........................B',
    'B............O.................B',
    'B............O.................B',
    'B..............................B',
    'B..............................B',
    'B.........................O....B',
    'B..............O...............B',
    'B......O........O..............B',
    'B...............O..............B',
    'B...............O.......F......B',
    'B..............O...............B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [#index 4
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBg', 
    'BBBBB..........................B',
    'B..............................B',
    'B.........BBF.BB......O........B',
    'B.........BB..BB...............B',
    'B........................O.....B',
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
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBp',
    'B..............................B',
    'B........E............D........B',
    'B.........B..........B.........B',
    'B........BB.....E....BB........B',
    'B....BBBBBB..........BBBBBB....B', 
    'B..............................B',
    'B..........D...BB...E..........B', 
    'B.............B..B.............B',
    'B.............B..B.............B',
    'B..........E...BB...D..........B', 
    'B..............................B',
    'B....BBBBBB..........BBBBBB....B', 
    'B........BB....E.....BB........B',
    'B.........B..........B.........B',
    'B........D............E........B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBp',
    'BBBBBB....................BBBBBB', 
    'BBB.....E............D.......BBB',
    'BB............................BB',
    'BB.......BBBBBBBBBBBBBB.......BB',
    'B.........D..........E.........B', 
    'B..............................B',
    'B..............BB..............B',
    'B....BB.E...BBBBBBBB...E.BB....B',
    'B....BB.....BBBBBBBB.....BB....B',
    'B..............BB..............B',
    'B..............................B',
    'B.........E..........D.........B',
    'BB.......BBBBBBBBBBBBBB.......BB', 
    'BB........D...................BB',
    'BBB..................E.......BBB',
    'BBBBBB....................BBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBp',
    'B..............................B',
    'B..............................B',
    'B..........D.............E.....B',
    'B......BBBB.........B..BB......B',
    'B....BBB..BBB......B....BB.....B',
    'B..................B.....B.....B',
    'B..................BB...BB.....B',
    'B.......E......D....BBBBB......B', 
    'B.....BBBBB...........E........B',
    'B....BB...BB...................B',
    'B....B.....B...................B',
    'B....BB....B.......BBB..BBB....B',
    'B.....BB..B..........BBBB......B',
    'B.....E.............D..........B',
    'B..............................B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBp',
    'B..............................B',
    'B..............................B',
    'B....B...E.....B.....E....B....B', 
    'B............BB.BB.............B',
    'B.......B..............B.......B',
    'B.......BB...........BB........B',
    'B.......BB...........BB........B', 
    'B........B....B.B....B.........B',
    'B........D....BBB....D.........B',
    'B..............B...............B',
    'B.....B.................B......B',
    'B.....BB...............BB......B',
    'B......B...............B.......B', 
    'B..........E....B....E.........B',
    'B..............................B',
    'B..............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBp',
    'BBBB........................BBBB',
    'BB......E.....................BB',
    'B........................E.....B',
    'B..E...........................B',
    'B..............................B',
    'B......BBBBBBBBBBBBBBBBBB......B',
    'B......BBBBBBBBBBBBBBBBBB......B', 
    'B......BBBBBBBBBBBBBBBBBB......B',
    'B......BBBBBBBBBBBBBBBBBB......B',
    'B......BBBBBBBBBBBBBBBBBB......B',
    'B......BBBBBBBBBBBBBBBBBB......B', 
    'B..............................B',
    'B...........................E..B',
    'B......E.......................B',
    'BB......................E.....BB',
    'BBBB........................BBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
], [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBp',
    'BBBB........................BBBB',
    'BBBB................E.......BBBB',
    'BBB........B........B........BBB',
    'BBB.E......BBBBBBBBBB........BBB',
    'BB....BB....BBBBBBBB....BB....BB',
    'B.....BB..E..........D..BB.....B', 
    'B.....BB................BB.....B',
    'B....BB................,.BB....B',
    'B....BB........D.........BB....B',
    'B.....BB................BB.....B',
    'B.....BB..D..........E..BB.....B',
    'BB....BB....BBBBBBBB....BB....BB',
    'BBB........BBBBBBBBBB......E.BBB',
    'BBB........B........B........BBB', 
    'BBBB.......E................BBBB',
    'BBBB........................BBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]]

#Authored by Charlenne Tan 4/27/2024
# B = block/wall | W = water | F = flower | P = path/bridge | S = stone/rock
greenRandomRooms = [[ # 0: water swirl room
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBg',
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
    'BWWWWWWWWWWWWWWFFFFF........FFFB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    ],[ # 1: balance room
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBg',
    'BBBBBFF.....................BBBB',
    'BBBFFF...BBBB..............FFBBB',
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
    'BBBFF..............BBBB...FFFBBB',
    'BBBB.....................FFBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    ],[ # 2: stone walls room
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBg',
    'BRRRB.FFFRRRB....RR..BBRRRRRRF.B',
    'BRRBB..FFRRB......R....BRRRFFF.B',
    'BRRB..NFRRB.......BR....BRFFFFRB', 
    'BRRB....RRBFF......BR....B..FRRB',
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
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBg',
    'BBBBBRR..RWWWWR........RRRWWWWWB',
    'BBBBRR....RWWR............RRWWWB',
    'BBBBR....RWR..........RR...RWWWB', 
    'BBBR.....R...........RRRR...RWWB',
    'BBRR................RWWWR....RWB',
    'BBR.......RRRRR....RRWWWR....RWB',
    'BR......RR....RRR.FRRWWR......RB', 
    'B.....RR...N.....FFFFRRR......RB',
    'B....FFRR.......F...F.R........B',
    'B.....FFFRR...RR......R.......RB', 
    'BR......FFFRRR........R.......RB',
    'BR........FF.................RRB',
    'BRR........................FRRBB', 
    'BRRWWW.....RRRR.........FFRRRBBB',
    'BRRWWWWWRRRRR......FFFFRRRRBBBBB',
    'BBRRWWWWWRRR....FFFFRRRRRBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    ],[ # 4: forest room
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBg',
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
    'BG.S.......GGGG......FFFG......B',
    'BGG......GGGRRGF...G...FFF...SGB',
    'BGGFF...FFGGFFFF..GGG.......FGGB',
    'BGGGF.....S.......GRGG.....FFGRB',
    'BRGGGFF.........FGGRGGF....FGGGB',
    'BRGGGGF.S........FGRRGGF..FFFFFB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    ],[ # 5: deforestation room
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBg',
    'BOOOFFFF......B.........SSSSSGGB',
    'BFFGGG.....GG.BFFF.....GGGGSSGGB',
    'B.FGFFG...G..GBFF..S.....GGGGG.B',
    'B..GF.G...GGGGBFGSSGG..........B',
    'B..G.G....GG..B.GSSGG.S........B',
    'B..G.....G....B.GSGG.SSS.......B', 
    'BBBBBBBBBBBBBBB.GGG..GSSSGG....B',
    'B...........GGS.GG...GGGSSG....B',
    'BG..........GGSS.......GGGG....B', 
    'BGG........S.GGSG..............B',
    'BSSG....GGSSG.GGG.GSSGG.......GB',
    'BSSG....GSSGGFF...GSSSG......G.B',
    'BSG.....GGGGFFF....GSSG......GGB',
    'BGGGSSGG...........GGGG...N.GGSB', 
    'BG.GGSSG...................GGSSB',
    'B.G.GGGG...GG..............GSSSB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    ]]

redMap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBr',
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

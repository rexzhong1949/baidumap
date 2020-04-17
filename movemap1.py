import random, sys, time, math, pygame
from pygame.locals import *
import TileToLnglat

FPS = 30 # frames per second to update the screen
WINWIDTH = 1024 # width of the program's window, in pixels
WINHEIGHT = 500 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

WHITE = (255, 255, 255)
RED   = (255, 0  , 0)
BLUE  = (0  , 0  , 255)


def main():
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    # load the image files
    MAP_IMG = pygame.image.load('./complexLevel/01-final_Map.png')
    map_rect = MAP_IMG.get_rect()
    print(map_rect)

    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    BASICFONT = pygame.font.Font('freesansbold.ttf', 24)



    gRect = pygame.Rect((0,
                         0,
                         WINWIDTH,
                         WINHEIGHT))
    DISPLAYSURF.blit(MAP_IMG, (0, 0), gRect)

    camerax=0
    cameray=0

    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'
    NOMOVE = 'nomove'
    move = NOMOVE
    MOVERATE = 50

    Xpix = 0
    Ypix = 0

    while True:
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_LEFT, K_a):
                    move = LEFT
                elif event.key in (K_RIGHT, K_d):
                    move = RIGHT
                elif event.key in (K_UP, K_w):
                    move = UP
                elif event.key in (K_DOWN, K_s):
                    move = DOWN
            elif event.type == KEYUP:
                if event.key in (K_RIGHT, K_d, K_LEFT, K_a,K_UP, K_w,K_DOWN, K_s):
                    move = NOMOVE
            elif event.type == MOUSEBUTTONUP:
                Xpix,Ypix = event.pos

        if move == LEFT:
            if camerax-MOVERATE >= 0:
                camerax -= MOVERATE
        elif move == RIGHT:
            if camerax+MOVERATE <= map_rect[2]-WINWIDTH:
                camerax += MOVERATE

        if move == UP:
            if cameray-MOVERATE >= 0:
                cameray -= MOVERATE
        elif move == DOWN:
            if cameray+MOVERATE <= map_rect[3]-WINHEIGHT:
                cameray += MOVERATE

        gRect = pygame.Rect((camerax,
                             cameray,
                             camerax + WINWIDTH,
                             cameray + WINHEIGHT))
        DISPLAYSURF.blit(MAP_IMG, (0, 0), gRect)

        #显示鼠标处的坐标
        if Xpix!=0 or Ypix!=0:
            #我们用的地图的左下角瓦块是（92575,26767），先要转换成瓦片的像素坐标，然后转换成墨卡托坐标，最后才能转换成百度地图的坐标。
            #在计算瓦片像素坐标时，要记住百度瓦片的0点在左下角（至少对于中国所在的区域，也就是坐标系的第一象限是如此）
            #因此，x轴的起始瓦块值为92575，但y轴就不一样了，
            Tile_x = 92575+int((camerax+Xpix)/256.0)
            Tile_y = 26766 + int((map_rect[3] - cameray - Ypix) / 256.0)
            x, y = TileToLnglat.TilePixel2Mercator(Tile_x, Xpix, Tile_y, Ypix, 19)
            Lnglat = TileToLnglat.Mercator2BD09(x, y)
            print(Lnglat)
            infoSurf = BASICFONT.render('Lnglat:{Tile_x},{Tile_y}'.format(Tile_x=Lnglat[0], Tile_y=Lnglat[1]), 1,RED)
            infoRect = infoSurf.get_rect()
            infoRect.topleft = (10, 25)
            DISPLAYSURF.blit(infoSurf, infoRect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
import pygame
import os
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 24

SCREEN_WIDTH =800
SCREEN_HEIGHT=500

SCREEN = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT ))

scroll = 0
bg_images= []  #空list
for i in range(6,11):             #create by craftpix.net
    bg_image = pygame.image.load(os.path.join("Background",f"plx-{i}.png")).convert_alpha()  
    bg_images.append(bg_image)      #照片疊加
bg_width = bg_images[0].get_width()

tiles = math.ceil(SCREEN_WIDTH / bg_width)  +1   #拼貼在右側
#print(tiles)

def draw_bg():
    for x in range(0,tiles):                          #迴圈 每一層速度加快
        speed = 1                               #  x設定張數 因為素材大小跟視窗不合
        for i in bg_images:
            SCREEN.blit(i, ((x *bg_width) - scroll *speed, 0))  
            speed+=  0.2





run = True
while run:

    clock.tick(FPS)
    draw_bg()
    scroll +=3
    if abs(scroll) > bg_width:
        scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
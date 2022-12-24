import pygame, sys
from button import Button
import math
import os





pygame.init()
clock = pygame.time.Clock()
FPS = 24

SCREEN_WIDTH =800
SCREEN_HEIGHT=500

SCREEN = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT ))

pygame.display.set_caption("Menu")

LACK = (21, 24, 29)
BLUE = (31, 25, 76)
RED = (252, 91, 122)
WHITE = (255, 255, 255)
LAWNGREEN = (124, 255,127)

bg = pygame.image.load("Background/bg.png")    #Cyberpunk Cityscape Backgrounds by FieraRyan
bg_width = bg.get_width()

tiles = math.ceil(SCREEN_WIDTH / bg_width)  +1   #拼貼在右側
print(tiles)

def get_font(size):                              #載入字形 
    return pygame.font.Font("Font/font.ttf", size)


 



def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(20).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(340, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(240, 460), 
                            text_input="BACK", font=get_font(25), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def p2():
    while True:
        P2_MOUSE_POS = pygame.mouse.get_pos()       #取得滑鼠位置

        SCREEN.fill("white")

        P2_TEXT = get_font(20).render("This is 2-player screen.", True, "Black")
        P2_RECT = P2_TEXT.get_rect(center=(340, 260))
        SCREEN.blit(P2_TEXT, P2_RECT)

        P2_BACK = Button(image=None, pos=(340, 460), 
                            text_input="BACK", font=get_font(25), base_color="Black", hovering_color="Green")

        P2_BACK.changeColor(P2_MOUSE_POS)
        P2_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if P2_BACK.checkForInput(P2_MOUSE_POS):
                    main_menu()

        pygame.display.update()



def main_menu():
    running= True
    scroll= 0
    while True or running:
        MENU_MOUSE_POS = pygame.mouse.get_pos()                    #讀取滑鼠位置
       
        clock.tick(FPS)
     
        for i in range(0, tiles):
            SCREEN.blit(bg, (i * bg_width + scroll, 0))

        scroll-= 5

        if abs(scroll) > bg_width:
            scroll = 0

        MENU_TEXT = get_font(100).render("TETRIS", True, "#b68f40")     #render 渲染      標題
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        P1_BUTTON = Button(image=pygame.image.load("Asset/Play Rect.png"), pos=(400, 390), 
                            text_input="Sigle Player", font=get_font(15), base_color="WHITE", hovering_color="LAWNGREEN")    #hovering_color  只到會變色
        P2_BUTTON = Button(image=pygame.image.load("Asset/Options Rect.png"), pos=(400,420), 
                            text_input="Two-player", font=get_font(15), base_color="WHITE", hovering_color="LAWNGREEN")      #base_colo  原本的顏色
        QUIT_BUTTON = Button(image=pygame.image.load("Asset/Quit Rect.png"), pos=(400, 450), 
                            text_input="Quit", font=get_font(15), base_color="WHITE", hovering_color="LAWNGREEN")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [P1_BUTTON, P2_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if P1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if P2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    p2()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
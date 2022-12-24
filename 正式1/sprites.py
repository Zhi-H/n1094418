import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('sheets/DinoSprites - mort.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (31, 25, 76)
RED = (252, 91, 122)
LAWNGREEN = (124, 255,127)

animation_list=[]
animation_steps = [4, 6, 3, 4]     #擷取的個數
action = 1                         #0=idle 1=run   2=生氣   3= 受傷
last_update= pygame.time.get_ticks()
animation_cooldown = 200
frame = 0
step_counter = 0

for animation in animation_steps:
	temp_img_list = []
	for _ in range(animation):
		temp_img_list.append(sprite_sheet.get_image(step_counter, 24, 24, 4, BLACK))
		step_counter +=1
	animation_list.append(temp_img_list)

print(animation_list)

run = True
while run:

	#update background
	screen.fill(BG)

	current_time = pygame.time.get_ticks()
	if current_time - last_update >= animation_cooldown:
		frame += 1
		last_update= current_time
		if frame >= len(animation_list[action]):      #條件回到初始
			frame =0

	screen.blit(animation_list[action][frame], (300, 400))              #2個參數   決定讀取位址
	

	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False


	
	pygame.draw.rect(screen, WHITE, (300,0,100,500),2)        #  技能邊條線
	pygame.draw.rect(screen, WHITE, (300,0,200,500),2)         
	pygame.draw.rect(screen, RED, (0, 500-120, 300,120))         #rect 矩形
	pygame.draw.rect(screen, BLUE, (500, 500-120, 500,120))




	pygame.display.update()

pygame.quit()
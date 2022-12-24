import os
import pygame
import sys
import random
import pygame.font
import time
pygame.init()

clos = 10						#遊戲網格列數，可以調整，>=8
rows = 20						#遊戲網格行數，可以調整
cell_size = 40					#一個網格的大小
block_size = cell_size - 1		#一個方塊的大小,小於等於cell_size
block_edge = int(block_size /2)	#方塊的立體感，數字>=1,數字越小立體感越強
fps = 40						#每秒幀數，建議範圍20-60，越大難度遞進越越緩

win_width = clos * 2 * cell_size + 6 * cell_size
win_hight = (rows + 1) * cell_size	
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400,40)
screen = pygame.display.set_mode((win_width, win_hight))
pygame.display.set_caption("Crystal方塊")

#在4*4的小網格內，以左上角座標為（0,0），7種方塊及其各形態4個方塊在小網格的相對座標
#移動時記錄小網路（0,0）點在遊戲網格的（x,y)，就知道4個方塊在遊戲網格中的位置
blocks = {
	1: [[(0,1),(1,1),(2,1),(3,1)],
		[(2,0),(2,1),(2,2),(2,3)]],		#I型
	2: [[(1,1),(2,1),(1,2),(2,2)]],		#O型
	3: [[(0,1),(1,1),(2,1),(1,2)],
		[(1,0),(0,1),(1,1),(1,2)],
		[(1,1),(0,2),(1,2),(2,2)],
		[(1,0),(1,1),(2,1),(1,2)]],		#T型
	4: [[(0,1),(1,1),(2,1),(0,2)],
		[(0,0),(1,0),(1,1),(1,2)],
		[(2,1),(0,2),(1,2),(2,2)],
		[(1,0),(1,1),(1,2),(2,2)]],		#L型
	5: [[(0,1),(1,1),(2,1),(2,2)],
		[(1,0),(1,1),(0,2),(1,2)],
		[(0,1),(0,2),(1,2),(2,2)],
		[(1,0),(2,0),(1,1),(1,2)]],		#J型
	6: [[(1,1),(2,1),(0,2),(1,2)],
		[(0,0),(0,1),(1,1),(1,2)]],		#s型
	7: [[(0,1),(1,1),(1,2),(2,2)],
		[(2,0),(1,1),(2,1),(1,2)]],}	#Z型
		
#第1個為網格底色，後7個為對應方塊的顏色，因為要加和原色相近的明暗邊，自定義色RGB值最小得不低於50，最高不超過205，否則出錯。	
#最後一個顏色（灰）用來畫NEXT方塊，也可以用NEXT方塊的next_key值來指向本色	
block_color = [(199,238,206),(200,50,50),(50,200,200),(50,50,200),(200,200,50),(200,50,200),(50,200,50),(125,50,125),(180,180,180)]

class Game_machine():
	def __init__(self,x0,y0):
		self.x0, self.y0 = x0, y0				#記錄player遊戲區（0，0）點在螢幕的座標
		self.rect = pygame.Rect(0,0,block_size, block_size)	#方塊矩形大小			
		self.display_array = [[0 for i in range(clos)] for j in range(rows)]	#遊戲區每格初始值設為0，為1時不能透過
		self.color_array = [[0 for i in range(clos)] for j in range(rows)]		#遊戲區每格的顏色block_color的索引值
		self.x, self.y = 0, 0					#記錄移動方塊（0，0）點在遊戲網格的（clo,row)位置
		self.key = 0							#記錄移動方塊在blocks的鍵，是哪種方塊 =figure
		self.index_ = 0							#記錄移動方塊形態的索引
		self.next_key = self.rand_key()			#記錄NEXT方塊在blocks的鍵		
		self.speed = fps						#速度，和幀率一致
		self.fall_buffer = self.speed			#自動下落的緩衝時間，螢幕每刷一次自動減1
		self.fall_speed_up = False				#是否加速下落
		self.score = 0
		self.lines = 0
		self.level = 0
		self.creat_new_block()
		#print(self.display_array)				
	def creat_new_block(self):
		#產生新的移動方塊和NEXT方塊，以第一形態作為初始形態
		self.key = self.next_key
		self.next_key = self.rand_key()
		self.index = 0
		self.x = 4					#初始列設在第4列
		self.y = -1					#初始高度設為-1,保證方塊在最頂部位置出現，研究每種方塊第一形態座標可以找到答案

	def rand_key(self):
		keys = [1,1,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,7,7]		#決定每種方塊出現機率
		return keys[random.randint(0,len(keys)-1)]
		
	def move(self, dx, dy):
		#方塊左、右、下移動：左：dx=-1,dy=0  右:dx=1,dy=0  下：dx=0,dy=1
		if self.can_move(self.index, dx, dy):
			self.x += dx
			self.y += dy
		elif dy:
			#不能下落：在頂部位置不能下落，遊戲結束，以下位置則停止移動
			if self.y <= 0:
				self.game_over()
			else:
				self.stop_move()
			
	def rotate(self):
		#方塊旋轉至下一形態，使用的順時針旋轉，被註釋的是逆時針旋轉
		next_index = (self.index + 1) % len(blocks[self.key])
		#next_index = (self.index - 1 + len(blocks[self.key])) % len(blocks[self.key])
		if self.can_move(next_index, 0, 0):
			self.index = next_index
	
	def can_move(self, index, dx, dy):
		#方塊能否移動:出界或碰到其他方塊
		for (x,y) in blocks[self.key][index]:
			clo, row = self.x + x + dx , self.y + y + dy
			if clo >= clos  or clo < 0 or row >= rows or row < 0:	#出界
				return False
			if self.display_array[row][clo]:			#值等於1時不能移動
				return False
		return True

	def stop_move(self):
		#方塊停止移動，停落區域賦值1和相應的顏色
		self.score += 4	
		for (x,y) in  blocks[self.key][self.index]:
			self.display_array[y+self.y][x+self.x] = 1
			self.color_array[y+self.y][x+self.x] = self.key
		self.del_full_row()	
		self.creat_new_block()	
	
	def del_full_row(self):
		#刪除填滿的行，記錄成績
		lines = 0		
		for row in range(rows):
			if sum(self.display_array[row]) == clos:			#填滿行判斷
				lines += 1				#記錄一次連續刪除的行數，實現多消多獎
				self.lines += 1
				if self.lines % 5 == 0:				#每消5行等級升1，速度加快
					self.level = self.lines / 5
					self.speed = int(self.speed * 0.9)			#越小越快
				self.score += (self.level + clos * lines) * 5
				
				del self.display_array[row]
				self.display_array.insert(0,[0 for i in range(clos)])
				
	def display(self):
		self.display_stop_blocks()
		self.display_next_blocks()
		self.display_move_blocks()
		self.display_score()
		
		#每刷一次緩衝計數減1，緩衝計數=0，或按住了向下鍵則下落一格
		self.fall_buffer -= 1
		if self.fall_buffer == 0 or self.fall_speed_up:
			self.fall_buffer = self.speed
			self.move(0,1)
				
	def display_stop_blocks(self):
		#顯示不移動的方塊，值為1畫彩色立體方塊，值為0畫底色塊
		for y in range(rows):
			for x in range(clos):
				self.rect.topleft = x * cell_size, y * cell_size
				if  self.display_array[y][x]:
					self.draw_block(self.color_array[y][x], 1)
				else:
					self.draw_block(0, 0)
					
	def display_next_blocks(self):
		#顯示下一個方塊
		for (x,y) in  blocks[self.next_key][0]:
			self.rect.topleft = x * cell_size , (y - 1) * cell_size
			self.draw_block(8, 1)		

	def display_move_blocks(self):
		#顯示移動的方塊
		for (x,y) in  blocks[self.key][self.index]:
			self.rect.topleft = (self.x + x) * cell_size, (self.y + y) * cell_size
			self.draw_block(self.key, 1)	

	def display_score(self):
		#顯示得分記錄
		text = "得分：%d  行數：%d  等級：%d" %(self.score,self.lines,self.level)
		self.img = pygame.font.SysFont("kaiti",25).render(text, True, (0,0,255))
		self.img_rect = self.img.get_rect()
		self.img_rect.topleft = (self.x0, rows* cell_size)
		screen.blit(self.img, self.img_rect)
				
	def game_over(self):
		#只是簡單的資料重新初始化後立即重新開始
		self.__init__(self.x0, self.y0)
						
	def draw_block(self, color_index, draw_edge):
		#在指定位置畫方塊
		(r,g,b) = block_color[color_index]
		self.rect.centerx = self.rect.left + self.x0 + int(cell_size / 2)
		self.rect.centery = self.rect.top + self.y0 + int(cell_size / 2)
		if draw_edge:
			#畫方塊明暗過度邊，增加立體感，x0~x4是方塊四角和中心的座標。
			x0 = self.rect.center					
			x1 = self.rect.topleft
			x2 = self.rect.topright
			x3 = self.rect.bottomright
			x4 = self.rect.bottomleft
			pygame.draw.polygon(screen, (r+50, g+50, b+50), (x0,x1,x2), 0)
			pygame.draw.polygon(screen, (r+20, g+20, b+20), (x0,x2,x3), 0)
			pygame.draw.polygon(screen, (r-50, g-50, b-50), (x0,x3,x4), 0)
			pygame.draw.polygon(screen, (r-20, g-20, b-20), (x0,x4,x1), 0)
			pygame.draw.rect(screen, (r,g,b), self.rect.inflate(-block_edge, -block_edge), 0)
		else:
			pygame.draw.rect(screen, (r,g,b), self.rect, 0)

time = pygame.time.Clock()	
player1 = Game_machine(0, 0)
player2 = Game_machine((clos + 6) * cell_size, 0)

while True:
	time.tick(fps)
	screen.fill((166,124,64))
	player1.display()
	player2.display()
	pygame.display.update()
		
	#移動旋轉控制			
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_g:			#player1 :g鍵右移動一格
				player1.move(1,0)
			elif event.key == pygame.K_d:		#player1 :d鍵左移動一格
				player1.move(-1,0)
			elif event.key == pygame.K_r:		#player1 :r鍵旋轉一次
				player1.rotate()
			elif event.key == pygame.K_f:		#player1 :f鍵加速下移
				player1.fall_speed_up = True
				
			if event.key == pygame.K_RIGHT:		#player2 :→鍵右移動一格
				player2.move(1,0)
			elif event.key == pygame.K_LEFT:	#player2 :←鍵左移動一格
				player2.move(-1,0)
			elif event.key == pygame.K_UP:		#player2 :↑鍵旋轉一次
				player2.rotate()
			elif event.key == pygame.K_DOWN:	#player2 :↓鍵加速下移
				player2.fall_speed_up = True
				
			elif event.key == pygame.K_q:
				sys.exit()
				
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_f:
				player1.fall_speed_up = False
			if event.key == pygame.K_DOWN:
				player2.fall_speed_up = False	
		elif event.type == pygame.QUIT:
			sys.exit()
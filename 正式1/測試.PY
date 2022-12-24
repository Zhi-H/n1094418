import random
import pygame
import spritesheet

pygame. init()

SCREEN = WIDTH , HEIGHT  = 800, 500
win = pygame.display.set_mode(SCREEN)

clock = pygame.time.Clock()
FPS = 24


CELLSIZE = 20
ROWS = 19     #橫排格子數  19
COLS = 15           #直排格子數  15


BLACK = (21, 24, 29)
BLUE = (31, 25, 76)
RED = (252, 91, 122)
WHITE = (255, 255, 255)

sprite_sheet_image = pygame.image.load('sheets/DinoSprites - mort.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

img1 = pygame.image.load('Asset/01.png')
img2 = pygame.image.load('Asset/02.png')
img3 = pygame.image.load('Asset/03.png')
img4 = pygame.image.load('Asset/04.png')

Asset = {
	1 : img1,
	2 : img2,
	3 : img3,
	4 : img4
}

font = pygame.font.Font('Font/Kramola.ttf',50)
font2= pygame.font.SysFont('cursive',25)



class Tetramino:                      #類  首字大寫
	# matrix
	# 0   1   2   3
	# 4   5   6   7
	# 8   9   10  11
	# 12  13  14  15

    FIGURES = {
		'I' : [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z' : [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S' : [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L' : [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J' : [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T' : [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O' : [[1, 2, 5, 6]]
	}

    TYPES = ['I', 'Z', 'S', 'L', 'J', 'T', 'O']

    def __init__(self, x, y): 
        self.x= x
        self.y= y  
        self.type = random.choice(self.TYPES)
        self.shape = self.FIGURES[self.type]        #[  ]              
        self.color = random.randint(1, 4)         #random+integer
        self.rotation = 0                          #旋轉 

    def image(self):                              #最終的圖形
        return self.shape[self.rotation]

    def rotate(self):                              #rotate 旋轉
        self.rotation = (self.rotation + 1) % len(self.shape)     #   1除以每總型態的變化型最少變化田型1種到變化最多的L型4種(1~4)的餘數


class Tetris:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.score = 0
        self.level = 1
        self.board = [[0 for j in range(cols)] for i in range(rows)]     #定義所以格子裡的初始值為0
        self.next = None 
        self.gameover = False                                             #gameover條件
        self.new_figure()

    def draw_grid(self):
        for i in range(self.rows+1):       
            pygame.draw.line(win,WHITE, (0, CELLSIZE*i),(WIDTH,CELLSIZE*i), 1)             #格子線   橫線
        for j in range(self.cols):       
            pygame.draw.line(win,WHITE, (CELLSIZE*j, 0),(CELLSIZE*j,HEIGHT-120))            #格子線    直線

    def new_figure(self):
        if not self.next:
            self.next = Tetramino( 5, 0)
        self.figure = self.next
        self.next = Tetramino( 5, 0)

    def intersects(self):                                                   # (x)左側無法通行<0   右側無法通行>0     (y)下方無法通行     
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y >  self.rows- 1 or \
                       j + self.figure.x >  self.cols- 1 or \
                       j + self.figure.x < 0 or \
                        self.board[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True

        return intersection

    def remove_line(self):
        rerun = False
        for y in range(self.rows-1,0, -1):
            is_full = True
            for x in range(0, self.cols):
                if self.board[y][x] == 0:
                        is_full = False

            if is_full:
                del self.board[y]        # del   刪除 
                self.board.insert(0, [0 for i in range(self.cols)])
                self.score += 1
                if self.score % 10 ==0:       #等級堤升條件
                    self.level+= 1       
                rerun = True   

        if rerun:
            self.remove_line()    

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.board[i + self.figure.y][j+ self.figure.x] =self.figure.color                     #如果超出邊界   產生一個新圖形
        self.remove_line()           
        self.new_figure()                        
        if self.intersects():
            self.gameover = True

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y +=1                   #x不變   y值加1    
        if self.intersects():  
            self.figure.y -= 1
            self.freeze()

    def go_side(self, dx):                  #x值得變化
        self.figure.x += dx
        if self.intersects():
            self.figure.x -= dx

    def rotate(self):
        rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():                     #似乎跟超過邊框長度不能旋轉
            self.figure.rotation = rotation

counter = 0
move_down = False
can_move = True                        
tetris = Tetris(ROWS, COLS)


#t = Tetramino(10,3)
#image = t.image()


running = True
while running:
    win.fill(BLACK)

    counter +=1                             #記數  關於計分數的累加
    if counter >= 10000:
        counter = 0

    if can_move:
        if counter % (FPS // (tetris.level *2)) == 0 or move_down:      #掉落速度的計算公式
            if not tetris.gameover:
                tetris.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:          #設定鍵盤觸發
            if can_move and not tetris.gameover:
                if event.key == pygame.K_LEFT:
                    tetris.go_side(-1)
               
                if event.key == pygame.K_RIGHT:
                    tetris.go_side(1)
              
                if event.key == pygame.K_UP:
                    tetris.rotate()

                if event.key == pygame.K_DOWN:
                    move_down = True

                if event.key == pygame.K_SPACE:               #space直落
                    tetris.go_space()

            if event.key == pygame.K_p:
                can_move = not can_move 

            if event.key == pygame.K_r:
               tetris.__init__(ROWS,COLS)

            if event.key == pygame.K_q:
               running = False  


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                move_down = False
               

    #tetris.draw_grid()          #畫格子

    for x in range(ROWS):
        for y in range(COLS):
            if tetris.board[x][y] >0:
                val =  tetris.board[x][y]
                img = Asset[val]
                win.blit(img,(y*CELLSIZE, x*CELLSIZE))
                pygame.draw.rect(win,WHITE, (y*CELLSIZE,x*CELLSIZE,CELLSIZE,CELLSIZE), 1)   #形狀的邊框




    if tetris.figure:
        for i in range(4):                                                                 #4 x 4 的方陣   0~15的數字
            for j in range(4):
                if i * 4 + j in tetris.figure.image():
                    x = CELLSIZE *(tetris.figure.x +j)
                    y = CELLSIZE *(tetris.figure.y +i) 
                    img = Asset[tetris.figure.color]
                    win.blit(img,(x, y))
                    pygame.draw.rect(win,WHITE, (x,y,CELLSIZE,CELLSIZE),1)                   #形狀的邊框
                #pygame.draw.rect(win,RED, (x,y,CELLSIZE,CELLSIZE))  #這串是測驗是否在格子裡的 到時能消除

    if tetris.gameover:
        rect = pygame.Rect(50,140, WIDTH-100, HEIGHT-350)
        pygame.draw.rect(win, BLACK,rect)
        pygame.draw.rect(win,WHITE, rect, 2)

        over = font2.render('Game Over' , True, RED)
        msg1 = font2.render('press r to restart', True ,WHITE)
        msg2 = font2.render('press q to quit', True, WHITE)

        win.blit(over, (rect.centerx-over.get_width()//2, rect.y+20))
        win.blit(msg1, (rect.centerx-msg1.get_width()//2, rect.y+80))
        win.blit(msg2, (rect.centerx-msg2.get_width()//2, rect.y+110))
         
    pygame.draw.rect(win, RED, (0, 380, 300,120))   #下方展示板  起始位置0 500-120 w=300       ,120是劃多大   2點連成一直線

    if tetris.next:
        for i in range(4):                                                                #諭示下一個圖形
            for j in range(4):
                if i * 4 + j in tetris.next.image():
                    x = CELLSIZE * (tetris.next.x +j - 4)
                    y = HEIGHT - 100 + CELLSIZE * (tetris.next.y +i) 
                    img = Asset[tetris.next.color]
                    win.blit(img,(x, y))

    scoreimg = font.render(f'{tetris.score}', True, WHITE)                  #底部等級 分數字形
    levelimg = font2.render(f'Level :{tetris.level}', True, WHITE)
    win.blit(scoreimg,(250-scoreimg.get_width()//2, HEIGHT-110))
    win.blit(levelimg,(250-levelimg.get_width()//2,HEIGHT-30))

    pygame.draw.rect(win, BLUE, (0,0,WIDTH,HEIGHT),2)        #外框描線     起始位置0 0  

    current_time = pygame.time.get_ticks()

	
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
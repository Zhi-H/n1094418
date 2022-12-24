import random
import pygame

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
LAWNGREEN = (124, 255,127)


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



class Tetramino:

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


    def __init__(self, x, y):                     #x y 映射4x4方塊
        self.x= x
        self.y= y  
        self.type = random.choice(self.TYPES)
        self.shape = self.FIGURES[self.type]        #[4總轉類型  ]              
        self.color = random.randint(1, 4)         #random+integer
        self.rotation = 0                          #旋轉 
        



    def image(self):                              #最終的圖形
        return self.shape[self.rotation]

    def rotate(self):                              #rotate 旋轉
       self.rotation = (self.rotation + 1) % len(self.shape)     #   1除以每總型態的變化型最少變化田型1種到變化最多的L型4種(1~4)的餘數


class Tetris1:
    def __init__(self, rows1, cols1):
        self.rows1 = rows1
        self.cols1 = cols1
        self.level = 1
        self.board1 = [[0 for j in range(cols1)] for i in range(rows1)]  
        self.rotation = 0 
       
        self.new_figure1()     
        print(self.board1)
		
    def draw_grid(self):   
        for i in range(self.rows1+1):       
            pygame.draw.line(win,WHITE, (0, CELLSIZE*i),(WIDTH,CELLSIZE*i), 1)             #格子線   橫線 P1
        for j in range(self.cols1):       
            pygame.draw.line(win,WHITE, (CELLSIZE*j, 0),(CELLSIZE*j,HEIGHT-120))            #格子線    直線
            
	
    def new_figure1(self):
        self.figure1 = Tetramino(5,0)
        
    def go_down(self):
        self.figure1.y +=1
        if self.intersects():
            self.figure1.y -=1
            self.freeze()

    def go_side(self, dx):                  #x值得變化
        self.figure1.x += dx
        if self.intersects():
            self.figure1.x -= dx

        
    def rotate(self):
        rotation = self.figure1.rotation
        self.figure1.rotate()

    def intersects(self):                                                   # (x)左側無法通行<0   右側無法通行>0     (y)下方無法通行     
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure1.image():
                    if i + self.figure1.y >  self.rows1- 1 or \
                       j + self.figure1.x >  self.cols1- 1 or \
                       j + self.figure1.x < 0 or \
                        self.board1[i + self.figure1.y][j + self.figure1.x] > 0:
                        intersection = True
        return intersection

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure1.image():
                    self.board1[i + self.figure1.y][j+ self.figure1.x] =self.figure1.color
        self.new_figure1()   

tetris1 = Tetris1(ROWS,COLS)








class Tetris2:
    def __init__(self, rows2, cols2):
        self.rows2 = rows2
        self.cols2= cols2 
        self.level = 1   
        self.board2 = [[0 for j in range(cols2)] for i in range(rows2)]  
        self.rotation = 0    
        self.new_figure2()     
        print(self.board2)



    def draw_grid(self):                  
        for j in range(self.cols2):       
            pygame.draw.line(win,WHITE, (CELLSIZE*j, 0),(CELLSIZE*j,HEIGHT-120))            #格子線    直線
        for K in range(15):       
         pygame.draw.line(win,LAWNGREEN, (500+(CELLSIZE*K),0),(500+(CELLSIZE*K),HEIGHT-120)) 

    def new_figure2(self):
        self.figure2 = Tetramino(30,0)

    def go_down(self):
        self.figure2.y +=1
        if self.intersects():
            self.figure2.y -=1
            self.freeze()

    def go_side(self, dx):                  #x值得變化
        self.figure2.x += dx
        if self.intersects():
            self.figure2.x -= dx

    def rotate(self):
        rotation = self.figure2.rotation
        self.figure2.rotate()

    def intersects(self):                                                   # (x)左側無法通行<0   右側無法通行>0     (y)下方無法通行     
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure2.image():
                    if i + self.figure2.y >  self.rows2- 1 or \
                       j + self.figure2.x >  self.cols2- 1 or \
                       j + self.figure2.x < 0 or \
                        self.board2[i + self.figure2.y][j + self.figure2.x] > 0:
                        intersection = True

        return intersection

    def freeze(self):
        for i in range(4):
           for j in range(4):
                if i * 4 + j in self.figure2.image():
                    self.board2[i + self.figure2.y][j+ self.figure2.x] =self.figure2.color
        self.new_figure2()   

tetris2 = Tetris2(ROWS,COLS)

















move_down1 = False
move_down2 = False
counter1 = 0
counter2 = 0
running = True
while running:
    win.fill(BLACK)

    counter1 +=1                             #記數  關於計分數的累加
    if counter1 >= 10000:
        counter1 = 0
    if counter1 % (FPS // (tetris1.level *2)) == 0 or move_down1:
        tetris1.go_down()
    
    #counter2 +=1                             #記數  關於計分數的累加
    #if counter2 >= 10000:
        #counter2 = 0
    #if counter2 % (FPS // (tetris2.level *2)) == 0 or move_down2:   #有問題 先跳過
        #tetris2.go_down()

   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

               
        

        if event.type == pygame.KEYDOWN:          #設定鍵盤觸發
            if event.key == pygame.K_g:			#player1 :g鍵右移動一格
                tetris1.go_side(1)
            elif event.key == pygame.K_d:		#player1 :d鍵左移動一格
               tetris1.go_side(-1)
            elif event.key == pygame.K_r:		#player1 :r鍵旋轉一次
                tetris1.rotate()
            elif event.key == pygame.K_f:
                move_down1 = True

            if event.key == pygame.K_LEFT:
                tetris2.go_side(-1)              
            elif event.key == pygame.K_RIGHT:
                tetris2.go_side(1)              
            elif event.key == pygame.K_UP:
                tetris2.rotate()
            elif event.key == pygame.K_DOWN:
                move_down2 = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                move_down1 = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                move_down2 = False

        

    tetris1.draw_grid()

    for x in range(ROWS):
        for y in range(COLS):
            if tetris1.board1[x][y] >0:
                val =  tetris1.board1[x][y]
                img = Asset[val]
                win.blit(img,(y*CELLSIZE, x*CELLSIZE))

    for i in range(4):                                                                 #4 x 4 的方陣   0~15的數字
            for j in range(4):
                if i * 4 + j in tetris1.figure1.image():
                    x = CELLSIZE *(tetris1.figure1.x +j)
                    y = CELLSIZE *(tetris1.figure1.y +i) 
                    img = Asset[tetris1.figure1.color]
                    win.blit(img,(x, y))
                  
    
    tetris2.draw_grid()

    #for x in range(ROWS):
        #for y in range(COLS):
            #if tetris2.board2[x][y] >0:
                #val =  tetris2.board2[x][y]
                #img = Asset[val]
                #win.blit(img,(y*CELLSIZE, x*CELLSIZE))




    for i in range(4):                                                                 #4 x 4 的方陣   0~15的數字
        for j in range(4):
            if i * 4 + j in tetris2.figure2.image():
                x = CELLSIZE *(tetris2.figure2.x +j)
                y = CELLSIZE *(tetris2.figure2.y +i) 
                img = Asset[tetris2.figure2.color]
                win.blit(img,(x, y))


    

    pygame.draw.rect(win, BLUE, (500, 380, 500,120))
    pygame.draw.rect(win, WHITE, (300,0,200,500),2)  



    pygame.draw.rect(win, RED, (0, 380, 300,120))         #rect 矩形  下方面板
    pygame.draw.rect(win, WHITE, (300,0,100,500),2)        #  技能邊條線
    pygame.draw.rect(win, BLUE, (0,0,WIDTH,HEIGHT),2)

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()






 
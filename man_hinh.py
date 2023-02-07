import pygame , sys
pygame.init()
screen = pygame.display.set_mode((600,600))
black= (0, 0, 0), # background
white= (255, 255, 255), 
blue= (0, 0, 255), # diem bat dau
red= (255, 0, 0), # dich
gray= (128, 128, 135), # tuong
green= (0, 255, 127), # cac o duoc xet tim duong
purple= (204, 204, 255), # 
p_yellow= (255, 255, 0), # mau cua duong di chinh thuc
yellow= (255, 227, 132), # mau button khi duoc click
frontier= (255, 192, 203) # mau hong khi tao ma tran bang maze


"""
    ve cac nut  bat dau, ve tuong, xoa tuong, xoa all
"""
font_chu = pygame.font.SysFont(None,30)
list_button = [("start",0,550),("draw",100,550),
            ("erase",200,550),("delete",300,550),
            ("Dij",550,0),("A star",550,100),("bfs",550,200),
            ("dfs",550,300)] # (text, x_rect,y_rect) chieu cao dai cua button =50
list_button_rect =[]
def ve_button():
    for text,x,y in list_button:
        noi_dung = font_chu.render(text,True,black)
        rect_button = pygame.Rect(x,y,50,50)
        list_button_rect.append(rect_button)
        pygame.draw.rect(screen,white,rect_button)
        screen.blit(noi_dung,rect_button)




clock_time = pygame.time.Clock()
while(True) :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    ve_button()
    pygame.display.update()
    clock_time.tick(60)
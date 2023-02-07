import pygame
pygame.init()


class Node :
    
    """
        khoi tao 1 node voi state : vi tri hang x, cot y
                            action: nhung hoat dong up,down.. tuong ung voi hang xom co the di chuyen den
                            parent : node cha cua no
    """
    def __init__(self, state :tuple, action :str,parent= None):
        self.state = state
        self.action = action
        self.parent = parent

    def __eq__(self, other) :
        if isinstance(other,Node):
            return self.state == other.state
        else: 
            return False
    # print nut cha cua 1 nut
    def __repr__(self):
        if self.parent is None:
            fmt = "Node {} and no Parent".format(self.state)
        else:
            fmt = "Node {} with Parent {}".format(self.state, self.parent.state)
        return fmt
    
    def __hash__(self):
        return hash(self.state)

"""
    board : bang de ve ma tran , vi tri: goc tren trai

"""
class Board:
    def __init__(self, v_cells:int, h_cells:int, origin_x:int, origin_y:int, 
                 cell_size:int, screen:int, colors:dict):
        self.v_cells = v_cells 
        self.h_cells = h_cells
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.cell_size = cell_size
        self.screen = screen
        self.colors = colors
        self.wall = set()
        self.visited = set()  # cac node da di qua
        self.frontiers = set()  
        self.path = list()  # duong di ngan nhat toi dich
        self.start = None
        self.target = None
    

    #ve tat ca cac rect cua 1 bang : vi tri, mau sac
    # ket qua cua ham la tra ve vi tri cua cac rect
    def draw_board(self, return_cells = True)->bool:
        cells = []
        for i in range(self.v_cells):
            row =[]
            for j in range(self.h_cells):
                rect = pygame.Rect(self.origin_x + i*self.cell_size,
                                    self.origin_y+j*self.cell_size,
                                   self.cell_size,self.cell_size )
                color = self.colors["white"]
                if(i,j) == self.start:
                    color = self.colors["blue"]
                elif (i, j) == self.target:
                    color = self.colors["red"]
                elif (i, j) in self.frontiers:
                    color = self.colors["frontier"] # dung cho tao ma tran
                elif (i, j) in self.wall:
                    color = self.colors["gray"]
                elif (i, j) in self.path:
                    color = self.colors["p_yellow"]
                else:
                    for node in self.visited:  #visited la 1 day cac node da di qua
                        if(i,j) == node.state: 
                            color = self.colors["green"]
                pygame.draw.rect(self.screen,color, rect)
                row.append(rect)
            cells.append(row) # cells dung de luu tat ca cac rect cua bang: vi tri

        if return_cells:
            return cells
                
    # tra ve danh sach hang xom co the di chuyen den
    def neighbors(self, state : tuple, wall_included = False) ->list:
        col,row = state 
        # xac dinh 4 rect hang xom cung dia chi cua hang xom
        actions = {
            "UP":(col,row-1),
            "DOWN" : (col, row+1),
            "LEFT":(col-1,row),
            "RIGHT":(col+1,row)
        }
        res = []
        for action ,(r,c) in actions.items():
            if not wall_included:
                if 0<= r < self.v_cells and 0<=c <self.h_cells and \
                    (r,c) not in self.wall:
                    res.append([action,(r,c)])
            else:
                if 0<=r<self.v_cells and 0<=c<self.h_cells:
                    res.append([action,(r,c)])
        return res if len(res) !=0 else None


    # 
    def reset(self):
        self.wall = set()
        self.visited = set()
        self.path = list()
        self.start = None 
        self.target = None


    def clear_visited(self):
        self.visited = set()
        self.path = list()

    
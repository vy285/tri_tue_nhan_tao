import time
import heapq
import pygame
import random
from moi_truong import *
from collections import defaultdict
from abc import ABCMeta , abstractmethod
from hang_doi import *
from ngan_xep import *
INF = float('inf')
DELAY = 0.01
DISTANCE =1

class Search(metaclass = ABCMeta):
    @abstractmethod
    def solver(self):
        pass

    @abstractmethod
    def initialize(self):
        pass

    def output(self):

        # cell = toa do cac node trong board , ve lai bang va voi cac o da di
        cells = self.board.draw_board()

        # thiet lap duong di tu nguon toi dich
        node = self.target_node
        while node.parent is not None:
            self.board.path.append(node.state)
            node = node.parent
        self.board.path.reverse()  # dao nguoc danh sach

        # ve duong di nguon den dich
        color = self.board.colors["p_yellow"]
        for i,j in self.board.path:
            time.sleep(1.5*DELAY)
            rect = cells[i][j]
            pygame.draw.rect(self.board.screen,color,rect)
            pygame.display.flip()

class Dijkstra(Search):
    def __init__(self,board:Board):
        self.board = board
        self.find = False
    def initialize(self):


        self.node_dict = {} # quan ly cac node cua bang 
        self.distance = {} # khoang cach tu nguon toi node duoc xet


        for i in range(self.board.v_cells):
            for j in range(self.board.h_cells):
                if(i,j) in self.board.wall:
                    continue

                pos = (i,j)
                node  = Node (pos,None,None)
                if pos == self.board.start:
                    self.start_node = node
                elif pos == self.board.target:
                    self.target_node = node

                self.node_dict[pos] = node
                
                
                self.distance[node] = INF # thiet lap khoang cach tu nguon den not co the di = vo cung
        self.distance[self.start_node] =0
        # print(len(self.node_dict))
        #
        self.adj_list = defaultdict(dict) # tao dict voi value : dict
        for _,node in self.node_dict.items():  #xet tat ca cac node khong phai tuong va dua ra hang xom co the di den
            neighbors = self.board.neighbors(node.state) #neighnors la tuple (string,(int,int))
            for action,(row,col) in neighbors:
                # print(row," ",col)
                neighbor_node = self.node_dict[(row,col)]

                self.adj_list[node][neighbor_node] = [action,DISTANCE] #ptu [node][neighbor] = "up or down.." "khoang cach = 1"



    def relax(self,node :Node,neighbor : Node):
        if self.distance[neighbor] > self.distance[node] + self.adj_list[node][neighbor][1]:
            self.distance[neighbor] = self.distance[node] + self.adj_list[node][neighbor][1]
            neighbor.parent = node
            neighbor.action = self.adj_list[node][neighbor][0]
             # day neighbor vao heapq de sap xep
            self.entry_count+=1
            heapq.heappush(self.heap,(self.distance[neighbor],self.entry_count,neighbor))

    def solver(self):
        """"""
        self.heap = []
        self.entry_count = 1 # entry_count co tac dung sap xep khi distance bang nhau, thi se sap xep node nao co thu tu be ra truoc
        # heapq tu dong sap xep theo distance tang dan
        heapq.heappush(self.heap,(self.distance[self.start_node],self.entry_count,self.start_node))
        while self.heap and self.find == False:
            time.sleep(DELAY)
            # lay node co distance be nhat
            (_,_,node ) = heapq.heappop(self.heap)
            if node.state == self.target_node.state:
                self.find = True
            #them node vao danh sach da di qua
            self.board.visited.add(node)
            self.board.draw_board(return_cells=False) #ve lai

            # neu node khong co hang xom co the di
            if not self.adj_list[node] :
                continue

            for neighbor in self.adj_list[node]: # xet tung hang xom khong phai tuong
                if neighbor not in self.board.visited: # neu hang xom chua duoc di qua
                    self.relax(node,neighbor)

            pygame.display.flip()


            
class A_search(Search):
    def __init__(self,board:Board):
        self.board = board
        self.find = False
    def initialize(self):
        self.node_dict ={}
        self.g_scores = {}
        self.h_scores = {}
        for i in range(self.board.v_cells):
            for j in range (self.board.h_cells):
                if(i,j) in self.board.wall:
                    continue

                pos = (i,j)
                node = Node(pos,None,None)
                if pos == self.board.start:
                    self.start_node = node
                elif pos == self.board.target:
                    self.target_node = node
                
                self.node_dict[pos] = node
                self.g_scores[node] = INF  # khoang cach tu nguon den nut vi tri pos = vo cung
                self.h_scores[node] = 0 # khoang cach uoc tinh tu pos den nguon = 0

        self.g_scores[self.start_node] = 0
        self.adj_list = defaultdict(dict)

        for _,node in self.node_dict.items():
            neighbors = self.board.neighbors(node.state)
            for action,(row,col) in neighbors:
                neighbor_node = self.node_dict[(row,col)]
                self.adj_list[node][neighbor_node] = [action,DISTANCE]

    
 
    def relax(self,node :Node,neighbor : Node):
        if self.g_scores[neighbor] > self.g_scores[node] + self.adj_list[node][neighbor][1]:
            self.g_scores[neighbor] = self.g_scores[node] + self.adj_list[node][neighbor][1]
            neighbor.parent = node
            neighbor.action = self.adj_list[node][neighbor][0]

            self.entry_count +=1
            self.h_scores[neighbor] = A_search.manhattan(neighbor,self.target_node)
            print(self.g_scores[neighbor]+ self.h_scores[neighbor],",",neighbor.action,",",self.entry_count,node.state,neighbor.state)
            heapq.heappush(self.heap,(self.g_scores[neighbor]+ self.h_scores[neighbor],self.entry_count,neighbor))

    def solver(self):
        self.heap = []
        self.entry_count =1

        h_score_start = A_search.manhattan(self.start_node,self.target_node)
        heapq.heappush(self.heap,(h_score_start,self.entry_count,self.start_node))
        # khi heap con khac rong va chua tim thay target
        while self.heap and not self.find:
            time.sleep(DELAY)
            
            #lay ra phan tu co g+ h min
            _,_,node = heapq.heappop(self.heap)
            if node.state == self.target_node.state:
                self.find = True

            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)

            if not self.adj_list[node]:
                continue

            for neighbor in self.adj_list[node]:
                # print(neighbor.action)
                if neighbor not in self.board.visited:
                    self.relax(node,neighbor)
            pygame.display.flip() 

    @staticmethod
    def manhattan(node_1:Node, node_2:Node)->int:
        """
        Compute manhattan distance between two nodes

        node_1: first node to be computed --> Node
        node_2: second node to be computed --> Node
        """
        start_x, start_y = node_1.state
        target_x, target_y = node_2.state
        return abs(start_x-target_x) + abs(start_y-target_y)   

class BFS(Search):
    def __init__(self,board:Board):
        self.board = board
        self.find = False
    def initialize(self):
        self.node_dict={}
        for i in range(self.board.v_cells):
            for j in range(self.board.h_cells):
                if (i,j)in self.board.wall:
                    continue
                pos = (i,j)
                node = Node(pos, None,None)
                if pos == self.board.start:
                    self.start_node = node
                if pos == self.board.target:
                    self.target_node = node
                self.node_dict[pos] = node


    def solver(self):
        self.queue = Queue()
        self.queue.add(self.start_node)
        self.queue.frontier.add(self.start_node.state)

        while not self.queue.empty() and not self.find :
            time.sleep(DELAY)
            node = self.queue.remove()
            print(node.state,node.action)
            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)

            neighbors = self.board.neighbors(node.state)
            for action, (row,col) in neighbors:
                if (row,col) == self.target_node.state:
                    self.find = True
                    self.target_node.parent = node
                    self.target_node.action = action
                    break
                
                if (row,col) not in self.queue.frontier and \
                self.node_dict[(row,col)] not in self.board.visited:

                    neighbor = self.node_dict[(row,col)]
                    neighbor.parent = node
                    neighbor.action = action
                    self.queue.add(neighbor)
                    self.queue.frontier.add((row,col))
            pygame.display.flip()


class DFS(Search):
    def __init__(self,board:Board):
        self.board = board
        self.find = False
    def initialize(self):
        self.node_dict = {}

        for i in range(self.board.v_cells):
            for j in range( self.board.h_cells):

                if(i,j) in self.board.wall:
                    continue
                pos = (i,j)
                node = Node (pos,None ,None)
                if pos == self.board.start:
                    self.start_node = node
                if pos == self.board.target:

                    self.target_node = node
                self.node_dict[pos] = node

    def solver(self):
        self.stack = Stack()
        self.stack.add(self.start_node)
        self.stack.frontier.add(self.start_node.state)

        while not self.stack.empty() and not self.find:
            time.sleep(DELAY)
            node  = self.stack.remove()
            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)
            print("lay ra: ", node.state)
            neighbors = self.board.neighbors(node.state)
            for action,(row,col) in neighbors:
                if (row,col) == self.target_node.state:
                    self.target_node.parent = node
                    self.target_node.action = action
                    self.find = True
                    break

                if (row,col) not in self.stack.frontier and \
                self.node_dict[(row,col)] not in self.board.visited:
                    neighbor = self.node_dict[(row,col)]
                    
                    neighbor.parent = node
                    neighbor.action = action
                    self.stack.frontier.add((row,col))
                    self.stack.add(neighbor)
                    print("cho vao: ",neighbor.state)

            pygame.display.flip()

